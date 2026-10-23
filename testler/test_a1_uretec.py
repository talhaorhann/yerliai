"""sistem.md §10, §11; K-007, K-008: sentetik soy ağacı üreteci, bölmeler, kelime çantası kapısı, kilitli kümeler.

Testlerde hiçbir ilişki adı yazılmaz (KODLAMA_PROMPTU §2.4): adlar veri dosyalarından okunur.
"""
import dataclasses
import json
import random
import tempfile
import unittest
from collections import deque
from pathlib import Path

from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.altyapi.olay_gunlugu import OlayGunlugu
from cekirdek.altyapi.sema_dogrulayici import sema_yukle
from cekirdek.bilgi_tabani import KABUL, BilgiTabani
from cekirdek.iliski_semasi import _dogrula_ve_kur, iliski_semasi_yukle
from degerlendirme import uretec
from degerlendirme.dunya import Dunya, TanimHatasi, tanimlar_yukle
from degerlendirme.kilitli_kumeler import KilitliKumeHatasi, kesisim_denetle, kilitli_ozetler
from degerlendirme.kisa_yol import KisaYolHatasi, NaiveBayes, kapi_denetle, ozellikler
from degerlendirme.uretec import Parametreler, UretimDurduHatasi, aday_uret, bolme_uret, hepsini_uret
from testler.yardimci import KOK, kod_dosyalari, goreli

AYAR = ayar_yukle(KOK / "config.json")
ALG = AYAR.deger("hash_algoritmasi")
SEMA_YOLU = KOK / "sema" / "iliskiler_v1.json"
SEMA = iliski_semasi_yukle(SEMA_YOLU, KOK / "kilit" / "sema_onayi.json", KOK / "sema" / "iliski_semasi_v1.schema.json")
TANIM_YOLU = KOK / "degerlendirme" / "veri" / "tanimlar_v1.json"
TANIM_BICIMI = KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json"
TANIM = tanimlar_yukle(TANIM_YOLU, TANIM_BICIMI, SEMA)
PRM = Parametreler.ayardan(AYAR)
KUCUK = dataclasses.replace(PRM, ana_kume_sayisi=24, dedektor_egitim_sayisi=24)
BOLUM_DOG = sema_yukle(KOK / "sema" / "bolum_v1.schema.json")
CEVAP_DOG = sema_yukle(KOK / "sema" / "cevap_v1.schema.json")


def en_kisa_yol(bolum):
    komsu = {}
    for o in bolum["olgular"]:
        komsu.setdefault(o["ozne"], set()).add(o["nesne"])
        komsu.setdefault(o["nesne"], set()).add(o["ozne"])
    bas, son = bolum["sorgu"]["ozne"], bolum["sorgu"]["nesne"]
    uzaklik = {bas: 0}
    kuyruk = deque([bas])
    while kuyruk:
        x = kuyruk.popleft()
        for y in sorted(komsu.get(x, ())):
            if y not in uzaklik:
                uzaklik[y] = uzaklik[x] + 1
                kuyruk.append(y)
    return uzaklik.get(son)


class TanimTesti(unittest.TestCase):
    def test_tanimlar_onayli_semayla_ortusur(self):
        self.assertEqual(set(TANIM.adlar), set(SEMA.adlar))
        self.assertTrue(set(TANIM.olgu_iliskileri) <= set(SEMA.adlar))

    def tanim_bozuk(self, degistir):
        veri = json.loads(TANIM_YOLU.read_text(encoding="utf-8"))
        degistir(veri)
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "tanimlar_v1.json"
            yol.write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(TanimHatasi):
                tanimlar_yukle(yol, TANIM_BICIMI, SEMA)

    def test_eksik_fazla_ya_da_bicimsiz_tanim_reddedilir(self):
        self.tanim_bozuk(lambda v: v["tanimlar"].pop())
        self.tanim_bozuk(lambda v: v["tanimlar"].append({"ad": "glim", "secenekler": [[{"yon": "U", "tip": None}]]}))
        self.tanim_bozuk(lambda v: v["olgu_iliskileri"].append("glim"))
        self.tanim_bozuk(lambda v: v["tanimlar"][0]["secenekler"][0][0].update(yon="X"))

    def test_okunur_tablo_her_tanimi_icerir(self):
        from degerlendirme.dunya import okunur_tanimlar
        tablo = okunur_tanimlar(TANIM)
        for ad in TANIM.adlar:
            self.assertIn(f"| {ad} |", tablo)

    def test_gizli_tanimlara_yalniz_degerlendirme_dokunur(self):
        for yol in kod_dosyalari():
            if goreli(yol).startswith("degerlendirme/"):
                continue
            metin = yol.read_text(encoding="utf-8")
            self.assertNotIn("tanimlar_v", metin, goreli(yol))
            self.assertNotIn("degerlendirme/veri", metin, goreli(yol))


