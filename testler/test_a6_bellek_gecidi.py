"""V-054: bellek geçidi. Bozuk aday kurallar (yanlış, kısayol, gereksiz, çelişkili) reddedilir, doğru kurallar kabul
edilir; gözlemle denetlenemeyen kural "sınanamadı" kalır. Etiket yok: bölümlerde yalnız olgular ve sorgu var.

Sentetik dünya (blorp şeması, ilişki adları anlamsız). Doğru kurallar:
  T1: blorp(X,Y) ∧ blorp(Y,Z) → quax(X,Z);  T2: quax(X,Y) ∧ blorp(Y,Z) → vonk(X,Z);  T3: frumb(X,Y) → frumb(Y,X).
Her bölüm: a→b→c→d→e blorp zinciri, gözlenen quax(a,c) ve vonk(a,d); iki yönlü frumb(g,h), tek yönlü frumb(i,j);
p→q→r zindle zinciri. Olağan ortamda (p,r) için vonk, kaydırılmış ortamda frumb gözlenir: zindle∘zindle → vonk kuralı
birincide tutar, ikincide tutmaz (kısayol). Sorgular sırayla (b,d), (b,e), (j,i): cevapları gözlenmez.
"""
import dataclasses

from cekirdek.bellek_gecidi import (CELISKILI, GEREKSIZ, KABUL, KISAYOL, RET, SINANAMADI, YANLIS, GecitEsikleri,
                                    gecit, kanonik_bicim)
from cekirdek.vektor_hizli import HizliKodKitabi
from testler.test_a3_temel import halka, hucre
from testler.test_a5_h1 import GUNLUK
import testler.test_a3_cekirdek as t3

KK = HizliKodKitabi(t3.AYAR.deger("vektor_tohum"), t3.AYAR.deger("vektor_boyutu"))
ESIK = GecitEsikleri.ayardan(t3.AYAR)
T1 = hucre("t_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
T2 = hucre("t_qb", [halka("quax", "X", "Y"), halka("blorp", "Y", "Z")], ("vonk", "X", "Z"))
T3 = hucre("t_ff", [halka("frumb", "X", "Y")], ("frumb", "Y", "X"))
YANLIS_SONUC = hucre("y_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("vonk", "X", "Z"))
YANLIS_SEMA = hucre("y_bz", [halka("blorp", "X", "Y")], ("zindle", "X", "Y"))
KISAYOL_ZZ = hucre("k_zz", [halka("zindle", "X", "Y"), halka("zindle", "Y", "Z")], ("vonk", "X", "Z"))
ESDEGER = hucre("g_bb", [halka("blorp", "B", "C"), halka("blorp", "A", "B")], ("quax", "A", "C"))
KATKISIZ = hucre("g_bbb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z"), halka("blorp", "Z", "W")],
                 ("quax", "X", "Z"))
