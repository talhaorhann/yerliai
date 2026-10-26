"""K-043, ÖK-005 taslağı §7, §8, §13.2: genel kural değerlendiricisi (`degerlendirme/kural.py`). Her değişken adı, `farkli`
şartı ve OI ile çalışır; şablon adaylarında sembolik sayaçla birebir aynı sayıları verir. Çift kısıtlı kapanış
(maskelenen çiftin olguları yeniden türetilir) ve θ-kapsama da burada sınanır. İlişki adları anlamsızdır."""
import itertools
import random
import unittest

from degerlendirme import kural
from kesif import sablon, sayac

ADLAR = ("zra", "zrb", "zrc")
DEG = ("X", "Y", "Z", "W")


def kayit(halkalar, bas, oi=False, farkli=()):
    return {"halkalar": [{"gen": g, "sol": s, "sag": a} for g, s, a in halkalar],
            "sonuc": {"gen": bas[0], "sol": bas[1], "sag": bas[2]}, "oi": oi, "farkli": [list(c) for c in farkli]}


def dunya(n, yogunluk, tohum):
    rng = random.Random(tohum)
    kisiler = tuple(range(n))
    return sorted({(a, r, b) for a in kisiler for b in kisiler for r in ADLAR if a != b and rng.random() < yogunluk})


class SayacEsitlikTesti(unittest.TestCase):
    def test_sablon_adaylarinda_sayacla_ayni(self):
        govdeler = sablon.govdeler(len(ADLAR), DEG, 3, False)
        for n, yog, tohum in ((9, 0.15, 1), (12, 0.1, 2)):
            olg = dunya(n, yog, tohum)
            R = sayac.iliski_tensoru(tuple(range(n)), olg, ADLAR)
            hizli = sayac.sablon_say(govdeler, R, parca_boyu=64)
            indeks = kural.Indeks(olg)
            for i in range(0, len(govdeler), 7):
                g = govdeler[i]
                for oi in ((False, True) if sablon.oi_anlamli_mi(g) else (False,)):
                    for bas in range(len(ADLAR)):
                        k = kural.Kural.kayittan(sablon.aday_kaydi(g, bas, oi, ADLAR, DEG))
                        t, d = (hizli.tahmin_oi, hizli.dogru_oi) if oi else (hizli.tahmin, hizli.dogru)
                        tah = k.tahminler(indeks)
                        self.assertEqual(len(tah), int(t[i]))
                        self.assertEqual(sum((a, ADLAR[bas], b) in indeks.olgu for a, b in tah), int(d[i][bas]))


class AnlamTesti(unittest.TestCase):
    A, B, C = ADLAR

    def test_farkli_ve_degisken_adlari(self):
        olg = [("p", self.A, "q"), ("r", self.A, "q"), ("p", self.C, "r")]
        k = kural.Kural.kayittan(kayit([(self.A, "K", "M"), (self.A, "L", "M")], (self.C, "K", "L")))
        self.assertEqual(k.tahminler(kural.Indeks(olg)), {("p", "p"), ("p", "r"), ("r", "p"), ("r", "r")})
        k2 = kural.Kural.kayittan(kayit([(self.A, "K", "M"), (self.A, "L", "M")], (self.C, "K", "L"), farkli=[("K", "L")]))
        self.assertEqual(k2.tahminler(kural.Indeks(olg)), {("p", "r"), ("r", "p")})

    def test_bas_degiskenleri_ters_sirada(self):
        olg = [("p", self.A, "q")]
        k = kural.Kural.kayittan(kayit([(self.A, "X", "Y")], (self.B, "Y", "X")))
        self.assertEqual(k.tahminler(kural.Indeks(olg)), {("q", "p")})

    def test_bagli_ciftin_baglamasi(self):
        olg = [("p", self.A, "q"), ("q", self.A, "r"), ("p", self.A, "s"), ("s", self.A, "r")]
        k = kural.Kural.kayittan(kayit([(self.A, "X", "Z"), (self.A, "Z", "Y")], (self.B, "X", "Y")))
        idx = kural.Indeks(olg)
        self.assertTrue(k.turetir_mi(idx, "p", "r"))
        self.assertFalse(k.turetir_mi(idx, "p", "q"))
        self.assertTrue(k.turetir_mi(idx, "p", "r", haric={("p", self.A, "q"), ("q", self.A, "r")}))  # s yolu kalır
        self.assertFalse(k.turetir_mi(idx, "p", "r", haric={("p", self.A, "q"), ("s", self.A, "r")}))


