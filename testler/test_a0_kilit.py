"""KODLAMA_PROMPTU §5 (Kilitli kümeler), §6: test ve eşik dosyaları hash kilidinde (V-008)."""
import hashlib
import json
import unittest

from testler.yardimci import KOK


def kilitler():
    return json.loads((KOK / "kilit" / "kilitler.json").read_text(encoding="utf-8"))


class KilitTesti(unittest.TestCase):
    def test_kilitli_dosyalar_degismemis(self):
        kilit = kilitler()
        self.assertEqual(kilit["algoritma"], "sha256")
        degisen = []
        for yol, beklenen in sorted(kilit["dosyalar"].items()):
            gercek = hashlib.sha256((KOK / yol).read_bytes()).hexdigest()
            if gercek != beklenen:
                degisen.append(yol)
        self.assertEqual(degisen, [], "kilitli dosya değişmiş; kullanıcı onayı gerekir")

    def test_her_test_dosyasi_ve_config_kilitli(self):
        kilitli = set(kilitler()["dosyalar"])
        beklenen = {p.relative_to(KOK).as_posix() for p in (KOK / "testler").rglob("*") if p.is_file()
                    and "__pycache__" not in p.parts}
        beklenen.add("config.json")
        beklenen.add("config_h2.json")  # V-060
        self.assertEqual(sorted(beklenen - kilitli), [], "kilitsiz test/eşik dosyası var")


if __name__ == "__main__":
    unittest.main()
