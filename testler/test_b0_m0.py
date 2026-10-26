"""K-041, ÖK-005 taslağı §4 madde 5 ve 22, §6: M0 (bütün şablon uzayını sayan referans yöntem). Süzgeç: geliştirme
dünyalarında yanlış 0 ve tanık ≥ 3; sıra: tanık azalan, halka artan, kanonik kimlik artan; çıktı bit-aynı.
Sentetik dünyalar, anlamsız ilişki adları: ilk ilişki bir yol, ikincisi ilkinin iki adımlık bileşimi, üçüncüsü gürültü."""
import json
import random
import unittest

from cekirdek.altyapi.ayar import ayar_yukle
from kesif import aday as ad
from kesif import m0
from testler.yardimci import KOK

H2 = ayar_yukle(KOK / "config_h2.json")
ADLAR = ("zra", "zrb", "zrc")
DEG = tuple(H2.deger("sablon_degiskenleri"))


def yol_dunyasi(aile, uzunluk, tohum, gurultu=4):
    rng = random.Random(tohum)
    kisiler = tuple(range(uzunluk))
    olgular = {(i, ADLAR[0], i + 1) for i in range(uzunluk - 1)} | {(i, ADLAR[1], i + 2) for i in range(uzunluk - 2)}
    while len(olgular) < 2 * uzunluk - 3 + gurultu:
        a, b = rng.sample(kisiler, 2)
        if not any((a, r, b) in olgular for r in ADLAR[:2]):
            olgular.add((a, ADLAR[2], b))
    return m0.Dunya(aile, kisiler, tuple(sorted(olgular)))


def kimlik(halkalar, bas):
    k = {"sema_surumu": "1", "kimlik": "x", "halkalar": [{"gen": ADLAR[r], "sol": s, "sag": a} for r, s, a in halkalar],
         "sonuc": {"gen": ADLAR[bas], "sol": "X", "sag": "Y"}, "farkli": [], "oi": False,
         "kaynak": {"tur": "m0", "aile": None, "tohum": None, "ust": []}, "tanik_ozeti": None, "surum": 1}
    return ad.kanonik_kimlik(k, "sha256")


DUNYALAR = [yol_dunyasi("F1", 7, 1), yol_dunyasi("F2", 11, 2), yol_dunyasi("F1", 13, 3)]
DOGRU_KURAL = kimlik([(0, "X", "Z"), (0, "Z", "Y")], 1)
YANLIS_KURAL = kimlik([(0, "X", "Y")], 1)


class M0Testi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sonuc = m0.m0(DUNYALAR, ADLAR, H2, kademe="K3")

    def test_dogru_kural_bulunur_yanlis_kural_elenir(self):
        kimlikler = {a["kanonik_kimlik"] for a in self.sonuc.adaylar}
        self.assertIn(DOGRU_KURAL, kimlikler)
        self.assertNotIn(YANLIS_KURAL, kimlikler)
        dogru = next(a for a in self.sonuc.adaylar if a["kanonik_kimlik"] == DOGRU_KURAL)
        self.assertEqual(dogru["dogru"], {"F1": 5 + 11, "F2": 9})
        self.assertEqual(dogru["tahmin"], dogru["dogru"])

    def test_suzgec_esikleri(self):
        for a in self.sonuc.adaylar:
            self.assertEqual(sum(a["tahmin"].values()) - sum(a["dogru"].values()), 0)
            self.assertGreaterEqual(sum(a["dogru"].values()), H2.deger("m0_en_az_tanik"))
        az = m0.m0([yol_dunyasi("F1", 4, 5, gurultu=0)], ADLAR, H2, kademe="K3")  # bileşim yalnız 2 kez
        self.assertNotIn(DOGRU_KURAL, {a["kanonik_kimlik"] for a in az.adaylar})
        tam = m0.m0([yol_dunyasi("F1", 5, 5, gurultu=0)], ADLAR, H2, kademe="K3")  # 3 kez
        self.assertIn(DOGRU_KURAL, {a["kanonik_kimlik"] for a in tam.adaylar})

    def test_siralama(self):
        anahtar = [(-sum(a["dogru"].values()), a["halka_sayisi"], a["kanonik_kimlik"]) for a in self.sonuc.adaylar]
        self.assertEqual(anahtar, sorted(anahtar))
        self.assertEqual(len(set(k for *_, k in anahtar)), len(anahtar))

    def test_kayitlar_semaya_uyar_ve_kimlik_tutarli(self):
        for a in self.sonuc.adaylar:
            ad.aday_denetle(a["aday"], frozenset(ADLAR))
            self.assertEqual(ad.kanonik_kimlik(a["aday"], "sha256"), a["kanonik_kimlik"])
            self.assertEqual(a["aday"]["kaynak"]["tur"], "m0")

    def test_bit_ayni_ve_girdi_sirasindan_bagimsiz(self):
        ikinci = m0.m0(DUNYALAR, ADLAR, H2, kademe="K3")
        self.assertEqual(ikinci.cikti, self.sonuc.cikti)
        karisik = [m0.Dunya(d.aile, d.kisiler[::-1], tuple(random.Random(9).sample(d.olgular, len(d.olgular))))
                   for d in reversed(DUNYALAR)]
        self.assertEqual(m0.m0(karisik, ADLAR, H2, kademe="K3").cikti, self.sonuc.cikti)
        self.assertEqual(self.sonuc.ozet["cikti_ozeti"], __import__("hashlib").sha256(self.sonuc.cikti).hexdigest())

    def test_ozet(self):
        oz = self.sonuc.ozet
        self.assertEqual(oz["kademe"], "K3")
        self.assertEqual(oz["dunya_sayisi"], 3)
        self.assertEqual(oz["aday_sayisi"], len(self.sonuc.adaylar))
        self.assertEqual(oz["aday_uzayi"], 621)  # K3, 3 ilişki: 129 gövde, OI'li aday sayısı (sablon.sayim)
        satirlar = self.sonuc.cikti.decode("utf-8").splitlines()
        self.assertEqual([json.loads(s)["kanonik_kimlik"] for s in satirlar],
                         [a["kanonik_kimlik"] for a in self.sonuc.adaylar])

    def test_bilinmeyen_kademe(self):
        with self.assertRaises(KeyError):
            m0.m0(DUNYALAR, ADLAR, H2, kademe="K9")


if __name__ == "__main__":
    unittest.main()
