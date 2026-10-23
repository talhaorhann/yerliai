"""KODLAMA_PROMPTU §5 (Defter), sistem.md §18, V-035: destek/çelişki defteri altyapısı.

Sadece-ekleme, hash zincirli; her ateşleme/yazma/atma kayıtlı; defterde izi olmayan sonuç yanıta giremez;
kök-ayrık destek. Çelişki ve müdahale testi V-036/V-037 onayına bağlıdır, burada yoktur.
"""
import dataclasses
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.olay_gunlugu import KayitHatasi, OlayGunlugu
from cekirdek.defter import ATESLEME, ATMA, YAZMA, Defter
from cekirdek.dongu import calistir
from cekirdek.havuz import Havuz
from cekirdek.plazma import cevapla
import testler.test_a3_cekirdek as t3
from testler.test_a3_temel import halka, hucre


def gunluk_ayari():
    return dict(algoritma=AYAR.deger("hash_algoritmasi"), sema_surumu=AYAR.deger("olay_sema_surumu"),
                izinli_kaynaklar=AYAR.deger("kaynaklar"))


class GunlukGenislemeTesti(unittest.TestCase):
    def test_bellekte_gunluk_dosya_acmaz(self):
        with tempfile.TemporaryDirectory() as d:
            g = OlayGunlugu(None, **gunluk_ayari())
            g.ekle("DENEME", "çekirdek", {"i": 7})
            g.ekle_toplu([("DENEME", "çekirdek", {"i": 11}), ("DENEME", "çekirdek", {"i": 13})])
            self.assertEqual([k["sira"] for k in g.kayitlar()], [0, 1, 2])
            self.assertEqual(list(Path(d).iterdir()), [])

    def test_toplu_ekleme_tek_tek_eklemeyle_ayni_bayt(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.jsonl", Path(d) / "b.jsonl"
            olaylar = [("DENEME", "çekirdek", {"i": i}) for i in (7, 11, 13)]
            ga = OlayGunlugu(a, **gunluk_ayari())
            for o in olaylar:
                ga.ekle(*o)
            OlayGunlugu(b, **gunluk_ayari()).ekle_toplu(olaylar)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            self.assertEqual(len(OlayGunlugu(b, **gunluk_ayari()).kayitlar()), 3)

    def test_toplu_eklemede_bir_hata_hicbirini_yazdirmaz(self):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "a.jsonl"
            g = OlayGunlugu(yol, **gunluk_ayari())
            g.ekle("DENEME", "çekirdek", {"i": 7})
            onceki = yol.read_bytes()
            with self.assertRaises(KayitHatasi):
                g.ekle_toplu([("DENEME", "çekirdek", {"i": 11}), ("DENEME", "uydurma", {})])
            self.assertEqual(yol.read_bytes(), onceki)
            self.assertEqual(len(g.kayitlar()), 1)


AYAR, BB_Q, DUNYA, KK, PRM, QZ_V = t3.AYAR, t3.BB_Q, t3.DUNYA, t3.KK, t3.PRM, t3.QZ_V
IKI_YOL = t3.PlazmaTesti.IKI_YOL


class DefterTesti(t3.Ortam):
    def test_atesleme_yazma_kayitli_ve_dizin(self):
        h, d, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        turler = [k["tur"] for k in d.kayitlar()]
        self.assertEqual(turler.count(ATESLEME), 2)
        self.assertEqual(turler.count(YAZMA), 2)
        for k in h.kayitlar():
            self.assertEqual(d.yazildi_mi(k.kimlik), k.katman == 1)
        yazma = [k["veri"] for k in d.kayitlar() if k["tur"] == YAZMA]
        self.assertEqual(yazma[0]["kokler"], [0, 1])
        self.assertEqual(yazma[1]["kokler"], [0, 1, 2])

    def test_atesleme_atilan_eslesmeleri_de_kaydeder(self):
        olgular = [(i, "blorp", i + 100, 1.0) for i in range(13)]
        kopya = hucre("h1", [halka("blorp", "X", "Y")], ("quax", "X", "Y"))
        _, d, _ = self.kos(olgular, kopya, prm=dataclasses.replace(PRM, tur_siniri=1))
        self.assertEqual(d.sayac(ATESLEME), 13)
        self.assertEqual(d.sayac(YAZMA), PRM.hucre_yazma_siniri)

    def test_dizin_dosyadan_yeniden_kurulur(self):
        h, d, _ = self.kos(DUNYA, BB_Q, QZ_V, sorgu=(1, 4))
        yeniden = Defter(d.yol, **gunluk_ayari())
        for k in h.kayitlar():
            self.assertEqual(yeniden.yazildi_mi(k.kimlik), d.yazildi_mi(k.kimlik))
        self.assertEqual(yeniden.canli_ispatlar((1, "vonk", 4)), d.canli_ispatlar((1, "vonk", 4)))

    def test_kok_ayrik_destek(self):
        _, d, _ = self.kos(IKI_YOL, BB_Q, sorgu=(1, 3), gunluk_adi="a.jsonl")
        self.assertEqual(d.destek((1, "quax", 3)), 2)
        kopyalar = [dict(BB_Q, kimlik=f"h_kopya{i}") for i in range(10)]
        _, d10, _ = self.kos(IKI_YOL[:2], *kopyalar, sorgu=(1, 3), gunluk_adi="b.jsonl")
        self.assertEqual(len(d10.canli_ispatlar((1, "quax", 3))), 10)
        self.assertEqual(d10.destek((1, "quax", 3)), 1)
        self.assertEqual(d10.destek((1, "vonk", 3)), 0)

    def test_atilan_ispat_canli_sayilmaz(self):
        olgular = [(1, "blorp", 2, 0.9), (2, "blorp", 3, 0.9), (5, "blorp", 6, 0.4), (6, "blorp", 7, 0.4)]
        kv = hucre("h_qv", [halka("quax", "X", "Y")], ("vonk", "X", "Y"))
        h, d, _ = self.kos(olgular, BB_Q, kv, kapasite=6)
        atilanlar = [k["veri"]["kimlik"] for k in d.kayitlar() if k["tur"] == ATMA]
        self.assertTrue(atilanlar)
        for a in atilanlar:
            self.assertTrue(d.yazildi_mi(a))
            self.assertNotIn(a, d.canli_ispatlar(tuple(h.kayit(a).uclu)))

    def test_defterde_izi_olmayan_sonuc_yanita_giremez(self):
        """Havuza defteri atlayarak yazılan çıkarım ispat sayılmaz (KODLAMA_PROMPTU §5)."""
        h = Havuz(PRM.kapasite, KK)
        for s, r, o, g in DUNYA:
            h.epitop_ekle(s, r, o, guven=g)
        d = self.gunluk()
        h.cikarim_ekle((1, "quax", 3), zincir="sahte", ebeveynler=(0, 1), guven=1.0)
        self.assertIsNone(cevapla(h, (1, 3), d).iliski)
        calistir(self.hucreler(BB_Q), h, KK, PRM, d, iliski_semasi=self.sema, sorgu=(1, 3))
        c = cevapla(h, (1, 3), d)
        self.assertEqual(c.iliski, "quax")
        self.assertTrue(all(d.yazildi_mi(a["kimlik"]) for a in c.gerekce))

    def test_dongu_defter_ister(self):
        h = Havuz(PRM.kapasite, KK)
        for s, r, o, g in DUNYA:
            h.epitop_ekle(s, r, o, guven=g)
        with self.assertRaises(TypeError):
            calistir(self.hucreler(BB_Q), h, KK, PRM, OlayGunlugu(None, **gunluk_ayari()), iliski_semasi=self.sema,
                     sorgu=(1, 3))


if __name__ == "__main__":
    unittest.main()