class KapanisTesti(unittest.TestCase):
    A, B, C = ADLAR

    def test_cift_kisitli_kapanis_iki_adim(self):
        """Maskelenen çiftin olgusu önce tersinden, sonra ondan türer (iki adım)."""
        olg = {("p", self.A, "q"), ("q", self.A, "r")}
        bilesim = kural.Kural.kayittan(kayit([(self.A, "X", "Z"), (self.A, "Z", "Y")], (self.C, "Y", "X")))
        ters = kural.Kural.kayittan(kayit([(self.C, "Y", "X")], (self.B, "X", "Y")))
        idx = kural.Indeks(olg)
        self.assertEqual(kural.cift_kapanisi([bilesim, ters], idx, "p", "r", tur_siniri=8),
                         {("r", self.C, "p"), ("p", self.B, "r")})
        self.assertEqual(kural.cift_kapanisi([ters], idx, "p", "r", tur_siniri=8), set())
        self.assertEqual(kural.cift_kapanisi([bilesim, ters], idx, "p", "r", tur_siniri=1), {("r", self.C, "p")})

    def test_kurala_gore_maske(self):
        """Her kural kendi maskesini görmez: ters olguyu yalnız ona izin verilen kural okuyabilir."""
        olg = {("p", self.A, "q"), ("q", self.C, "p")}
        okuyan = kural.Kural.kayittan(kayit([(self.C, "Y", "X")], (self.B, "X", "Y")))
        idx = kural.Indeks(olg)
        f = ("p", self.B, "q")
        tersli = frozenset({f, ("q", self.C, "p")})
        self.assertEqual(kural.cift_kapanisi([okuyan], idx, "p", "q", 8, haric=tersli), set())
        self.assertEqual(kural.cift_kapanisi([okuyan], idx, "p", "q", 8, maske=lambda k: frozenset({f})), {f})


class KapsamaTesti(unittest.TestCase):
    A, B, C = ADLAR

    def test_theta_kapsama(self):
        genel = kural.Kural.kayittan(kayit([(self.A, "X", "Z")], (self.B, "X", "Z")))
        ozel = kural.Kural.kayittan(kayit([(self.A, "K", "L"), (self.C, "L", "M")], (self.B, "K", "L")))
        self.assertTrue(kural.kapsar_mi(genel, ozel))
        self.assertFalse(kural.kapsar_mi(ozel, genel))
        farkli = kural.Kural.kayittan(kayit([(self.A, "X", "Z")], (self.C, "X", "Z")))
        self.assertFalse(kural.kapsar_mi(farkli, ozel))
        oili = kural.Kural.kayittan(kayit([(self.A, "X", "Y"), (self.C, "Y", "Z")], (self.B, "X", "Y"), oi=True))
        self.assertFalse(kural.kapsar_mi(oili, ozel))  # genel kuralın farklılık şartı özelde yok
        self.assertTrue(kural.kapsar_mi(ozel, ozel))

    def test_ters_dayanakli(self):
        self.assertTrue(kural.Kural.kayittan(kayit([(self.A, "Y", "X"), (self.C, "X", "Z")], (self.B, "X", "Y"))).ters_dayanakli)
        self.assertFalse(kural.Kural.kayittan(kayit([(self.A, "X", "Z"), (self.C, "Z", "Y")], (self.B, "X", "Y"))).ters_dayanakli)


if __name__ == "__main__":
    unittest.main()
