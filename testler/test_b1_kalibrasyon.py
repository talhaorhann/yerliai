"""K-041, K-043 (ÖK-005 taslağı §4 madde 3, 9, 10, 12, 20; K kalibrasyon kuralı), V-065: K ızgarası, seçim kuralı,
C sayımı, P* ve boş koşu sayısı. Ölçümler elle kurulur (geçidin kendisi `test_b1_gecit`'te)."""
import unittest

from degerlendirme import h2_gecit as G
from degerlendirme import h2_kalibrasyon as KAL
from testler.test_b1_gecit import H2, SABIT, olcum


def wilsonlu(w, mud=1.0):
    return olcum(taze__wilson=w, gel_wilson__wilson=w, cekirdek__bolumler=[{"mudahale": [mud] * 3}],
                 cekirdek__pi__mudahale_orijinal=[mud], cekirdek__pi__mudahale_ikiz=[mud])


class IzgaraTesti(unittest.TestCase):
    def test_81_nokta(self):
        iz = KAL.izgara(H2)
        self.assertEqual(len(iz), 81)
        self.assertIn(dict(H2.deger("esik_baslangic")), iz)

    def test_secim_en_cok_kabul_sahte_sifir(self):
        ilk = {"a": wilsonlu(0.82), "b": wilsonlu(0.87), "c": wilsonlu(0.95)}
        sonuc = KAL.kalibre_et({}, ilk, SABIT, H2)
        self.assertEqual(sonuc["secilen"]["tau"], 0.80)  # τ = 0,80 üçünü de kabul eder
        self.assertEqual(sonuc["secilen"]["mudahale"], 0.9)  # müdahale eşittir: başlangıç kalır
        self.assertEqual((sonuc["secilen"]["T"], sonuc["secilen"]["sigma"]), (0.04, 0.01))

    def test_sahte_kabul_noktayi_eler(self):
        ilk = {"a": wilsonlu(0.82), "b": wilsonlu(0.87)}
        sahte = {"s": wilsonlu(0.83)}  # τ = 0,80'de sahte kabul
        sonuc = KAL.kalibre_et(sahte, ilk, SABIT, H2)
        self.assertEqual(sonuc["secilen"]["tau"], 0.85)
        self.assertTrue(all(n["sahte_kabul"] == ["s"] for n in sonuc["noktalar"] if n["esik"]["tau"] == 0.80))

    def test_esitlikte_baslangic(self):
        ilk = {"a": wilsonlu(0.95)}
        self.assertEqual(KAL.kalibre_et({}, ilk, SABIT, H2)["secilen"], dict(H2.deger("esik_baslangic")))

    def test_mudahale_eseigi(self):
        ilk = {"a": wilsonlu(0.95, mud=0.85)}  # yalnız müdahale 0,8'de kabul
        self.assertEqual(KAL.kalibre_et({}, ilk, SABIT, H2)["secilen"]["mudahale"], 0.8)

    def test_hepsi_sahte_kabulse_secim_yok(self):
        self.assertIsNone(KAL.kalibre_et({"s": wilsonlu(0.99)}, {}, SABIT, H2)["secilen"])


class TalepTesti(unittest.TestCase):
    def test_c_sayimi_kapsananlari_saymaz_ve_durur(self):
        gecen = {"gelistirme": {"tanik": 5, "yanlis": 0, "yolkesme_tanik": 3}, "obiter": [], "bag_ikizi": {"tanik": 0, "yanlis": 9}}
        yanlis = {"gelistirme": {"tanik": 5, "yanlis": 1, "yolkesme_tanik": 3}, "obiter": []}
        akis = [("a", gecen, "A"), ("b", yanlis, "B"), ("c", gecen, "A2"), ("d", gecen, "D")]
        kapsar = lambda k, onceki: k == "A2" and "A" in onceki  # noqa: E731
        self.assertEqual(KAL.talep(akis, kapsar, SABIT, 10), (2, True))
        self.assertEqual(KAL.talep(akis, kapsar, SABIT, 1), (1, False))


class PYildizTesti(unittest.TestCase):
    def test_ilk_sahte_kabul_ve_sansur(self):
        akis = [("a", G.RET), ("b", G.KABUL), ("c", G.KABUL)]
        self.assertEqual(KAL.p_yildiz(akis, lambda k: k == "c", 4800), (3, False))
        self.assertEqual(KAL.p_yildiz(akis, lambda k: False, 4800), (4801, True))


class BosKosuTesti(unittest.TestCase):
    def test_maliyet_kurali(self):
        self.assertEqual(KAL.bos_kosu_sayisi(4000, H2), (100, 2))
        self.assertEqual(KAL.bos_kosu_sayisi(4400, H2), (50, 1))  # 100 × 4400 s > 120 saat


if __name__ == "__main__":
    unittest.main()
