"""K-035, V-057: bellek geçidi için gözlem bölümleri. Türetilmiş ilişkiler kâhin etiketi olarak değil, bölümde olgu
olarak geçen bağımsız gözlemlerdir. Bölümde sorgu ve cevap yoktur; her gözlem gerçek ağaçta doğrudur.
Testlerde ilişki adı yazılmaz (KODLAMA_PROMPTU §2.4): tanımlar dosyadan gelir."""
import random
import unittest

from degerlendirme import uretec
import testler.test_a1_uretec as t1


def uret(tohum, k=None):
    return uretec.gozlem_bolumu(random.Random(tohum), t1.TANIM, t1.PRM, k or t1.PRM.egitim_k)


class GozlemBolumuTesti(unittest.TestCase):
    def test_yalniz_olgular_var(self):
        g = uret(1)
        self.assertEqual(set(g.bolum), {"sema_surumu", "olgular", "ozet"})
        self.assertTrue(all(o["guven"] == uretec.TAM_GUVEN and o["kaynak"] == uretec.KAYNAK for o in g.bolum["olgular"]))

    def test_her_gozlem_gercek_agacta_dogru_ve_cift_basina_bir(self):
        for tohum in range(12):
            g = uret(tohum)
            geri = {v: k for k, v in g.kimlik_esleme.items()}
            ciftler = [(o["ozne"], o["nesne"]) for o in g.bolum["olgular"]]
            self.assertEqual(len(ciftler), len(set(ciftler)))
            for o in g.bolum["olgular"]:
                with self.subTest(tohum=tohum, olgu=o):
                    self.assertEqual(g.dunya.iliski(geri[o["ozne"]], geri[o["nesne"]], t1.TANIM), o["iliski"])

    def test_kisiler_arasindaki_butun_iliskiler_gozlenir(self):
        g = uret(2)
        geri = {v: k for k, v in g.kimlik_esleme.items()}
        kisiler = set(geri.values())
        beklenen = {(x, r, y) for x in kisiler for y, r in g.dunya.iliskiler(x, t1.TANIM).items() if y in kisiler}
        self.assertEqual({(geri[o["ozne"]], o["iliski"], geri[o["nesne"]]) for o in g.bolum["olgular"]}, beklenen)

    def test_dikkat_dagitici_baglar_kisi_ekler(self):
        """Kişiler yalnız zincirden gelmez: eğitim uzunluğundaki zincirin kişi sayısını aşan bölümler vardır."""
        en_cok_zincir = t1.PRM.egitim_k[1] + 1
        self.assertTrue(any(len(uret(t).kimlik_esleme) > en_cok_zincir for t in range(8)))

    def test_turetilmis_ve_temel_iliskiler_birlikte(self):
        temel = set(t1.TANIM.olgu_iliskileri)
        iliskiler = {o["iliski"] for t in range(12) for o in uret(t).bolum["olgular"]}
        self.assertTrue(iliskiler - temel)
        self.assertTrue(iliskiler & temel)

    def test_belirlenimli_ve_ozet_tutar(self):
        from cekirdek.altyapi.kanonik import kanonik_json, ozet
        a, b = uret(3), uret(3)
        self.assertEqual(a.bolum, b.bolum)
        govde = {k: v for k, v in a.bolum.items() if k != "ozet"}
        self.assertEqual(a.bolum["ozet"], ozet(kanonik_json(govde), t1.PRM.algoritma))
        self.assertNotEqual(uret(4).bolum["ozet"], a.bolum["ozet"])

    def test_uzun_zincirli_ortam_daha_buyuk(self):
        kisa = sum(len(uret(t).bolum["olgular"]) for t in range(8))
        uzun = sum(len(uret(t, t1.PRM.test_k).bolum["olgular"]) for t in range(8))
        self.assertGreater(uzun, kisa)

    def test_gozlem_bolumleri_tohumdan(self):
        a = uretec.gozlem_bolumleri(t1.TANIM, t1.PRM, "olagan", 3, t1.PRM.egitim_k)
        self.assertEqual(a, uretec.gozlem_bolumleri(t1.TANIM, t1.PRM, "olagan", 3, t1.PRM.egitim_k))
        self.assertEqual(len({b["ozet"] for b in a}), 3)
        self.assertNotEqual(a, uretec.gozlem_bolumleri(t1.TANIM, t1.PRM, "kaydirilmis", 3, t1.PRM.egitim_k))


if __name__ == "__main__":
    unittest.main()
