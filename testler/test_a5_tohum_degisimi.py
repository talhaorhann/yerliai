"""K-030, V-050: kısa yol kapısında (K-008) duran tohumun yerine kullanılmamış ilk tohum.

Eşik gevşemez (üretim aynı ayarla çağrılır); en çok `sinir` değişim; yalnız kapı durması değişim sebebidir.
Kapı koşusu tohumları üretim klasöründeki kayıttan alır; kayıt ön kayıtla ve sınırla tutarlı olmalıdır.
"""
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json
from degerlendirme import h1
from degerlendirme.kisa_yol import KisaYolHatasi
from degerlendirme.uretec import UretimDurduHatasi

ON_KAYIT = [12, 13, 14, 15, 16]
GELISTIRME = [7, 8, 9, 10, 11]


def ureteci(duranlar, baska=()):
    cagrilar = []

    def uret(tohum):
        cagrilar.append(tohum)
        if tohum in baska:
            raise UretimDurduHatasi(f"tohum {tohum}: aday sınırı")
        if tohum in duranlar:
            raise KisaYolHatasi(f"tohum {tohum}: kapı")
    return uret, cagrilar


class SecimTesti(unittest.TestCase):
    def test_durma_yoksa_on_kayit_aynen(self):
        uret, cagrilar = ureteci(set())
        kullanilan, degisimler = h1.tohumlari_uret(uret, ON_KAYIT, GELISTIRME, 3)
        self.assertEqual((kullanilan, degisimler, cagrilar), (ON_KAYIT, [], ON_KAYIT))

    def test_duran_tohum_yerine_kullanilmamis_ilk_tohum(self):
        uret, cagrilar = ureteci({15})
        kullanilan, degisimler = h1.tohumlari_uret(uret, ON_KAYIT, GELISTIRME, 3)
        self.assertEqual(kullanilan, [12, 13, 14, 17, 16])
        self.assertEqual(cagrilar, [12, 13, 14, 15, 17, 16])
        self.assertEqual(degisimler, [{"tohum": 15, "yerine": 17, "neden": "tohum 15: kapı"}])

    def test_yerine_gecen_de_durursa_siradaki(self):
        uret, _ = ureteci({13, 17, 18})
        kullanilan, degisimler = h1.tohumlari_uret(uret, ON_KAYIT, GELISTIRME, 3)
        self.assertEqual(kullanilan, [12, 19, 14, 15, 16])
        self.assertEqual([(d["tohum"], d["yerine"]) for d in degisimler], [(13, 17), (17, 18), (18, 19)])

    def test_kullanilmis_tohum_atlanir(self):
        uret, _ = ureteci({12})
        kullanilan, _ = h1.tohumlari_uret(uret, [12, 13], [7, 14, 15], 3)
        self.assertEqual(kullanilan, [16, 13])

    def test_sinir_asilirsa_durur(self):
        uret, _ = ureteci({12, 17, 18, 19})
        with self.assertRaises(h1.H1Hatasi):
            h1.tohumlari_uret(uret, ON_KAYIT, GELISTIRME, 3)

    def test_kapi_disindaki_durma_degisim_sebebi_degildir(self):
        uret, cagrilar = ureteci(set(), baska={14})
        with self.assertRaises(UretimDurduHatasi):
            h1.tohumlari_uret(uret, ON_KAYIT, GELISTIRME, 3)
        self.assertEqual(cagrilar, [12, 13, 14])


class KayitTesti(unittest.TestCase):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.klasor = Path(self._d.name)

    def tearDown(self):
        self._d.cleanup()

    def yaz(self, kayit):
        atomik_yaz(self.klasor / h1.TOHUM_KAYDI, kanonik_json(kayit))

    def test_gecerli_kayit(self):
        self.yaz({"on_kayit": ON_KAYIT, "kullanilan": [12, 13, 14, 17, 16],
                  "degisimler": [{"tohum": 15, "yerine": 17, "neden": "kapı"}]})
        self.assertEqual(h1.kapi_tohumlari(self.klasor, ON_KAYIT, 3), [12, 13, 14, 17, 16])

    def test_kayit_yoksa_durur(self):
        with self.assertRaises(h1.H1Hatasi):
            h1.kapi_tohumlari(self.klasor, ON_KAYIT, 3)

    def test_on_kayit_uyusmazsa_durur(self):
        """Kullanılan tohumlar ön kayıtla tutarlı görünse bile kaydın kendi ön kayıt listesi aynı olmalı."""
        self.yaz({"on_kayit": [12, 13, 14, 15, 17], "kullanilan": ON_KAYIT, "degisimler": []})
        with self.assertRaises(h1.H1Hatasi):
            h1.kapi_tohumlari(self.klasor, ON_KAYIT, 3)

    def test_degisimle_tutarsiz_kayit_durur(self):
        self.yaz({"on_kayit": ON_KAYIT, "kullanilan": [12, 13, 14, 18, 16],
                  "degisimler": [{"tohum": 15, "yerine": 17, "neden": "kapı"}]})
        with self.assertRaises(h1.H1Hatasi):
            h1.kapi_tohumlari(self.klasor, ON_KAYIT, 3)

    def test_degisimsiz_farkli_tohum_durur(self):
        self.yaz({"on_kayit": ON_KAYIT, "kullanilan": [12, 13, 14, 17, 16], "degisimler": []})
        with self.assertRaises(h1.H1Hatasi):
            h1.kapi_tohumlari(self.klasor, ON_KAYIT, 3)

    def test_sinirdan_fazla_degisim_durur(self):
        degisimler = [{"tohum": a, "yerine": b, "neden": "kapı"} for a, b in ((12, 17), (13, 18), (14, 19), (15, 20))]
        self.yaz({"on_kayit": ON_KAYIT, "kullanilan": [17, 18, 19, 20, 16], "degisimler": degisimler})
        with self.assertRaises(h1.H1Hatasi):
            h1.kapi_tohumlari(self.klasor, ON_KAYIT, 3)

    def test_kayit_ozeti_on_kayit_ekinde_aranir(self):
        self.yaz({"on_kayit": [12], "kullanilan": [12], "degisimler": []})
        (self.klasor / "tohum_12").mkdir()
        (self.klasor / "tohum_12" / "ozet.json").write_bytes(b"{}")
        dna = self.klasor / "dna.json"
        dna.write_bytes(b"{}")
        kok = Path(__file__).resolve().parents[1]
        ozetler = h1.gerekli_ozetler(kok, self.klasor, dna, [12], "sha256")
        self.assertIn(h1.TOHUM_KAYDI, ozetler)


if __name__ == "__main__":
    unittest.main()
