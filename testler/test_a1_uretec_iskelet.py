"""sistem.md §10, KODLAMA_PROMPTU §3: onaysız "önsel-ters" bölmesi (V-020) çalışıyormuş gibi davranmamalı."""
import random
import unittest

from degerlendirme import uretec


class UretecIskeletTesti(unittest.TestCase):
    def test_onaysiz_bolme_calismaz(self):
        with self.assertRaises(NotImplementedError) as baglam:
            uretec.aday_uret(random.Random(7), None, None, "onsel_ters")
        self.assertIn("V-020", str(baglam.exception))
        self.assertNotIn("onsel_ters", uretec.BOLMELER)


if __name__ == "__main__":
    unittest.main()
