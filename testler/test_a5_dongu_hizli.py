"""K-015, V-042: hızlı yol çekirdek döngüsüne bağlı; sonuçlar değişmez.

Aynı senaryolar (`testler/yardimci_senaryo.py`) referans ve hızlı kod kitabıyla koşturulur. Defterin her olayı
(afinite ve güven ondalıkları dahil, kanonik JSON ile, yani bit düzeyinde), havuzdaki kayıt vektörleri, döngü ve
müdahale sonuçları iki yolda aynı olmalı. Ayrıca referans yolun izi, bağlamadan önceki koddan (commit 797eeaa)
alınmış altın değerlerle aynı olmalı: bağlama, referans yolun davranışını da değiştirmemeli.
K-028 (kopya kuralı C) davranışı bilerek değiştirdi: yalnız C'nin "yeni dayanak yok" diye aday attığı senaryonun
izi değişti; o senaryonun altın değeri C'li referans yoldan yenilendi, 797eeaa değeri ONCEKI_C_SIZ'da duruyor.
K-031 (C hücre sınırından önce) yine yalnız o senaryoyu değiştirdi (hem sınırı aşan hücre hem dayanaksız aday var);
altın değeri yenilendi, K-028 değeri ONCEKI_K028'de duruyor.
"""
import collections
import unittest
from unittest import mock

from cekirdek import vektor as V
from cekirdek import vektor_hizli as H
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.eslesme import afinite, afinite_tablosu, alici
from testler.test_a1_iliski_semasi import SemaOrtami, blorp_semasi
from testler.yardimci_senaryo import AYAR, senaryolar

KK = V.KodKitabi(AYAR.deger("vektor_tohum"), AYAR.deger("vektor_boyutu"))
HKK = H.HizliKodKitabi(AYAR.deger("vektor_tohum"), AYAR.deger("vektor_boyutu"))

# Bağlamadan önceki kodun (797eeaa) referans yoldaki izi: (olay sayısı, son zincir özeti, kayıt vektörlerinin özeti).
ONCEKI_C_SIZ = {
    "kalabalik": (186, "7e076c30b7f6e7176a2fb43ea4edd259df78f561361c66a237d5d63d24bb9001",
                  "701cb127fdf80be98ec5c01b98f29900f9a04dc6c462e141e1eb5f8a3c13c812"),
}
# K-028 sonrası, K-031 öncesi (C hücre sınırından sonra).
ONCEKI_K028 = {
    "kalabalik": (139, "9d58526b9e90121baef35680813f32b8ae87a3f6f54467ccd646867d1bff1148",
                  "998fb8cff4bba0dc567fda135b0a53dddf2f91dabc93330ea92acb1c71bca919"),
}
# K-031 sonrası; diğer senaryolar 797eeaa ile aynı.
ONCEKI = {
    "kalabalik": (124, "afa484b61c5f93bec5f199a690316c9af617182e0b2088707a865a7a7146e33b",
                  "38f885f075b1297a73f33727b24265d6bdab0b0f416918cc6c583cd55ad32a51"),
    "impasse_cevapli": (6, "1bafcabdc1d4920e6706268a513acab12cb81fc5752e39c3a0490a32cfae7055",
                        "e50a4c5ac126f7f1d804b9ca39034316ee25e36638e0f66d2392b58814942c39"),
    "impasse_cevapsiz": (6, "9885755328682882616a304fecd50fddbc6f1be36fa9e659ad5210eaa85d1bea",
                         "e50a4c5ac126f7f1d804b9ca39034316ee25e36638e0f66d2392b58814942c39"),
    "celiski_mudahale": (11, "2de3d7e2d6bce084d519574259ea20b2e2250eb5607157f83161450ade5baa89",
                         "f5ba350fe913319d5a1cd2bbec29580ee3f2ee407b416e5e9d05956b18d6a352"),
}


def ilk_fark(a, b):
    """Büyük dizilerde unittest'in fark çıktısı (difflib) dakikalar sürüyor; ilk farklı konum yeterli."""
    if len(a) != len(b):
        return f"uzunluk {len(a)} ile {len(b)}"
    return next((f"ilk farklı konum {i}" for i, (x, y) in enumerate(zip(a, b)) if x != y), None)


class DonguHizliYolTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ortam = SemaOrtami(blorp_semasi())
        cls.sema = cls.ortam.yukle()
        cls.referans = senaryolar(KK, cls.sema)
        cls.hizli = senaryolar(HKK, cls.sema)

    @classmethod
    def tearDownClass(cls):
        cls.ortam.kapat()

    def test_senaryolar_butun_dallari_calistirir(self):
        """Eşitlik boş bir koşuda anlamsız olurdu: atma, bütçe, impasse, çelişki ve müdahale gerçekten oluşmalı."""
        turler = collections.Counter(k["tur"] for oz in self.referans.values() for k in oz.satirlar)
        for tur in ("ATESLEME", "YAZMA", "ATMA", "ESLESME_ATILDI", "ESIK_DUSURME", "CELISKI", "MUDAHALE"):
            self.assertGreater(turler[tur], 0, tur)
        nedenler = {k["veri"]["neden"] for oz in self.referans.values() for k in oz.satirlar
                    if k["tur"] in ("ESLESME_ATILDI", "DURMA")}
        self.assertTrue({"hucre_siniri", "butce", "tur_siniri", "impasse", "yeni_kayit_yok"} <= nedenler, nedenler)

    def test_referans_yol_baglamadan_onceki_kodla_ayni(self):
        self.assertEqual({ad: oz.altin() for ad, oz in self.referans.items()}, ONCEKI)

    def test_c_yalniz_dayanaksiz_aday_atilan_senaryoyu_degistirdi(self):
        for ad, oz in self.referans.items():
            dayanaksiz = sum(k["veri"]["sayi"] for k in oz.satirlar
                             if k["tur"] == "ESLESME_ATILDI" and k["veri"]["neden"] == "dayanak_yok")
            with self.subTest(senaryo=ad):
                self.assertEqual(dayanaksiz > 0, ad in ONCEKI_C_SIZ)
                self.assertNotEqual(ONCEKI_C_SIZ.get(ad), oz.altin())

    def test_k031_yalniz_dayanaksiz_aday_olan_senaryoyu_degistirdi(self):
        """Dayanaksız aday yoksa C'nin sınırdan önce gelmesi hiçbir şeyi değiştiremez; değişen senaryoda vardır."""
        for ad, oz in self.referans.items():
            dayanaksiz = any(k["tur"] == "ESLESME_ATILDI" and k["veri"]["neden"] == "dayanak_yok" for k in oz.satirlar)
            with self.subTest(senaryo=ad):
                self.assertEqual(ad in ONCEKI_K028, dayanaksiz)
                self.assertNotEqual(ONCEKI_K028.get(ad), oz.altin())

    def test_hizli_yol_defteri_referansla_bit_duzeyinde_ayni(self):
        for ad in ONCEKI:
            with self.subTest(senaryo=ad):
                r, h = self.referans[ad], self.hizli[ad]
                self.assertEqual(len(h.satirlar), len(r.satirlar))
                for sr, sh in zip(r.satirlar, h.satirlar):
                    self.assertEqual(kanonik_json(sh), kanonik_json(sr))
                self.assertEqual(h.altin(), ONCEKI[ad])

    def test_hizli_kosuda_saf_python_vektor_hesabi_cagrilmaz(self):
        """Eşitlik, hızlı yolun kullanıldığını göstermez (referansa dönen kod da aynı sonucu verir). Burada saf Python
        evrişimi ve kosinüsü yasaklanır: hızlı kod kitabıyla bütün senaryolar yine aynı izi vermeli."""
        def yasak(*_):
            raise AssertionError("hızlı koşuda saf Python vektör hesabı çağrıldı")
        with mock.patch.object(V, "evrisim", yasak), mock.patch.object(V, "kosinus", yasak), \
                mock.patch("cekirdek.eslesme.kosinus", yasak):
            hizli = senaryolar(HKK, self.sema)
            with self.assertRaises(AssertionError):
                senaryolar(KK, self.sema)
        self.assertEqual({ad: oz.altin() for ad, oz in hizli.items()}, ONCEKI)

    def test_hizli_yol_vektorleri_ve_sonuclari_ayni(self):
        for ad in ONCEKI:
            with self.subTest(senaryo=ad):
                r, h = self.referans[ad], self.hizli[ad]
                self.assertIsNone(ilk_fark(h.vektorler, r.vektorler))
                self.assertEqual(repr(h.sonuc), repr(r.sonuc))
                self.assertEqual(repr(h.mudahale), repr(r.mudahale))


