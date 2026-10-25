"""V-056: bellek deposu. Sadece-ekleme, hash zincirli; kabul edilen kayıt değiştirilemez, geri alma yeni bir olaydır;
dosyadan yeniden açılınca aynı aktif hücreler ve aynı sürüm; kurcalanmış dosya açılmaz.
Geçitten geçen kural belleğe girer; sonradan veri onu yalanlarsa gözden geçirmede geri alınır (EK A P7).
İlişki adları anlamsızdır (blorp şeması)."""
import json
from pathlib import Path

from cekirdek.altyapi.olay_gunlugu import ZincirHatasi
from cekirdek.bellek import BELLEK_GERI_ALMA, BELLEK_KABUL, Bellek, BellekHatasi
from cekirdek.bellek_gecidi import KABUL, YANLIS
from degerlendirme.bellek_hatti import degerlendir, gozden_gecir
from testler.test_a5_h1 import GUNLUK
from testler.test_a6_bellek_gecidi import ESIK, KK, ORTAMLAR, T1, T2, bolum
import testler.test_a3_cekirdek as t3

DNA_V2 = Path(__file__).resolve().parents[1] / "sema" / "dna_v2.schema.json"


class BellekTesti(t3.Ortam):
    def bellek(self, ad="bellek.jsonl"):
        return Bellek(Path(self._d.name) / ad, **GUNLUK)

    def test_kabul_geri_alma_ve_yeniden_acma(self):
        b = self.bellek()
        b.kabul_et(T1, {"not": 1})
        b.kabul_et(T2, {"not": 2})
        b.geri_al("t_bb", "deneme")
        self.assertEqual([h["kimlik"] for h in b.aktif_veriler()], ["t_qb"])
        self.assertEqual([k["tur"] for k in b.kayitlar()], [BELLEK_KABUL, BELLEK_KABUL, BELLEK_GERI_ALMA])
        yeniden = self.bellek()
        self.assertEqual((yeniden.aktif_veriler(), yeniden.surum), (b.aktif_veriler(), b.surum))
        self.assertEqual([h.kimlik for h in yeniden.hucreler(DNA_V2, self.sema)], ["t_qb"])

    def test_bos_bellegin_hucresi_yok(self):
        b = self.bellek()
        self.assertEqual(tuple(b.hucreler(DNA_V2, self.sema)), ())
        b.kabul_et(T1, {})
        b.geri_al("t_bb", "deneme")
        self.assertEqual(tuple(b.hucreler(DNA_V2, self.sema)), ())

    def test_gecmis_kayit_degismez(self):
        b = self.bellek()
        b.kabul_et(T1, {})
        ilk = (Path(self._d.name) / "bellek.jsonl").read_bytes()
        b.geri_al("t_bb", "deneme")
        self.assertTrue((Path(self._d.name) / "bellek.jsonl").read_bytes().startswith(ilk))
        kopya = b.aktif_veriler()
        self.assertEqual(kopya, [])

    def test_disaridan_degistirilemez(self):
        b = self.bellek()
        b.kabul_et(T1, {})
        b.aktif_veriler()[0]["halkalar"][0]["gen"] = "vonk"
        self.assertEqual(b.aktif_veriler()[0]["halkalar"][0]["gen"], "blorp")

    def test_kurcalanmis_dosya_acilmaz(self):
        b = self.bellek()
        b.kabul_et(T1, {})
        yol = Path(self._d.name) / "bellek.jsonl"
        satir = json.loads(yol.read_text(encoding="utf-8"))
        satir["veri"]["hucre"]["sonuc"]["gen"] = "vonk"
        yol.write_text(json.dumps(satir) + "\n", encoding="utf-8")
        with self.assertRaises(ZincirHatasi):
            self.bellek()

    def test_cift_kabul_ve_olmayani_geri_alma_reddedilir(self):
        b = self.bellek()
        b.kabul_et(T1, {})
        with self.assertRaises(BellekHatasi):
            b.kabul_et(T1, {})
        with self.assertRaises(BellekHatasi):
            b.geri_al("t_qb", "yok")

    def test_gecitten_bellege_ve_gozden_gecirmede_geri_alma(self):
        b = self.bellek()
        aday = self.hucreler(T1)[0]
        k = degerlendir(aday, (), ORTAMLAR, self.sema, KK, t3.PRM, GUNLUK, ESIK)
        self.assertEqual(k.karar, KABUL)
        b.kabul_et(T1, k.olcumler)
        self.assertEqual(gozden_gecir(b, DNA_V2, ORTAMLAR, self.sema, KK, t3.PRM, GUNLUK, ESIK), [])
        # yeni veri: (a,c) için quax yerine frumb gözleniyor; kural bu veride yanlış çıkar ve geri alınır
        yalanlayan = {"yeni": [bolum([(1, "blorp", 2), (2, "blorp", 3), (1, "frumb", 3), (7, "frumb", 8)])
                               for _ in range(ESIK.en_az_kanit)]}
        self.assertEqual(gozden_gecir(b, DNA_V2, yalanlayan, self.sema, KK, t3.PRM, GUNLUK, ESIK), ["t_bb"])
        self.assertEqual(b.aktif_veriler(), [])
        self.assertEqual(b.kayitlar()[-1]["veri"], {"kimlik": "t_bb", "neden": YANLIS})
