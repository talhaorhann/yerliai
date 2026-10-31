"""K-041, K-043 (ÖK-005 taslağı §4 madde 4–14, §7, §13), V-065: H2 kabul geçidi (aşama 1–5) ve hüküm sırası.

Sentetik dünya (blorp şeması, ilişki adları anlamsız): her kişinin en çok bir blorp'u vardır (işlevsel, ağaç); blorp'un
tersi F1 ve F2'de hep zindle, F3'te tek kimliklilerde quax; iki adımlık blorp yolunun uçları vonk ile gözlenir; aynı
blorp'u olanlar arasında iki yönlü frumb vardır. Doğru kural: blorp∘blorp → vonk. Yanlış kural: blorp → vonk.
"""
import dataclasses
import random
import unittest

from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h2_gecit as G
from degerlendirme import h2_ikiz, kural
from kesif import m0
from testler.test_a1_iliski_semasi import SemaOrtami, blorp_semasi
from testler.test_a5_h1 import GUNLUK
from testler.yardimci import KOK
import testler.test_a3_cekirdek as t3

H2 = ayar_yukle(KOK / "config_h2.json")
B, ZN, Q, F, V = "blorp", "zindle", "quax", "frumb", "vonk"
TEMEL = (B, ZN, Q, F)
SABIT = G.Sabitler(en_az_tanik=3, kapsam_en_az_aile=2, ret_aile_sayisi=2, wilson_z=1.959963984540054, fwer=0.01,
                   tur_siniri=12, wy_cekilis=20, bolum_sayisi=2, taze_aile_basina=2, adim_araligi=(2, 3),
                   dikkat_sayisi=2, pi_bolum_sayisi=1, mudahale_en_az_kanit=3, kapanis_tur_siniri=8,
                   bagla_deneme_carpani=10, halka_esigi=0.5, guvenilirlik=1.0)
ESIK = G.Esikler(tau=0.5, mudahale=0.9, T=0.04, sigma=0.01)


def dunya(aile, n, tohum):
    rng = random.Random(tohum)
    ust = {i: rng.randrange(i) for i in range(3, n)}
    olg = set()
    for i, p in ust.items():
        olg |= {(i, B, p), (p, Q if aile == "F3" and i % 2 else ZN, i)}
        if p in ust:
            olg.add((i, V, ust[p]))
    for i in ust:
        for j in ust:
            if i != j and ust[i] == ust[j]:
                olg.add((i, F, j))
    return m0.Dunya(aile, tuple(range(n)), tuple(sorted(olg)))


def k(halkalar, bas, farkli=()):
    return kural.Kural(halkalar, bas, farkli)


DOGRU = k([(B, "X", "Z"), (B, "Z", "Y")], (V, "X", "Y"))
YANLIS = k([(B, "X", "Y")], (V, "X", "Y"))
TERS = k([(B, "X", "Y")], (ZN, "Y", "X"))  # F3'te yanlış
YALNIZ_F3 = k([(Q, "X", "Y")], (B, "Y", "X"))  # gövdesi yalnız F3'te eşleşir
SIMETRIK = k([(F, "X", "Y")], (F, "Y", "X"))
FAZLA = k([(B, "X", "Z"), (B, "Z", "Y"), (ZN, "Z", "X")], (V, "X", "Y"))


class Ortak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.so = SemaOrtami(blorp_semasi())
        cls.sema = cls.so.yukle()
        gel = [(f"gel|{a}|{i}", dunya(a, 30, 100 * j + i)) for j, a in enumerate(("F1", "F2", "F3")) for i in (1, 2)]
        cls.ortam = G.Ortam(cls.sema, TEMEL, SABIT, H2, [(e, d, kural.Indeks(d.olgular)) for e, d in gel],
                            h2_ikiz.bijeksiyonlar(cls.sema, TEMEL), HizliKodKitabi(t3.AYAR.deger("vektor_tohum"),
                                                                                  t3.AYAR.deger("vektor_boyutu")),
                            t3.PRM, GUNLUK)
        cls.taze = [G.dunya_kaydi(f"taze|{a}|{i}", dunya(a, 30, 1000 + 100 * j + i))
                    for j, a in enumerate(("F1", "F2", "F3")) for i in (1, 2)]

    @classmethod
    def tearDownClass(cls):
        cls.so.kapat()


