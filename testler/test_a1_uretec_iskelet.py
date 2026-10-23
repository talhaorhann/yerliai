"""sistem.md §11, KODLAMA_PROMPTU §3: üreteç tasarımı onay bekliyor (V-015), iskelet çalışıyormuş gibi davranmamalı."""
import unittest

from degerlendirme import uretec


class UretecIskeletTesti(unittest.TestCase):
    def test_onaysiz_uretec_calismaz(self):
        for ad in ("bolum_uret", "kisa_yol_dedektoru"):
            with self.assertRaises(NotImplementedError) as baglam:
                getattr(uretec, ad)()
            self.assertIn("V-01", str(baglam.exception))


if __name__ == "__main__":
    unittest.main()
