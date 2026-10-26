"""K-043 (ÖK-005 taslağı §4 madde 9, 12, 16, 21): Wilson alt sınırı, kümeli Wilson (ICC ANOVA), Laplace gürültüsü,
kümeli bootstrap farkı."""
import math
import random
import unittest

from degerlendirme import istatistik as ist

Z = 1.959963984540054


class WilsonTesti(unittest.TestCase):
    def test_bilinen_degerler(self):
        self.assertAlmostEqual(ist.wilson_alt(22, 22, Z), 0.8513, places=4)
        self.assertAlmostEqual(ist.wilson_alt(220, 244, Z), 0.8578, places=4)
        self.assertAlmostEqual(ist.wilson_alt(3, 3, Z), 0.4385, places=4)
        self.assertEqual(ist.wilson_alt(0, 0, Z), 0.0)
        self.assertLess(ist.wilson_alt(21, 22, Z), ist.wilson_alt(22, 22, Z))

    def test_kumeli_esit_kumelerde_duz_wilson(self):
        kumeler = [(9, 10)] * 20
        self.assertAlmostEqual(ist.kumeli_wilson_alt(kumeler, Z), ist.wilson_alt(180, 200, Z), places=9)

    def test_kumeli_hep_ya_hic_kumelerde_etkin_n_kume_sayisi(self):
        kumeler = [(10, 10)] * 18 + [(0, 10)] * 2
        self.assertAlmostEqual(ist.kumeli_wilson_alt(kumeler, Z), ist.wilson_alt(18, 20, Z), places=6)

    def test_kumeli_tek_kume(self):
        self.assertAlmostEqual(ist.kumeli_wilson_alt([(5, 7)], Z), ist.wilson_alt(5, 7, Z), places=12)


class GurultuVeBootstrapTesti(unittest.TestCase):
    def test_laplace_ortalama_ve_olcek(self):
        rng = random.Random(1)
        cekim = [ist.laplace(rng, 0.5) for _ in range(20000)]
        self.assertAlmostEqual(sum(cekim) / len(cekim), 0.0, delta=0.02)
        self.assertAlmostEqual(sum(abs(c) for c in cekim) / len(cekim), 0.5, delta=0.02)  # E|X| = ölçek

    def test_kumeli_bootstrap_fark(self):
        a = [(90, 100)] * 10
        b = [(80, 100)] * 10
        alt, ust = ist.kumeli_bootstrap_fark(a, b, 2000, 0.95, 3)
        self.assertAlmostEqual(alt, 0.10, places=9)
        self.assertAlmostEqual(ust, 0.10, places=9)
        alt, ust = ist.kumeli_bootstrap_fark([(90, 100), (70, 100)] * 5, b, 2000, 0.95, 3)
        self.assertLess(alt, 0.0 + 1e-12 + 0.05)
        self.assertTrue(alt <= ust)
        self.assertEqual(ist.kumeli_bootstrap_fark(a, b, 500, 0.95, 4), ist.kumeli_bootstrap_fark(a, b, 500, 0.95, 4))


if __name__ == "__main__":
    unittest.main()
