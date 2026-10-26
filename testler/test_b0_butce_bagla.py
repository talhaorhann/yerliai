"""K-041 (ÖK-005 taslağı §2.2, §4 madde 2, 3, 13, 20; §13.6), V-063: sorgu bütçesi defteri, derece-koruyan yeniden
bağlama (veto ikizi, boş dünya), şemadan okunabilir kural sınıfı, boş-dünya sayacı ve çekirdek özeti.
Testlerde ilişki adı yazılmaz; şema ve dünyalar veri dosyalarından gelir."""
import random
import shutil
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from araclar import cekirdek_ozeti
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.olay_gunlugu import ZincirHatasi
from degerlendirme import h1, h2_bagla, h2_butce, h2_dunya
from degerlendirme.dunya import tanimlar_yukle
from testler.yardimci import KOK

H2 = ayar_yukle(KOK / "config_h2.json")
_, SEMA, _ = h1._ortam(KOK)
TANIMLAR = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                          KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", SEMA)
DUNYA = h2_dunya.aile_dunyasi("A1", H2.deger("dunya_aileleri")["A1"], 77, TANIMLAR)


def defter(yol=None):
    return h2_butce.SorguDefteri(yol, H2, tur_basina_aday=3)


class SorguDefteriTesti(unittest.TestCase):
    def test_tur_ve_aday_siniri(self):
        d = defter()
        with self.assertRaises(h2_butce.ButceHatasi):
            d.sorgu("a1", "w1")  # tur açılmadan sorgu yok
        d.tur_ac()
        for a in ("a1", "a2", "a3"):
            d.sorgu(a, "w1")
            d.sorgu(a, "w2")
        with self.assertRaises(h2_butce.ButceHatasi):
            d.sorgu("a4", "w1")  # turda en çok 3 aday
        with self.assertRaises(h2_butce.ButceHatasi):
            d.sorgu("a1", "w1")  # aynı çift iki kez
        for _ in range(H2.deger("sorgu_tur_siniri") - 1):
            d.tur_ac()
        with self.assertRaises(h2_butce.ButceHatasi):
            d.tur_ac()
        self.assertEqual(d.tur, H2.deger("sorgu_tur_siniri"))

    def test_taze_dunya_yanar_ve_grup_sorgusu_yok(self):
        d = defter()
        d.tur_ac()
        d.sorgu("a1", "w1")
        d.tur_ac()
        with self.assertRaises(h2_butce.ButceHatasi):
            d.sorgu("a2", "w1")  # önceki turda kullanılan dünya yandı
        with self.assertRaises(h2_butce.ButceHatasi):
            d.sorgu(["a2", "a3"], "w2")  # grup sorgusu yasak

    def test_kaldigi_yerden_devam_ve_kurcalama(self):
        with tempfile.TemporaryDirectory() as k:
            yol = Path(k) / "defter.jsonl"
            d = defter(yol)
            d.tur_ac()
            d.sorgu("a1", "w1")
            d.sorgu("a2", "w1")
            yeni = defter(yol)
            self.assertEqual((yeni.tur, yeni.turdaki_adaylar()), (1, {"a1", "a2"}))
            yeni.sorgu("a3", "w9")  # üçüncü aday sığar
            with self.assertRaises(h2_butce.ButceHatasi):
                yeni.sorgu("a4", "w9")  # dördüncüsü sığmaz (sayaç dosyadan geri yüklendi)
            yol.write_bytes(yol.read_bytes().replace(b'"a1"', b'"a9"'))
            with self.assertRaises(ZincirHatasi):
                defter(yol)

    def test_tur_anahtari(self):
        gen, dar = H2.deger("sorgu_tur_basina_aday_genis"), H2.deger("sorgu_tur_basina_aday")
        tur = H2.deger("sorgu_tur_siniri")
        self.assertEqual(h2_butce.tur_basina_aday(dar * tur, None, H2), dar)
        self.assertEqual(h2_butce.tur_basina_aday(dar * tur + 1, None, H2), gen)
        self.assertEqual(h2_butce.tur_basina_aday(10, 3000, H2), min(dar, 3000 // 24))
        self.assertEqual(h2_butce.tur_basina_aday(10 ** 6, 10 ** 7, H2), gen)


def dereceler(olgular):
    return Counter((a, r) for a, r, _ in olgular), Counter((b, r) for _, r, b in olgular)


class YenidenBaglamaTesti(unittest.TestCase):
    def test_veto_ikizi_yalniz_bas_iliskisi(self):
        r = SEMA.adlar[0]
        yeni = h2_bagla.yeniden_bagla(DUNYA.olgular, {r}, SEMA, random.Random(1), tersleri_yaz=False,
                                       deneme_carpani=H2.deger("bagla_deneme_carpani"))
        self.assertEqual({o for o in yeni if o[1] != r}, {o for o in DUNYA.olgular if o[1] != r})
        self.assertNotEqual({o for o in yeni if o[1] == r}, {o for o in DUNYA.olgular if o[1] == r})
        self.assertEqual(dereceler(yeni), dereceler(DUNYA.olgular))

    def test_bos_dunya_dereceyi_ve_sema_tutarliligini_korur_yapiyi_bozar(self):
        yeni = h2_bagla.bos_dunya(DUNYA.olgular, SEMA, random.Random(2), H2.deger("bagla_deneme_carpani"))
        self.assertEqual(dereceler(yeni), dereceler(DUNYA.olgular))
        var = set(yeni)
        for a, r, b in yeni:
            self.assertNotEqual(a, b)
            self.assertTrue(any((b, t, a) in var for t in SEMA.ters(r)), "ters tutarlılığı bozuldu")
        cift = Counter((a, b) for a, _, b in yeni)
        self.assertEqual(max(cift.values()), 1, "bir çifte iki ilişki")
        degisen = len(set(DUNYA.olgular) - var)
        self.assertGreater(degisen, len(DUNYA.olgular) // 4)

    def test_belirlenimci(self):
        a = h2_bagla.bos_dunya(DUNYA.olgular, SEMA, random.Random(3), H2.deger("bagla_deneme_carpani"))
        b = h2_bagla.bos_dunya(DUNYA.olgular, SEMA, random.Random(3), H2.deger("bagla_deneme_carpani"))
        self.assertEqual(a, b)

    def test_ileri_taraflar_her_sinifi_kapsar(self):
        taraf = h2_bagla.ileri_taraflar(SEMA)
        kapsanan = set(taraf)
        for r in taraf:
            kapsanan |= set(SEMA.ters(r))
        self.assertEqual(kapsanan, set(SEMA.adlar))


def aday(govde, bas):
    return {"halkalar": [{"gen": g, "sol": s, "sag": a} for g, s, a in govde], "sonuc": dict(zip(("gen", "sol", "sag"), bas))}


class SemadanOkunabilirTesti(unittest.TestCase):
    def test_tek_halka_ters_ya_da_simetrik(self):
        r = next(a for a in SEMA.adlar if not SEMA.simetrik(a))
        t = sorted(SEMA.ters(r))[0]
        s = next(a for a in SEMA.adlar if SEMA.simetrik(a))
        self.assertTrue(h2_bagla.semadan_okunabilir_mi(aday([(r, "X", "Y")], (t, "Y", "X")), SEMA))
        self.assertTrue(h2_bagla.semadan_okunabilir_mi(aday([(s, "X", "Y")], (s, "Y", "X")), SEMA))
        self.assertFalse(h2_bagla.semadan_okunabilir_mi(aday([(r, "X", "Y")], (t, "X", "Y")), SEMA))
        self.assertFalse(h2_bagla.semadan_okunabilir_mi(aday([(r, "X", "Z"), (r, "Z", "Y")], (t, "Y", "X")), SEMA))


class BosDunyaSayaciTesti(unittest.TestCase):
    def test_tetik(self):
        s = h2_bagla.BosDunyaSayaci(H2, SEMA)
        r = next(a for a in SEMA.adlar if SEMA.simetrik(a))
        okunabilir = aday([(r, "X", "Y")], (r, "Y", "X"))
        yapisal = aday([(r, "X", "Z"), (r, "Z", "Y")], (r, "X", "Y"))
        self.assertFalse(s.kaydet([okunabilir]))  # şemadan okunabilir sınıf sayılmaz
        self.assertFalse(s.kaydet([yapisal]))  # 1 koşu
        self.assertTrue(s.kaydet([yapisal, okunabilir]))  # 2 koşu → tetik (≥2)
        self.assertEqual((s.kosu, s.kabullu_kosu), (3, 2))


class CekirdekOzetiTesti(unittest.TestCase):
    def test_belirlenimci_ve_degisiklige_duyarli(self):
        self.assertEqual(cekirdek_ozeti.ozet_al(KOK / "cekirdek"), cekirdek_ozeti.ozet_al(KOK / "cekirdek"))
        with tempfile.TemporaryDirectory() as k:
            kopya = Path(k) / "cekirdek"
            shutil.copytree(KOK / "cekirdek", kopya, ignore=shutil.ignore_patterns("__pycache__"))
            ilk = cekirdek_ozeti.ozet_al(kopya)
            (kopya / "__pycache__").mkdir(exist_ok=True)
            (kopya / "__pycache__" / "x.pyc").write_bytes(b"0")
            self.assertEqual(cekirdek_ozeti.ozet_al(kopya), ilk)
            yol = kopya / "dongu.py"
            yol.write_text(yol.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            self.assertNotEqual(cekirdek_ozeti.ozet_al(kopya), ilk)


if __name__ == "__main__":
    unittest.main()