CELISKILI_BB = hucre("c_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("frumb", "X", "Z"))
GOZLEMSIZ = hucre("s_vb", [halka("vonk", "X", "Y"), halka("blorp", "Y", "Z")], ("vonk", "X", "Z"))
BOLUM_SAYISI = 6  # V-054: ortam başına bölüm (sorgu türü başına 2)


def bolum(olgular, sorgu):
    return {"olgular": [{"ozne": s, "iliski": r, "nesne": o, "guven": 1.0} for s, r, o in olgular],
            "sorgu": {"ozne": sorgu[0], "nesne": sorgu[1]}}


def ortam(kaydirilmis=False, gozlem=True):
    bolumler = []
    for n in range(BOLUM_SAYISI):
        a, b, c, d, e, g, h, i, j, p, q, r = range(20 * n, 20 * n + 12)
        olgular = [(a, "blorp", b), (b, "blorp", c), (c, "blorp", d), (d, "blorp", e), (g, "frumb", h),
                   (h, "frumb", g), (i, "frumb", j), (p, "zindle", q), (q, "zindle", r),
                   (p, "frumb" if kaydirilmis else "vonk", r)]
        if gozlem:
            olgular += [(a, "quax", c), (a, "vonk", d)]
        bolumler.append(bolum(olgular, [(b, d), (b, e), (j, i)][n % 3]))
    return bolumler


ORTAMLAR = {"olagan": ortam(), "kaydirilmis": ortam(kaydirilmis=True)}


class Ortam(t3.Ortam):
    def gec(self, aday, bellek=(), ortamlar=ORTAMLAR, **ayar):
        hucreler = self.hucreler(*bellek, aday)
        return gecit(hucreler[-1], hucreler[:-1], ortamlar, self.sema, KK, t3.PRM, GUNLUK, ESIK, **ayar)


class DogruKabulTesti(Ortam):
    def test_dogru_kurallar_sirayla_kabul(self):
        bellek = []
        for aday in (T1, T2, T3):
            with self.subTest(aday=aday["kimlik"]):
                k = self.gec(aday, bellek)
                self.assertEqual((k.karar, k.neden), (KABUL, None), k.olcumler)
                for o in k.olcumler.values():
                    self.assertEqual(o["dogruluk"], 1.0)
                    self.assertGreaterEqual(o["destek"], ESIK.en_az_kanit)
            bellek.append(aday)

    def test_karar_belirlenimli(self):
        self.assertEqual(self.gec(T1), self.gec(T1))

    def test_cevap_alani_okunmaz(self):
        """Bölüme konan sahte bir cevap alanı kararı değiştirmez: geçit etiket görmez."""
        sahte = {ad: [dict(b, cevap="vonk") for b in liste] for ad, liste in ORTAMLAR.items()}
        self.assertEqual(self.gec(T1, ortamlar=sahte), self.gec(T1))


class BozukRetTesti(Ortam):
    def test_yanlis_sonuc(self):
        for aday in (YANLIS_SONUC, YANLIS_SEMA):
            with self.subTest(aday=aday["kimlik"]):
                k = self.gec(aday)
                self.assertEqual((k.karar, k.neden), (RET, YANLIS), k.olcumler)
                self.assertTrue(all(o["dogruluk"] == 0.0 for o in k.olcumler.values()))

    def test_kisayol_en_kotu_ortamda_yakalanir(self):
        k = self.gec(KISAYOL_ZZ)
        self.assertEqual((k.karar, k.neden), (RET, KISAYOL), k.olcumler)
        self.assertEqual((k.olcumler["olagan"]["dogruluk"], k.olcumler["kaydirilmis"]["dogruluk"]), (1.0, 0.0))
        # tek ortamla sınansaydı kısayol görünmezdi: kaydırılmış doğrulama zorunlu (EK A P7)
        tek = self.gec(KISAYOL_ZZ, ortamlar={"olagan": ORTAMLAR["olagan"]})
        self.assertNotEqual(tek.neden, KISAYOL)

    def test_yapica_esdeger_gereksiz(self):
        self.assertEqual(kanonik_bicim(self.hucreler(ESDEGER)[0]), kanonik_bicim(self.hucreler(T1)[0]))
        k = self.gec(ESDEGER, [T1])
        self.assertEqual((k.karar, k.neden, k.olcumler), (RET, GEREKSIZ, {"esdeger": True}))

    def test_katkisiz_gereksiz(self):
        k = self.gec(KATKISIZ, [T1])
        self.assertEqual((k.karar, k.neden), (RET, GEREKSIZ), k.olcumler)
        self.assertEqual(sum(o["katki"] for o in k.olcumler.values()), 0)
        self.assertEqual(self.gec(KATKISIZ).karar, KABUL)  # bellek boşken aynı kural katkı yapar

    def test_bellekle_celiskili(self):
        gozlemsiz = {"gozlemsiz": ortam(gozlem=False)}
        k = self.gec(CELISKILI_BB, [T1], ortamlar=gozlemsiz)
        self.assertEqual((k.karar, k.neden), (RET, CELISKILI), k.olcumler)
        self.assertGreater(k.olcumler["gozlemsiz"]["celiski"], 0)


class SinanamadiTesti(Ortam):
    def test_gozlenmeyen_sonuc_sinanamadi(self):
        k = self.gec(GOZLEMSIZ, [T1, T2])
        self.assertEqual((k.karar, k.neden), (SINANAMADI, None), k.olcumler)
        self.assertTrue(all(o["dogruluk"] is None for o in k.olcumler.values()))

    def test_dis_skor_kanali_kapali(self):
        with self.assertRaises(NotImplementedError):
            self.gec(T1, dis_kanit={"olagan": 1.0})

    def test_mudahale_kaniti_yetmezse_sinanamadi(self):
        sorgusuz = {ad: [dict(b, sorgu=None) for b in liste] for ad, liste in ORTAMLAR.items()}
        self.assertEqual(self.gec(T1, ortamlar=sorgusuz).karar, SINANAMADI)

    def test_esik_gevsetilirse_kisayol_gecer(self):
        """Eşik geçidin parçasıdır: en kötü ortam doğruluğu eşiği 0 olsaydı kısayol kabul edilirdi."""
        gevsek = dataclasses.replace(ESIK, dogruluk=0.0)
        hucreler = self.hucreler(KISAYOL_ZZ)
        k = gecit(hucreler[0], (), ORTAMLAR, self.sema, KK, t3.PRM, GUNLUK, gevsek)
        self.assertNotEqual(k.neden, KISAYOL)
