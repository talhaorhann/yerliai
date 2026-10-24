"""ÖK-002 §6, V-047: H1 hata incelemesi (yalnız teşhis; ayar ve DNA değişmez).

Hatalı bölüm, sınırlar gevşetilerek yeniden koşturulur: yalnız tur, yalnız havuz, ikisi birden. Cevap doğrulaşırsa
hata "sınır yetmedi" sınıfına, hiçbirinde doğrulaşmazsa "sınırdan bağımsız" sınıfına girer (elle incelenecek).
İlişki adları anlamsızdır (blorp şeması).
"""
import dataclasses

from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1, h1_inceleme
from testler.test_a3_temel import halka, hucre
from testler.test_a5_h1 import GUNLUK, bolum, cevap
import testler.test_a3_cekirdek as t3

KK = HizliKodKitabi(t3.AYAR.deger("vektor_tohum"), t3.AYAR.deger("vektor_boyutu"))
BB = hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
QZ = hucre("h_qz", [halka("quax", "X", "Y"), halka("zindle", "Y", "Z")], ("vonk", "X", "Z"))


class IncelemeTesti(t3.Ortam):
    def test_tur_siniri_yetmeyen_hata_ayrilir(self):
        b = bolum([(1, "blorp", 2), (2, "blorp", 3), (3, "zindle", 4)], (1, 4))
        c = cevap(b, "uzunluk", "vonk")
        dar = dataclasses.replace(t3.PRM, tur_siniri=1)
        hucreler = self.hucreler(BB, QZ)
        satir = h1.degerlendir(h1.bolum_kos(b, hucreler, self.sema, KK, dar, GUNLUK), c)
        self.assertFalse(satir["dogru"])
        teshis = h1_inceleme.teshis(b, c, hucreler, self.sema, KK, dar, GUNLUK)
        self.assertEqual(teshis["sinif"], h1_inceleme.SINIR_TUR)
        self.assertEqual(teshis["olagan"], None)
        self.assertEqual(teshis["genis_tur"], "vonk")

    def test_sinirdan_bagimsiz_hata(self):
        b = bolum([(1, "blorp", 2), (2, "zindle", 3)], (1, 3))
        c = cevap(b, "uzunluk", "quax")
        hucreler = self.hucreler(BB, QZ)
        teshis = h1_inceleme.teshis(b, c, hucreler, self.sema, KK, t3.PRM, GUNLUK)
        self.assertEqual(teshis["sinif"], h1_inceleme.SINIRDAN_BAGIMSIZ)

    def test_okunur_olgular(self):
        b = bolum([(1, "blorp", 2), (2, "zindle", 3)], (1, 3))
        metin = h1_inceleme.okunur(b)
        self.assertIn("1 —blorp→ 2", metin)
        self.assertIn("soru: 1 → 3", metin)
