"""KODLAMA_PROMPTU §9: tüm testleri tek komutla koşturur, ham çıktıyı ve zorunlu sayaç satırını basar.

Kullanım: python3 araclar/kostur.py
"""
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def main():
    sys.path.insert(0, str(KOK))
    paket = unittest.defaultTestLoader.discover(str(KOK / "testler"), pattern="test_*.py",
                                                top_level_dir=str(KOK))
    sonuc = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(paket)  # KODLAMA_PROMPTU §9: ham çıktıda her testin adı
    gecen = (sonuc.testsRun - len(sonuc.failures) - len(sonuc.errors) - len(sonuc.skipped)
             - len(sonuc.expectedFailures) - len(sonuc.unexpectedSuccesses))
    print(f"SAYAÇ: koşulan={sonuc.testsRun} geçen={gecen} kalan={len(sonuc.failures)} "
          f"hata={len(sonuc.errors)} atlanan={len(sonuc.skipped)} "
          f"xfail={len(sonuc.expectedFailures)} beklenmedik_geçen={len(sonuc.unexpectedSuccesses)}")
    return 0 if sonuc.wasSuccessful() and not sonuc.skipped and not sonuc.expectedFailures else 1


if __name__ == "__main__":
    sys.exit(main())
