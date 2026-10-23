"""KODLAMA_PROMPTU §2, §6: yasak kalıp taramaları (import yönü, kâhin yalıtımı, sihirli sayı, test atlatma)."""
import ast
import json
import sys
import unittest

from testler.yardimci import (ETIKET_DESENI, KIMLIK_DESENI, KOK, agac, goreli, importlar, kayitli_kimlikler,
                              kod_dosyalari)

PROJE_PAKETLERI = {"cekirdek", "tercuman", "degerlendirme", "karsilastirma", "araclar", "testler"}


def ayar_degeri(ad):
    return json.loads((KOK / "config.json").read_text(encoding="utf-8"))["degerler"][ad]["deger"]


def paket_dosyalari(paket):
    return sorted((KOK / paket).rglob("*.py"))


class CekirdekImportTesti(unittest.TestCase):
    """Çekirdek yalnız standart kütüphane (ağ hariç) + kendi + izinli ek paketleri import eder."""

    def test_cekirdek_importlari_izinli(self):
        izinli_ek = set(ayar_degeri("izinli_ek_paketler"))
        yasak = set(ayar_degeri("yasak_cekirdek_modulleri"))
        dosyalar = paket_dosyalari("cekirdek")
        self.assertTrue(dosyalar)
        for yol in dosyalar:
            for kok, tam, seviye, satir in importlar(yol):
                yer = f"{goreli(yol)}:{satir} '{tam}'"
                if seviye > 0:
                    continue  # göreli import paket içinde kalır
                self.assertNotEqual(kok, "<dinamik>", f"{yer}: dinamik import yasak")
                self.assertNotIn(kok, yasak, f"{yer}: çekirdekte yasak modül")
                if kok == "cekirdek":
                    continue
                self.assertNotIn(kok, PROJE_PAKETLERI, f"{yer}: çekirdek başka proje paketine bağlanamaz")
                self.assertTrue(kok in sys.stdlib_module_names or kok in izinli_ek,
                                f"{yer}: izinli liste dışı paket")

    def test_yasak_liste_ag_modullerini_kapsar(self):
        yasak = set(ayar_degeri("yasak_cekirdek_modulleri"))
        for ad in ("socket", "ssl", "http", "urllib", "subprocess"):
            self.assertIn(ad, yasak)

    def test_tarayici_yasak_importu_yakalar(self):
        """Taramanın kendisi de sınanır: yasak örnekler gerçekten yakalanmalı."""
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            for kod, beklenen in (("import socket\n", "socket"), ("from tercuman import x\n", "tercuman"),
                                  ("__import__('os')\n", "<dinamik>")):
                yol = Path(d) / "ornek.py"
                yol.write_text(kod, encoding="utf-8")
                self.assertIn(beklenen, [k for k, _, _, _ in importlar(yol)])


class BagimlilikYonuTesti(unittest.TestCase):
    def test_kahin_yalnizca_degerlendirmede(self):
        """degerlendirme/ yalnız kendisi ve testler tarafından import edilebilir (kâhin yalıtımı)."""
        for paket in ("cekirdek", "tercuman", "karsilastirma", "araclar"):
            for yol in paket_dosyalari(paket):
                for kok, tam, _, satir in importlar(yol):
                    self.assertNotEqual(kok, "degerlendirme", f"{goreli(yol)}:{satir}")

    def test_karsilastirma_kimseye_sizmaz(self):
        for paket in ("cekirdek", "tercuman", "degerlendirme"):
            for yol in paket_dosyalari(paket):
                for kok, _, _, satir in importlar(yol):
                    self.assertNotEqual(kok, "karsilastirma", f"{goreli(yol)}:{satir}")

    def test_tercuman_degerlendirmeye_baglanmaz(self):
        for yol in paket_dosyalari("tercuman"):
            for kok, _, _, satir in importlar(yol):
                self.assertNotIn(kok, {"degerlendirme", "karsilastirma"}, f"{goreli(yol)}:{satir}")


class SihirliSayiTesti(unittest.TestCase):
    SERBEST = {0, 1}  # V-004

    def sayi_ihlalleri(self, yol, ad=None):
        ad = ad or goreli(yol)
        satirlar = yol.read_text(encoding="utf-8").splitlines()
        ihlaller = []
        for dugum in ast.walk(agac(yol)):
            if (isinstance(dugum, ast.Constant) and isinstance(dugum.value, (int, float, complex))
                    and not isinstance(dugum.value, bool) and dugum.value not in self.SERBEST):
                satir = satirlar[dugum.lineno - 1]
                yorum = satir.split("#", 1)[1] if "#" in satir else ""
                if not ETIKET_DESENI.search(yorum):
                    ihlaller.append(f"{ad}:{dugum.lineno} sayı {dugum.value!r} etiketsiz")
        return ihlaller

    def test_koddaki_her_sayi_etiketli(self):
        ihlaller = []
        for yol in kod_dosyalari():
            ihlaller.extend(self.sayi_ihlalleri(yol))
        self.assertEqual(ihlaller, [])

    def test_tarayici_etiketsiz_sayiyi_yakalar(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "ornek.py"
            yol.write_text("a = 64\nb = 64  # sistem.md §2\nc = 0.95  # V-999\nd = 1\n", encoding="utf-8")
            ihlaller = self.sayi_ihlalleri(yol, ad="ornek.py")
            self.assertEqual(len(ihlaller), 1)
            self.assertIn("ornek.py:1", ihlaller[0])

    def test_etiketlerdeki_kimlikler_kayitli(self):
        kayitli = kayitli_kimlikler()
        for yol in kod_dosyalari():
            for kimlik in KIMLIK_DESENI.findall(yol.read_text(encoding="utf-8")):
                self.assertIn(kimlik, kayitli, goreli(yol))


class TestAtlatmaTesti(unittest.TestCase):
    """skip/xfail sayısı raporda zorunlu satırdır (araclar/kostur.py). A0'da hiç olmamalı."""

    def test_atlanan_test_yok(self):
        bulunan = []
        for yol in sorted((KOK / "testler").glob("*.py")):
            if yol.name == "test_a0_yasak_kaliplar.py":
                continue
            metin = yol.read_text(encoding="utf-8")
            for kalip in ("unittest.skip", "expectedFailure", "skipTest", "@skip"):
                if kalip in metin:
                    bulunan.append(f"{yol.name}: {kalip}")
        self.assertEqual(bulunan, [])


if __name__ == "__main__":
    unittest.main()