class GelistirmeTesti(Ortak):
    def test_yanlis_kural_aşama1de_ret(self):
        g = G.gelistirme_sayilari(YANLIS, self.ortam)
        self.assertGreater(g["yanlis"], 0)
        self.assertEqual(G.hukum(G.sembolik_olcum(YANLIS, "y", self.taze, "B1", 1, self.ortam), ESIK, SABIT),
                         (G.RET, "gelistirme_yanlis"))

    def test_dogru_kural_tanik_ve_yol_kesme(self):
        g = G.gelistirme_sayilari(DOGRU, self.ortam)
        self.assertEqual(g["yanlis"], 0)
        self.assertGreaterEqual(g["tanik"], SABIT.en_az_tanik)
        self.assertEqual(g["yolkesme_tanik"], SABIT.en_az_tanik)  # sayım eşiğe ulaşınca durur
        self.assertEqual(G.obiterler(DOGRU, g["tanik"], self.ortam), [])

    def test_yol_kesme_ters_maskesi(self):
        """Gövdesi baş çiftine dokunmayan kuralda tersler de maskelenir; ters-dayanaklıda maskelenmez."""
        ters_okuyan = k([(ZN, "Y", "X")], (B, "X", "Y"))
        self.assertTrue(ters_okuyan.ters_dayanakli)
        f = (5, B, 1)
        olg = {f, (1, ZN, 5)}
        self.assertEqual(G._maske(ters_okuyan, self.sema, olg, f), {f})
        self.assertEqual(G._maske(DOGRU, self.sema, {(5, V, 1), (1, ZN, 5)}, (5, V, 1)), {(5, V, 1)})
        dolasan = k([(B, "X", "Z"), (ZN, "Z", "W"), (B, "W", "Y")], (B, "X", "Y"))  # tersin tersiyle geri dönüş
        self.assertFalse(dolasan.ters_dayanakli)
        self.assertEqual(G._maske(dolasan, self.sema, olg, f), {f, (1, ZN, 5)})

    def test_obiter_halka(self):
        g = G.gelistirme_sayilari(FAZLA, self.ortam)
        self.assertEqual(g["yanlis"], 0)
        ob = G.obiterler(FAZLA, g["tanik"], self.ortam)
        self.assertIn(G.kural_ozu(DOGRU), ob)
        o = G.sembolik_olcum(FAZLA, "fazla", self.taze, "B1", 1, self.ortam)
        self.assertEqual(G.hukum(o, ESIK, SABIT), (G.BILMIYORUM, "obiter"))
        self.assertNotIn("taze", o)  # aşama 5'e gitmez

    def test_gerekli_farklilik_obiter_degil(self):
        """Farklılık şartı çıkarılınca X = Y bağlaması yanlış tahmin verir: şart gereklidir, obiter değildir."""
        kardes = k([(B, "X", "Z"), (ZN, "Z", "Y")], (F, "X", "Y"), [("X", "Y")])
        g = G.gelistirme_sayilari(kardes, self.ortam)
        self.assertEqual(g["yanlis"], 0)
        self.assertGreaterEqual(g["tanik"], SABIT.en_az_tanik)
        self.assertEqual(G.obiterler(kardes, g["tanik"], self.ortam), [])

    def test_farklilik_sarti_obiter(self):
        oi = k(DOGRU.halkalar, DOGRU.bas, [("X", "Y"), ("X", "Z"), ("Y", "Z")])
        self.assertIn(G.kural_ozu(DOGRU), G.obiterler(oi, G.gelistirme_sayilari(oi, self.ortam)["tanik"], self.ortam))


class BagIkiziTesti(Ortak):
    def test_simetrik_okunur_kural_ikizde_de_dogru(self):
        b = G.bag_ikizi(SIMETRIK, "s", self.ortam)
        self.assertEqual(b["yanlis"], 0)
        self.assertGreaterEqual(b["tanik"], SABIT.en_az_tanik)
        o = G.sembolik_olcum(SIMETRIK, "s", self.taze, "B1", 1, self.ortam)
        self.assertEqual(G.hukum(o, ESIK, SABIT), (G.BILMIYORUM, "bag_ikizi"))

    def test_dogru_kural_ikizde_yanlis(self):
        self.assertGreater(G.bag_ikizi(DOGRU, "d", self.ortam)["yanlis"], 0)

    def test_belirlenimci(self):
        self.assertEqual(G.bag_ikizi(DOGRU, "d", self.ortam), G.bag_ikizi(DOGRU, "d", self.ortam))


