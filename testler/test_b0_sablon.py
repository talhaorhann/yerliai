"""K-041, ÖK-005 taslağı §5 (tohum türetme), §6 (tipli şablon ailesi T ve kademeleri K1–K5): sayılar kâğıt üstü hesapla
(`H2_TASARIM.md` §6.1) aynı olmalı; şablonun kanonik biçimi depodaki `kanonik_bicim` ile ikinci yoldan doğrulanır.
İlişki adları anlamsızdır (sayılar yalnız ilişki sayısına bağlıdır)."""
import hashlib
import unittest

from cekirdek.altyapi.ayar import ayar_yukle
from kesif import aday as ad
from kesif import sablon, tohum
from testler.yardimci import KOK

H2 = ayar_yukle(KOK / "config_h2.json")
DEGISKENLER = tuple(H2.deger("sablon_degiskenleri"))
KADEMELER = H2.deger("sablon_kademeleri")
BAS_SAYISI = 21  # H2_TASARIM.md §6.1: baş her zaman şemanın 21 ilişkisinden biri


def adlar(n):
    return tuple(f"zr{chr(ord('a') + i)}" for i in range(n))


def kademe(ad_, iliski_sayisi):
    en_cok, zincir = KADEMELER[ad_]
    return sablon.govdeler(iliski_sayisi, DEGISKENLER, en_cok, zincir)


class TohumTesti(unittest.TestCase):
    def test_tohum_tanimi(self):
        onek, uzunluk = H2.deger("tohum_oneki"), H2.deger("tohum_hex_uzunlugu")
        beklenen = int(hashlib.sha256((onek + "havuz|gelistirme|A1|1").encode("utf-8")).hexdigest()[:uzunluk], 16)
        self.assertEqual(tohum.tohum(H2, "havuz", "gelistirme", "A1", 1), beklenen)

    def test_farkli_etiket_farkli_tohum_ve_aralik(self):
        t = {tohum.tohum(H2, "taze", "B2b", tur, "A1", j) for tur in range(1, 13) for j in range(1, 3)}
        self.assertEqual(len(t), 24)
        self.assertTrue(all(0 <= x < 16 ** H2.deger("tohum_hex_uzunlugu") for x in t))

    def test_parcada_ayirici_yasak(self):
        with self.assertRaises(ValueError):
            tohum.tohum(H2, "a|b", 1)


class SablonSayimTesti(unittest.TestCase):
    """`H2_TASARIM.md` §6.1 tablosu: (gövde, kural, OI'li kural)."""

    def test_kademe_sayilari(self):
        beklenen = {("K1", 21): (42, 861, 861), ("K2", 21): (1806, 37905, 74949), ("K3", 21): (6195, 127449, 236817),
                    ("K4", 7): (2954, 62027, 123767), ("K5", 7): (33593, 693833, 1322209)}
        for (k, m), (g, kural, oili) in beklenen.items():
            with self.subTest(kademe=k, iliski=m):
                govdeler = kademe(k, m)
                self.assertEqual(len(govdeler), g)
                self.assertEqual(sablon.sayim(govdeler, BAS_SAYISI), (kural, oili))

    def test_govde_kurallari(self):
        x, y = DEGISKENLER[:2]
        for g in kademe("K5", 2):
            degisken = {d for _, a, b in g for d in (a, b)}
            self.assertTrue({x, y} <= degisken)
            self.assertTrue(all(a != b for _, a, b in g))
            self.assertEqual(len(set(g)), len(g))
            self.assertEqual(g, tuple(sorted(g)))

    def test_bas_govdeyle_ayni_tek_halka_atilir(self):
        x, y = DEGISKENLER[:2]
        bas_listesi = {(g, b) for g, b, _ in sablon.adaylar(kademe("K1", 3), 3)}
        for r in range(3):
            self.assertNotIn((((r, x, y),), r), bas_listesi)
            self.assertIn((((r, y, x),), r), bas_listesi)
        z = DEGISKENLER[2]
        cok = {(g, b) for g, b, _ in sablon.adaylar(kademe("K3", 2), 2)}
        self.assertNotIn((((0, x, y), (1, y, z)), 0), cok)  # gövde başın kendisini içeremez
        self.assertIn((((0, x, y), (1, y, z)), 1), cok)

    def test_kanonik_kimlikler_tekil_ve_sablonla_ayni_sayida(self):
        """Şablonun kendi kanonik biçimi ile depodaki `kanonik_bicim` aynı sayıda farklı aday verir (ikinci yol)."""
        isimler = adlar(4)
        govdeler = kademe("K3", 4)
        kimlikler = {ad.kanonik_kimlik(sablon.aday_kaydi(g, b, oi, isimler, DEGISKENLER), "sha256")
                     for g, b, oi in sablon.adaylar(govdeler, 4)}
        self.assertEqual(len(kimlikler), sablon.sayim(govdeler, 4)[1])

    def test_aday_kaydi_semaya_uyar(self):
        isimler = adlar(3)
        for g, b, oi in list(sablon.adaylar(kademe("K5", 3), 3))[::997]:
            ad.aday_denetle(sablon.aday_kaydi(g, b, oi, isimler, DEGISKENLER), frozenset(isimler))

    def test_zincir_ve_oi(self):
        x, y, z, w = DEGISKENLER
        self.assertTrue(sablon.zincir_mi(((0, x, z), (1, w, y), (2, z, w)), DEGISKENLER))
        self.assertFalse(sablon.zincir_mi(((0, x, y), (1, x, z)), DEGISKENLER))
        self.assertTrue(sablon.oi_anlamli_mi(((0, x, z), (1, z, y))))
        self.assertFalse(sablon.oi_anlamli_mi(((0, x, y), (1, y, x))))


if __name__ == "__main__":
    unittest.main()
