"""sistem.md §2, §3, §5, §6; K-016..K-019, V-033, V-034: A3 kabul testleri (LLM'siz çekirdek, saf Python).

Afinite/güven formülü, θ süzgeci, hücre başına 8 sınırı, bütçe, döngü ve durma, impasse, havuzdan atma,
plazma (noisy-OR, kök kümesi, "bilmiyorum", çelişki), gerekçe, belirlenim ve girdiye duyarlılık.
İlişki adları anlamsızdır (blorp şeması); hücreler elle yazılmış DNA'dır.
"""
import dataclasses
import math
import tempfile
import unittest
from pathlib import Path

from cekirdek import vektor as V
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.olay_gunlugu import YEDEK_KULLANILDI
from cekirdek.defter import Defter
from cekirdek.dna import dna_kur
from cekirdek.dongu import DURMA_IMPASSE, DURMA_TUR_SINIRI, DURMA_YENI_YOK, CekirdekParametreleri, calistir
from cekirdek.eslesme import afinite, alici, eslesmeler
from cekirdek.havuz import Havuz
from cekirdek.plazma import cevapla, kok_kumesi, noisy_or
from testler.test_a1_iliski_semasi import SemaOrtami, blorp_semasi
from testler.test_a3_temel import DNA_BICIMI, dna_verisi, halka, hucre
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")
KK = V.KodKitabi(AYAR.deger("vektor_tohum"), AYAR.deger("vektor_boyutu"))
PRM = CekirdekParametreleri.ayardan(AYAR)

BB_Q = hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
QZ_V = hucre("h_qz", [halka("quax", "X", "Y"), halka("zindle", "Y", "Z")], ("vonk", "X", "Z"))
DUNYA = [(1, "blorp", 2, 1.0), (2, "blorp", 3, 1.0), (3, "zindle", 4, 1.0), (7, "frumb", 8, 1.0)]


