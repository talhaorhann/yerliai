"""sistem.md §9, KODLAMA_PROMPTU §5–§6; K-020, K-021, V-038: çelişki defteri ve müdahale testi.

Çelişki: dışlayıcı / işlevsel / ters; kayıt silinmez, ortak destek kalıcı. Müdahale: (a) kök silme (yalnız etkilenen
köken alt grafı), (b) ilgisiz epitopu tür uyumlu yedekle değiştirme, (c) ters tutarlılığı + çelişkisizlik;
puan = a·b·c; ilgisiz epitop yoksa "sınanamadı" (başarı sayılmaz, ayrı sayılır). İlişki adları anlamsızdır.
"""
import unittest
from unittest import mock

import testler.test_a3_cekirdek as t3
from cekirdek import mudahale as M
from cekirdek.defter import CELISKI, Defter
from cekirdek.plazma import Cevap, cevapla
from testler.test_a3_temel import halka, hucre

BB_Q, QZ_V, DUNYA = t3.BB_Q, t3.QZ_V, t3.DUNYA


def turlu_celiskiler(defter):
    return sorted((k["veri"]["tur_adi"], tuple(k["veri"]["kayitlar"])) for k in defter.kayitlar() if k["tur"] == CELISKI)


class CeliskiTesti(t3.Ortam):
    def test_epitop_celiskileri(self):
        _, d, _ = self.kos([(1, "blorp", 2, 1.0), (1, "zindle", 2, 1.0)], BB_Q, gunluk_adi="a.jsonl")
        self.assertEqual(turlu_celiskiler(d), [("dislayici", (0, 1))])
        (veri,) = [k["veri"] for k in d.kayitlar() if k["tur"] == CELISKI]
        self.assertEqual(veri["ortak_destek"], [])
        self.assertEqual(veri["tur"], 0)
        _, d, _ = self.kos([(1, "blorp", 2, 1.0), (1, "blorp", 5, 1.0)], BB_Q, gunluk_adi="b.jsonl")
        self.assertEqual(turlu_celiskiler(d), [("islevsel", (0, 1))])
        _, d, _ = self.kos([(1, "quax", 3, 1.0), (3, "zindle", 1, 1.0)], BB_Q, gunluk_adi="c.jsonl")
        self.assertEqual(turlu_celiskiler(d), [("ters", (0, 1))])

    def test_tutarli_ters_ve_tanimsiz_ters_celiski_degil(self):
        _, d, _ = self.kos([(1, "quax", 3, 1.0), (3, "blorp", 1, 1.0)], BB_Q, gunluk_adi="a.jsonl")
        self.assertEqual(turlu_celiskiler(d), [])
        _, d, _ = self.kos([(1, "vonk", 3, 1.0), (3, "zindle", 1, 1.0)], BB_Q, gunluk_adi="b.jsonl")
        self.assertEqual(turlu_celiskiler(d), [])
        _, d, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="c.jsonl")
        self.assertEqual(turlu_celiskiler(d), [])

    def test_cikarim_celiskisi_ortak_destek_kalici_kayit_silinmez(self):
        bf = hucre("h_bf", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("frumb", "X", "Z"), guvenilirlik=0.5)
        h, d, _ = self.kos(DUNYA, BB_Q, bf, sorgu=(1, 3))
        celiskiler = [k["veri"] for k in d.kayitlar() if k["tur"] == CELISKI]
        self.assertEqual(len(celiskiler), 1)
        c = celiskiler[0]
        self.assertEqual(c["tur_adi"], "dislayici")
        self.assertEqual(c["ortak_destek"], [0, 1])
        for kimlik in c["kayitlar"]:
            self.assertIn(kimlik, {k.kimlik for k in h.kayitlar()})
            self.assertTrue(d.celiskiye_karisti(kimlik))
        self.assertEqual(cevapla(h, (1, 3), d).iliski, "quax")
        yeniden = Defter(d.yol, algoritma=d.algoritma, sema_surumu=d.sema_surumu, izinli_kaynaklar=d.izinli_kaynaklar)
        self.assertEqual(turlu_celiskiler(yeniden), turlu_celiskiler(d))
        self.assertTrue(all(yeniden.celiskiye_karisti(k) for k in c["kayitlar"]))


