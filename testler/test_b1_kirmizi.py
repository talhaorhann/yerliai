"""K-041, K-043 (ÖK-005 taslağı §4 madde 19 ve görünür aileler tablosu; §5), V-065: kırmızı takım.

Sentetik blorp dünyaları (`test_b1_gecit`): G1 baş değişimi, G2 halka silme (geliştirmede yanlış > 0), G3 yalnız ilk
ailede tutan kural, G4 şemadan (eksik G1'den), tohumla belirlenim ve tekillik. Gizli dosya yalnız sayılarla özetlenir.
"""
import json
import tempfile
import unittest
import unittest.mock
from pathlib import Path

from degerlendirme import h2_kirmizi as K, kural
from kesif import sablon
from testler import test_b1_gecit as tg
from testler.test_a1_iliski_semasi import SemaOrtami, blorp_semasi
from testler.test_b1_tur import kayit


class KucukAyar:
    def __init__(self, h2, **degerler):
        self.h2, self.degerler = h2, degerler

    def deger(self, ad):
        return self.degerler[ad] if ad in self.degerler else self.h2.deger(ad)


def m0_listesi(kurallar):
    return K.M0Listesi([json.dumps({"aday": kayit(k)}).encode() for k in kurallar])


# F(Y,X) halkası çıkarılınca X = Y bağlaması yanlış tahmin verir (G2'nin tek geçerli silmesi)
U1 = tg.k([(tg.B, "X", "Z"), (tg.ZN, "Z", "Y"), (tg.F, "Y", "X")], (tg.F, "X", "Y"))
U2 = tg.k([(tg.B, "Y", "Z"), (tg.ZN, "Z", "X"), (tg.F, "Y", "X")], (tg.F, "X", "Y"))
U3 = tg.k([(tg.B, "X", "Z"), (tg.B, "Y", "Z"), (tg.F, "Y", "X")], (tg.F, "X", "Y"))


class GorunurTesti(tg.Ortak):
    M0 = [tg.DOGRU, tg.SIMETRIK, tg.k([(tg.B, "X", "Z"), (tg.B, "Z", "W"), (tg.B, "W", "Y")], (tg.V, "X", "Y"))]

    def test_g1_bas_degisir_tekil_ve_belirlenimci(self):
        a = K.g1(m0_listesi(self.M0), self.sema, tg.H2, 4)
        self.assertEqual(a, K.g1(m0_listesi(self.M0), self.sema, tg.H2, 4))
        self.assertEqual(len({x["kimlik"] for x in a}), 4)
        ustler = {kayit(k)["kimlik"]: kayit(k) for k in self.M0}
        for x in a:
            ust = ustler[x["kaynak"]["ust"][0]]
            self.assertEqual(x["halkalar"], ust["halkalar"])
            self.assertNotEqual(x["sonuc"]["gen"], ust["sonuc"]["gen"])
            self.assertTrue(self.sema.dislayici_mi(x["sonuc"]["gen"], ust["sonuc"]["gen"]))
            self.assertEqual(x["kaynak"]["aile"], "G1")

    def test_g2_silinen_halka_gelistirmede_yanlis(self):
        for u in (U1, U2, U3):
            self.assertEqual(K._gelistirmede_yanlis(u, self.ortam.gelistirme), 0)
        a = K.g2(m0_listesi(self.M0 + [U1, U2, U3]), self.ortam.gelistirme, tg.H2, 3)
        self.assertEqual({x["kaynak"]["ust"][0] for x in a}, {kayit(u)["kimlik"] for u in (U1, U2, U3)})
        for x in a:
            self.assertEqual([h["gen"] for h in x["halkalar"]].count(tg.F), 0)  # silinen F(Y,X)
            self.assertGreater(K._gelistirmede_yanlis(kural.Kural.kayittan(x), self.ortam.gelistirme), 0)

    def test_uretilemezse_durur(self):
        with unittest.mock.patch.object(K, "DENEME_SINIRI", 50):
            with self.assertRaises(K.UretimHatasi):
                K.g2(m0_listesi(self.M0), self.ortam.gelistirme, tg.H2, 1)

    def test_g3_yalniz_ilk_ailede_tutan(self):
        adlar = tuple(self.sema.adlar)
        govdeler = sablon.govdeler(len(adlar), ("X", "Y", "Z", "W"), 1, False)
        dunyalar = [d for _, d, _ in self.ortam.gelistirme]
        liste = K.g3_listesi(dunyalar, adlar, tg.H2, govdeler)
        kimlikler = {K._kayit(*K._parca(sablon.aday_kaydi(govdeler[g], b, oi, adlar, ("X", "Y", "Z", "W")))[:2],
                              oi, [], "G3", 0, [])["kimlik"] for g, b, oi in liste}
        self.assertIn(kayit(tg.TERS)["kimlik"], kimlikler)  # F1'de doğru, F3'te yanlış
        self.assertNotIn(kayit(tg.SIMETRIK)["kimlik"], kimlikler)  # her yerde doğru
        a = K.g3(liste, govdeler, adlar, tg.H2, 1)
        for x in a:
            kk = kural.Kural.kayittan(x)
            f1 = [(e, d, i) for e, d, i in self.ortam.gelistirme if d.aile == "F1"]
            self.assertEqual(K._gelistirmede_yanlis(kk, f1), 0)
            self.assertGreater(K._gelistirmede_yanlis(kk, self.ortam.gelistirme), 0)

    def test_g4_semadan_eksik_g1den(self):
        veri = blorp_semasi()
        for r in veri["iliskiler"]:
            if r["ad"] == tg.F:
                r["islevsel"] = True
        so = SemaOrtami(veri)
        try:
            sema = so.yukle()
            self.assertEqual(K.g4_uclari(sema), [(tg.Q, tg.B, tg.F), (tg.ZN, tg.B, tg.F)])
            a, eksik = K.g4(sema, tg.H2, 3)
            self.assertEqual((len(a), eksik), (2, 1))
            self.assertEqual({x["sonuc"]["gen"] for x in a}, {tg.Q, tg.ZN})
            self.assertEqual([(h["sol"], h["sag"]) for h in a[0]["halkalar"]], [("Z", "X"), ("Z", "W"), ("W", "Y")])
            self.assertFalse(a[0]["oi"])
            hepsi, sayilar = K.gorunur(m0_listesi(self.M0 + [U1]), self.ortam.gelistirme, [(0, 0, False)],
                                       sablon.govdeler(5, ("X", "Y", "Z", "W"), 1, False), sema,
                                       KucukAyar(tg.H2, kirmizi_aile_basina=1))
            self.assertEqual(sayilar, {"G1": 1, "G2": 1, "G3": 1, "G4": 1, "G4_eksigi_G1den": 0})
            self.assertEqual(len({x["kimlik"] for x in hepsi}), len(hepsi))
        finally:
            so.kapat()