class Ortam(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ortam = SemaOrtami(blorp_semasi())
        cls.sema = cls.ortam.yukle()

    @classmethod
    def tearDownClass(cls):
        cls.ortam.kapat()

    def setUp(self):
        self._d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self._d.cleanup()

    def gunluk(self, ad="olaylar.jsonl"):
        return Defter(Path(self._d.name) / ad, algoritma=AYAR.deger("hash_algoritmasi"),
                           sema_surumu=AYAR.deger("olay_sema_surumu"), izinli_kaynaklar=AYAR.deger("kaynaklar"))

    def hucreler(self, *veriler):
        return dna_kur(dna_verisi(*veriler), DNA_BICIMI, self.sema)

    def havuz(self, olgular, kapasite=None):
        h = Havuz(kapasite or PRM.kapasite, KK)
        for s, r, o, g in olgular:
            h.epitop_ekle(s, r, o, guven=g)
        return h

    @staticmethod
    def cevap(kos_sonucu, sorgu):
        """Defter iz kuralı (V-035): plazma, koşunun kendi defterini ister."""
        havuz, defter, _ = kos_sonucu
        return cevapla(havuz, sorgu, defter)

    def kos(self, olgular, *dna, sorgu=None, prm=PRM, kapasite=None, gunluk_adi="olaylar.jsonl"):
        h = self.havuz(olgular, kapasite)
        g = self.gunluk(gunluk_adi)
        sonuc = calistir(self.hucreler(*dna), h, KK, prm, g, iliski_semasi=self.sema, sorgu=sorgu)
        return h, g, sonuc


class AfiniteGuvenTesti(Ortam):
    def test_alici_ve_afinite(self):
        self.assertEqual(alici(KK, "blorp"), tuple(KK.olcek * x for x in KK.vektor("iliski", "blorp")))
        a = KK.vektor("varlik", 7)
        self.assertEqual(afinite(a, a), 1.0)
        self.assertEqual(afinite(a, tuple(-x for x in a)), 0.0)
        for i in range(13):
            v = V.kayit_vektoru(KK, i, "blorp", i + 1)
            self.assertGreater(afinite(alici(KK, "blorp"), v), 0.8)
            self.assertLess(afinite(alici(KK, "zindle"), v), 0.3)

    def test_guven_formulu_bagimsiz_hesapla(self):
        h = self.havuz([(1, "blorp", 2, 0.9), (2, "blorp", 3, 0.6)])
        (hc,) = self.hucreler(hucre("h", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"),
                                    guvenilirlik=0.8))
        (e,) = eslesmeler(hc, h, frozenset([0, 1]), KK, esik_carpani=1.0)
        afler = [afinite(alici(KK, "blorp"), h.kayit(k).vektor) for k in (0, 1)]
        self.assertEqual(e.afiniteler, tuple(afler))
        self.assertEqual(e.guven, min(afler + [0.9, 0.6]) * 0.8)
        self.assertEqual(e.uclu, (1, "quax", 3))

    def test_esik_suzgeci_ve_carpan(self):
        h = self.havuz([(1, "blorp", 2, 1.0), (2, "blorp", 3, 1.0)])
        (hc,) = self.hucreler(hucre("h", [halka("blorp", "X", "Y", 1.0), halka("blorp", "Y", "Z", 1.0)],
                                    ("quax", "X", "Z")))
        self.assertEqual(eslesmeler(hc, h, frozenset([0, 1]), KK, esik_carpani=1.0), [])
        self.assertEqual(len(eslesmeler(hc, h, frozenset([0, 1]), KK, esik_carpani=PRM.impasse_carpani)), 1)


class DonguTesti(Ortam):
    def test_iki_adimli_cikarim_ve_cevap(self):
        h, g, s = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        self.assertEqual(s.durma_nedeni, DURMA_YENI_YOK)
        self.assertEqual(s.tur, 3)
        self.assertEqual(sorted(k.uclu for k in h.kayitlar() if k.katman == 1), [(1, "quax", 3), (1, "vonk", 4)])
        c = cevapla(h, (1, 4), g)
        self.assertEqual(c.iliski, "vonk")
        self.assertFalse(c.celiski)
        self.assertGreater(c.guven, 0.8)

    def test_gerekce_epitoplara_iner(self):
        h, g, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        c = cevapla(h, (1, 4), g)
        yapraklar = set()

        def gez(dugum):
            if not dugum["ebeveynler"]:
                yapraklar.add(tuple(dugum["uclu"]))
            for e in dugum["ebeveynler"]:
                gez(e)
        for agac in c.gerekce:
            gez(agac)
        self.assertEqual(yapraklar, {(1, "blorp", 2), (2, "blorp", 3), (3, "zindle", 4)})

    def test_tur_siniri(self):
        _, g, s = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), prm=dataclasses.replace(PRM, tur_siniri=1))
        self.assertEqual((s.durma_nedeni, s.tur), (DURMA_TUR_SINIRI, 1))
        self.assertTrue(any(k["tur"] == "DURMA" for k in g.kayitlar()))

    def test_impasse_esigi_bir_kez_dusurur(self):
        yuksek = hucre("h", [halka("blorp", "X", "Y", 1.0), halka("blorp", "Y", "Z", 1.0)], ("quax", "X", "Z"))
        h, g, s = self.kos(DUNYA, yuksek, sorgu=(1, 3))
        self.assertEqual((s.durma_nedeni, s.esik_dusurme), (DURMA_YENI_YOK, 1))
        self.assertEqual(cevapla(h, (1, 3), g).iliski, "quax")

    def test_cevapsiz_ikinci_impassete_durur(self):
        h, g, s = self.kos(DUNYA, BB_Q, sorgu=(1, 8))
        self.assertEqual((s.durma_nedeni, s.esik_dusurme), (DURMA_IMPASSE, 1))
        self.assertIsNone(cevapla(h, (1, 8), g).iliski)

    def test_sorgusuz_sabit_noktada_durur(self):
        _, _, s = self.kos(DUNYA, BB_Q, QZ_V)
        self.assertEqual((s.durma_nedeni, s.esik_dusurme), (DURMA_YENI_YOK, 0))

    def test_hucre_basina_sekiz_yazma(self):
        olgular = [(i, "blorp", i + 100, 0.5 + i / 100) for i in range(13)]
        kopya = hucre("h1", [halka("blorp", "X", "Y")], ("quax", "X", "Y"))
        h, g, s = self.kos(olgular, kopya, prm=dataclasses.replace(PRM, tur_siniri=1))
        yazilan = [k for k in h.kayitlar() if k.katman == 1]
        self.assertEqual(len(yazilan), PRM.hucre_yazma_siniri)
        hepsi = eslesmeler(self.hucreler(kopya)[0], self.havuz(olgular), frozenset(range(13)), KK, 1.0)
        en_iyi = sorted(hepsi, key=lambda e: (-(min(e.afiniteler) * e.guven), e.baglama.kayitlar))[:8]
        self.assertEqual(sorted(k.uclu for k in yazilan), sorted(e.uclu for e in en_iyi))
        atilan = [k for k in g.kayitlar() if k["tur"] == "ESLESME_ATILDI"]
        self.assertEqual(sum(k["veri"]["sayi"] for k in atilan), 13 - 8)

    def test_tur_butcesi(self):
        olgular = [(i, "blorp", i + 100, 1.0) for i in range(5)]
        h1 = hucre("h1", [halka("blorp", "X", "Y")], ("quax", "X", "Y"))
        h2 = hucre("h2", [halka("blorp", "X", "Y")], ("vonk", "X", "Y"))
        h, g, _ = self.kos(olgular, h1, h2, prm=dataclasses.replace(PRM, butce=3, tur_siniri=1))
        self.assertEqual(len([k for k in h.kayitlar() if k.katman == 1]), 3)
        self.assertEqual(sum(k["veri"]["sayi"] for k in g.kayitlar() if k["tur"] == "ESLESME_ATILDI"), 7)


