"""K-011, V-023, KODLAMA_PROMPTU §5: altın küme soruları (2 × 50, A/B/C/D), kilit kaydı, kullanıcı cevabı ayrıştırma."""
import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.ayar import ayar_yukle
from degerlendirme import altin
from degerlendirme.kilitli_kumeler import KilitliKumeHatasi, kilitli_ozetler
from degerlendirme.uretec import bolme_uret
from testler.test_a1_uretec import KUCUK, SEMA, SEMA_YOLU, TANIM
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")
AP = altin.AltinParametreleri.ayardan(AYAR)


class AltinUretimTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parcalar = altin.altin_uret(AP, KUCUK, TANIM, SEMA)

    def test_parca_ve_soru_sayilari(self):
        self.assertEqual(len(self.parcalar), AYAR.deger("altin_parca_sayisi"))
        for parca in self.parcalar:
            self.assertEqual(len(parca), AYAR.deger("altin_normal_sayisi") + AYAR.deger("altin_bozuk_sayisi"))
            bozuk = [s for s in parca if s["cevap"] is None]
            self.assertEqual(len(bozuk), AYAR.deger("altin_bozuk_sayisi"))

    def test_secenekler(self):
        for parca in self.parcalar:
            for s in parca:
                self.assertEqual(len(s["secenekler"]), len(altin.HARFLER))
                self.assertEqual(s["secenekler"][-1], altin.BILGI_YETMEZ)
                adlar = s["secenekler"][:-1]
                self.assertEqual(len(set(adlar)), len(adlar))
                self.assertTrue(set(adlar) <= set(SEMA.adlar))
                dogru = s["secenekler"][altin.HARFLER.index(s["dogru_harf"])]
                self.assertEqual(dogru, altin.BILGI_YETMEZ if s["cevap"] is None else s["cevap"])

    def test_dogru_harf_dagilimi_tek_tip_degil(self):
        harfler = {s["dogru_harf"] for p in self.parcalar for s in p if s["cevap"] is not None}
        self.assertEqual(harfler, set(altin.HARFLER[:-1]))

    def test_elle_izlenebilir_kucuk_ornekler(self):
        for parca in self.parcalar:
            for s in parca:
                self.assertTrue(KUCUK.egitim_k[0] <= s["k"] <= KUCUK.egitim_k[1])
                self.assertEqual(len(s["bolum"]["olgular"]), s["k"] + AP.dikkat_dagitici)
                self.assertEqual(sorted(s["etiketler"].values()), list(range(1, len(s["etiketler"]) + 1)))

    def test_belirlenim(self):
        self.assertEqual(json.dumps(self.parcalar, sort_keys=True),
                         json.dumps(altin.altin_uret(AP, KUCUK, TANIM, SEMA), sort_keys=True))

    def test_soru_metninde_cevap_yok(self):
        for p_no, parca in enumerate(self.parcalar, start=1):
            metin = altin.parca_metni(p_no, parca)
            for no, s in enumerate(parca, start=1):
                self.assertIn(f"Soru {no}", metin)
            secenek_satirlari = [s for s in metin.splitlines() if ") " in s and "·" in s]
            self.assertEqual(len(secenek_satirlari), len(parca))
            for satir, soru in zip(secenek_satirlari, parca):
                beklenen = "  ·  ".join(f"{h}) {sec.replace('_', ' ')}" for h, sec in zip(altin.HARFLER, soru["secenekler"]))
                self.assertEqual(satir, beklenen)
            self.assertNotIn("dogru", metin.lower())
            self.assertNotIn("doğru cevap", metin.lower())
            self.assertNotIn("ozet", metin)

    def test_egitim_uretimiyle_kesismez(self):
        ozetler = {s["bolum"]["ozet"] for p in self.parcalar for s in p}
        egitim = bolme_uret("egitim", KUCUK, TANIM, SEMA, SEMA_YOLU, yasakli=frozenset(ozetler))
        self.assertTrue(egitim["ana"])


class AltinYazimTesti(unittest.TestCase):
    def test_yaz_kilitle_ve_yeniden_yazmayi_reddet(self):
        with tempfile.TemporaryDirectory() as d:
            kok = Path(d)
            parcalar = altin.altin_uret(AP, KUCUK, TANIM, SEMA)
            kayit = kok / "kilitli_kumeler.json"
            altin.altin_yaz(kok / "altin", parcalar, kayit, kok)
            yasakli = kilitli_ozetler(kayit, kok)
            self.assertEqual(len(yasakli), sum(len(p) for p in parcalar))
            sorular = (kok / "altin" / "altin_sorular.jsonl").read_text(encoding="utf-8")
            self.assertNotIn('"cevap"', sorular)
            self.assertNotIn('"dogru_harf"', sorular)
            self.assertTrue((kok / "altin" / "uretec_cevaplari.jsonl").exists())
            with self.assertRaises(KilitliKumeHatasi):
                altin.altin_yaz(kok / "altin", altin.altin_uret(dataclasses.replace(AP, tohum=AP.tohum + 1), KUCUK, TANIM, SEMA),
                                kayit, kok)

    def test_projedeki_altin_kume_kilitli_ve_tutarli(self):
        kayit = KOK / "kilit" / "kilitli_kumeler.json"
        yasakli = kilitli_ozetler(kayit, KOK)
        beklenen = AYAR.deger("altin_parca_sayisi") * (AYAR.deger("altin_normal_sayisi") + AYAR.deger("altin_bozuk_sayisi"))
        self.assertEqual(len(yasakli), beklenen)


class KullaniciCevabiTesti(unittest.TestCase):
    def test_coz(self):
        self.assertEqual(altin.kullanici_cevaplarini_coz("1B 2a 3?  4D", 4), {1: "B", 2: "A", 3: "?", 4: "D"})
        self.assertEqual(altin.kullanici_cevaplarini_coz("1-B, 2-C\n3) D 4.A", 4), {1: "B", 2: "C", 3: "D", 4: "A"})

    def test_eksik_fazla_ya_da_yinelenen_reddedilir(self):
        for kotu in ("1B 2A 3C", "1B 2A 3C 4D 5A", "1B 1C 3A 4D", "1B 2E 3A 4D", "1B 2A 3C 4"):
            with self.assertRaises(ValueError, msg=kotu):
                altin.kullanici_cevaplarini_coz(kotu, 4)

    def test_karsilastir(self):
        uretec = {1: "A", 2: "B", 3: "D", 4: "C"}
        farkli, emin_degil = altin.karsilastir({1: "A", 2: "C", 3: "?", 4: "C"}, uretec)
        self.assertEqual((farkli, emin_degil), ([2], [3]))


if __name__ == "__main__":
    unittest.main()
