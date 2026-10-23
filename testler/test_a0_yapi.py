"""KODLAMA_PROMPTU §3, §4: A0 klasör iskeleti, modül başlıkları, izlenebilirlik tablosu."""
import ast
import re
import unittest

from testler.yardimci import (BASLIK_DESENI, KIMLIK_DESENI, KOK, agac, goreli, kayitli_kimlikler,
                              kod_dosyalari)

PAKETLER = ("cekirdek", "cekirdek/altyapi", "tercuman", "degerlendirme", "karsilastirma")
VERI_KLASORLERI = ("veri", "sema", "kilit")
KAYIT_DOSYALARI = ("VARSAYIMLAR.md", "KARARLAR.md", "ILERLEME.md", "DEVIR.md", "DURUM.md",
                   "izlenebilirlik.md", "BAGIMLILIKLAR.md", "LISANSLAR.md", "ONKAYIT.md",
                   "config.json", "kur.sh", "kur.bat")


class IskeletTesti(unittest.TestCase):
    def test_paketler_var(self):
        for p in PAKETLER:
            self.assertTrue((KOK / p / "__init__.py").is_file(), p)

    def test_veri_klasorleri_var(self):
        for k in VERI_KLASORLERI:
            self.assertTrue((KOK / k).is_dir(), k)

    def test_kayit_dosyalari_var(self):
        for d in KAYIT_DOSYALARI:
            self.assertTrue((KOK / d).is_file(), d)


class BaslikTesti(unittest.TestCase):
    def test_her_modulun_basinda_sartname_atfi(self):
        dosyalar = kod_dosyalari()
        self.assertTrue(dosyalar)
        for yol in dosyalar:
            belge = ast_docstring(yol)
            self.assertIsNotNone(belge, f"{goreli(yol)}: modül başlığı (docstring) yok")
            ilk_satir = belge.strip().splitlines()[0]
            self.assertRegex(ilk_satir, BASLIK_DESENI, f"{goreli(yol)}: başlıkta §N atfı yok")

    def test_koddaki_varsayim_kimlikleri_kayitli(self):
        kayitli = kayitli_kimlikler()
        for yol in kod_dosyalari() + [KOK / "config.json"]:
            for kimlik in KIMLIK_DESENI.findall(yol.read_text(encoding="utf-8")):
                self.assertIn(kimlik, kayitli, f"{goreli(yol)}: {kimlik} VARSAYIMLAR/KARARLAR'da yok")


class IzlenebilirlikTesti(unittest.TestCase):
    def satirlar(self):
        metin = (KOK / "izlenebilirlik.md").read_text(encoding="utf-8")
        sonuc = []
        for satir in metin.splitlines():
            if not satir.startswith("|") or set(satir) <= set("|-: "):
                continue
            hucreler = [h.strip() for h in satir.strip("|").split("|")]
            if hucreler[0] == "Şartname":
                continue
            sonuc.append(hucreler)
        return sonuc

    def test_tablo_bicimi(self):
        satirlar = self.satirlar()
        self.assertTrue(satirlar)
        for h in satirlar:
            self.assertEqual(len(h), 3, h)
            self.assertRegex(h[0], BASLIK_DESENI, h)

    def test_her_modul_tabloda(self):
        metin = (KOK / "izlenebilirlik.md").read_text(encoding="utf-8")
        for yol in kod_dosyalari():
            if yol.name == "__init__.py":
                continue
            self.assertIn(f"`{goreli(yol)}`", metin, f"{goreli(yol)} izlenebilirlik.md'de yok")

    def test_tablodaki_dosyalar_var_ve_her_satirin_testi_var(self):
        for sartname, kod, test in self.satirlar():
            for yol in re.findall(r"`([^`]+)`", kod + " " + test):
                self.assertTrue((KOK / yol).exists(), f"tabloda olan {yol} yok")
            self.assertRegex(test, r"`testler/[^`]+\.py`", f"{sartname}: test sütunu boş")


def ast_docstring(yol):
    return ast.get_docstring(agac(yol), clean=True)


if __name__ == "__main__":
    unittest.main()
