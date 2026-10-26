"""K-041 (ÖK-005 taslağı §4 madde 22, §7 B0 bitişi), V-064: M0 koşucusu. Geliştirme havuzunu kurar, M0'ı koşar,
çıktıyı atomik yazar; aynı girdi bit-aynı dosyalar verir. Testte küçük kademe (K1) kullanılır."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from degerlendirme import h2_m0
from testler.yardimci import KOK


class M0KosucuTesti(unittest.TestCase):
    def test_dosyalar_ve_bit_aynilik(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            oz_a = h2_m0.kos(KOK, a, kademe="K1")
            oz_b = h2_m0.kos(KOK, b, kademe="K1")
            for ad in h2_m0.DOSYALAR:
                self.assertEqual((a / ad).read_bytes(), (b / ad).read_bytes(), ad)
            ozet = json.loads((a / "m0_ozet.json").read_text(encoding="utf-8"))
            self.assertEqual(ozet, oz_a)
            self.assertEqual(oz_a, oz_b)
            self.assertEqual(ozet["havuz"], "gelistirme")
            self.assertEqual(len(ozet["dunya_ozetleri"]), 16)
            self.assertEqual(ozet["m0"]["cikti_ozeti"], hashlib.sha256((a / "m0_adaylar.jsonl").read_bytes()).hexdigest())
            self.assertEqual(ozet["m0"]["kademe"], "K1")

    def test_yalniz_gelistirme_havuzu(self):
        with tempfile.TemporaryDirectory() as d, self.assertRaises(ValueError):
            h2_m0.kos(KOK, Path(d), kademe="K1", havuz_adi="final")


if __name__ == "__main__":
    unittest.main()
