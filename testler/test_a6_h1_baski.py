"""ÖK-004 §4: havuz ve eşleşme bütçesi baskısı ölçümü. Ölçüm defterdeki olaylardan okunur; sınırlar değişmez.
Küçük sınırlarla her baskı türünün sayıldığı, bol sınırlarla hiçbirinin sayılmadığı gösterilir (blorp şeması)."""
import dataclasses

from degerlendirme import h1_baski
from testler.test_a3_temel import halka, hucre
from testler.test_a5_h1 import GUNLUK
import testler.test_a3_cekirdek as t3

BB = hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
QB = hucre("h_qb", [halka("quax", "X", "Y"), halka("blorp", "Y", "Z")], ("vonk", "X", "Z"))
ZINCIR = 7  # zincirdeki kişi sayısı


def bolum(sorgu):
    olgular = [{"ozne": i, "iliski": "blorp", "nesne": i + 1, "guven": 1.0} for i in range(ZINCIR - 1)]
    return {"ozet": "x", "olgular": olgular, "sorgu": {"ozne": sorgu[0], "nesne": sorgu[1]}}


class BaskiTesti(t3.Ortam):
    def olc(self, prm, sorgu=(0, 3)):
        return h1_baski.bolum_baskisi(bolum(sorgu), self.hucreler(BB, QB), self.sema, t3.KK, prm, GUNLUK)

    def test_bol_sinirda_baski_yok(self):
        b = self.olc(t3.PRM)
        self.assertEqual((b["tur_siniri"], b["atma"], b["yedek"], b["butce_atilan"], b["hucre_atilan"]),
                         (False, 0, 0, 0, 0))
        self.assertEqual(b["cevap"], "vonk")
        self.assertGreater(b["en_cok_eslesme"], 0)

    def test_tur_siniri(self):
        b = self.olc(dataclasses.replace(t3.PRM, tur_siniri=1))
        self.assertTrue(b["tur_siniri"])
        self.assertEqual(b["tur"], 1)

    def test_havuz_dolunca_atma(self):
        b = self.olc(dataclasses.replace(t3.PRM, kapasite=ZINCIR + 1))
        self.assertGreater(b["atma"], 0)
        self.assertEqual(b["en_cok_doluluk"], ZINCIR + 1)

    def test_butce_ve_hucre_siniri(self):
        self.assertGreater(self.olc(dataclasses.replace(t3.PRM, butce=1))["butce_atilan"], 0)
        self.assertGreater(self.olc(dataclasses.replace(t3.PRM, hucre_yazma_siniri=1))["hucre_atilan"], 0)

    def test_ozet_sinirla_iliskili_hatayi_ayirir(self):
        satirlar = [dict(self.olc(t3.PRM), bolme="b", tohum=1, beklenen="vonk"),
                    dict(self.olc(dataclasses.replace(t3.PRM, tur_siniri=1)), bolme="b", tohum=1, beklenen="vonk")]
        o = h1_baski.ozetle(satirlar)["b"]
        self.assertEqual((o["n"], o["dogru"], o["tur_siniri"], o["sinirla_iliskili_hata"]), (2, 1, 1, 1))
