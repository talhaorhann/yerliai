"""KODLAMA_PROMPTU §5 (İstatistik), ÖK-002 §5, V-044: Clopper–Pearson aralığı ve yüzdelik bootstrap.

Clopper–Pearson sınırları tanım denklemiyle, kesir aritmetiğiyle (yuvarlamasız) bağımsızca denetlenir; kapalı
biçimli uç durumlar (0 ve n hata) ayrıca sınanır. Bootstrap aynı tohumla aynı sonucu vermeli.
"""
import math
import unittest
from fractions import Fraction

from degerlendirme.istatistik import bootstrap_araligi, clopper_pearson

GUVEN = 0.95


def kesin_kdf(x, n, p):
    """P(X ≤ x), X ~ Binom(n, p), p kesir olarak: yuvarlamasız."""
    p = Fraction(p)
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))


class ClopperPearsonTesti(unittest.TestCase):
    def test_sifir_ve_tam_hata_kapali_bicim(self):
        alfa = 1 - GUVEN
        for n in (1, 7, 400, 2000):
            alt, ust = clopper_pearson(0, n, GUVEN)
            self.assertEqual(alt, 0.0)
            self.assertAlmostEqual(ust, 1 - (alfa / 2) ** (1 / n), delta=1e-12)
            alt, ust = clopper_pearson(n, n, GUVEN)
            self.assertEqual(ust, 1.0)
            self.assertAlmostEqual(alt, (alfa / 2) ** (1 / n), delta=1e-12)

    def test_tanim_denklemi_kesin_hesapla(self):
        """Üst sınırda P(X ≤ x) = α/2, alt sınırda P(X ≥ x) = α/2 (kesir aritmetiğiyle)."""
        yari = Fraction(1 - GUVEN) / 2
        for x, n in ((1, 10), (3, 13), (11, 400)):
            alt, ust = clopper_pearson(x, n, GUVEN)
            self.assertLess(abs(kesin_kdf(x, n, ust) - yari), Fraction(1, 10 ** 9))
            self.assertLess(abs((1 - kesin_kdf(x - 1, n, alt)) - yari), Fraction(1, 10 ** 9))
            self.assertLess(alt, x / n)
            self.assertGreater(ust, x / n)

    def test_bilinen_deger(self):
        alt, ust = clopper_pearson(1, 10, GUVEN)  # yayımlanmış tablo değeri: (0.00253, 0.44502)
        self.assertAlmostEqual(alt, 0.0025286, delta=1e-6)
        self.assertAlmostEqual(ust, 0.4450161, delta=1e-6)

    def test_gecersiz_girdi(self):
        for x, n in ((-1, 10), (11, 10), (0, 0)):
            with self.assertRaises(ValueError):
                clopper_pearson(x, n, GUVEN)
        with self.assertRaises(ValueError):
            clopper_pearson(1, 10, 1.0)


class BootstrapTesti(unittest.TestCase):
    def test_belirlenimli(self):
        veri = [0.0, 1.0, 0.5, 0.25, 1.0, 0.0, 0.75]
        self.assertEqual(bootstrap_araligi(veri, 997, GUVEN, 13), bootstrap_araligi(veri, 997, GUVEN, 13))
        self.assertNotEqual(bootstrap_araligi(veri, 997, GUVEN, 13), bootstrap_araligi(veri, 997, GUVEN, 17))

    def test_sabit_veri_ve_bos_liste(self):
        self.assertEqual(bootstrap_araligi([0.5] * 11, 101, GUVEN, 7), (0.5, 0.5))
        self.assertIsNone(bootstrap_araligi([], 101, GUVEN, 7))

    def test_aralik_ortalamayi_icerir_ve_daralir(self):
        kucuk = [0.0, 1.0] * 7
        buyuk = [0.0, 1.0] * 700
        a1, u1 = bootstrap_araligi(kucuk, 2001, GUVEN, 7)
        a2, u2 = bootstrap_araligi(buyuk, 2001, GUVEN, 7)
        self.assertTrue(a1 <= 0.5 <= u1 and a2 <= 0.5 <= u2)
        self.assertLess(u2 - a2, u1 - a1)
        self.assertTrue(0.0 <= a1 <= u1 <= 1.0)


if __name__ == "__main__":
    unittest.main()