class TazeTesti(Ortak):
    def test_dogru_kural_bolumleri(self):
        t = G.taze_sembolik(DOGRU, "d", self.taze, self.ortam)
        self.assertEqual(sorted(t["aileler"]), ["F1", "F2", "F3"])
        self.assertTrue(all(v["yanlis"] == 0 and v["dogru"] >= SABIT.en_az_tanik for v in t["aileler"].values()))
        self.assertEqual((t["kanitli"], t["basarili"]), (len(t["bolumler"]), len(t["bolumler"])))
        self.assertEqual(len(t["bolumler"]), len(self.taze) * SABIT.bolum_sayisi)

    def test_tek_aile_vetosu_ve_iki_aile_reddi(self):
        t = G.taze_sembolik(TERS, "t", self.taze, self.ortam)
        self.assertEqual([a for a, v in sorted(t["aileler"].items()) if v["yanlis"]], ["F3"])
        self.assertEqual(G._taze_hukmu({"taze": t}, SABIT), (G.BILMIYORUM, "aile_vetosu"))
        t2 = G.taze_sembolik(YANLIS, "y", self.taze, self.ortam)
        self.assertEqual(len(t2["aileler"]), SABIT.ret_aile_sayisi)  # iki ailede yanlış görülünce durur
        self.assertEqual(G._taze_hukmu({"taze": t2}, SABIT), (G.RET, "taze_yanlis"))

    def test_kapsam_tek_aile(self):
        t = G.taze_sembolik(YALNIZ_F3, "f3", self.taze, self.ortam)
        self.assertEqual(G.kapsam({"taze": t}, SABIT), ["F3"])
        self.assertEqual(G._taze_hukmu({"taze": t}, SABIT), (G.BILMIYORUM, "kapsam"))

    def test_sembolik_dogru_maskeli_yeniden_turetme(self):
        b = G.bolumler(DOGRU, "d", self.taze[0], 1, self.ortam)[0]
        s = G.sembolik_bolum(DOGRU, b, self.ortam)
        vonklar = [o for o in b.olgular if o[1] == V]
        idx = kural.Indeks(b.olgular)
        beklenen = sum(DOGRU.turetir_mi(idx, a, c, haric={(a, V, c)}) for a, _, c in vonklar)
        self.assertEqual(s["dogru"], beklenen)
        self.assertGreater(s["dogru"], 0)
        self.assertEqual(s["yanlis"], 0)

    def test_sembolik_dogru_tek_adim(self):
        """ÖK-005 taslağı §13.2: tanık, gövdenin maskeli olgular çıkarılmış olgular üzerindeki eşleşmesidir (tek adım).
        Kuralın kendi türettiği ters olgu üzerinden ikinci adımda bulunan olgu sayılmaz."""
        from degerlendirme import h2_bolum
        r = k([(F, "W", "X"), (B, "W", "Z"), (B, "Y", "Z")], (F, "X", "Y"))
        self.assertFalse(r.ters_dayanakli)
        olg = ((1, B, 9), (2, B, 9), (4, B, 9), (1, F, 2), (2, F, 1), (4, F, 1))
        bolum = h2_bolum.Bolum("e", olg, {i: i for i in (1, 2, 4, 9)}, h2_bolum.bolum_ozeti(olg))
        self.assertEqual(G.sembolik_bolum(r, bolum, self.ortam)["dogru"], 1)  # yalnız (1, F, 2); kapanışla 3 olurdu

    def test_gelistirme_wilson_ayni_bicim(self):
        secilen = G.gelistirme_dunyalari(self.ortam)
        self.assertEqual([s[1] for s in secilen], ["F1", "F1", "F2", "F2", "F3", "F3"])
        w = G.gelistirme_wilson(DOGRU, "d", self.ortam)
        self.assertEqual(w["kanitli"], len(secilen) * SABIT.bolum_sayisi)


