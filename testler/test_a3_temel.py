"""sistem.md §2, §3; V-032: DNA biçimi, havuz yapısı ve sembolik (yarı-naif) eşleşme.

Afinite, güven formülü, havuzdan atma ve durma V-028..V-031 onayına bağlıdır; burada yalnız §3'ün doğrudan
tarif ettiği sembolik kısım sınanır. İlişki adları anlamsızdır (blorp şeması).
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from cekirdek import vektor as V
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.dna import DnaHatasi, dna_kur, dna_yukle
from cekirdek.eslesme import baglamalar, sonuc_uclusu
from cekirdek.havuz import Havuz, HavuzHatasi
from testler.test_a1_iliski_semasi import SemaOrtami, blorp_semasi
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")
DNA_BICIMI = KOK / "sema" / "dna_v1.schema.json"
KK = V.KodKitabi(AYAR.deger("vektor_tohum"), AYAR.deger("vektor_boyutu"))


def halka(gen, sol, sag, esik=0.5):
    return {"gen": gen, "sol": sol, "sag": sag, "esik": esik}


def hucre(kimlik, halkalar, sonuc, guvenilirlik=1.0):
    return {"kimlik": kimlik, "halkalar": halkalar, "sonuc": {"gen": sonuc[0], "sol": sonuc[1], "sag": sonuc[2]},
            "guvenilirlik": guvenilirlik}


def dna_verisi(*hucreler):
    return {"sema_surumu": "1", "hucreler": list(hucreler)}


ZINCIR2 = hucre("h_zincir", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))


class Ortam(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ortam = SemaOrtami(blorp_semasi())
        cls.sema = cls.ortam.yukle()

    @classmethod
    def tearDownClass(cls):
        cls.ortam.kapat()

    def havuz(self, olgular, kapasite=None):
        h = Havuz(kapasite or AYAR.deger("havuz_kapasitesi"), KK)
        for s, r, o in olgular:
            h.epitop_ekle(s, r, o, guven=1.0)
        return h


class DnaTesti(Ortam):
    def test_gecerli_dna(self):
        hucreler = dna_kur(dna_verisi(ZINCIR2), DNA_BICIMI, self.sema)
        self.assertEqual(len(hucreler), 1)
        h = hucreler[0]
        self.assertEqual(h.kimlik, "h_zincir")
        self.assertEqual([x.gen for x in h.halkalar], ["blorp", "blorp"])
        self.assertEqual(h.sonuc.gen, "quax")

    def test_dosyadan_yukleme(self):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "dna.json"
            yol.write_text(json.dumps(dna_verisi(ZINCIR2)), encoding="utf-8")
            self.assertEqual(dna_yukle(yol, DNA_BICIMI, self.sema), dna_kur(dna_verisi(ZINCIR2), DNA_BICIMI, self.sema))

    def reddedilir(self, degistir):
        veri = dna_verisi(copy.deepcopy(ZINCIR2))
        degistir(veri)
        with self.assertRaises(DnaHatasi):
            dna_kur(veri, DNA_BICIMI, self.sema)

    def test_bozuk_dna_reddedilir(self):
        self.reddedilir(lambda v: v["hucreler"][0]["halkalar"].clear())
        self.reddedilir(lambda v: v["hucreler"][0]["halkalar"].extend([halka("blorp", "Z", "W")] * 2))
        self.reddedilir(lambda v: v["hucreler"][0]["halkalar"][0].update(gen="glim"))
        self.reddedilir(lambda v: v["hucreler"][0]["sonuc"].update(gen="glim"))
        self.reddedilir(lambda v: v["hucreler"][0]["sonuc"].update(sag="W"))
        self.reddedilir(lambda v: v["hucreler"].append(copy.deepcopy(v["hucreler"][0])))
        self.reddedilir(lambda v: v["hucreler"][0].update(not_="x"))
        self.reddedilir(lambda v: v["hucreler"][0]["halkalar"][0].update(esik=1.5))


class HavuzTesti(Ortam):
    def test_epitop_kaydi(self):
        h = self.havuz([(7, "blorp", 11), (11, "zindle", 13)])
        k0, k1 = h.kayitlar()
        self.assertEqual((k0.kimlik, k1.kimlik), (0, 1))
        self.assertEqual(k0.uclu, (7, "blorp", 11))
        self.assertEqual(k0.katman, 0)
        self.assertEqual((k0.zincir, k0.ebeveynler), (None, ()))
        self.assertEqual(k0.vektor, V.kayit_vektoru(KK, 7, "blorp", 11))
        self.assertEqual(h.iliski_dizini("blorp"), (0,))
        self.assertEqual(h.iliski_dizini("frumb"), ())

    def test_cikarim_kaydi_ve_tekillestirme(self):
        h = self.havuz([(7, "blorp", 11), (11, "blorp", 13)])
        k = h.cikarim_ekle((7, "quax", 13), zincir="h_zincir", ebeveynler=(0, 1), guven=0.5)
        self.assertEqual((k.kimlik, k.katman, k.ebeveynler), (2, 1, (0, 1)))
        self.assertIsNone(h.cikarim_ekle((7, "quax", 13), zincir="h_zincir", ebeveynler=(0, 1), guven=0.5))
        self.assertIsNotNone(h.cikarim_ekle((7, "quax", 13), zincir="h_baska", ebeveynler=(0, 1), guven=0.5))
        self.assertEqual(h.iliski_dizini("quax"), (2, 3))

    def test_yas_tur_ile_artar(self):
        h = self.havuz([(7, "blorp", 11)])
        self.assertEqual(h.yas(0), 0)
        h.tur_ilerlet()
        h.tur_ilerlet()
        self.assertEqual(h.yas(0), 2)
        k = h.cikarim_ekle((7, "quax", 11), zincir="h", ebeveynler=(0,), guven=1.0)
        self.assertEqual((k.yazildigi_tur, h.yas(k.kimlik)), (2, 0))

    def test_epitoplar_kapasiteyi_asarsa_durur(self):
        with self.assertRaises(HavuzHatasi):
            self.havuz([(i, "blorp", i + 1) for i in range(7)], kapasite=5)

    def test_gecersiz_guven_ve_kendine_ebeveyn_reddedilir(self):
        h = self.havuz([(7, "blorp", 11)])
        for g in (-0.1, 1.1, float("nan")):
            with self.assertRaises(HavuzHatasi):
                h.cikarim_ekle((7, "quax", 11), zincir="h", ebeveynler=(0,), guven=g)
        with self.assertRaises(HavuzHatasi):
            h.cikarim_ekle((7, "quax", 11), zincir="h", ebeveynler=(99,), guven=1.0)
        with self.assertRaises(HavuzHatasi):
            h.cikarim_ekle((7, "quax", 11), zincir="h", ebeveynler=(), guven=1.0)


class EslesmeTesti(Ortam):
    def hucreler(self, *veriler):
        return dna_kur(dna_verisi(*veriler), DNA_BICIMI, self.sema)

    def test_zincir_tutarli_baglanir(self):
        h = self.havuz([(7, "blorp", 11), (11, "blorp", 13), (13, "zindle", 17), (19, "blorp", 7)])
        (hc,) = self.hucreler(ZINCIR2)
        sonuc = baglamalar(hc, h, yeni=frozenset(range(4)))
        self.assertEqual([b.kayitlar for b in sonuc], [(0, 1), (3, 0)])
        self.assertEqual([sonuc_uclusu(hc, b) for b in sonuc], [(7, "quax", 13), (19, "quax", 11)])

    def test_halkalar_farkli_kayitlara_baglanir(self):
        h = self.havuz([(7, "blorp", 7)])
        (hc,) = self.hucreler(hucre("h", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z")))
        self.assertEqual(baglamalar(hc, h, yeni=frozenset([0])), [])

    def test_ayni_degisken_ayni_varlik(self):
        h = self.havuz([(7, "blorp", 7), (7, "blorp", 11)])
        (hc,) = self.hucreler(hucre("h", [halka("blorp", "X", "X")], ("frumb", "X", "X")))
        self.assertEqual([b.kayitlar for b in baglamalar(hc, h, yeni=frozenset([0, 1]))], [(0,)])

    def test_yari_naif_en_az_bir_yeni_kayit(self):
        h = self.havuz([(7, "blorp", 11), (11, "blorp", 13), (13, "blorp", 17)])
        (hc,) = self.hucreler(ZINCIR2)
        self.assertEqual(baglamalar(hc, h, yeni=frozenset()), [])
        self.assertEqual([b.kayitlar for b in baglamalar(hc, h, yeni=frozenset([2]))], [(1, 2)])
        self.assertEqual([b.kayitlar for b in baglamalar(hc, h, yeni=frozenset([0, 1, 2]))], [(0, 1), (1, 2)])

    def test_uc_halka(self):
        h = self.havuz([(7, "blorp", 11), (11, "zindle", 13), (13, "blorp", 17), (13, "blorp", 19)])
        (hc,) = self.hucreler(hucre("h3", [halka("blorp", "A", "B"), halka("zindle", "B", "C"), halka("blorp", "C", "D")],
                                    ("vonk", "A", "D")))
        sonuc = baglamalar(hc, h, yeni=frozenset(range(4)))
        self.assertEqual([sonuc_uclusu(hc, b) for b in sonuc], [(7, "vonk", 17), (7, "vonk", 19)])

    def test_girdiye_duyarli_ilgisize_duyarsiz(self):
        """Sahte kod denetimi: zincirin bir halkası silinince sonuç düşer; ilgisiz olgu sonucu değiştirmez."""
        (hc,) = self.hucreler(ZINCIR2)
        tam = self.havuz([(7, "blorp", 11), (11, "blorp", 13), (23, "zindle", 29)])
        eksik = self.havuz([(7, "blorp", 11), (23, "zindle", 29)])
        ilgisiz = self.havuz([(7, "blorp", 11), (11, "blorp", 13), (31, "zindle", 37)])
        uc = lambda h: [sonuc_uclusu(hc, b) for b in baglamalar(hc, h, yeni=frozenset(range(3)))]
        self.assertEqual(uc(tam), [(7, "quax", 13)])
        self.assertEqual(uc(eksik), [])
        self.assertEqual(uc(ilgisiz), uc(tam))

    def test_yon_onemli(self):
        h = self.havuz([(11, "blorp", 7), (11, "blorp", 13)])
        (hc,) = self.hucreler(ZINCIR2)
        self.assertEqual(baglamalar(hc, h, yeni=frozenset([0, 1])), [])


if __name__ == "__main__":
    unittest.main()
