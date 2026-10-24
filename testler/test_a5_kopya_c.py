"""K-028, V-046: kopya kuralı C ("yalnız yeni dayanak getiren kopya yazılır").

Tanım: adayın dayanağı = ebeveynlerinin kök kümelerinin birleşimi (dayandığı olgular). Aynı üçlünün havuzdaki
canlı bir çıkarımının kök kümesi adayın dayanağının alt kümesiyse aday yeni dayanak getirmez ve yazılmaz.
Gösterilenler: tanımın uç durumları; simetrik kural döngüsünün kendiliğinden durması; kök-ayrık (bağımsız) iki
ispatın ikisinin de korunması (destek 2, noisy-OR); müdahale testinin anlamı: B kuralında ("aynı üçlü varsa hiç
yazma") ikinci ispatın olgusu "ilgisiz" sanılıp soru puanlanır, C'de bu olgu dayanak sayılır ve soru sınanamadı
olur. İlişki adları anlamsızdır (blorp şeması).
"""
from unittest import mock

from cekirdek import dongu
from cekirdek.dongu import DAYANAK_YOK, DURMA_TUR_SINIRI, DURMA_YENI_YOK, calistir, yeni_dayanak_mi
from cekirdek.havuz import CIKARIM
from cekirdek.mudahale import PUANLI, SINANAMADI, mudahale_testi
from cekirdek.plazma import cevapla
from testler.test_a3_temel import halka, hucre
import testler.test_a3_cekirdek as t3

