"""K-029, ÖK-003 §3.1, V-048: "cevap olgulardan çıkarılabilir" denetimi, çekirdekten bağımsız.

Ağaç yapısı sabit; eşler karşı cinsten. Olguların izin verdiği bütün cinsiyet atamalarında sorgu çiftinin ilişkisi
aynı olmalı. Testlerde ilişki adı yazılmaz (KODLAMA_PROMPTU §2.4): anlamsız adlı küçük bir tanım kümesi kullanılır.
Tip 1 ve 0 iki cinsiyettir.
"""
import dataclasses
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from degerlendirme import uretec
from degerlendirme.dunya import ASAGI, ES, YUKARI, Dunya, Tanimlar, cikarilabilir_mi
import testler.test_a1_uretec as t1

TANIM = Tanimlar(
    ["ust1", "ust0", "alt1", "alt0", "ess", "kar1", "kar0", "buyuk1", "buyuk0", "torunn"],
    {"ust1": (((YUKARI, 1),),), "ust0": (((YUKARI, 0),),), "alt1": (((ASAGI, 1),),), "alt0": (((ASAGI, 0),),),
     "ess": (((ES, None),),), "kar1": (((YUKARI, None), (ASAGI, 1)),), "kar0": (((YUKARI, None), (ASAGI, 0)),),
     "buyuk1": (((YUKARI, None), (YUKARI, 1)),), "buyuk0": (((YUKARI, None), (YUKARI, 0)),),
     "torunn": (((ASAGI, None), (ASAGI, None)),)},
    ["ust1", "ust0", "alt1", "alt0", "ess", "kar1", "kar0"])
# 0 (tip 1) ile 1 (tip 0) evli; çocukları 2 (tip 1) ve 3 (tip 0); 2 ile 4 (tip 0) evli; onların çocuğu 5 (tip 1).
DUNYA = Dunya([1, 0, 1, 0, 0, 1], {2: (0, 1), 3: (0, 1), 5: (2, 4)}, {0: 1, 1: 0, 2: 4, 4: 2})

# Küçük parametrelerle, denetim kapalıyken üretecin denetim eklenmeden önceki çıktısı (manifest özeti).
ONCEKI_KUCUK = {7: "d993901675091f009efaee43ddcb06583d973b811f18b0a52233fc61a1a445a9",
                12: "eb89cb82e481bcb0fe879d8ac4f2ab8289ebeeb4361321c75b7ea6922922c203"}


class TanimTesti(unittest.TestCase):
    def test_gerceklik_kontrolu(self):
        self.assertEqual(DUNYA.iliski(5, 0, TANIM), "buyuk1")
        self.assertEqual(DUNYA.iliski(0, 5, TANIM), "torunn")

    def test_cinsiyet_belirsizse_cikarilamaz(self):
        self.assertFalse(cikarilabilir_mi(DUNYA, TANIM, [(5, "ust1", 2)], (5, 0)))

    def test_olgu_cinsiyeti_sabitlerse_cikarilabilir(self):
        self.assertTrue(cikarilabilir_mi(DUNYA, TANIM, [(5, "ust1", 2), (2, "ust1", 0)], (5, 0)))

    def test_es_uzerinden_cinsiyet(self):
        """1'in tipi olguyla sabit; eşi 0 karşı cinsten olmak zorunda."""
        self.assertTrue(cikarilabilir_mi(DUNYA, TANIM, [(5, "ust1", 2), (2, "ust0", 1)], (5, 0)))

    def test_cinsiyetten_bagimsiz_iliski_cikarilabilir(self):
        self.assertTrue(cikarilabilir_mi(DUNYA, TANIM, [(5, "ust1", 2)], (0, 5)))

    def test_ilgisiz_olgu_sonucu_degistirmez(self):
        self.assertFalse(cikarilabilir_mi(DUNYA, TANIM, [(5, "ust1", 2), (2, "kar0", 3)], (5, 0)))

    def test_gercek_dunyaya_uymayan_olgu_reddedilir(self):
        with self.assertRaises(ValueError):
            cikarilabilir_mi(DUNYA, TANIM, [(5, "ust0", 2)], (5, 0))

    def test_cekirdek_calistirilmaz(self):
        with mock.patch("cekirdek.dongu.calistir", side_effect=AssertionError("çekirdek çağrıldı")), \
                mock.patch("cekirdek.plazma.cevapla", side_effect=AssertionError("plazma çağrıldı")):
            self.assertTrue(cikarilabilir_mi(DUNYA, TANIM, [(5, "ust1", 2), (2, "ust1", 0)], (5, 0)))


