"""K-041, ÖK-005 taslağı §4 madde 5, §7, §13.2 (tanık), V-059 (kapalı dünya): sembolik sayaç. Önce referans (açık döngü),
sonra hızlı (toplu tensör) sürüm; ikisi aynı girdide birebir aynı sayıları vermeli (KODLAMA_PROMPTU §4). Testlerde
ilişki adları anlamsızdır; eksen boyları bilerek farklıdır (7, 11, 13)."""
import random
import unittest

import torch

from cekirdek.sekiller import SEKILLER
from kesif import sablon, sayac

ADLAR = ("zra", "zrb", "zrc")
DEG = ("X", "Y", "Z", "W")


def rastgele_dunya(kisi_sayisi, yogunluk, tohum):
    rng = random.Random(tohum)
    kisiler = tuple(f"k{i}" for i in range(kisi_sayisi))
    olgular = sorted({(a, r, b) for a in kisiler for b in kisiler for r in ADLAR if a != b and rng.random() < yogunluk})
    return kisiler, olgular


class ReferansHizliEsitlikTesti(unittest.TestCase):
    def test_rastgele_dunyalarda_birebir_ayni(self):
        govdeler = sablon.govdeler(len(ADLAR), DEG, 3, False)
        for kisi, yog, tohum, adim in ((7, 0.2, 1, 1), (11, 0.12, 2, 5), (13, 0.08, 3, 23)):
            with self.subTest(kisi=kisi):
                kisiler, olgular = rastgele_dunya(kisi, yog, tohum)
                R = sayac.iliski_tensoru(kisiler, olgular, ADLAR)
                hizli = sayac.sablon_say(govdeler, R, parca_boyu=97)
                for i in range(0, len(govdeler), adim):
                    g = govdeler[i]
                    t, d = sayac.referans_say(g, False, kisiler, olgular, ADLAR)
                    self.assertEqual((int(hizli.tahmin[i]), tuple(int(x) for x in hizli.dogru[i])), (t, d), g)
                    if sablon.oi_anlamli_mi(g):
                        t, d = sayac.referans_say(g, True, kisiler, olgular, ADLAR)
                        self.assertEqual((int(hizli.tahmin_oi[i]), tuple(int(x) for x in hizli.dogru_oi[i])), (t, d), g)

    def test_parca_boyu_sonucu_degistirmez(self):
        govdeler = sablon.govdeler(len(ADLAR), DEG, 2, False)
        kisiler, olgular = rastgele_dunya(11, 0.15, 7)
        R = sayac.iliski_tensoru(kisiler, olgular, ADLAR)
        a, b = sayac.sablon_say(govdeler, R, parca_boyu=1), sayac.sablon_say(govdeler, R, parca_boyu=10 ** 6)
        for alan in ("tahmin", "dogru", "tahmin_oi", "dogru_oi"):
            self.assertTrue((getattr(a, alan) == getattr(b, alan)).all(), alan)


class AnlamTesti(unittest.TestCase):
    """Elle kurulmuş küçük dünyalar: kapalı dünya, tanığın bir kez sayılması, OI, sarkan halka."""
    A, B, C = ADLAR
    X, Y, Z, W = DEG

    def say(self, govde, oi, olgular, kisiler=None):
        kisiler = kisiler or tuple(sorted({k for a, _, b in olgular for k in (a, b)}))
        R = sayac.iliski_tensoru(kisiler, olgular, ADLAR)
        hizli = sayac.sablon_say([govde], R, parca_boyu=7)
        t, d = (hizli.tahmin_oi, hizli.dogru_oi) if oi else (hizli.tahmin, hizli.dogru)
        sonuc = (int(t[0]), tuple(int(x) for x in d[0]))
        self.assertEqual(sonuc, sayac.referans_say(govde, oi, kisiler, olgular, ADLAR))
        return sonuc

    def test_zincir_dogru_ve_kapali_dunya_yanlisi(self):
        olgular = [("p", self.A, "q"), ("q", self.A, "r"), ("r", self.A, "s"), ("p", self.B, "r")]
        govde = ((0, self.X, self.Z), (0, self.Z, self.Y))
        tahmin, dogru = self.say(govde, False, olgular)
        self.assertEqual(tahmin, 2)  # (p, r) ve (q, s)
        self.assertEqual(dogru, (0, 1, 0))  # yalnız (p, r) B ile gözlenmiş; (q, s) ilişkisiz → yanlış

    def test_iki_yoldan_gelen_cift_bir_kez(self):
        olgular = [("p", self.A, "q"), ("q", self.A, "r"), ("p", self.A, "t"), ("t", self.A, "r"), ("p", self.B, "r")]
        tahmin, dogru = self.say(((0, self.X, self.Z), (0, self.Z, self.Y)), False, olgular)
        self.assertEqual((tahmin, dogru[1]), (1, 1))

    def test_oi_ayni_kisiye_baglanmayi_dislar(self):
        olgular = [("p", self.A, "q"), ("r", self.A, "q"), ("p", self.C, "r"), ("r", self.C, "p")]
        govde = ((0, self.X, self.Z), (0, self.Y, self.Z))  # X ile Y aynı Z'ye bağlı; X = Y olabilir
        tahmin, _ = self.say(govde, False, olgular)
        self.assertEqual(tahmin, 4)  # (p,p), (p,r), (r,p), (r,r)
        tahmin_oi, dogru_oi = self.say(govde, True, olgular)
        self.assertEqual((tahmin_oi, dogru_oi[2]), (2, 2))

    def test_sarkan_halka_varlik_ister(self):
        olgular = [("p", self.A, "q"), ("r", self.A, "s"), ("p", self.B, "u"), ("p", self.C, "q"), ("r", self.C, "s")]
        govde = ((0, self.X, self.Y), (1, self.X, self.Z))
        tahmin, dogru = self.say(govde, False, olgular)
        self.assertEqual((tahmin, dogru[2]), (1, 1))  # yalnız p'nin B-bağı var

    def test_bilinmeyen_kisi_ve_ilisiki_reddedilir(self):
        with self.assertRaises(ValueError):
            sayac.iliski_tensoru(("p",), [("p", self.A, "q")], ADLAR)
        with self.assertRaises(ValueError):
            sayac.iliski_tensoru(("p", "q"), [("p", "zzyok", "q")], ADLAR)

    def test_sekiller(self):
        for eksen in ("iliski", "kisi", "govde", "bas"):
            self.assertIn(eksen, SEKILLER)
        R = sayac.iliski_tensoru(("p", "q", "r"), [("p", self.A, "q")], ADLAR)
        self.assertEqual(tuple(R.shape), (3, 3, 3))
        self.assertEqual(R.dtype, torch.float32)
        with self.assertRaises(ValueError):
            sayac.sablon_say([((0, self.X, self.Y),)], R[:, :2, :], parca_boyu=7)

    def test_bos_govde_listesi(self):
        R = sayac.iliski_tensoru(("p", "q"), [], ADLAR)
        s = sayac.sablon_say([], R, parca_boyu=7)
        self.assertEqual((len(s.tahmin), tuple(s.dogru.shape)), (0, (0, len(ADLAR))))


if __name__ == "__main__":
    unittest.main()
