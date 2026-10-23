"""sistem.md §10, K-010, V-022: önsel-ters bölmesi (eski iskelet testinin yerine; dosya adı izlenebilirlik için korundu).

Önsel-ters bölmesinde cevap dağılımı eğitimdekinin tersi olmalı: eğitimde sık cevaplar nadir, nadir olanlar sık.
"""
import dataclasses
import random
import unittest
from collections import Counter

from degerlendirme import uretec
from degerlendirme.uretec import aday_uret, bolme_uret
from testler.test_a1_uretec import PRM, SEMA, SEMA_YOLU, TANIM


def sira(degerler):
    """Ortalama sıralar (eşitlikte ortalama), Spearman için."""
    sirali = sorted(range(len(degerler)), key=lambda i: degerler[i])
    sonuc = [0.0] * len(degerler)
    i = 0
    while i < len(sirali):
        j = i
        while j + 1 < len(sirali) and degerler[sirali[j + 1]] == degerler[sirali[i]]:
            j += 1
        for t in range(i, j + 1):
            sonuc[sirali[t]] = (i + j) / 2
        i = j + 1
    return sonuc


def spearman(a, b):
    ra, rb = sira(a), sira(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    pay = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    payda = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return pay / payda


class OnselTersTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prm = dataclasses.replace(PRM, ana_kume_sayisi=200)
        cls.sonuc = bolme_uret("onsel_ters", cls.prm, TANIM, SEMA, SEMA_YOLU)

    def test_bolme_listede_ve_aday_egitim_gibi(self):
        self.assertIn("onsel_ters", uretec.BOLMELER)
        a = aday_uret(random.Random(7), TANIM, PRM, "onsel_ters")
        self.assertEqual(a.cevap["bolme"], "onsel_ters")
        self.assertTrue(PRM.egitim_k[0] <= a.cevap["k"] <= PRM.egitim_k[1])

    def test_dagilim_ters(self):
        dogal = Counter(a.cevap["cevap"] for a in self.sonuc["dedektor"])
        cikti = Counter(a.cevap["cevap"] for a in self.sonuc["ana"] + self.sonuc["treg"])
        adlar = sorted(dogal)
        p = [dogal[r] / sum(dogal.values()) for r in adlar]
        q = [cikti[r] / sum(cikti.values()) for r in adlar]
        self.assertLess(spearman(p, q), 0)
        en_sik = max(adlar, key=lambda r: (dogal[r], r))
        self.assertLess(q[adlar.index(en_sik)], p[adlar.index(en_sik)])

    def test_kapi_gecer_ve_ana_kume_dolu(self):
        dogruluk, sans = self.sonuc["kapi"]
        self.assertLessEqual(dogruluk, sans + PRM.sans_payi)
        self.assertEqual(len(self.sonuc["ana"]), self.prm.ana_kume_sayisi)


if __name__ == "__main__":
    unittest.main()
