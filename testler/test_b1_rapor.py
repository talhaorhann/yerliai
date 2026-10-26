"""K-041, K-043 (ÖK-005 taslağı §8 rapor kalıbı, §12 yasak iddialar), V-065: H2 rapor metinleri. Koşu dosyaları elle
kurulur; metinde zorunlu cümleler bulunur, yasak iddialar bulunmaz, gizli aileler yalnız sırasıyla anılır."""
import json
import tempfile
import unittest
from pathlib import Path

from degerlendirme import h2_rapor as R

K = {"tau": 0.85, "mudahale": 0.9, "T": 0.04, "sigma": 0.01}
B1 = {
    "sonuc.json": {"basari_araliginda": True, "sartlar": {"k_secildi": True, "kacak_0": True, "alt_sinir": True,
                                                         "bos_tetik_yok": True}, "K": K, "C": 900},
    "k.json": {"secilen": K, "baslangic": K, "sahte_sayisi": 4500},
    "p_yildiz.json": {"P*": 4801, "sansurlu": True, "tur_basina_aday": 200},
    "talep.json": {"C": 900, "sayim_tamam": True, "sayim_ustu": 4801},
    "bos_kosular.json": {"kosu_sayisi": 100, "tetik": 2, "yapilan": 100, "kabullu_kosu": 0, "tetiklendi": False},
    "kirmizi.json": {"gorunur": {"G1": {"mutant": 40, "sahte": 40, "kacak": 0}},
                     "gizli": {"1": {"kural": 45, "etkin": 44, "kacak": 0}}, "sahte_toplam": 344, "kacak": 0,
                     "alt_sinir": 0.9913, "alt_sinir_gecti": True},
}
B2 = {"karar": {"karar": "GECTI", "sartlar": {"geri_bulma": True}, "bulunan": 225, "geri_bulma": 0.922, "bicimce": 0.5,
                "kumeli_wilson": 0.87, "kume_sayisi": 21, "kabul": 230, "bozuk": 0, "cp_ust": 0.013,
                "bilmiyorum_farki": 0.02, "siniflar": {"ozdes": 100}},
      "ikincil_paydalar": {"okunur_haric": [220, 235], "ornekli": [225, 240]},
      "a3_aktarim": {"kabul_kumesi": {"A1": {"geri_bulma": 0.9}, "A3": {"geri_bulma": 0.8}}}}


class RaporTesti(unittest.TestCase):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.k = Path(self._d.name)
        for ad, v in B1.items():
            (self.k / ad).write_text(json.dumps(v), encoding="utf-8")
        (self.k / "B2b_sonuc.json").write_text(json.dumps(B2), encoding="utf-8")

    def tearDown(self):
        self._d.cleanup()

    def test_metinler(self):
        ek = R.ek3_metni(self.k)
        self.assertIn("τ = 0.85", ek)
        self.assertIn("> 4800 (sansürlü", ek)
        b1 = R.b1_raporu(self.k)
        k2 = R.kapi2_ham_raporu(self.k)
        for m in (b1, k2):
            self.assertIn(R.GIZLI_SINIR, m)
            self.assertEqual(R.yasak_var_mi(m), [])
        self.assertIn("gizli 1", b1)
        self.assertIn("225/244", k2)
        self.assertIn(R.HAT.capitalize(), k2)
        self.assertIn("A3 0.8000", k2)

    def test_yasak_yakalanir(self):
        self.assertEqual(R.yasak_var_mi("Sistem kuralı Kendi Buldu."), ["kendi buldu"])


if __name__ == "__main__":
    unittest.main()
