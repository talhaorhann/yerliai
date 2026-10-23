"""KODLAMA_PROMPTU §5 (Uzun koşular): atomik kayıt, üreteç durumu, öldürülüp devam eden koşu = kesintisiz koşu."""
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz, durum_kaydet, durum_yukle, uretec_durumu, uretec_kur
from testler.yardimci import KOK


class AtomikTesti(unittest.TestCase):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.klasor = Path(self._d.name)

    def tearDown(self):
        self._d.cleanup()

    def test_yazar_ve_gecici_dosya_birakmaz(self):
        yol = self.klasor / "a.bin"
        atomik_yaz(yol, b"birinci")
        atomik_yaz(yol, b"ikinci")
        self.assertEqual(yol.read_bytes(), b"ikinci")
        self.assertEqual(sorted(p.name for p in self.klasor.iterdir()), ["a.bin"])

    def test_yarim_kalan_gecici_dosya_asli_bozmaz(self):
        """Yazma yeniden adlandırmadan önce kesilirse eski durum aynen okunur."""
        yol = self.klasor / "durum.json"
        durum_kaydet(yol, {"adim": 7})
        (self.klasor / "durum.json.gecici").write_bytes(b'{"adim": 8, "yar')
        self.assertEqual(durum_yukle(yol), {"adim": 7})

    def test_bayt_olarak_yalniz_bytes_kabul(self):
        with self.assertRaises(TypeError):
            atomik_yaz(self.klasor / "a", "metin")

    def test_uretec_durumu_json_uzerinden_doner(self):
        rng = random.Random(13)
        rng.random()
        durum = json.loads(json.dumps(uretec_durumu(rng)))
        kopya = uretec_kur(durum)
        self.assertEqual([rng.randrange(10**9) for _ in range(11)],
                         [kopya.randrange(10**9) for _ in range(11)])


class OldurDevamTesti(unittest.TestCase):
    ADIM = 13
    TOHUM = 7

    def kos(self, durum_yolu, olunecek=None):
        arg = [sys.executable, "-m", "testler.yardimci_uzun_kosu", str(durum_yolu), str(self.TOHUM), str(self.ADIM)]
        if olunecek is not None:
            arg.append(str(olunecek))
        return subprocess.run(arg, cwd=KOK, capture_output=True, text=True, timeout=60)

    def test_olduruldukten_sonra_devam_kesintisizle_ayni(self):
        with tempfile.TemporaryDirectory() as d:
            kesintisiz = self.kos(Path(d) / "a.json")
            self.assertEqual(kesintisiz.returncode, 0, kesintisiz.stderr)

            yol = Path(d) / "b.json"
            olen = self.kos(yol, olunecek=5)
            self.assertNotEqual(olen.returncode, 0, "süreç gerçekten öldürülmedi")
            self.assertEqual(durum_yukle(yol)["adim"], 5)
            devam = self.kos(yol)
            self.assertEqual(devam.returncode, 0, devam.stderr)

            self.assertEqual(kesintisiz.stdout, devam.stdout)
            self.assertEqual(durum_yukle(Path(d) / "a.json"), durum_yukle(yol))
            self.assertEqual(sorted(os.listdir(d)), ["a.json", "b.json"])


if __name__ == "__main__":
    unittest.main()