class HavuzAtmaTesti(Ortam):
    def test_en_dusuk_guvenli_cikarim_atilir_mezar_tasi_kalir(self):
        olgular = [(1, "blorp", 2, 0.9), (2, "blorp", 3, 0.9), (5, "blorp", 6, 0.4), (6, "blorp", 7, 0.4)]
        kv = hucre("h_qv", [halka("quax", "X", "Y")], ("vonk", "X", "Y"))
        h, g, _ = self.kos(olgular, BB_Q, kv, kapasite=6)
        self.assertLessEqual(len(h.kayitlar()), 6)
        atmalar = [k["veri"] for k in g.kayitlar() if k["tur"] == "ATMA"]
        self.assertTrue(atmalar)
        self.assertEqual(atmalar[0]["uclu"], [5, "quax", 7])
        canli = {k.kimlik for k in h.kayitlar()}
        for a in atmalar:
            self.assertNotIn(a["kimlik"], canli)
            self.assertEqual(tuple(h.kayit(a["kimlik"]).uclu), tuple(a["uclu"]))
        for k in h.kayitlar():
            self.assertTrue(all(h.kayit(r).katman == 0 for r in kok_kumesi(h, k.kimlik)))
        self.assertNotIn(atmalar[0]["kimlik"], h.iliski_dizini("quax"))

    def test_atilacak_cikarim_yoksa_yedek_olayi(self):
        h, g, s = self.kos(DUNYA, BB_Q, sorgu=(1, 3), kapasite=4)
        self.assertEqual([k for k in h.kayitlar() if k.katman == 1], [])
        self.assertGreaterEqual(g.sayac(YEDEK_KULLANILDI), 1)
        self.assertIsNone(cevapla(h, (1, 3), g).iliski)


