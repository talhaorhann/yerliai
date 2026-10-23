"""KODLAMA_PROMPTU §2.4: dil veridir. Veri dosyalarındaki hiçbir ilişki adı kodda (yorum dahil) geçemez."""
import json
import re
import unittest

from testler.yardimci import KOK, goreli, kod_dosyalari

SOZCUK = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşü_]+")


def turkce_kucuk(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def veri_sozcukleri():
    """sema/ ve veri/ altındaki ilişki şeması dosyalarından ilişki adları."""
    sozcukler = set()
    for yol in sorted((KOK / "sema").glob("iliskiler_*.json")) + sorted((KOK / "veri").rglob("iliskiler_*.json")):
        for iliski in json.loads(yol.read_text(encoding="utf-8"))["iliskiler"]:
            sozcukler.add(turkce_kucuk(iliski["ad"]))
            sozcukler.update(turkce_kucuk(p) for p in iliski["ad"].split("_") if p)
    return sozcukler


def ihlaller(metin, sozcukler, ad):
    bulunan = []
    for no, satir in enumerate(metin.splitlines(), start=1):
        for sozcuk in SOZCUK.findall(satir):
            if turkce_kucuk(sozcuk) in sozcukler:
                bulunan.append(f"{ad}:{no} '{sozcuk}'")
    return bulunan


class DilVeridirTesti(unittest.TestCase):
    def test_sozluk_bos_degil(self):
        self.assertTrue(veri_sozcukleri(), "tarama anlamsız: hiç ilişki adı bulunamadı")

    def test_kodda_iliski_sozcugu_yok(self):
        sozcukler = veri_sozcukleri()
        dosyalar = kod_dosyalari() + sorted((KOK / "testler").glob("*.py"))
        bulunan = []
        for yol in dosyalar:
            bulunan.extend(ihlaller(yol.read_text(encoding="utf-8"), sozcukler, goreli(yol)))
        self.assertEqual(bulunan, [])

    def test_tarayici_yakalar(self):
        sozcukler = {"blorp", "zindle"}
        metin = "x = 1\nif r == 'Blorp':  # zindle\n    pass\nblorpish = 2\n"
        self.assertEqual(ihlaller(metin, sozcukler, "ornek.py"), ["ornek.py:2 'Blorp'", "ornek.py:2 'zindle'"])

    def test_turkce_buyuk_kucuk(self):
        self.assertEqual(turkce_kucuk("IŞIK"), "ışık")
        self.assertEqual(turkce_kucuk("İPEK"), "ipek")


if __name__ == "__main__":
    unittest.main()
