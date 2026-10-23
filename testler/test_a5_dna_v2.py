"""K-025, V-043: DNA sürüm 2, isteğe bağlı "farklı kişi" şartı.

Şart yokken iki değişken aynı varlığa bağlanabilir (sürüm 1 davranışı, değişmez). `farkli` ile verilen değişken
çiftleri farklı varlıklara bağlanmak zorundadır. İlişki adları anlamsızdır (blorp şeması).
"""
import copy
import unittest

from cekirdek.dna import DnaHatasi, dna_kur
from cekirdek.dongu import calistir
from cekirdek.eslesme import eslesmeler
from testler.test_a1_iliski_semasi import SemaOrtami, blorp_semasi
from testler.test_a3_temel import DNA_BICIMI, dna_verisi, halka, hucre
from testler.yardimci import KOK
import testler.test_a3_cekirdek as t3

DNA_V2 = KOK / "sema" / "dna_v2.schema.json"
GERI_DONEN = [(1, "blorp", 2, 1.0), (2, "zindle", 1, 1.0), (2, "zindle", 3, 1.0)]


def v2(*hucreler):
    return {"sema_surumu": "2", "hucreler": list(hucreler)}


def farkli_hucre(farkli=(("X", "Z"),), **ek):
    h = hucre("h_fark", [halka("blorp", "X", "Y"), halka("zindle", "Y", "Z")], ("quax", "X", "Z"))
    if farkli is not None:
        h["farkli"] = [list(c) for c in farkli]
    h.update(ek)
    return h


class Ortam(t3.Ortam):
    def kur(self, *hucreler):
        return dna_kur(v2(*hucreler), DNA_V2, self.sema)


class DnaV2BicimTesti(Ortam):
    def test_farkli_sarti_yuklenir(self):
        (h,) = self.kur(farkli_hucre(okunus="X'in blorp'u Y, Y'nin zindle'ı Z ise Z, X'in quax'ıdır."))
        self.assertEqual(h.farkli, (("X", "Z"),))

    def test_sartsiz_hucre_ve_surum_1_aynen_calisir(self):
        (h,) = self.kur(farkli_hucre(farkli=None))
        self.assertEqual(h.farkli, ())
        (h1,) = dna_kur(dna_verisi(farkli_hucre(farkli=None)), DNA_BICIMI, self.sema)
        self.assertEqual(h1, h)

    def reddedilir(self, veri, bicim=DNA_V2):
        with self.assertRaises(DnaHatasi):
            dna_kur(veri, bicim, self.sema)

    def test_bozuk_farkli_reddedilir(self):
        self.reddedilir(v2(farkli_hucre(farkli=(("X", "W"),))))
        self.reddedilir(v2(farkli_hucre(farkli=(("X", "X"),))))
        self.reddedilir(v2(farkli_hucre(farkli=(("X", "Y", "Z"),))))
        self.reddedilir(v2(farkli_hucre(farkli=(("X", "z"),))))
        self.reddedilir(v2(farkli_hucre(farkli=())))
        self.reddedilir(v2(farkli_hucre(okunus="")))
        self.reddedilir(v2(farkli_hucre(not_="x")))

    def test_surumler_karismaz(self):
        self.reddedilir(dna_verisi(farkli_hucre()), DNA_BICIMI)
        self.reddedilir(dna_verisi(farkli_hucre(farkli=None)), DNA_V2)
        self.reddedilir(v2(farkli_hucre()), DNA_BICIMI)


class FarkliEslesmeTesti(Ortam):
    def eslesen_ucluler(self, h):
        havuz = self.havuz(GERI_DONEN)
        return sorted(e.uclu for e in eslesmeler(h, havuz, frozenset(range(3)), t3.KK, esik_carpani=1.0))

    def test_sart_yokken_ayni_varliga_baglanir(self):
        (h,) = self.kur(farkli_hucre(farkli=None))
        self.assertEqual(self.eslesen_ucluler(h), [(1, "quax", 1), (1, "quax", 3)])

    def test_farkli_sarti_ayni_varlik_baglamasini_engeller(self):
        (h,) = self.kur(farkli_hucre())
        self.assertEqual(self.eslesen_ucluler(h), [(1, "quax", 3)])

    def test_ara_degisken_icin_de_calisir(self):
        (h,) = self.kur(farkli_hucre(farkli=(("Y", "Z"), ("X", "Z"))))
        self.assertEqual(self.eslesen_ucluler(h), [(1, "quax", 3)])

    def test_dongu_kendine_iliski_yazmaz(self):
        havuz = self.havuz(GERI_DONEN)
        defter = self.gunluk()
        calistir(self.kur(farkli_hucre()), havuz, t3.KK, t3.PRM, defter, iliski_semasi=self.sema)
        yazilan = [k["veri"]["uclu"] for k in defter.kayitlar() if k["tur"] == "YAZMA"]
        self.assertEqual(yazilan, [[1, "quax", 3]])


if __name__ == "__main__":
    unittest.main()
