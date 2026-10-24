"""K-031, V-051: kopya kuralı C hücre sınırından önce uygulanır (sistem.md §3 "hücre başına tur başına ≤8 yazma").

Sınır, yeni dayanak getirmeyen (C'nin atacağı) adayları saymaz; yalnız yazılabilecek adaylar arasında en iyi
`hucre_yazma_siniri` tanesi kalır. Sınır yazılabilecek adaylarda yine geçerlidir.
Senaryo: simetrik kural kopya üretir; kopyanın puanı, aynı hücrenin bulduğu yeni üçlününkinden yüksektir. Sınır 1.
İlişki adları anlamsızdır (blorp şeması).
"""
import dataclasses

from cekirdek.dongu import DAYANAK_YOK, DURMA_YENI_YOK
from cekirdek.havuz import CIKARIM
from testler.test_a3_temel import halka, hucre
import testler.test_a3_cekirdek as t3

SIMETRIK = hucre("h_sim", [halka("frumb", "X", "Y")], ("frumb", "Y", "X"))
ZQ = hucre("h_zq", [halka("zindle", "X", "Y")], ("quax", "X", "Y"))
QF = hucre("h_qf", [halka("quax", "X", "Y")], ("frumb", "X", "Y"))
DUNYA = [(1, "frumb", 2, 1.0), (3, "zindle", 4, 0.3)]
SINIR_1 = dataclasses.replace(t3.PRM, hucre_yazma_siniri=1)


def olaylar(g, tur_adi, tur=None):
    return [k["veri"] for k in g.kayitlar() if k["tur"] == tur_adi and (tur is None or k["veri"].get("tur") == tur)]


class SiraTesti(t3.Ortam):
    def test_kopya_yeni_uclunun_yerini_almaz(self):
        h, g, s = self.kos(DUNYA, SIMETRIK, ZQ, QF, prm=SINIR_1)
        # ön koşul: 3. turda simetrik hücrede önce kopya (C'nin atacağı), sonra yeni üçlü sıralanır
        sirali = [tuple(v["uclu"]) for v in olaylar(g, "ATESLEME", 3) if v["hucre"] == "h_sim"]
        self.assertEqual(sirali, [(2, "frumb", 1), (4, "frumb", 3)])
        yazilan = {tuple(v["uclu"]): v["tur"] for v in olaylar(g, "YAZMA")}
        self.assertEqual(yazilan.get((4, "frumb", 3)), 3)
        self.assertIn((4, "frumb", 3), {k.uclu for k in h.kayitlar() if k.katman == CIKARIM})
        atilan = olaylar(g, "ESLESME_ATILDI", 3)
        self.assertEqual([(v["neden"], v["sayi"]) for v in atilan], [(DAYANAK_YOK, 1)])
        self.assertEqual(s.durma_nedeni, DURMA_YENI_YOK)

    def test_sinir_yazilabilecek_adaylarda_gecerli(self):
        h, g, _ = self.kos([(1, "frumb", 2, 1.0), (5, "frumb", 6, 1.0)], SIMETRIK, prm=SINIR_1)
        self.assertEqual(len(olaylar(g, "YAZMA", 1)), 1)
        self.assertEqual([(v["neden"], v["hucre"], v["sayi"]) for v in olaylar(g, "ESLESME_ATILDI", 1)],
                         [("hucre_siniri", "h_sim", 1)])

    def test_dayanaksiz_sayisi_tur_basina_tek_olay(self):
        """C öne alınınca da 'dayanak yok' turda tek olaydır; ön süzgeç ve yazma sırasındaki ret birlikte sayılır."""
        _, g, _ = self.kos(DUNYA, SIMETRIK, ZQ, QF)
        for tur in {v["tur"] for v in olaylar(g, "ESLESME_ATILDI")}:
            self.assertLessEqual(sum(1 for v in olaylar(g, "ESLESME_ATILDI", tur) if v["neden"] == DAYANAK_YOK), 1)