class PlazmaTesti(Ortam):
    IKI_YOL = [(1, "blorp", 2, 0.6), (2, "blorp", 3, 0.6), (1, "blorp", 5, 0.7), (5, "blorp", 3, 0.7)]

    def test_bagimsiz_ispatlar_noisy_or(self):
        h, g, _ = self.kos(self.IKI_YOL, BB_Q, sorgu=(1, 3))
        ispatlar = [k for k in h.kayitlar() if k.katman == 1 and k.uclu == (1, "quax", 3)]
        self.assertEqual(len(ispatlar), 2)
        self.assertEqual(sorted(k.guven for k in ispatlar), [0.6, 0.7])
        c = cevapla(h, (1, 3), g)
        self.assertAlmostEqual(c.guven, 1 - (1 - 0.6) * (1 - 0.7), places=12)

    def test_ortak_kokenli_kopyalar_guveni_sisirmez(self):
        """10 aynı hücre aynı olgulardan 10 ispat yazar; kök kümeleri aynı olduğu için güven değişmez."""
        tek = self.cevap(self.kos(self.IKI_YOL[:2], BB_Q, sorgu=(1, 3), gunluk_adi="a.jsonl"), (1, 3))
        kopyalar = [dict(BB_Q, kimlik=f"h_kopya{i}") for i in range(10)]
        h10, g10, _ = self.kos(self.IKI_YOL[:2], *kopyalar, sorgu=(1, 3), gunluk_adi="b.jsonl")
        self.assertEqual(len([k for k in h10.kayitlar() if k.katman == 1]), 10)
        self.assertEqual(cevapla(h10, (1, 3), g10).guven, tek.guven)

    def test_noisy_or_ucler(self):
        self.assertEqual(noisy_or([]), 0.0)
        self.assertEqual(noisy_or([1.0, 0.3]), 1.0)
        self.assertAlmostEqual(noisy_or([0.5, 0.5, 0.5]), 0.875, places=12)
        for g in noisy_or([0.2] * 13), noisy_or([0.999999] * 7):
            self.assertTrue(0 <= g <= 1)

    def test_ispat_yoksa_bilmiyorum(self):
        h, g, _ = self.kos(DUNYA, BB_Q, sorgu=(1, 7))
        c = cevapla(h, (1, 7), g)
        self.assertEqual((c.iliski, c.guven, c.gerekce), (None, None, ()))

    def test_esit_celiski_bilmiyorum_esitsiz_celiski_isaretli(self):
        bv = hucre("h_bv", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("vonk", "X", "Z"))
        h, g, _ = self.kos(DUNYA, BB_Q, bv, sorgu=(1, 3), gunluk_adi="a.jsonl")
        c = cevapla(h, (1, 3), g)
        self.assertEqual((c.iliski, c.celiski), (None, True))
        zayif = dict(bv, guvenilirlik=0.5)
        h, g, _ = self.kos(DUNYA, BB_Q, zayif, sorgu=(1, 3), gunluk_adi="b.jsonl")
        c = cevapla(h, (1, 3), g)
        self.assertEqual((c.iliski, c.celiski), ("quax", True))


class GenelTest(Ortam):
    def test_belirlenim(self):
        h1, g1, s1 = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="a.jsonl")
        h2, g2, s2 = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="b.jsonl")
        self.assertEqual(h1.kayitlar(), h2.kayitlar())
        self.assertEqual(s1, s2)
        self.assertEqual((Path(self._d.name) / "a.jsonl").read_bytes(), (Path(self._d.name) / "b.jsonl").read_bytes())

    def test_girdiye_duyarli_ilgisize_duyarsiz(self):
        tam = self.cevap(self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="a.jsonl"), (1, 4))
        eksik = self.cevap(self.kos([o for o in DUNYA if o[:3] != (2, "blorp", 3)], BB_Q, QZ_V, sorgu=(1, 4),
                                 gunluk_adi="b.jsonl"), (1, 4))
        ilgisiz = self.cevap(self.kos(DUNYA[:3] + [(9, "frumb", 11, 1.0)], BB_Q, QZ_V, sorgu=(1, 4),
                                   gunluk_adi="c.jsonl"), (1, 4))
        self.assertEqual(tam.iliski, "vonk")
        self.assertIsNone(eksik.iliski)
        self.assertEqual((ilgisiz.iliski, ilgisiz.guven), (tam.iliski, tam.guven))

    def test_yeniden_adlandirma_tutarli(self):
        """blorp testi: ilişki adları tutarlı biçimde değişince cevap da aynı eşlemeyle değişir."""
        es = {"blorp": "zindle", "zindle": "blorp", "quax": "frumb", "frumb": "quax", "vonk": "vonk"}

        def adla(hucre_verisi):
            v = dict(hucre_verisi, halkalar=[dict(x, gen=es[x["gen"]]) for x in hucre_verisi["halkalar"]])
            v["sonuc"] = dict(v["sonuc"], gen=es[v["sonuc"]["gen"]])
            return v
        asil = self.cevap(self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="a.jsonl"), (1, 4))
        yeni = self.cevap(self.kos([(s, es[r], o, g) for s, r, o, g in DUNYA], adla(BB_Q), adla(QZ_V), sorgu=(1, 4),
                                gunluk_adi="b.jsonl"), (1, 4))
        self.assertEqual(yeni.iliski, es[asil.iliski])
        self.assertTrue(math.isfinite(yeni.guven))


if __name__ == "__main__":
    unittest.main()