class ThresholdoutTesti(unittest.TestCase):
    def test_kural(self):
        e = G.Esikler(0.85, 0.9, 0.04, 0.01)
        self.assertEqual(G.thresholdout(0.90, 0.89, [0.0, 0.0], e), 0.90)  # fark ≤ T → T_gel
        self.assertAlmostEqual(G.thresholdout(0.95, 0.80, [0.0, 1.0], e), 0.81)  # fark > T → T_taze + η₂ (σ·1)
        self.assertEqual(G.thresholdout(0.90, 0.85, [1.0, 1.0], e), 0.90)  # η₁ = 2σ·1: 0.05 ≤ 0.04 + 0.02

    def test_gurultu_tohumlu(self):
        o = G.Ortam(None, (), SABIT, H2, [])
        self.assertEqual(G.gurultu("a", "B1", 1, o), G.gurultu("a", "B1", 1, o))
        self.assertNotEqual(G.gurultu("a", "B1", 1, o), G.gurultu("a", "B1", 2, o))


class WestfallYoungTesti(Ortak):
    def test_dogru_kural_null_ustunde(self):
        olcum = {"taze": G.taze_sembolik(DOGRU, "d", self.taze, self.ortam)}
        aile = G.wy_ailesi([("d", DOGRU, olcum)])
        T = G.wy_gozlenen(aile, self.taze, SABIT.wilson_z)
        self.assertGreater(T["d"], 0.5)
        maks = G.wy_maksimumlar(aile, self.taze, "B1", 1, self.ortam, range(1, SABIT.wy_cekilis + 1))
        self.assertEqual(len(maks), SABIT.wy_cekilis)
        self.assertLess(max(maks), T["d"])
        self.assertEqual(G.wy_p(T, maks, SABIT.wy_cekilis), {"d": 1 / (SABIT.wy_cekilis + 1)})
        self.assertEqual(maks, G.wy_maksimumlar(aile, self.taze, "B1", 1, self.ortam, range(1, SABIT.wy_cekilis + 1)))

    def test_p_formulu(self):
        self.assertEqual(G.wy_p({"a": 0.5, "b": 0.9}, [0.1, 0.6, 0.95, 0.2], 4), {"a": 3 / 5, "b": 2 / 5})


def olcum(**ek):
    o = {"gelistirme": {"tanik": 10, "yanlis": 0, "yolkesme_tanik": 3}, "obiter": [],
         "bag_ikizi": {"tanik": 5, "yanlis": 2},
         "taze": {"aileler": {a: {"dogru": 5, "yanlis": 0, "bolum": 16} for a in ("A1", "A2")}, "wilson": 0.9},
         "gel_wilson": {"wilson": 0.9}, "gurultu": [0.0, 0.0], "wy_p": 0.0001,
         "cekirdek": {"uyum": True, "bolumler": [{"mudahale": [1.0, 1.0]}, {"mudahale": [1.0]}],
                      "pi": {"sayilar_ayni": True, "mudahale_orijinal": [1.0], "mudahale_ikiz": [1.0]}}}
    for yol, deger in ek.items():
        hedef = o
        parca = yol.split("__")
        for p in parca[:-1]:
            hedef = hedef[p]
        hedef[parca[-1]] = deger
    return o


