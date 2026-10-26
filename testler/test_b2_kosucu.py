"""K-041, K-043 (ÖK-005 taslağı §4 madde 2, 3, 15–18, 21; §8; §9 madde 4–6), V-065: B2 koşucusu sentetik blorp
dünyalarında. Hedef kurallar elle seçilir (DNA kullanılmaz); "final" ve "kontrol" sentetik dünyalardır.
B2a: seçim tohumla belirlenir, tohumlar yalnız bellekte; B2b: tur başına makas, final ölçümü, kapı kararı."""
import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from degerlendirme import h2_b2, h2_gecit as G, h2_kirmizi as KR, h2_olcum as O, h2_tur
from testler import test_b1_gecit as tg
from testler.test_b1_kirmizi import KucukAyar
from testler.test_b1_tur import SABIT, ZINDLE_YOLU, kayit, taze_fn
from testler.yardimci import KOK

HEDEF = {"h1": tg.DOGRU, "h2": ZINDLE_YOLU, "h3": tg.SIMETRIK}


class B2Testi(tg.Ortak):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        ortam = self.ortam_ = dataclasses.replace(type(self).ortam, sabit=SABIT)
        b = self.b2 = object.__new__(h2_b2.B2)
        b.kok, b.cikis, b.is_sayisi = KOK, Path(self._d.name), 1
        b.h2 = KucukAyar(tg.H2, sorgu_tur_siniri=2, b2a_silinen=1,
                         b2_kapi={**tg.H2.deger("b2_kapi"), "hedef_sayisi": len(HEDEF)},
                         makas={"en_az_olgu": 10, "genis_olgu": 20, "yari_genislik_siniri": 0.02, "tetik": 0.03,
                                "bootstrap": 200, "guven": 0.95})
        b.esik, b.tur_basina = G.Esikler(0.5, 0.9, 0.04, 0.01), 2
        b.m0 = KR.M0Listesi([json.dumps({"aday": kayit(k)}).encode()
                             for k in (tg.DOGRU, tg.SIMETRIK, ZINDLE_YOLU, tg.YANLIS)])
        b.ortam, b.taze_fn, b.sabit = ortam, taze_fn, SABIT
        b._kosucu = lambda klasor, defter: h2_tur.Kosucu(klasor, ortam, taze_fn, None, defter, [])
        b.hedefler = lambda: dict(HEDEF)
        dunya = {"final": [(a, idx) for _, a, _, idx in type(self).taze], "kontrol": [(a, idx) for _, a, _, idx in
                                                                                      taze_fn("B2b", 9)]}
        b._dunyalar = lambda ad: dunya[ad]

    def tearDown(self):
        self._d.cleanup()

    def test_b2a_secimi_belirlenimci(self):
        import hashlib
        self.assertEqual(h2_b2.b2a_silinenler(["a", "b", "c"], 2), h2_b2.b2a_silinenler(["c", "b", "a"], 2))
        beklenen = sorted("abcdef", key=lambda k: hashlib.sha256(("ÖK-005|B2a|" + k).encode()).hexdigest())[:3]
        self.assertEqual(h2_b2.b2a_silinenler(list("abcdef"), 3), beklenen)
        s = self.b2.b2a()
        self.assertEqual(s["silinen"], 1)
        self.assertEqual(sum(s["silinen_siniflari"].values()), 1)
        self.assertLessEqual(len(s["arama"]["turlar"]), 2)

    def test_b2b_makas_olcum_karar(self):
        s = self.b2.b2b()
        turlar = s["arama"]["turlar"]
        self.assertTrue(turlar)
        self.assertIn("makas", turlar[0])
        self.assertEqual(s["hedef_siniflari"]["h1"], O.OZDES)
        self.assertEqual(s["hedef_siniflari"]["h2"], O.OZDES)  # yedek olduğu için uyutuldu: uyutulmuş da özdeştir
        self.assertEqual(s["hedef_siniflari"]["h3"], O.BULUNAMADI)  # simetrik kural yeniden bağlı ikizde BİLMİYORUM
        self.assertIn(s["karar"]["karar"], (O.GECTI, O.ARA_BOLGE, O.DUR))
        self.assertEqual(s["karar"]["bulunan"], 2)
        self.assertEqual(s["ikincil_paydalar"]["okunur_haric"], [2, 2])  # h3 şemadan okunur sınıfta
        self.assertTrue((Path(self._d.name) / "b2b_olcum.json").exists())
        self.assertEqual(self.b2.olcum(h2_tur.Bellek(), {})["karar"], s["karar"])  # ölçüm bir kez: dosyadan döner

    def test_b1_basarisizsa_b2_baslamaz(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "sonuc.json").write_text(json.dumps({"basari_araliginda": False}), encoding="utf-8")
            with self.assertRaises(h2_b2.B2Hatasi):
                h2_b2.B2(KOK, "yok", d, self._d.name, 1, onkayit=False)


if __name__ == "__main__":
    unittest.main()
