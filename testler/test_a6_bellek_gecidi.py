"""V-054, K-035: bellek geçidi. Bozuk aday kurallar (yanlış, kısayol, gereksiz, çelişkili) reddedilir, doğru kurallar kabul
edilir; gözlemle denetlenemeyen kural "sınanamadı" kalır. Etiket ve sorgu yok: bölümlerde yalnız gözlemler (olgular) var.
Kuralın tahmin ettiği gözlem maskelenir; doğruluk çekirdek dışında (`degerlendirme/gozlem_puani.py`) hesaplanır.

Sentetik dünya (blorp şeması, ilişki adları anlamsız). Doğru kurallar:
  T1: blorp(X,Y) ∧ blorp(Y,Z) → quax(X,Z);  T2: quax(X,Y) ∧ blorp(Y,Z) → vonk(X,Z);  T3: frumb(X,Y) → frumb(Y,X).
Her bölüm: a→b→c→d→e blorp zinciri, gözlenen quax(a,c) ve vonk(b,e); iki yönlü frumb(g,h), tek yönlü frumb(i,j);
p→q→r zindle zinciri. Olağan ortamda (p,r) için vonk, kaydırılmış ortamda frumb gözlenir: zindle∘zindle → vonk kuralı
birincide tutar, ikincide tutmaz (kısayol). vonk(b,e)'nin ara adımı quax(b,d) gözlenmez: cevap tek yoldan gelir.
Ara adımı da gözlenen bir sonuçta cevap iki yoldan gelir; bunun müdahale puanına etkisi `ArtiklikTesti`'nde (V-058).
"""
import dataclasses
import unittest
from unittest import mock

from cekirdek.bellek_gecidi import (CELISKILI, GEREKSIZ, KABUL, KISAYOL, RET, SINANAMADI, YANLIS, GecitEsikleri,
                                    kanonik_bicim, karar_ver, maskeli_kos)
from cekirdek.havuz import Havuz
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import gozlem_puani
from degerlendirme.bellek_hatti import degerlendir
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
BOLUM_SAYISI = 6  # V-054: ortam başına bölüm


def bolum(olgular):
    return {"olgular": [{"ozne": s, "iliski": r, "nesne": o, "guven": 1.0} for s, r, o in olgular]}


def ortam(kaydirilmis=False, gozlem=True):
    bolumler = []
    for n in range(BOLUM_SAYISI):
        a, b, c, d, e, g, h, i, j, p, q, r = range(20 * n, 20 * n + 12)
        olgular = [(a, "blorp", b), (b, "blorp", c), (c, "blorp", d), (d, "blorp", e), (g, "frumb", h),
                   (h, "frumb", g), (i, "frumb", j), (p, "zindle", q), (q, "zindle", r),
                   (p, "frumb" if kaydirilmis else "vonk", r)]
        if gozlem:
            olgular += [(a, "quax", c), (b, "vonk", e)]
        bolumler.append(bolum(olgular))
    return bolumler


ORTAMLAR = {"olagan": ortam(), "kaydirilmis": ortam(kaydirilmis=True)}


class Ortam(t3.Ortam):
    def gec(self, aday, bellek=(), ortamlar=ORTAMLAR, esikler=ESIK):
        hucreler = self.hucreler(*bellek, aday)
        return degerlendir(hucreler[-1], hucreler[:-1], ortamlar, self.sema, KK, t3.PRM, GUNLUK, esikler)

    def olc(self, aday, bellek, b):
        hucreler = self.hucreler(*bellek, aday)
        return gozlem_puani.bolum_olcumu(hucreler[-1], hucreler[:-1], b, self.sema, KK, t3.PRM, GUNLUK)


