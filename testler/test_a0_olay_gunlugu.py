"""KODLAMA_PROMPTU §5 (Defter, Hata yutma yok): sadece-ekleme, sıra numaralı, hash zincirli olay günlüğü."""
import json
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import KanonikHata, kanonik_json, ozet
from cekirdek.altyapi.olay_gunlugu import YEDEK_KULLANILDI, KayitHatasi, OlayGunlugu, ZincirHatasi
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")


def gunluk(yol):
    return OlayGunlugu(yol, algoritma=AYAR.deger("hash_algoritmasi"),
                       sema_surumu=AYAR.deger("olay_sema_surumu"),
                       izinli_kaynaklar=AYAR.deger("kaynaklar"))


class KanonikTesti(unittest.TestCase):
    def test_anahtar_sirasi_onemsiz(self):
        self.assertEqual(kanonik_json({"b": 1, "a": [2, "ğ"]}), kanonik_json({"a": [2, "ğ"], "b": 1}))

    def test_nan_inf_reddedilir(self):
        for kotu in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(KanonikHata):
                kanonik_json({"x": kotu})

    def test_json_disi_tip_reddedilir(self):
        for kotu in ({1, 2}, b"x", object()):
            with self.assertRaises(KanonikHata):
                kanonik_json({"x": kotu})

    def test_ozet_bilinen_deger(self):
        # Bağımsız hesap: sha256(b'{"a":1}')
        self.assertEqual(ozet(kanonik_json({"a": 1}), "sha256"),
                         "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862")


class GunlukTesti(unittest.TestCase):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.yol = Path(self._d.name) / "olaylar.jsonl"

    def tearDown(self):
        self._d.cleanup()

    def satirlar(self):
        return self.yol.read_text(encoding="utf-8").splitlines()

    def test_sira_ve_zincir(self):
        g = gunluk(self.yol)
        a = g.ekle("DENEME", "çekirdek", {"i": 7})
        b = g.ekle("DENEME", "çekirdek", {"i": 11})
        self.assertEqual((a["sira"], b["sira"]), (0, 1))
        self.assertEqual(b["onceki_ozet"], a["ozet"])
        self.assertEqual(len(self.satirlar()), 2)

    def test_ozet_kaydin_kendi_icerigidir(self):
        g = gunluk(self.yol)
        k = g.ekle("DENEME", "çekirdek", {"i": 13})
        govde = {a: d for a, d in k.items() if a != "ozet"}
        self.assertEqual(k["ozet"], ozet(kanonik_json(govde), "sha256"))

    def test_yeniden_acinca_zincir_surer(self):
        g = gunluk(self.yol)
        g.ekle("DENEME", "çekirdek", {"i": 7})
        ikinci = gunluk(self.yol)
        k = ikinci.ekle("DENEME", "çekirdek", {"i": 11})
        self.assertEqual(k["sira"], 1)
        self.assertEqual(len(ikinci.kayitlar()), 2)

    def test_degistirilmis_kayit_yakalanir(self):
        g = gunluk(self.yol)
        g.ekle("DENEME", "çekirdek", {"i": 7})
        g.ekle("DENEME", "çekirdek", {"i": 11})
        satirlar = self.satirlar()
        satirlar[0] = satirlar[0].replace('"i":7', '"i":8')
        self.yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        with self.assertRaises(ZincirHatasi):
            gunluk(self.yol)

    def test_silinmis_kayit_yakalanir(self):
        g = gunluk(self.yol)
        for i in range(3):
            g.ekle("DENEME", "çekirdek", {"i": i})
        satirlar = self.satirlar()
        del satirlar[1]
        self.yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        with self.assertRaises(ZincirHatasi):
            gunluk(self.yol)

    def test_ozeti_yeniden_hesaplanmis_sahte_kayit_yakalanir(self):
        """Saldırgan bir kaydı değiştirip özetini de yeniden hesaplarsa sonraki kaydın bağı kopar."""
        g = gunluk(self.yol)
        g.ekle("DENEME", "çekirdek", {"i": 7})
        g.ekle("DENEME", "çekirdek", {"i": 11})
        satirlar = self.satirlar()
        ilk = json.loads(satirlar[0])
        ilk["veri"]["i"] = 8
        ilk["ozet"] = ozet(kanonik_json({a: d for a, d in ilk.items() if a != "ozet"}), "sha256")
        satirlar[0] = kanonik_json(ilk).decode("utf-8")
        self.yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        with self.assertRaises(ZincirHatasi):
            gunluk(self.yol)

    def test_yarim_satir_yakalanir(self):
        g = gunluk(self.yol)
        g.ekle("DENEME", "çekirdek", {"i": 7})
        with open(self.yol, "a", encoding="utf-8") as f:
            f.write('{"sira":1,"tu')
        with self.assertRaises(ZincirHatasi):
            gunluk(self.yol)

    def test_kaynaksiz_ya_da_bilinmeyen_kaynak_reddedilir(self):
        g = gunluk(self.yol)
        for kaynak in ("", "uydurma", None):
            with self.assertRaises(KayitHatasi):
                g.ekle("DENEME", kaynak, {})
        self.assertFalse(self.yol.exists() and self.satirlar())

    def test_bicimsiz_tur_ve_veri_reddedilir(self):
        g = gunluk(self.yol)
        for tur, veri in (("", {}), ("kucuk harf", {}), ("DENEME", [1]), ("DENEME", {"x": float("nan")})):
            with self.assertRaises((KayitHatasi, KanonikHata)):
                g.ekle(tur, "çekirdek", veri)
        self.assertEqual(g.kayitlar(), [])

    def test_yedek_kullanildi_sayaci(self):
        g = gunluk(self.yol)
        self.assertEqual(g.sayac(YEDEK_KULLANILDI), 0)
        g.yedek_kullanildi("çekirdek", yer="ornek.py:7", neden="deneme")
        g.ekle("DENEME", "çekirdek", {})
        g.yedek_kullanildi("üreteç", yer="ornek.py:11", neden="deneme")
        self.assertEqual(g.sayac(YEDEK_KULLANILDI), 2)
        self.assertEqual(gunluk(self.yol).sayac(YEDEK_KULLANILDI), 2)

    def test_deterministik_bayt_esitligi(self):
        yol2 = Path(self._d.name) / "ikinci.jsonl"
        for y in (self.yol, yol2):
            g = gunluk(y)
            g.ekle("DENEME", "çekirdek", {"b": 1, "a": "ş"})
            g.yedek_kullanildi("çekirdek", yer="x", neden="y")
        self.assertEqual(self.yol.read_bytes(), yol2.read_bytes())


if __name__ == "__main__":
    unittest.main()
