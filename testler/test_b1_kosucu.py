"""K-041, K-043 (ÖK-005 taslağı §4 madde 3, 9–12, 19, 20; §9 madde 3), V-065: B1 koşucusunun evreleri (C, kalibrasyon
ölçümü, K seçimi, kırmızı takım, P*, boş koşular, sonuç) sentetik blorp dünyalarında; gerçek havuzlar açılmaz.
Gizli dosya sentetiktir; sonuçta yalnız aile sırası ve sayılar bulunur."""
import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json
from degerlendirme import h2_b1, h2_gecit as G, h2_kirmizi as KR, h2_tur
from testler import test_b1_gecit as tg
from testler.test_b1_kirmizi import KucukAyar, U1
from testler.test_b1_tur import SABIT, ZINDLE_YOLU, kayit, taze_fn
from testler.yardimci import KOK

IZGARA = {"tau": [0.5, 0.85, 0.9], "mudahale": [0.8, 0.9, 1.0], "T": [0.02, 0.04, 0.06], "sigma": [0.005, 0.01, 0.02]}


class B1Testi(tg.Ortak):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.ortam = dataclasses.replace(type(self).ortam, sabit=SABIT)
        b = self.b1 = object.__new__(h2_b1.B1)
        b.kok, b.cikis, b.is_sayisi = KOK, Path(self._d.name), 1
        b.h2 = KucukAyar(tg.H2, sorgu_tur_basina_aday=2, sorgu_tur_siniri=1, kalibrasyon_aday_sayisi=2,
                         esik_izgarasi=IZGARA, esik_baslangic={"tau": 0.5, "mudahale": 0.9, "T": 0.04, "sigma": 0.01},
                         p_yildiz_aday_sayisi=2, bos_dunya_kosu_sayisi=3, bos_dunya_tetik=2,
                         kirmizi_gizli_aile_sayisi=2, kirmizi_aile_basina=1)
        b.m0 = KR.M0Listesi([json.dumps({"aday": kayit(k)}).encode() for k in (tg.DOGRU, ZINDLE_YOLU, U1, tg.TERS)])
        b.ortam, b.taze_fn, b.sabit = self.ortam, taze_fn, SABIT
        b._kosucu = lambda klasor, kurulum=None, defter=None, obiter_sirala=False: h2_tur.Kosucu(
            klasor, self.ortam, taze_fn, None, defter, [], obiter_sirala)
        b._bos_m0 = lambda k: ([{"aday": kayit(c)} for c in (tg.SIMETRIK, tg.DOGRU)], 10, {})
        gor = [kayit(c) for c in (tg.YANLIS, tg.SIMETRIK)]
        for g in gor:
            g["kaynak"] = {"tur": KR.GORUNUR, "aile": "G1", "tohum": 1, "ust": []}
        b._jsonl_yaz("kirmizi_gorunur.jsonl", gor)
        atomik_yaz(b.cikis / "kirmizi_gorunur.json", kanonik_json({"sahte": [gor[0]["kimlik"]], "sayilar": {}}))
        bos = [kayit(c) for c in (tg.YANLIS, tg.TERS, tg.DOGRU)]  # DOGRU sahte değil: ölçülmez (V-065 madde 15)
        b._jsonl_yaz("bos_adaylar.jsonl", bos)
        atomik_yaz(b.cikis / "bos_adaylar.json", kanonik_json({"sahte": [k["kimlik"] for k in bos[:2]], "akis": 3,
                                                               "m0_sure_s": 10}))

    def tearDown(self):
        self._d.cleanup()

    def test_talep(self):
        c = self.b1.evre("talep", self.b1.talep)
        # DOGRU geçer; ZINDLE_YOLU DOGRU'ca kapsanır; U1 obiterdir; TERS F3'te yanlış → 1 (üst sınır 2·2·1+1 = 5)
        self.assertEqual((c["C"], c["sayim_tamam"], c["sayim_ustu"], c["taranan"]), (1, True, 5, 4))

    def test_kalibrasyon_k_p_yildiz(self):
        b = self.b1
        o = b.evre("kalibrasyon_olcum", b.kalibrasyon_olcum)
        self.assertEqual((o["ilk"], o["gorunur"], o["bos"]), (2, 2, 2))
        k = b.evre("k", b.k)
        self.assertEqual(k["sahte_sayisi"], 2)  # YANLIS iki akışta da var
        self.assertEqual(k["secilen"]["tau"], 0.5)
        dogru = kayit(tg.DOGRU)["kimlik"]
        olc = b._olcumler()["ilk"][dogru]
        self.assertEqual(G.hukum(olc, b._esik(), SABIT)[0], G.KABUL)
        p = b.evre("p_yildiz", b.p_yildiz)
        self.assertEqual((p["P*"], p["sansurlu"]), (4, True))
        self.assertNotIn(dogru, b._olcumler()["bos"])

    def test_kirmizi_gizli_yalniz_sayilar(self):
        b = self.b1
        adaylar = []
        for aile, kurallar in (("P2", [tg.YANLIS]), ("P1", [tg.TERS, tg.DOGRU])):
            for c in kurallar:
                r = kayit(c)
                r["kaynak"] = {"tur": KR.GIZLI, "aile": aile, "tohum": None, "ust": []}
                adaylar.append(r)
        veri = {"sema_surumu": "1", "dosya_turu": KR.GIZLI, "yazan": "t", "tarih": "2026-10-26",
                "aileler": [{"ad": "P1", "aciklama": "x"}, {"ad": "P2", "aciklama": "y"}], "adaylar": adaylar}
        yol = b.cikis / "g.json"
        yol.write_text(json.dumps(veri), encoding="utf-8")
        kr = b.evre("kirmizi", lambda: b.kirmizi(yol))
        metin = json.dumps(kr)
        for gizli in ("P1", "P2", "gizli_"):
            self.assertNotIn(gizli, metin)
        self.assertEqual(kr["gizli"]["1"]["kural"], 2)
        self.assertEqual((kr["gizli"]["1"]["etkin"], kr["gizli"]["2"]["etkin"]), (1, 1))
        self.assertEqual(kr["gizli"]["1"]["etkin_olmayan_kabul"], 1)  # DOGRU: geliştirmede yanlış vermez, sahte sayılmaz
        self.assertEqual(kr["kacak"], 0)
        self.assertEqual(kr["sahte_toplam"], 3)
        self.assertFalse(kr["alt_sinir_gecti"])  # 3/3 ile tek yanlı alt sınır %98'in altında
        self.assertFalse(any(p.name.startswith("h2_gizli_") for p in Path(tempfile.gettempdir()).iterdir()))

    def test_bos_kosular_tetik(self):
        b = self.b1
        b.evre("kalibrasyon_olcum", b.kalibrasyon_olcum)
        atomik_yaz(b.cikis / "talep.json", kanonik_json({"C": 1}))
        bos = b.evre("bos_kosular", b.bos_kosular)
        self.assertEqual((bos["kabullu_kosu"], bos["yapilan"], bos["tetiklendi"]), (2, 2, True))  # DOGRU kabul edilir
        self.assertTrue(all(k["kabul"] == 1 for k in bos["kosular"]))


if __name__ == "__main__":
    unittest.main()
