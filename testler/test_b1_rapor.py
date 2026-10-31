"""K-041, K-043 (ÖK-005 taslağı §8 rapor kalıbı, §12 yasak iddialar), V-065: H2 rapor metinleri. Koşu dosyaları elle
kurulur; metinde zorunlu cümleler bulunur, yasak iddialar bulunmaz, gizli aileler yalnız sırasıyla anılır."""
import json
import tempfile
import unittest
from pathlib import Path

from degerlendirme import h2_rapor as R

K = {"tau": 0.85, "mudahale": 0.9, "T": 0.04, "sigma": 0.01}
B1 = {
    "sonuc.json": {"basari_araliginda": True, "kesif": True, "sartlar": {"k_secildi": True, "kacak_0": True, "alt_sinir": True,
                                                         "bos_tetik_yok": True}, "K": K, "C": 900},
    "k.json": {"secilen": K, "baslangic": K, "sahte_sayisi": 4500},
    "p_yildiz.json": {"P*": 4801, "sansurlu": True, "tur_basina_aday": 200},
    "talep.json": {"C": 900, "sayim_tamam": True, "sayim_ustu": 4801},
    "bos_kosular.json": {"kosu_sayisi": 100, "tetik": 2, "yapilan": 100, "kabullu_kosu": 0, "tetiklendi": False,
                         "kosular": [{"k": 1, "kabul": 0, "okunur_kabul": 7, "sema_turevi_kabul": 190}]},
    "tani_cinsiyet.json": {"kabul_toplam": 5, "sayilan": 3, "sema_turevi": 1, "okunur": 1, "yalniz_tani": True},
    "kirmizi.json": {"gorunur": {"G1": {"mutant": 40, "sahte": 40, "kacak": 0}},
                     "gizli": {"1": {"kural": 45, "etkin": 44, "kacak": 0}, "2": {"kural": 45, "etkin": 45, "kacak": 0}},
                     "etkin_olmayan_gizli": {"sayi": 1, "hukum": {"RET/gelistirme_yanlis": 1}},
                     "sahte_toplam": 344, "kacak": 0,
                     "alt_sinir": 0.9913, "alt_sinir_gecti": True},
}
B2 = {"karar": {"karar": "GECTI", "sartlar": {"geri_bulma": True}, "bulunan": 225, "geri_bulma": 0.922, "bicimce": 0.5,
                "kumeli_wilson": 0.87, "kume_sayisi": 21, "kabul": 230, "bozuk": 0, "cp_ust": 0.013,
                "bilmiyorum_farki": 0.02, "siniflar": {"ozdes": 100}},
      "ikincil_paydalar": {"okunur_haric": [220, 235], "ornekli": [225, 240]},
      "a3_aktarim": {"kabul_kumesi": {"A1": {"geri_bulma": 0.9}, "A3": {"geri_bulma": 0.8}}}, "kesif": True,
      "sema_turevi": {"kabul_sema_turevi": 40, "kabul": 230, "bulunan_sema_turevi": 30, "bulunan": 225,
                      "bulunan_sinif": {"ozdes": [100, 20], "daha_genel": [25, 5], "kapanis_esdeger": [100, 5]}},
      "karar_sema_turevi_haric": {"karar": "ARA_BOLGE", "bulunan": 195, "geri_bulma": 0.799},
      "arama": {"nedenler": {"BİLMİYORUM/uyum": 17, "KABUL": 230}}}


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
        self.assertIn("gizli (4 aile toplamı) | 90 | 89 | 0", b1)  # aile kırılımı yok
        self.assertNotIn("gizli 1", b1)
        self.assertIn("sahte sayılmayan gizli kural: 1", b1)
        self.assertIn("koşu 1: sayılan 0, şema-türevi 190, şemadan okunur 7", b1)
        self.assertIn("Tanı (c)", b1)
        self.assertIn(R.KESIF, b1)
        self.assertIn("225/244", k2)
        self.assertIn(R.HAT.capitalize(), k2)
        self.assertIn("A3 0.8000", k2)
        self.assertIn("195/244", k2)
        self.assertIn("en çok 8 sonuç", k2)
        self.assertIn("uyum nedeniyle BİLMİYORUM olan aday: 17", k2)
        self.assertIn(R.KESIF, k2)

    def test_yasak_yakalanir(self):
        self.assertEqual(R.yasak_var_mi("Sistem kuralı Kendi Buldu."), ["kendi buldu"])


if __name__ == "__main__":
    unittest.main()
