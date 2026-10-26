"""K-041, K-043 (ÖK-005 taslağı §4 madde 15–18, 21; §8), V-065: B2 ölçümü. Sentetik blorp dünyaları "final" yerine;
hedef kurallar elle seçilir (DNA kullanılmaz). Sınıf öncelikleri, kabul sınıfları, bilmiyorum ölçüsü, kapı kararı
(geçti / ara bölge / dur) ve makas."""
import unittest

from degerlendirme import h2_olcum as O, kural
from kesif import aday
from testler import test_b1_gecit as tg
from testler.test_b1_kirmizi import KucukAyar
from testler.test_b1_tur import ZINDLE_YOLU, kayit

DOGRU_OI = tg.k(tg.DOGRU.halkalar, tg.DOGRU.bas, [("X", "Y"), ("X", "Z"), ("Y", "Z")])
ORNEKSIZ = tg.k([(tg.Q, "X", "Y"), (tg.ZN, "X", "Y")], (tg.B, "Y", "X"))


class Ortak(tg.Ortak):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.final = [(a, idx) for _, a, _, idx in cls.taze]


class KanonikTesti(Ortak):
    def test_aday_kimligiyle_ayni(self):
        for k in (tg.DOGRU, DOGRU_OI, tg.TERS, ZINDLE_YOLU):
            self.assertEqual("k" + O.kanonik(k), kayit(k)["kimlik"])
        oi = kayit(tg.DOGRU)
        oi["oi"] = True
        self.assertEqual(O.kanonik(kural.Kural.kayittan(oi)), aday.kanonik_kimlik(oi, "sha256"))


class SinifTesti(Ortak):
    def test_hedef_siniflari(self):
        hedefler = {"h1": tg.DOGRU, "h2": DOGRU_OI, "h3": ORNEKSIZ, "h4": ZINDLE_YOLU, "h5": tg.SIMETRIK}
        s = O.hedef_siniflari(hedefler, {"a": tg.DOGRU}, {}, self.final, self.sema, 8)
        self.assertEqual(s, {"h1": O.OZDES, "h2": O.GENEL, "h3": O.ORNEKSIZ, "h4": O.KAPANIS, "h5": O.BULUNAMADI})
        self.assertEqual(O.hedef_siniflari({"h1": tg.DOGRU}, {}, {"u": tg.DOGRU}, self.final, self.sema, 8),
                         {"h1": O.OZDES})  # uyutulmuş da özdeş sayılır

    def test_bozuk_genel_kapsamaz(self):
        hedef = tg.k([(tg.B, "X", "Z"), (tg.B, "Z", "Y"), (tg.F, "X", "W")], (tg.V, "X", "Y"))
        genel_ama_yanlis = tg.k([(tg.F, "X", "W"), (tg.B, "Z", "Y")], (tg.V, "X", "Y"))  # θ-kapsar, finalde yanlış
        self.assertTrue(kural.kapsar_mi(genel_ama_yanlis, hedef))
        self.assertFalse(O.yanlissiz_mi(genel_ama_yanlis, self.final))
        self.assertTrue(O.yanlissiz_mi(hedef, self.final))
        s = O.hedef_siniflari({"h": hedef}, {"g": genel_ama_yanlis}, {}, self.final, self.sema, 8)
        self.assertNotEqual(s["h"], O.GENEL)

    def test_kabul_siniflari(self):
        kabul = {"a": tg.DOGRU, "b": tg.YANLIS, "c": tg.SIMETRIK, "d": tg.k(tg.DOGRU.halkalar[:1] + ((tg.B, "Z", "Y"),),
                                                                           tg.DOGRU.bas)}
        kapsam = {k: ["F1", "F2", "F3"] for k in kabul}
        s = O.kabul_siniflari(kabul, kapsam, {"u": ZINDLE_YOLU}, {"h": DOGRU_OI, "i": tg.DOGRU}, self.final)
        self.assertEqual(s, {"a": O.OZDES, "b": O.BOZUK, "c": O.FARKLI_DOGRU, "d": O.OZDES, "u": O.FAZLALIK})
        s2 = O.kabul_siniflari({"t": tg.TERS}, {"t": ["F1", "F2"]}, {}, {"h": DOGRU_OI}, self.final)
        self.assertEqual(s2, {"t": O.FARKLI_DOGRU})  # F3'te yanlış ama kapsamında değil
        s3 = O.kabul_siniflari({"t": tg.TERS}, {"t": ["F1", "F3"]}, {}, {"h": DOGRU_OI}, self.final)
        self.assertEqual(s3, {"t": O.BOZUK})