class MudahaleTesti(t3.Ortam):
    def mudahale(self, olgular, *dna, sorgu, **kw):
        h, d, _ = self.kos(olgular, *dna, sorgu=sorgu, **kw)
        return h, d, M.mudahale_testi(h, d, self.hucreler(*dna), olgular, t3.KK, kw.get("prm", t3.PRM), self.sema, sorgu)

    def test_tam_basari(self):
        h, d, m = self.mudahale(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        self.assertEqual((m.cevap, m.durum), ("vonk", M.PUANLI))
        self.assertEqual([s["epitop"] for s in m.silmeler], [0, 1, 2])
        self.assertTrue(all(s["dustu"] for s in m.silmeler))
        self.assertEqual([x["epitop"] for x in m.degisiklikler], [3])
        self.assertEqual(m.degisiklikler[0]["yedek"], [9, "frumb", 10])
        self.assertEqual((m.a, m.b, m.c, m.puan, m.sinanamadi), (1.0, 1.0, 1, 1.0, False))

    def test_yalniz_etkilenen_koken_alt_grafi(self):
        h, d, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        gorunum = M.BudanmisHavuz(h, 2)
        self.assertEqual(sorted(k.uclu for k in gorunum.kayitlar()),
                         sorted([(1, "blorp", 2), (2, "blorp", 3), (7, "frumb", 8), (1, "quax", 3)]))
        self.assertIsNone(cevapla(gorunum, (1, 4), d).iliski)
        self.assertEqual(cevapla(gorunum, (1, 3), d).iliski, "quax")
        self.assertEqual(len(h.kayitlar()), 6)

    def test_ortak_kokte_a_kismi(self):
        bz = hucre("h_bz", [halka("blorp", "X", "Y"), halka("zindle", "Y", "Z")], ("quax", "X", "Z"))
        olgular = [(1, "blorp", 2, 0.6), (2, "blorp", 3, 0.6), (2, "zindle", 3, 0.6)]
        _, _, m = self.mudahale(olgular, BB_Q, bz, sorgu=(1, 3))
        self.assertEqual(m.cevap, "quax")
        self.assertEqual([s["dustu"] for s in m.silmeler], [True, False, False])
        self.assertEqual(m.a, 1 / 3)
        self.assertTrue(m.celiski_var)
        self.assertEqual(m.c, 0)

    def test_ilgisiz_epitop_yoksa_sinanamadi_basari_sayilmaz(self):
        _, _, m = self.mudahale(DUNYA[:3], BB_Q, QZ_V, sorgu=(1, 4))
        self.assertEqual((m.durum, m.sinanamadi, m.b, m.puan), (M.SINANAMADI, True, None, None))
        self.assertEqual((m.a, m.c), (1.0, 1))

    def test_ilgisiz_degisiklik_cevabi_degistirirse_b_sifir(self):
        sahte = Cevap("quax", 0.1, (), False, ())
        with mock.patch.object(M, "_yeniden_cevapla", return_value=sahte):
            _, _, m = self.mudahale(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        self.assertEqual((m.b, m.puan, m.durum), (0.0, 0.0, M.PUANLI))
        self.assertFalse(m.degisiklikler[0]["ayni"])

    def test_ters_tutarsizlik_c_sifir(self):
        tz = hucre("h_tz", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("zindle", "Z", "X"))
        _, _, m = self.mudahale(DUNYA, BB_Q, tz, sorgu=(1, 3))
        self.assertEqual((m.cevap, m.ters_cevap, m.ters_tutarli, m.c, m.puan), ("quax", "zindle", False, 0, 0.0))

    def test_ters_tutarli(self):
        tb = hucre("h_tb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("blorp", "Z", "X"))
        _, _, m = self.mudahale(DUNYA, BB_Q, tb, sorgu=(1, 3))
        self.assertEqual((m.cevap, m.ters_cevap, m.ters_tutarli, m.celiski_var, m.c), ("quax", "blorp", True, False, 1))

    def test_cevapsiz(self):
        _, _, m = self.mudahale(DUNYA, BB_Q, sorgu=(1, 7))
        self.assertEqual((m.cevap, m.durum, m.puan, m.a, m.b, m.c), (None, M.CEVAPSIZ, None, None, None, None))

    def test_ana_havuz_ve_defter_degismez_tek_ozet_olayi(self):
        h, d, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        once_kayit, once_olay = h.kayitlar(), d.kayitlar()
        m = M.mudahale_testi(h, d, self.hucreler(BB_Q, QZ_V), DUNYA, t3.KK, t3.PRM, self.sema, (1, 4))
        self.assertEqual(h.kayitlar(), once_kayit)
        sonra = d.kayitlar()
        self.assertEqual(sonra[:len(once_olay)], once_olay)
        self.assertEqual([k["tur"] for k in sonra[len(once_olay):]], [M.MUDAHALE])
        self.assertEqual(sonra[-1]["veri"]["puan"], m.puan)

    def test_olgu_sirasi_havuzla_uyusmazsa_durur(self):
        h, d, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        with self.assertRaises(ValueError):
            M.mudahale_testi(h, d, self.hucreler(BB_Q, QZ_V), list(reversed(DUNYA)), t3.KK, t3.PRM, self.sema, (1, 4))

    def test_belirlenim(self):
        a = self.mudahale(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="a.jsonl")[2]
        b = self.mudahale(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="b.jsonl")[2]
        self.assertEqual(a, b)

    def test_ozet_sinanamadiyi_ayri_sayar(self):
        tam = self.mudahale(DUNYA, BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="a.jsonl")[2]
        sinanamadi = self.mudahale(DUNYA[:3], BB_Q, QZ_V, sorgu=(1, 4), gunluk_adi="b.jsonl")[2]
        cevapsiz = self.mudahale(DUNYA, BB_Q, sorgu=(1, 7), gunluk_adi="c.jsonl")[2]
        ozet = M.mudahale_ozeti([tam, sinanamadi, cevapsiz])
        self.assertEqual(ozet, {"toplam": 3, "puanli": 1, "sinanamadi": 1, "cevapsiz": 1, "ortalama_puan": 1.0})
        self.assertEqual(M.mudahale_ozeti([])["ortalama_puan"], None)


if __name__ == "__main__":
    unittest.main()
