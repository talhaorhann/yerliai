"""K-041, K-043 (ÖK-005 taslağı §9 madde 1), V-065: ön kayıt tutmazsa koşu başlamaz. Sahte depo: ÖK-005 bölümü, taslak,
çekirdek ve keşif klasörleri, ek tablolarında dosya özetleri (sonraki ek öncekinin yerine geçer), gizli dosya özeti."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from araclar.cekirdek_ozeti import ozet_al
from degerlendirme import h2_onkayit as OK


def h(b):
    return hashlib.sha256(b).hexdigest()


class KucukAyar:
    def __init__(self, **d):
        self.degerler = d

    def deger(self, ad):
        return self.degerler[ad]


class DepoTesti(unittest.TestCase):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        k = self.kok = Path(self._d.name)
        for klasor, icerik in (("cekirdek", b"x = 1\n"), ("kesif", b"y = 2\n")):
            (k / klasor).mkdir()
            (k / klasor / "a.py").write_bytes(icerik)
        (k / "ONKAYIT_H2_TASLAK.md").write_bytes(b"taslak")
        (k / "m.py").write_bytes(b"eski")
        (k / "g.json").write_bytes(b"gizli")
        self.yaz(f"| `m.py` | `{h(b'eski')}` |\n")

    def tearDown(self):
        self._d.cleanup()

    def yaz(self, ek):
        k = self.kok
        (k / "ONKAYIT.md").write_text(
            f"## ÖK-004 sonucu\n| `m.py` | `{'0' * 64}` |\n\n## ÖK-005 (H2): mühür (Kapı 1)\n"
            f"**Metin:** `ONKAYIT_H2_TASLAK.md`, sha256 `{h(b'taslak')}`.\n"
            f"   - çekirdek özeti (`araclar/cekirdek_ozeti.py`): `{ozet_al(k / 'cekirdek')}`;\n"
            f"   - keşif paketi özeti: `{ozet_al(k / 'kesif')}`.\n### ÖK-005 eki §1\n{ek}\n## Başka\n| `m.py` | `{'1' * 64}` |\n",
            encoding="utf-8")

    def test_tutuyor(self):
        self.assertTrue(OK.denetle(self.kok))
        self.assertEqual(OK.beklenenler((self.kok / "ONKAYIT.md").read_text(encoding="utf-8"))["m.py"], h(b"eski"))

    def test_degisen_dosya_ve_sonraki_ek(self):
        (self.kok / "m.py").write_bytes(b"yeni")
        with self.assertRaisesRegex(OK.OnkayitHatasi, "m.py"):
            OK.denetle(self.kok)
        self.yaz(f"| `m.py` | `{h(b'eski')}` |\n### ÖK-005 eki §2\n| `m.py` | `{h(b'yeni')}` |\n")
        self.assertTrue(OK.denetle(self.kok))

    def test_cekirdek_kesif_taslak(self):
        for yol in ("cekirdek/a.py", "kesif/a.py", "ONKAYIT_H2_TASLAK.md"):
            eski = (self.kok / yol).read_bytes()
            (self.kok / yol).write_bytes(eski + b"#")
            with self.assertRaises(OK.OnkayitHatasi):
                OK.denetle(self.kok)
            (self.kok / yol).write_bytes(eski)
        (self.kok / "kesif" / "yeni.py").write_bytes(b"")
        with self.assertRaisesRegex(OK.OnkayitHatasi, "kesif/"):
            OK.denetle(self.kok)

    def test_gizli_dosya_ozeti(self):
        self.assertTrue(OK.denetle(self.kok, KucukAyar(kirmizi_gizli_dosyasi={"yol": "g.json", "ozet": h(b"gizli")})))
        with self.assertRaisesRegex(OK.OnkayitHatasi, "gizli"):
            OK.denetle(self.kok, KucukAyar(kirmizi_gizli_dosyasi={"yol": "g.json", "ozet": "0" * 64}))

    def test_muhur_yoksa(self):
        (self.kok / "ONKAYIT.md").write_text("## ÖK-004\n", encoding="utf-8")
        with self.assertRaises(OK.OnkayitHatasi):
            OK.denetle(self.kok)

    def test_tablo(self):
        self.assertIn("| `m.py` | `", OK.tablo(OK.dosya_ozetleri(self.kok, ["m.py"])))


if __name__ == "__main__":
    unittest.main()