class BilmiyorumTesti(Ortak):
    def test_olcu(self):
        idx = self.final[0][1]
        o = O.olgu_olcusu([tg.DOGRU], idx, self.sema, 8)
        vonk = sum(f[1] == tg.V for f in idx.olgu)
        self.assertEqual(o[O.DOGRU], vonk)
        self.assertEqual(o[O.YANLIS], 0)
        self.assertEqual(o[O.BILMIYORUM], len(idx.olgu) - vonk)
        y = O.olgu_olcusu([tg.DOGRU, tg.YANLIS], idx, self.sema, 8)
        self.assertGreater(y[O.YANLIS], 0)
        b = O.bilmiyorum_olcusu([tg.DOGRU], self.final[:2], self.sema, 8)
        self.assertEqual(b["toplam"], sum(len(i.olgu) for _, i in self.final[:2]))


class KapiTesti(unittest.TestCase):
    H2 = KucukAyar(tg.H2)

    def kur(self, bulunan, bozuk=0, kabul=240, bilm=(0.10, 0.05)):
        bas = [tg.B, tg.ZN, tg.Q, tg.F, tg.V]
        hedefler = {f"h{i:03d}": tg.k([(tg.B, "X", "Y")], (bas[i % 5], "Y", "X")) for i in range(244)}
        sinif = {kim: (O.OZDES if i < bulunan else O.BULUNAMADI) for i, kim in enumerate(sorted(hedefler))}
        kabul_s = {f"a{i}": (O.BOZUK if i < bozuk else O.OZDES) for i in range(kabul)}
        return O.b2_karari(sinif, hedefler, kabul_s, {"bilmiyorum_orani": bilm[0]}, {"bilmiyorum_orani": bilm[1]},
                           tg.H2, 1.96)

    def test_karar(self):
        g = self.kur(230)
        self.assertEqual(g["karar"], O.GECTI, g)
        self.assertEqual((g["bulunan"], g["kume_sayisi"]), (230, 5))
        self.assertEqual(self.kur(200)["karar"], O.ARA_BOLGE)
        self.assertEqual(self.kur(100)["karar"], O.DUR)
        self.assertEqual(self.kur(230, bozuk=2)["karar"], O.ARA_BOLGE)  # CP üst > %2
        self.assertEqual(self.kur(230, bilm=(0.30, 0.10))["karar"], O.ARA_BOLGE)  # bilmiyorum farkı > 10 puan
        self.assertLess(self.kur(244, bozuk=0, kabul=149)["cp_ust"], 0.0201)  # 0 bozukta 149 kabul ≈ %2

    def test_hedef_sayisi_degismez(self):
        with self.assertRaises(ValueError):
            O.b2_karari({}, {"a": tg.DOGRU}, {}, {"bilmiyorum_orani": 0}, {"bilmiyorum_orani": 0}, tg.H2, 1.96)


class MakasTesti(Ortak):
    def test_tetik_yok_ve_yetersiz(self):
        ayar = KucukAyar(tg.H2, makas={"en_az_olgu": 10, "genis_olgu": 20, "yari_genislik_siniri": 0.02, "tetik": 0.03,
                                       "bootstrap": 200, "guven": 0.95})
        m = O.makas([tg.DOGRU], self.final[:3], self.final[3:], self.sema, 8, ayar, "B2b", 1)
        self.assertTrue(m["yeterli"])
        self.assertFalse(m["tetik"])
        self.assertLessEqual(m["alt"], m["ust"])
        az = KucukAyar(tg.H2, makas={**ayar.deger("makas"), "en_az_olgu": 10 ** 6})
        self.assertFalse(O.makas([tg.DOGRU], self.final[:3], self.final[3:], self.sema, 8, az, "B2b", 1)["yeterli"])


if __name__ == "__main__":
    unittest.main()