def kaba_kuvvet(dunya, tanimlar, olgular, sorgu):
    """Bağımsız denetim: bütün evli çift bileşenlerinin bütün çevirmeleri (budama ve ilgililik kısıtı olmadan)."""
    import itertools
    bilesenler = sorted({min(p, dunya.es[p]) if p in dunya.es else p for p in range(dunya.kisi_sayisi)})
    hedef, cevaplar = dunya.iliski(*sorgu, tanimlar), set()
    for bitler in itertools.product((0, 1), repeat=len(bilesenler)):
        cevir = {c for c, bit in zip(bilesenler, bitler) if bit}
        w = Dunya([t ^ ((min(p, dunya.es[p]) if p in dunya.es else p) in cevir) for p, t in enumerate(dunya.tip)],
                  dunya.ebeveynler, dunya.es)
        if all(w.iliskiler(x, tanimlar, tanimlar.olgu_iliskileri).get(y) == r for x, r, y in olgular):
            cevaplar.add(w.iliski(*sorgu, tanimlar))
    return cevaplar == {hedef}


class KabaKuvvetTesti(unittest.TestCase):
    def test_kucuk_rastgele_dunyalarda_kaba_kuvvetle_ayni(self):
        import random
        rng = random.Random(29)
        sayac = {True: 0, False: 0}
        for _ in range(40):
            dunya = Dunya.uret(rng, 3, 2, 2)
            baglar = dunya.olgu_baglari(t1.TANIM)
            tum = [(a, r, b) for a in baglar for b, r in baglar[a]]
            olgular = rng.sample(tum, rng.randint(1, 6))
            a, b = rng.sample(range(dunya.kisi_sayisi), 2)
            if dunya.iliski(a, b, t1.TANIM) is None:
                continue
            beklenen = kaba_kuvvet(dunya, t1.TANIM, olgular, (a, b))
            self.assertEqual(cikarilabilir_mi(dunya, t1.TANIM, olgular, (a, b)), beklenen)
            sayac[beklenen] += 1
        self.assertTrue(sayac[True] and sayac[False], sayac)


class UretecTesti(unittest.TestCase):
    def manifest_ozeti(self, prm):
        with tempfile.TemporaryDirectory() as d:
            m = uretec.hepsini_uret(Path(d), prm, t1.TANIM, t1.SEMA, t1.SEMA_YOLU,
                                    t1.KOK / "kilit" / "kilitli_kumeler.json", t1.KOK)
            return hashlib.sha256((Path(d) / "ozet.json").read_bytes()).hexdigest(), m

    def test_denetim_kapaliyken_cikti_aynen(self):
        for tohum, ozet in ONCEKI_KUCUK.items():
            with self.subTest(tohum=tohum):
                self.assertEqual(self.manifest_ozeti(dataclasses.replace(t1.KUCUK, tohum=tohum))[0], ozet)

    def test_denetim_acikken_her_bolum_cikarilabilir_ve_atilan_sayilir(self):
        prm = dataclasses.replace(t1.KUCUK, tohum=12, cikarilabilirlik=True)
        rng_bolme = "yon_ters"
        sonuc = uretec.bolme_uret(rng_bolme, prm, t1.TANIM, t1.SEMA, t1.SEMA_YOLU)
        self.assertEqual(len(sonuc["ana"]), prm.ana_kume_sayisi)
        self.assertGreater(sonuc["cikarilamaz_atilan"], 0)
        for a in sonuc["ana"] + sonuc["treg"]:
            ters = {v: k for k, v in a.kimlik_esleme.items()}
            olgular = [(ters[o["ozne"]], o["iliski"], ters[o["nesne"]]) for o in a.bolum["olgular"]]
            self.assertTrue(cikarilabilir_mi(a.dunya, t1.TANIM, olgular, a.sorgu_ham))
        _, manifest = self.manifest_ozeti(dataclasses.replace(prm, ana_kume_sayisi=8, dedektor_egitim_sayisi=8))
        self.assertEqual(sorted(manifest["cikarilamaz_atilan"]), sorted(uretec.BOLMELER))
        self.assertGreater(manifest["cikarilamaz_atilan"]["yon_ters"], 0)

    def test_bozuk_bolum_denetime_girmez(self):
        """Zincir-bozukta beklenen cevap "bilmiyorum"dur; çıkarılabilirlik sorulmaz."""
        import random
        prm = dataclasses.replace(t1.KUCUK, cikarilabilirlik=True)
        with mock.patch.object(uretec, "cikarilabilir_mi", side_effect=AssertionError("bozukta denetim yapıldı")):
            a = uretec.aday_uret(random.Random(3), t1.TANIM, prm, "zincir_bozuk")
        self.assertIsNone(a.cevap["cevap"])


if __name__ == "__main__":
    unittest.main()