class GizliTesti(tg.Ortak):
    def dosya(self, klasor, aileler):
        adaylar = []
        for ad_, kurallar in aileler.items():
            for k in kurallar:
                r = kayit(k)
                r["kaynak"] = {"tur": K.GIZLI, "aile": ad_, "tohum": None, "ust": []}
                adaylar.append(r)
        veri = {"sema_surumu": "1", "dosya_turu": K.GIZLI, "yazan": "test", "tarih": "2026-10-26",
                "aileler": [{"ad": a, "aciklama": "x"} for a in aileler], "adaylar": adaylar}
        yol = Path(klasor) / "g.json"
        yol.write_text(json.dumps(veri), encoding="utf-8")
        return yol

    def test_sayim_yalniz_sayilar(self):
        bos_govde = tg.k([(tg.Q, "X", "Y"), (tg.ZN, "X", "Y")], (tg.B, "Y", "X"))  # bir çiftte iki ters olmaz: eşleşmez
        aileler = {"P2": [tg.YANLIS, tg.TERS], "P1": [tg.DOGRU, bos_govde, tg.k([(tg.F, "X", "Y")], (tg.V, "X", "Y"))]}
        ayar = KucukAyar(tg.H2, kirmizi_gizli_aile_sayisi=2, kirmizi_aile_basina=2)
        with tempfile.TemporaryDirectory() as d:
            kayitlar = K.gizli_yukle(self.dosya(d, aileler), frozenset(self.sema.adlar), ayar)
        sayim, etkin = K.gelistirme_sayimi(kayitlar, self.ortam.gelistirme)
        self.assertEqual(sayim, {1: {"kural": 3, "yanlis": 1, "tetiklenmedi": 1}, 2: {"kural": 2, "yanlis": 2, "tetiklenmedi": 0}})
        self.assertEqual(len(etkin), 3)
        self.assertNotIn("P1", json.dumps(sayim))

    def test_bicim_bozuksa_hata(self):
        ayar = KucukAyar(tg.H2, kirmizi_gizli_aile_sayisi=2, kirmizi_aile_basina=2)
        with tempfile.TemporaryDirectory() as d:
            yol = self.dosya(d, {"P1": [tg.DOGRU, tg.YANLIS], "G1": [tg.TERS, tg.SIMETRIK]})  # görünür ad yasak
            with self.assertRaises(K.ad.AdayHatasi):
                K.gizli_yukle(yol, frozenset(self.sema.adlar), ayar)


if __name__ == "__main__":
    unittest.main()