class DogruKabulTesti(Ortam):
    def test_dogru_kurallar_sirayla_kabul(self):
        bellek = []
        for aday in (T1, T2, T3):
            with self.subTest(aday=aday["kimlik"]):
                k = self.gec(aday, bellek)
                self.assertEqual((k.karar, k.neden), (KABUL, None), k.olcumler)
                for o in k.olcumler.values():
                    self.assertEqual(o["dogruluk"], 1.0)
                    self.assertGreaterEqual(o["kanit"], ESIK.en_az_kanit)
            bellek.append(aday)

    def test_karar_belirlenimli(self):
        self.assertEqual(self.gec(T1), self.gec(T1))

    def test_sorgu_ve_cevap_alani_okunmaz(self):
        """Bölüme konan sahte sorgu ve cevap alanı kararı değiştirmez: geçit etiket görmez."""
        sahte = {ad: [dict(b, sorgu={"ozne": 0, "nesne": 2}, cevap="vonk") for b in liste]
                 for ad, liste in ORTAMLAR.items()}
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

    def test_bellekle_ayni_turda_uretilen_katki_degil(self):
        """Soy bir üçlüyü yeni dayanakla yazsa da bellek onu aynı turda zaten üretiyorsa katkı sayılmaz."""
        z_q = hucre("z_q", [halka("zindle", "X", "Y")], ("quax", "X", "Y"))
        b = bolum([(1, "blorp", 2), (2, "blorp", 3), (1, "zindle", 3)])
        hucreler = self.hucreler(T1, z_q)
        ham = maskeli_kos(hucreler[1], hucreler[:1], gozlem_puani.bolum_olgulari(b), None, self.sema, KK, t3.PRM,
                          GUNLUK)
        self.assertEqual((ham["tahminler"], ham["katki"]), ([[1, "quax", 3]], 0))
        self.assertEqual(self.olc(z_q, [], b)["katki"], 1)

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

    def test_hic_eslesmeyen_aday_sinanamadi(self):
        """Verideki hiçbir bölümde gövdesi eşleşmeyen kural için kanıt yoktur: gereksiz değil, sınanamadı."""
        hic = hucre("s_vv", [halka("vonk", "X", "Y"), halka("vonk", "Y", "Z")], ("quax", "X", "Z"))
        k = self.gec(hic)
        self.assertEqual((k.karar, k.neden), (SINANAMADI, None), k.olcumler)
        self.assertEqual(sum(o["eslesme"] for o in k.olcumler.values()), 0)

    def test_az_bolumle_sinanamadi(self):
        """Kanıt `en_az_kanit`'ten azsa doğruluk ölçülmüş sayılmaz."""
        az = {ad: liste[:ESIK.en_az_kanit - 1] for ad, liste in ORTAMLAR.items()}
        k = self.gec(T1, ortamlar=az)
        self.assertEqual((k.karar, k.neden), (SINANAMADI, None), k.olcumler)

    def test_esik_gevsetilirse_kisayol_gecer(self):
        """Eşik geçidin parçasıdır: en kötü ortam doğruluğu eşiği 0 olsaydı kısayol kabul edilirdi."""
        k = self.gec(KISAYOL_ZZ, esikler=dataclasses.replace(ESIK, dogruluk=0.0))
        self.assertNotEqual(k.neden, KISAYOL)


