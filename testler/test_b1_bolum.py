"""K-041, K-043 (ÖK-005 taslağı §2.1 gövde-merkezli bölüm, §5 tohumlar): aşama 5 gözlem bölümleri. Bölüm, adayın
gövdesinin dünyadaki bir eşleşmesinin kişileri + kısa yürüyüş + dikkat dağıtıcı bağlardan kurulur ve bu kişiler
arasındaki bütün olguları içerir (kapalı dünya). Kişi kimlikleri karıştırılır. Testler sentetik dünyada, anlamsız
ilişki adlarıyla."""
import random
import unittest

from degerlendirme import h2_bolum, kural
from kesif import m0

A, B, C = "zra", "zrb", "zrc"


def yol_dunyasi(n=12):
    olg = ({(i, A, i + 1) for i in range(n - 1)} | {(i + 1, B, i) for i in range(n - 1)}
           | {(i, C, i + 2) for i in range(n - 2)})
    return m0.Dunya("F1", tuple(range(n)), tuple(sorted(olg)))


def k(halkalar, bas):
    return kural.Kural(halkalar, bas, ())


class BolumTesti(unittest.TestCase):
    TEMEL = (A, B)

    def test_govde_eslesmesi_bolumde_ve_kapali_dunya(self):
        d = yol_dunyasi()
        aday = k([(A, "X", "Z"), (A, "Z", "Y")], (C, "X", "Y"))
        b = h2_bolum.govde_merkezli(d, aday, self.TEMEL, random.Random(1), (2, 3), 2, "e1")
        geri = {v: w for w, v in b.esleme.items()}
        olgular = {(geri[x], r, geri[y]) for x, r, y in b.olgular}
        kisiler = set(geri.values())
        self.assertEqual(olgular, {o for o in d.olgular if o[0] in kisiler and o[2] in kisiler})
        idx = kural.Indeks(b.olgular)
        self.assertTrue(aday.tahminler(idx))  # seçilen eşleşme bölümde
        self.assertEqual(len(set(b.esleme.values())), len(b.esleme))

    def test_belirlenimci_ve_tohuma_bagli(self):
        d = yol_dunyasi()
        aday = k([(A, "X", "Y")], (B, "Y", "X"))
        a = h2_bolum.govde_merkezli(d, aday, self.TEMEL, random.Random(5), (2, 3), 2, "e")
        b = h2_bolum.govde_merkezli(d, aday, self.TEMEL, random.Random(5), (2, 3), 2, "e")
        c = h2_bolum.govde_merkezli(d, aday, self.TEMEL, random.Random(6), (2, 3), 2, "e")
        self.assertEqual((a.olgular, a.esleme, a.ozet), (b.olgular, b.esleme, b.ozet))
        self.assertNotEqual((a.esleme, a.olgular), (c.esleme, c.olgular))

    def test_eslesme_yoksa_bolum_yok(self):
        d = yol_dunyasi()
        aday = k([(C, "X", "Z"), (C, "Z", "W"), (C, "W", "Y")], (A, "X", "Y"))
        self.assertIsNotNone(aday)
        yok = k([(B, "X", "Z"), (C, "Z", "Y")], (A, "X", "Y"))
        self.assertIsNone(h2_bolum.govde_merkezli(m0.Dunya("F1", (0, 1), ((0, A, 1),)), yok, self.TEMEL,
                                                  random.Random(1), (2, 3), 2, "e"))

    def test_ozet_icerikten(self):
        d = yol_dunyasi()
        aday = k([(A, "X", "Y")], (B, "Y", "X"))
        b = h2_bolum.govde_merkezli(d, aday, self.TEMEL, random.Random(2), (2, 3), 2, "e")
        self.assertEqual(b.ozet, h2_bolum.bolum_ozeti(b.olgular))
        self.assertNotEqual(b.ozet, h2_bolum.bolum_ozeti(b.olgular[1:]))


if __name__ == "__main__":
    unittest.main()