class DunyaTesti(unittest.TestCase):
    """Her ağaçta tanımlar onaylı şemayla tutarlı olmalı (V-019): tek ilişki, ters, işlevsellik, simetri."""

    def dunya(self, tohum):
        return Dunya.uret(random.Random(tohum), PRM.nesil_sayisi, PRM.cocuk_en_az, PRM.cocuk_en_cok)

    def test_yapi(self):
        for tohum in (7, 11, 13):
            d = self.dunya(tohum)
            self.assertGreater(d.kisi_sayisi, 2)
            for cocuk, (x, y) in d.ebeveynler.items():
                self.assertEqual(d.es[x], y)
                self.assertNotEqual(d.tip[x], d.tip[y])
                self.assertIn(cocuk, d.cocuklar[x])

    def test_tanimlar_semayla_tutarli(self):
        for tohum in (7, 11, 13):
            d = self.dunya(tohum)
            tablo = {a: d.iliskiler(a, TANIM) for a in range(d.kisi_sayisi)}
            self.assertTrue(any(tablo.values()))
            for a, satir in tablo.items():
                for ad in SEMA.adlar:
                    if SEMA.islevsel(ad):
                        self.assertLessEqual(sum(1 for r in satir.values() if r == ad), 1, (tohum, a, ad))
                for b, ad in satir.items():
                    self.assertNotEqual(a, b)
                    ters = tablo[b].get(a)
                    self.assertIsNotNone(ters, (tohum, a, b, ad))
                    self.assertIn(ters, SEMA.ters(ad), (tohum, a, b, ad))
                    if SEMA.simetrik(ad):
                        self.assertEqual(ters, ad)

    def test_tanim_degisince_cevap_degisir(self):
        """Sahte kod denetimi: iki ilişkinin tanımı yer değiştirince hesaplanan ilişkiler de yer değiştirmeli."""
        a_ad, b_ad = TANIM.adlar[0], TANIM.adlar[1]
        takas = TANIM.takasli(a_ad, b_ad)
        d = self.dunya(7)
        degisti = 0
        for x in range(d.kisi_sayisi):
            asil, yeni = d.iliskiler(x, TANIM), d.iliskiler(x, takas)
            for y, r in asil.items():
                beklenen = {a_ad: b_ad, b_ad: a_ad}.get(r, r)
                self.assertEqual(yeni[y], beklenen)
                degisti += r in (a_ad, b_ad)
        self.assertGreater(degisti, 0)