class MaskeTesti(Ortam):
    def test_maskelenen_gozlem_cekirdege_verilmez(self):
        """Maskelenen gözlem havuza hiç eklenmez; kural onu kendi kendine onaylayamaz (K-035)."""
        aday = self.hucreler(T1)[0]
        olgular = gozlem_puani.bolum_olgulari(ORTAMLAR["olagan"][0])
        maske = [i for i, o in enumerate(olgular) if o[1] == "quax"][0]
        eklenen, asil = [], Havuz.epitop_ekle

        def kaydet(havuz, s, r, o, guven):
            eklenen.append((s, r, o))
            return asil(havuz, s, r, o, guven=guven)
        with mock.patch.object(Havuz, "epitop_ekle", kaydet):
            ham = maskeli_kos(aday, (), olgular, maske, self.sema, KK, t3.PRM, GUNLUK)
        self.assertNotIn(olgular[maske][:3], eklenen)
        self.assertLessEqual({o[:3] for i, o in enumerate(olgular) if i != maske}, set(eklenen))
        self.assertIn(list(olgular[maske][:3]), ham["tahminler"])  # yeniden türetildi: tahmin

    def test_maskesiz_tahmin_dogru_sayilmaz(self):
        """Görünen bir gözlemi yeniden türetmek (kendini onaylama) doğru sayılmaz: maske olmadan doğru = 0."""
        aday = self.hucreler(T1)[0]
        b = ORTAMLAR["olagan"][0]
        gorunur = maskeli_kos(aday, (), gozlem_puani.bolum_olgulari(b), None, self.sema, KK, t3.PRM, GUNLUK)
        self.assertIn([0, "quax", 2], gorunur["tahminler"])
        self.assertEqual(self.olc(T1, [], b)["dogru"], 1)
        with mock.patch.object(gozlem_puani, "maskelenecekler", return_value=[]):
            self.assertEqual(self.olc(T1, [], b)["dogru"], 0)

    def test_yalniz_sonuc_iliskisindeki_gozlemler_maskelenir(self):
        aday = self.hucreler(T2)[0]
        olgular = gozlem_puani.bolum_olgulari(ORTAMLAR["olagan"][0])
        self.assertEqual([olgular[i][1] for i in gozlem_puani.maskelenecekler(aday, olgular)], ["vonk", "vonk"])

    def test_tek_yonlu_gozlem_kanit_degil(self):
        """Tek yönlü gözlenen frumb(1,2): maskelenince bakışım kuralının dayanağı kalmaz; kanıt yok, sınanamadı."""
        tek_yon = {"tek_yon": [bolum([(1, "frumb", 2), (5, "blorp", 6)]) for _ in range(BOLUM_SAYISI)]}
        k = self.gec(T3, ortamlar=tek_yon)
        self.assertEqual((k.olcumler["tek_yon"]["kanit"], k.karar), (0, SINANAMADI))

    def test_ayni_celiski_bolumde_bir_kez_sayilir(self):
        """Her maske koşusunda yeniden görünen aynı (tahmin, gözlem) çelişkisi bir kez sayılır."""
        b = bolum([(1, "blorp", 2), (2, "blorp", 3), (1, "quax", 3), (7, "vonk", 8), (9, "vonk", 4)])
        self.assertEqual(self.olc(YANLIS_SONUC, [], b)["yanlis"], 1)

    def test_soydan_tureyen_celiski_sayilir(self):
        """Adayın çıktısından bellekteki kuralla türeyen kayıt da adayın tahminidir."""
        b = bolum([(1, "blorp", 2), (2, "blorp", 3), (3, "blorp", 4), (4, "blorp", 5), (2, "frumb", 5)])
        self.assertEqual(self.olc(T1, [T2], b)["yanlis"], 1)
        self.assertEqual(self.olc(T1, [], b)["yanlis"], 0)


class AyrintiTesti(Ortam):
    def test_mudahale_esigi_uygulanir(self):
        """Müdahale ortalaması eşiğin altındaysa aday geçemez (eşik, ulaşılabilecek en yüksek puanın üstüne çekildi)."""
        k = self.gec(T1, esikler=dataclasses.replace(ESIK, mudahale=1.5))
        self.assertEqual((k.karar, k.neden), (RET, KISAYOL), k.olcumler)
        self.assertTrue(all(o["dogruluk"] == 1.0 and o["mudahale"] for o in k.olcumler.values()))

    def test_bellekteki_kimlikle_aday_reddedilir(self):
        ayni_ad = dict(T2, kimlik=T1["kimlik"])
        hucreler = self.hucreler(T1) + self.hucreler(ayni_ad)
        with self.assertRaises(ValueError):
            degerlendir(hucreler[1], hucreler[:1], ORTAMLAR, self.sema, KK, t3.PRM, GUNLUK, ESIK)

    def test_ortamsiz_degerlendirme_reddedilir(self):
        with self.assertRaises(ValueError):
            self.gec(T1, ortamlar={})