class HukumSirasiTesti(unittest.TestCase):
    E = G.Esikler(0.85, 0.9, 0.04, 0.01)

    def h(self, **ek):
        return G.hukum(olcum(**ek), self.E, SABIT)

    def test_sira(self):
        self.assertEqual(self.h(), (G.KABUL, "A1,A2"))
        self.assertEqual(self.h(gelistirme__yanlis=1, obiter=[{}]), (G.RET, "gelistirme_yanlis"))
        self.assertEqual(self.h(obiter=[{}], gelistirme__yolkesme_tanik=0), (G.BILMIYORUM, "obiter"))
        self.assertEqual(self.h(gelistirme__yolkesme_tanik=2), (G.BILMIYORUM, "yol_kesme"))
        self.assertEqual(self.h(bag_ikizi__yanlis=0), (G.BILMIYORUM, "bag_ikizi"))
        self.assertEqual(self.h(bag_ikizi__yanlis=0, bag_ikizi__tanik=2), (G.KABUL, "A1,A2"))
        iki = {"A1": {"dogru": 5, "yanlis": 1}, "A2": {"dogru": 5, "yanlis": 1}}
        self.assertEqual(self.h(taze__aileler=iki), (G.RET, "taze_yanlis"))
        bir = {"A1": {"dogru": 5, "yanlis": 1}, "A2": {"dogru": 5, "yanlis": 0}, "A3": {"dogru": 5, "yanlis": 0}}
        self.assertEqual(self.h(taze__aileler=bir), (G.BILMIYORUM, "aile_vetosu"))
        az = {"A1": {"dogru": 5, "yanlis": 0}, "A2": {"dogru": 2, "yanlis": 0}}
        self.assertEqual(self.h(taze__aileler=az), (G.BILMIYORUM, "kapsam"))
        self.assertEqual(self.h(taze__wilson=0.84, gel_wilson__wilson=0.84), (G.BILMIYORUM, "wilson"))
        self.assertEqual(self.h(taze__wilson=0.80, gel_wilson__wilson=0.95), (G.BILMIYORUM, "wilson"))
        self.assertEqual(self.h(taze__wilson=0.87, gel_wilson__wilson=0.84), (G.BILMIYORUM, "wilson"))  # |fark| ≤ T → T_gel
        self.assertEqual(self.h(wy_p=SABIT.alfa * 1.01), (G.BILMIYORUM, "null"))
        self.assertEqual(self.h(wy_p=None), (G.BILMIYORUM, "null"))
        self.assertEqual(self.h(cekirdek=None), (G.BILMIYORUM, "cekirdek_olculmedi"))
        self.assertEqual(self.h(cekirdek__uyum=False), (G.BILMIYORUM, "uyum"))
        self.assertEqual(self.h(cekirdek__bolumler=[{"mudahale": [1.0, 1.0]}]), (G.BILMIYORUM, "mudahale_kaniti"))
        self.assertEqual(self.h(cekirdek__bolumler=[{"mudahale": [1.0, 0.8, 0.8]}]), (G.RET, "kisayol"))
        self.assertEqual(self.h(cekirdek__pi__sayilar_ayni=False), (G.BILMIYORUM, "pi_ikizi"))
        self.assertEqual(self.h(cekirdek__pi__mudahale_ikiz=[0.5]), (G.BILMIYORUM, "pi_ikizi"))
        self.assertEqual(self.h(cekirdek__pi__mudahale_ikiz=[], cekirdek__pi__mudahale_orijinal=[]), (G.KABUL, "A1,A2"))

    def test_esiksiz_hukum_k_degerlerine_bagli_degil(self):
        o = olcum(taze__wilson=0.1, wy_p=1.0, cekirdek=None)
        self.assertIsNone(G.esiksiz_hukum(o, SABIT))
        self.assertEqual(G.sembolik_hukum(o, self.E, SABIT), (G.BILMIYORUM, "wilson"))

    def test_alfa(self):
        self.assertAlmostEqual(SABIT.alfa, 0.01 / 12)

    def test_ayardan_onkayit_degerleri(self):
        """ÖK-005 taslağı §4 madde 4, 5, 7, 9, 13, 14; §2.1 (bölüm); §8 (8 tur)."""
        s = G.Sabitler.ayardan(H2)
        self.assertEqual((s.en_az_tanik, s.kapsam_en_az_aile, s.ret_aile_sayisi, s.wilson_z, s.wy_cekilis), (3, 2, 2, 1.96, 10000))
        self.assertAlmostEqual(s.alfa, 0.01 / 12)
        self.assertEqual((s.bolum_sayisi, s.taze_aile_basina, s.adim_araligi, s.dikkat_sayisi, s.kapanis_tur_siniri),
                         (8, 2, (2, 3), 4, 8))
        self.assertEqual((s.bagla_deneme_carpani, s.halka_esigi, s.guvenilirlik), (10, 0.5, 1.0))
        self.assertEqual(G.Esikler.sozlukten(H2.deger("esik_baslangic")), G.Esikler(0.85, 0.9, 0.04, 0.01))