class BolumTesti(unittest.TestCase):
    def adaylar(self, bolme, adet=30, tohum=7):
        rng = random.Random(tohum)
        esleme = uretec.ad_eslemesi(random.Random(tohum), SEMA, PRM) if bolme == "yeniden_adlandirma" else None
        return [aday_uret(rng, TANIM, PRM, bolme, ad_esleme=esleme) for _ in range(adet)]

    def ortak_denetim(self, aday, k_araligi):
        bolum, cevap = aday.bolum, aday.cevap
        self.assertEqual(BOLUM_DOG.hatalar(bolum), [])
        self.assertEqual(CEVAP_DOG.hatalar(cevap), [])
        self.assertEqual(set(bolum), {"sema_surumu", "olgular", "sorgu", "ozet"})
        self.assertEqual(cevap["bolum_ozeti"], bolum["ozet"])
        self.assertTrue(k_araligi[0] <= cevap["k"] <= k_araligi[1])
        self.assertEqual(len(bolum["olgular"]), cevap["k"] + PRM.dikkat_dagitici)
        metin = kanonik_json(bolum).decode("utf-8")
        self.assertNotIn(cevap["bolme"], metin)
        kisiler = {o["ozne"] for o in bolum["olgular"]} | {o["nesne"] for o in bolum["olgular"]}
        self.assertIn(bolum["sorgu"]["ozne"], kisiler)
        self.assertIn(bolum["sorgu"]["nesne"], kisiler)

    def test_egitim(self):
        for a in self.adaylar("egitim"):
            self.ortak_denetim(a, PRM.egitim_k)
            self.assertEqual(en_kisa_yol(a.bolum), a.cevap["k"])
            self.assertIn(a.cevap["cevap"], SEMA.adlar)
            self.assertEqual(a.cevap["cevap"], a.dunya.iliski(a.sorgu_ham[0], a.sorgu_ham[1], TANIM))
            for o in a.bolum["olgular"]:
                self.assertIn(o["iliski"], TANIM.olgu_iliskileri)

    def test_olgular_gercek_bag_ve_kimlikler_karisik(self):
        ozdes = 0
        for a in self.adaylar("egitim"):
            ters_esleme = {yeni: eski for eski, yeni in a.kimlik_esleme.items()}
            for o in a.bolum["olgular"]:
                x, y = ters_esleme[o["ozne"]], ters_esleme[o["nesne"]]
                self.assertEqual(a.dunya.iliski(x, y, TANIM), o["iliski"])
            ozdes += all(eski == yeni for eski, yeni in a.kimlik_esleme.items())
        self.assertLess(ozdes, 3)

    def test_olgu_sirasi_zinciri_ele_vermez(self):
        """Olgular karıştırılmalı: ilk olgunun sorgu öznesiyle başlaması nadir olmalı."""
        adaylar = self.adaylar("egitim", adet=60)
        bastan = sum(1 for a in adaylar if a.bolum["olgular"][0]["ozne"] == a.bolum["sorgu"]["ozne"])
        self.assertLess(bastan, len(adaylar) // 2)

    def test_bilgi_tabani_tum_olgulari_kabul_eder(self):
        with tempfile.TemporaryDirectory() as d:
            gunluk = OlayGunlugu(Path(d) / "o.jsonl", algoritma=ALG, sema_surumu=AYAR.deger("olay_sema_surumu"),
                                 izinli_kaynaklar=AYAR.deger("kaynaklar"))
            for a in self.adaylar("egitim", adet=13):
                tb = BilgiTabani(SEMA, sema_yukle(KOK / "sema" / "uclu_kaydi_v1.schema.json"), gunluk, ALG)
                for o in a.bolum["olgular"]:
                    self.assertEqual(tb.ekle(o), KABUL)

    def test_uzunluk(self):
        for a in self.adaylar("uzunluk", adet=13):
            self.ortak_denetim(a, PRM.test_k)
            self.assertEqual(en_kisa_yol(a.bolum), a.cevap["k"])

    def test_zincir_bozuk(self):
        for a in self.adaylar("zincir_bozuk"):
            self.ortak_denetim(a, PRM.egitim_k)
            self.assertIsNone(a.cevap["cevap"])
            self.assertIsNone(en_kisa_yol(a.bolum))

    def test_yon_ters(self):
        for a in self.adaylar("yon_ters"):
            self.ortak_denetim(a, PRM.egitim_k)
            bas, son = a.sorgu_ham
            ileri = a.dunya.iliski(son, bas, TANIM)
            self.assertEqual(a.cevap["cevap"], a.dunya.iliski(bas, son, TANIM))
            self.assertIn(a.cevap["cevap"], SEMA.ters(ileri))
            self.assertEqual(en_kisa_yol(a.bolum), a.cevap["k"])

    def test_yeniden_adlandirma(self):
        esleme = uretec.ad_eslemesi(random.Random(7), SEMA, PRM)
        self.assertEqual(set(esleme), set(SEMA.adlar))
        self.assertEqual(len(set(esleme.values())), len(esleme))
        self.assertFalse(set(esleme.values()) & set(SEMA.adlar))
        yeni_sema = uretec.yeniden_adlandirilmis_sema(json.loads(SEMA_YOLU.read_text(encoding="utf-8")), esleme)
        s = _dogrula_ve_kur(yeni_sema, KOK / "sema" / "iliski_semasi_v1.schema.json")
        for ad in SEMA.adlar:
            self.assertEqual(s.ters(esleme[ad]), tuple(esleme[t] for t in SEMA.ters(ad)))
        for a in self.adaylar("yeniden_adlandirma"):
            self.ortak_denetim(a, PRM.egitim_k)
            self.assertIn(a.cevap["cevap"], set(esleme.values()))
            for o in a.bolum["olgular"]:
                self.assertIn(o["iliski"], set(esleme.values()))

    def test_bilinmeyen_bolme(self):
        with self.assertRaises(ValueError):
            aday_uret(random.Random(7), TANIM, PRM, "uydurma")

    def test_deneme_siniri_asilinca_durur(self):
        imkansiz = dataclasses.replace(PRM, egitim_k=(50, 50), deneme_siniri=5)
        with self.assertRaises(UretimDurduHatasi):
            aday_uret(random.Random(7), TANIM, imkansiz, "egitim")


class KisaYolTesti(unittest.TestCase):
    @staticmethod
    def sahte(iliski, cevap, kimlik=7):
        return ({"olgular": [{"ozne": kimlik, "iliski": iliski, "nesne": kimlik + 1}],
                 "sorgu": {"ozne": kimlik, "nesne": kimlik + 1}}, {"cevap": cevap})

    def test_ozellikler_yapiya_bakmaz(self):
        b1 = {"olgular": [{"ozne": 7, "iliski": "blorp", "nesne": 11}, {"ozne": 11, "iliski": "zindle", "nesne": 13}],
              "sorgu": {"ozne": 7, "nesne": 13}}
        b2 = {"olgular": [{"ozne": 11, "iliski": "zindle", "nesne": 13}, {"ozne": 7, "iliski": "blorp", "nesne": 11}],
              "sorgu": {"ozne": 7, "nesne": 13}}
        self.assertEqual(sorted(ozellikler(b1)), sorted(ozellikler(b2)))
        self.assertIn("r:blorp", ozellikler(b1))

    def test_ayrilabilir_veride_dogru_bilir(self):
        nb = NaiveBayes(1)
        veri = [self.sahte("blorp", "x"), self.sahte("zindle", "y")] * 5
        nb.egit([ozellikler(b) for b, _ in veri], [c["cevap"] for _, c in veri])
        self.assertEqual(nb.tahmin(ozellikler(self.sahte("blorp", "?")[0])), "x")
        self.assertEqual(nb.tahmin(ozellikler(self.sahte("zindle", "?")[0])), "y")

    def test_kapi_sizintili_veriyi_durdurur(self):
        veri = [self.sahte("blorp" if i % 2 else "zindle", "x" if i % 2 else None, kimlik=i) for i in range(40)]
        with self.assertRaises(KisaYolHatasi):
            kapi_denetle([b for b, _ in veri], [c for _, c in veri], laplace=1, pay=PRM.sans_payi)

    def test_kapi_bilgisiz_veriyi_gecirir(self):
        rng = random.Random(13)
        veri = [self.sahte("blorp", rng.choice(["x", "y", "z"]), kimlik=7) for _ in range(60)]
        dogruluk, sans = kapi_denetle([b for b, _ in veri], [c for _, c in veri], laplace=1, pay=PRM.sans_payi)
        self.assertLessEqual(dogruluk, sans + PRM.sans_payi)

    def test_treg_ayrimi_dedektorle_tutarli(self):
        sonuc = bolme_uret("egitim", KUCUK, TANIM, SEMA, SEMA_YOLU)
        nb = NaiveBayes(KUCUK.laplace)
        nb.egit([ozellikler(a.bolum) for a in sonuc["dedektor"]], [a.cevap["cevap"] for a in sonuc["dedektor"]])
        for a in sonuc["treg"]:
            self.assertEqual(nb.tahmin(ozellikler(a.bolum)), a.cevap["cevap"])
            self.assertEqual(a.cevap["kume"], "treg")
        for a in sonuc["ana"]:
            self.assertNotEqual(nb.tahmin(ozellikler(a.bolum)), a.cevap["cevap"])
            self.assertEqual(a.cevap["kume"], "ana")
        self.assertEqual(len(sonuc["ana"]), KUCUK.ana_kume_sayisi)
        ozetler = [a.bolum["ozet"] for k in ("ana", "treg", "dedektor") for a in sonuc[k]]
        self.assertEqual(len(ozetler), len(set(ozetler)))

    def test_dedektor_gercek_kisa_yolu_yakalar(self):
        """Dedektör değersiz değil: dikkat dağıtıcısız, Treg ayrımı yapılmamış ham veride kapı kapanmalı."""
        prm = dataclasses.replace(PRM, dikkat_dagitici=0)
        rng = random.Random(7)
        adaylar = [aday_uret(rng, TANIM, prm, "egitim") for _ in range(600)]
        with self.assertRaises(KisaYolHatasi):
            kapi_denetle([a.bolum for a in adaylar], [a.cevap for a in adaylar], laplace=1, pay=PRM.sans_payi)

    def test_ilk_kabul_olcutu_gercek_parametrelerle(self):
        """KODLAMA_PROMPTU §6: kelime çantası sınıflayıcısı ana kümede şans + %5'i geçmemeli (config boyutlarıyla)."""
        for bolme in ("egitim", "uzunluk"):
            sonuc = bolme_uret(bolme, PRM, TANIM, SEMA, SEMA_YOLU)
            dogruluk, sans = sonuc["kapi"]
            self.assertLessEqual(dogruluk, sans + PRM.sans_payi, bolme)


class BelirlenimTesti(unittest.TestCase):
    def test_ayni_tohum_ayni_cikti_farkli_tohum_farkli(self):
        def bayt(prm):
            s = bolme_uret("yon_ters", prm, TANIM, SEMA, SEMA_YOLU)
            return kanonik_json([[a.bolum, a.cevap] for k in ("dedektor", "ana", "treg") for a in s[k]])
        self.assertEqual(bayt(KUCUK), bayt(KUCUK))
        self.assertNotEqual(bayt(KUCUK), bayt(dataclasses.replace(KUCUK, tohum=KUCUK.tohum + 1)))

    def test_hepsini_uret_dosyalari_ve_manifest(self):
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            m1 = hepsini_uret(Path(d1), KUCUK, TANIM, SEMA, SEMA_YOLU, KOK / "kilit" / "yok.json", KOK)
            hepsini_uret(Path(d2), KUCUK, TANIM, SEMA, SEMA_YOLU, KOK / "kilit" / "yok.json", KOK)
            adlar = sorted(p.relative_to(d1).as_posix() for p in Path(d1).rglob("*") if p.is_file())
            self.assertEqual(adlar, sorted(p.relative_to(d2).as_posix() for p in Path(d2).rglob("*") if p.is_file()))
            for ad in adlar:
                self.assertEqual((Path(d1) / ad).read_bytes(), (Path(d2) / ad).read_bytes(), ad)
            self.assertIn("ozet.json", adlar)
            import hashlib
            self.assertEqual(sorted(m1["dosyalar"]), sorted(a for a in adlar if a != "ozet.json"))
            for dosya, deger in m1["dosyalar"].items():
                self.assertEqual(hashlib.sha256((Path(d1) / dosya).read_bytes()).hexdigest(), deger)
            for bolme in uretec.BOLMELER:
                self.assertIn(bolme, m1["kapilar"])
            ozetler = []
            for ad in adlar:
                if ad.startswith("bolumler/") and ad.endswith(".jsonl"):
                    ozetler += [json.loads(s)["ozet"] for s in (Path(d1) / ad).read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(ozetler), len(set(ozetler)), "bölmeler arası yineleme")
            for ad in adlar:
                if ad.startswith("bolumler/"):
                    metin = (Path(d1) / ad).read_text(encoding="utf-8")
                    self.assertNotIn('"cevap"', metin, ad)
                    self.assertNotIn('"bolme"', metin, ad)


class KilitliKumeTesti(unittest.TestCase):
    def test_kayit_yoksa_bos(self):
        self.assertEqual(kilitli_ozetler(KOK / "kilit" / "yok.json", KOK), frozenset())

    def test_hash_dogrulanir_ve_kesisim_durdurur(self):
        with tempfile.TemporaryDirectory() as d:
            kok = Path(d)
            aday = aday_uret(random.Random(7), TANIM, PRM, "egitim")
            (kok / "altin.jsonl").write_bytes(kanonik_json(aday.bolum) + b"\n")
            import hashlib
            kayit = {"kumeler": {"altin": {"dosya": "altin.jsonl", "algoritma": "sha256",
                                           "ozet": hashlib.sha256((kok / "altin.jsonl").read_bytes()).hexdigest()}}}
            (kok / "kumeler.json").write_text(json.dumps(kayit), encoding="utf-8")
            yasakli = kilitli_ozetler(kok / "kumeler.json", kok)
            self.assertEqual(yasakli, frozenset([aday.bolum["ozet"]]))
            with self.assertRaises(KilitliKumeHatasi):
                kesisim_denetle(yasakli, [aday.bolum["ozet"]])
            kesisim_denetle(yasakli, ["0" * 64])
            with open(kok / "altin.jsonl", "ab") as f:
                f.write(b"\n")
            with self.assertRaises(KilitliKumeHatasi):
                kilitli_ozetler(kok / "kumeler.json", kok)

    def test_uretim_kilitli_kumeyle_kesisirse_durur(self):
        ilk = bolme_uret("egitim", KUCUK, TANIM, SEMA, SEMA_YOLU)
        yasakli = frozenset([ilk["ana"][0].bolum["ozet"]])
        with self.assertRaises(KilitliKumeHatasi):
            bolme_uret("egitim", KUCUK, TANIM, SEMA, SEMA_YOLU, yasakli=yasakli)


if __name__ == "__main__":
    unittest.main()