class ArtiklikTesti(Ortam):
    """V-058 (açık): ara adımı (quax(a,c)) hem gözlenen hem bellekten türetilebilen vonk(a,d) maskelenince cevabın iki
    ispatı olur; bir kökü silmek güveni düşürmez, müdahale (a) bileşeni 1'in altına iner ve doğru T2 kısayol sayılır.
    Bu test bugünkü davranışı sabitler; kullanıcı kararıyla değişecek."""

    def test_artik_gozlemde_dogru_kural_kisayol_sayiliyor(self):
        artik = {ad: [dict(b, olgular=b["olgular"] + bolum([(20 * n, "vonk", 20 * n + 3)])["olgular"])
                      for n, b in enumerate(liste)] for ad, liste in ORTAMLAR.items()}
        k = self.gec(T2, [T1], ortamlar=artik)
        self.assertEqual((k.karar, k.neden), (RET, KISAYOL), k.olcumler)
        for o in k.olcumler.values():
            self.assertEqual(o["dogruluk"], 1.0)
            self.assertLess(min(o["mudahale"]), ESIK.mudahale)
            self.assertEqual(set(o["mudahale_bc"]), {1.0})  # düşük olan yalnız (a) bileşeni


def olcum(**ortamlar):
    """Kısa yazım: ortam → (kanıt, doğruluk, çelişki, katkı, eşleşme, müdahale puanları)."""
    alanlar = ("kanit", "dogruluk", "celiski", "katki", "eslesme", "mudahale")
    return {ad: dict(zip(alanlar, d)) for ad, d in ortamlar.items()}


class KararTesti(unittest.TestCase):
    """`karar_ver` yalnız eşikleri uygular; sayılar dışarıda hesaplanır (K-035)."""
    TAM = (6, 1.0, 0, 2, 6, [1.0, 1.0, 1.0])

    def karar(self, esdeger=False, esikler=ESIK, **ortamlar):
        k = karar_ver(esdeger, olcum(**ortamlar), esikler)
        return k.karar, k.neden

    def test_sira(self):
        self.assertEqual(self.karar(True, a=self.TAM), (RET, GEREKSIZ))
        self.assertEqual(self.karar(a=self.TAM, b=self.TAM), (KABUL, None))
        self.assertEqual(self.karar(a=(6, 0.5, 0, 2, 6, [1.0] * 3), b=(6, 0.0, 0, 2, 6, [])), (RET, YANLIS))
        self.assertEqual(self.karar(a=self.TAM, b=(6, 0.5, 0, 2, 6, [1.0] * 3)), (RET, KISAYOL))
        self.assertEqual(self.karar(a=(6, 1.0, 1, 2, 6, [1.0] * 3)), (RET, CELISKILI))
        self.assertEqual(self.karar(a=(0, None, 0, 0, 0, [])), (SINANAMADI, None))
        self.assertEqual(self.karar(a=(6, 1.0, 0, 0, 6, [1.0] * 3)), (RET, GEREKSIZ))
        self.assertEqual(self.karar(a=self.TAM, b=(0, None, 0, 2, 6, [])), (SINANAMADI, None))
        self.assertEqual(self.karar(a=(6, 1.0, 0, 2, 6, [1.0, 1.0])), (SINANAMADI, None))
        self.assertEqual(self.karar(a=(6, 1.0, 0, 2, 6, [0.5, 1.0, 1.0])), (RET, KISAYOL))

    def test_az_kanitli_dogruluk_olculmus_sayilmaz(self):
        az = (ESIK.en_az_kanit - 1, 0.0, 0, 2, 6, [1.0] * 3)
        self.assertEqual(self.karar(a=self.TAM, b=az), (SINANAMADI, None))
        self.assertEqual(self.karar(a=(ESIK.en_az_kanit, 0.0, 0, 2, 6, [])), (RET, YANLIS))

    def test_esikler_sinirda(self):
        self.assertEqual(self.karar(a=(6, 1.0, 0, 2, 6, [0.9, 0.9, 0.9]),
                                    esikler=dataclasses.replace(ESIK, mudahale=0.9)), (KABUL, None))
        self.assertEqual(self.karar(a=(6, 0.75, 0, 2, 6, [1.0] * 3),
                                    esikler=dataclasses.replace(ESIK, dogruluk=0.75)), (KABUL, None))


if __name__ == "__main__":
    unittest.main()