class IkizTesti(Ortak):
    def test_bijeksiyonlar(self):
        b = h2_ikiz.bijeksiyonlar(self.sema, TEMEL)
        self.assertEqual(len(b), 2)  # kimlik ve iki tersin takası
        self.assertEqual(b[0], {r: r for r in self.sema.adlar})
        self.assertEqual(b[1][ZN], Q)
        self.assertEqual(len(h2_ikiz.bijeksiyonlar(self.sema, (B, ZN))), 1)  # temel olma korunur

    def test_gercek_semada_1536(self):
        from degerlendirme import h1
        from degerlendirme.dunya import tanimlar_yukle
        _, sema, _ = h1._ortam(KOK)
        tanim = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                               KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
        b = h2_ikiz.bijeksiyonlar(sema, tanim.olgu_iliskileri)
        self.assertEqual(len(b), 1536)  # ÖK-005 taslağı §13.4
        for pi in b[:50]:
            for r in sema.adlar:
                self.assertEqual({pi[t] for t in sema.ters(r)}, set(sema.ters(pi[r])))

    def test_ikiz_dunyada_ikiz_kural_ayni_sayilar(self):
        pi = h2_ikiz.bijeksiyonlar(self.sema, TEMEL)[1]
        d = self.taze[4][2]  # F3: iki ters de var
        ters_okuyan = k([(B, "X", "Y")], (Q, "Y", "X"))
        idx, idx_pi = kural.Indeks(d.olgular), kural.Indeks(h2_ikiz.dunyaya(pi, d.olgular))
        k_pi = h2_ikiz.kurala(pi, ters_okuyan)
        self.assertEqual(k_pi.bas[0], ZN)
        self.assertEqual(ters_okuyan.tahminler(idx), k_pi.tahminler(idx_pi))


class CekirdekTesti(Ortak):
    """Çekirdek adımı (yavaş): bellek boş, taze bölümlerde sembolik sayımla uyum, müdahale ve π-ikizi."""

    def test_dogru_kural_uyum_ve_kabul(self):
        ortam = dataclasses.replace(self.ortam, gelistirme=self.ortam.gelistirme[:1])
        taze = self.taze[:1]
        c = G.cekirdek_olcum(DOGRU, "d", taze, ortam)
        self.assertTrue(c["uyum"], c["bolumler"])
        self.assertEqual(len(c["bolumler"]), SABIT.bolum_sayisi)
        for b in c["bolumler"]:
            self.assertEqual([b["dogru"], b["yanlis"]], b["sembolik"])
            self.assertTrue(all(m >= 0.9 for m in b["mudahale"]))
        self.assertEqual(c["pi"]["bolum"], 1)
        self.assertTrue(c["pi"]["sayilar_ayni"])
        o = olcum(cekirdek=c)
        self.assertEqual(G.hukum(o, G.Esikler(0.85, 0.9, 0.04, 0.01),
                                 dataclasses.replace(SABIT, mudahale_en_az_kanit=1))[0], G.KABUL)

    def test_havuza_sigmayan_bolum_olculemez(self):
        ortam = dataclasses.replace(self.ortam, prm=dataclasses.replace(t3.PRM, kapasite=8))
        c = G.cekirdek_olcum(DOGRU, "d", self.taze[:1], ortam)
        self.assertFalse(c["uyum"])
        self.assertTrue(c["bolumler"][0]["havuz_asimi"])
        self.assertEqual(G.hukum(olcum(cekirdek=c), ESIK, SABIT), (G.BILMIYORUM, "uyum"))

    def test_yanlis_tahmin_cekirdekte_de_yanlis(self):
        b = G.bolumler(YANLIS, "y", self.taze[0], 1, self.ortam)[0]
        c = G.cekirdek_bolum(G.hucre(YANLIS, "y", SABIT), False, b.olgular, self.ortam)
        s = G.sembolik_bolum(YANLIS, b, self.ortam)
        self.assertGreater(s["yanlis"], 0)
        self.assertEqual((c["dogru"], c["yanlis"]), (s["dogru"], s["yanlis"]))


if __name__ == "__main__":
    unittest.main()