class HizliKodKitabiTesti(unittest.TestCase):
    def test_kod_kitabi_ayni_vektorleri_verir(self):
        for tur, ad in (("varlik", 7), ("iliski", "blorp"), ("rol", "ozne")):
            self.assertEqual(HKK.vektor(tur, ad), KK.vektor(tur, ad))
        self.assertEqual((HKK.tohum, HKK.boyut, HKK.olcek), (KK.tohum, KK.boyut, KK.olcek))

    def test_kayit_vektoru_referansla_ayni(self):
        for uclu in ((7, "blorp", 11), (11, "blorp", 7), (0, "zindle", 0), ("a", "quax", "b")):
            v = HKK.kayit_vektoru(*uclu)
            self.assertIsInstance(v, tuple)
            self.assertTrue(all(type(x) is int for x in v))
            self.assertEqual(v, V.kayit_vektoru(KK, *uclu))
            self.assertEqual(KK.kayit_vektoru(*uclu), V.kayit_vektoru(KK, *uclu))

    def test_onbellekli_donusum_matrisleri_dogru(self):
        """V-042 eki: dönüşüm matrisleri kod kitabı kurulurken bir kez hesaplanır; her çağrıda kurulanla aynı."""
        for rol in ("ozne", "nesne"):
            p = H.torch.tensor(KK.vektor("rol", rol), dtype=H.TAMSAYI)
            self.assertTrue(H.torch.equal(HKK._donusumler[rol], H.donusum_matrisi(p)))
        u = [(7, "blorp", 11), (11, "zindle", 13), (0, "quax", 0)]
        self.assertEqual(H.kayit_matrisi_hizli(KK, u, HKK._donusumler).tolist(), H.kayit_matrisi_hizli(KK, u).tolist())

    def test_benzerlik_matrisi_referansla_ayni(self):
        a = [V.kayit_vektoru(KK, i, "blorp", i + 1) for i in range(7)]
        b = [alici(KK, g) for g in ("blorp", "zindle", "quax")]
        hizli, referans = HKK.benzerlik_matrisi(a, b), KK.benzerlik_matrisi(a, b)
        self.assertEqual([[x.hex() for x in s] for s in hizli], [[x.hex() for x in s] for s in referans])
        self.assertTrue(all(type(x) is float for s in hizli for x in s))
        self.assertEqual(HKK.benzerlik_matrisi([], b), [])


class AfiniteTablosuTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from cekirdek.havuz import Havuz
        cls.havuzlar = []
        for kk in (KK, HKK):
            h = Havuz(16, kk)
            for i, r in enumerate(("blorp", "blorp", "zindle", "quax", "blorp")):
                h.epitop_ekle(i, r, i + 1, guven=1.0)
            cls.havuzlar.append(h)

    def test_tablo_yalniz_kendi_genindeki_kayitlari_icerir(self):
        tablo = afinite_tablosu(KK, self.havuzlar[0], ("blorp", "quax", "vonk"))
        self.assertEqual(sorted(tablo), [("blorp", 0), ("blorp", 1), ("blorp", 4), ("quax", 3)])

    def test_tablo_dogrudan_afiniteyle_ve_iki_yolda_ayni(self):
        genler = ("blorp", "zindle", "quax")
        referans = afinite_tablosu(KK, self.havuzlar[0], genler)
        hizli = afinite_tablosu(HKK, self.havuzlar[1], genler)
        self.assertEqual(sorted(hizli), sorted(referans))
        for (gen, kimlik), deger in referans.items():
            dogrudan = afinite(alici(KK, gen), self.havuzlar[0].kayit(kimlik).vektor)
            self.assertEqual(deger.hex(), dogrudan.hex())
            self.assertEqual(hizli[(gen, kimlik)].hex(), dogrudan.hex())


if __name__ == "__main__":
    unittest.main()