BB = hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
BB_IKIZ = hucre("h_bb_ikiz", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
UC = hucre("h_uc", [halka("frumb", "X", "Y"), halka("vonk", "Y", "W"), halka("zindle", "W", "Z")], ("quax", "X", "Z"))
SIMETRIK = hucre("h_sim", [halka("frumb", "X", "Y")], ("frumb", "Y", "X"))
IKI_YOL = [(1, "blorp", 2, 0.9), (2, "blorp", 3, 0.9), (1, "frumb", 5, 0.9), (5, "vonk", 6, 0.9), (6, "zindle", 3, 0.9)]


def b_kurali(havuz, uclu, _ebeveynler, ispat_mi):
    """Karşılaştırma için B: aynı üçlünün izli bir çıkarımı varsa (dayanağına bakmadan) yazma."""
    return not any(havuz.kayit(k).katman == CIKARIM and havuz.kayit(k).uclu == tuple(uclu) and ispat_mi(k)
                   for k in havuz.iliski_dizini(uclu[1]))


def hepsi_izli(_kimlik):
    return True


class TanimTesti(t3.Ortam):
    def setUp(self):
        super().setUp()
        self.h = self.havuz([(1, "blorp", 2, 1.0), (2, "blorp", 3, 1.0), (1, "frumb", 5, 1.0)])
        self.c = self.h.cikarim_ekle((1, "quax", 3), "h_bb", (0, 1), 1.0)

    def test_ayni_ya_da_daha_genis_dayanak_yeni_degil(self):
        self.assertFalse(yeni_dayanak_mi(self.h, (1, "quax", 3), (0, 1), hepsi_izli))
        self.assertFalse(yeni_dayanak_mi(self.h, (1, "quax", 3), (0, 1, 2), hepsi_izli))
        self.assertFalse(yeni_dayanak_mi(self.h, (1, "quax", 3), (self.c.kimlik, 2), hepsi_izli))

    def test_ayrik_ya_da_kismen_yeni_dayanak_yeni(self):
        self.assertTrue(yeni_dayanak_mi(self.h, (1, "quax", 3), (2,), hepsi_izli))
        self.assertTrue(yeni_dayanak_mi(self.h, (1, "quax", 3), (1, 2), hepsi_izli))

    def test_baska_uclu_ve_epitop_ispat_sayilmaz(self):
        self.assertTrue(yeni_dayanak_mi(self.h, (1, "vonk", 3), (0, 1), hepsi_izli))
        self.assertTrue(yeni_dayanak_mi(self.h, (1, "blorp", 2), (0,), hepsi_izli))

    def test_izsiz_kayit_dayanak_sayilmaz(self):
        """Defteri atlayıp havuza konan kayıt (V-035) meşru ispatı engelleyemez."""
        self.assertTrue(yeni_dayanak_mi(self.h, (1, "quax", 3), (0, 1), lambda kimlik: kimlik != self.c.kimlik))


class DonguTesti(t3.Ortam):
    def test_simetrik_kural_dongusu_kendiliginden_durur(self):
        h, g, s = self.kos([(1, "frumb", 2, 1.0)], SIMETRIK)
        yazilan = [k["veri"]["uclu"] for k in g.kayitlar() if k["tur"] == "YAZMA"]
        self.assertEqual((s.durma_nedeni, s.tur), (DURMA_YENI_YOK, 3))
        self.assertEqual(yazilan, [[2, "frumb", 1], [1, "frumb", 2]])
        atilan = [k["veri"] for k in g.kayitlar() if k["tur"] == "ESLESME_ATILDI"]
        self.assertEqual(atilan, [{"tur": 3, "neden": DAYANAK_YOK, "sayi": 1}])

    def test_eski_kural_dongusu_tur_sinirina_kadar_surerdi(self):
        with mock.patch.object(dongu, "yeni_dayanak_mi", lambda *_: True):
            _, _, s = self.kos([(1, "frumb", 2, 1.0)], SIMETRIK)
        self.assertEqual(s.durma_nedeni, DURMA_TUR_SINIRI)

    def test_bagimsiz_iki_ispat_korunur_ayni_dayanakli_kopya_atilir(self):
        h, g, _ = self.kos(IKI_YOL, BB, BB_IKIZ, UC, sorgu=(1, 3))
        yazilan = [(k["veri"]["uclu"], k["veri"]["zincir"]) for k in g.kayitlar() if k["tur"] == "YAZMA"]
        self.assertEqual(yazilan, [([1, "quax", 3], "h_bb"), ([1, "quax", 3], "h_uc")])
        self.assertEqual(g.destek((1, "quax", 3)), 2)
        c = cevapla(h, (1, 3), g)
        tek = [p["guven"] for p in c.gerekce]
        self.assertEqual(len(tek), 2)
        self.assertGreater(c.guven, max(tek))

    def test_mudahale_destegi_gorur_b_kurali_gormez(self):
        """C: ikinci ispatın olguları dayanaktır, ilgisiz epitop kalmaz → sınanamadı. B: ikinci ispat yazılmadığı için
        onun ortadaki olgusu "ilgisiz" sanılır, değiştirilince cevap değişmez → soru puanlanır (yanıltıcı)."""
        sonuclar = {}
        for ad, kural in (("C", yeni_dayanak_mi), ("B", b_kurali)):
            with mock.patch.object(dongu, "yeni_dayanak_mi", kural):
                h, g, _ = self.kos(IKI_YOL, BB, UC, sorgu=(1, 3), gunluk_adi=f"{ad}.jsonl")
                sonuclar[ad] = mudahale_testi(h, g, self.hucreler(BB, UC), IKI_YOL, t3.KK, t3.PRM, self.sema, (1, 3))
        self.assertEqual((sonuclar["C"].cevap, sonuclar["B"].cevap), ("quax", "quax"))
        self.assertEqual(sonuclar["C"].durum, SINANAMADI)
        self.assertEqual(sonuclar["B"].durum, PUANLI)
        self.assertEqual([d["uclu"] for d in sonuclar["B"].degisiklikler], [[5, "vonk", 6]])
        self.assertEqual(len(sonuclar["C"].silmeler), 5)
        self.assertEqual(len(sonuclar["B"].silmeler), 2)
