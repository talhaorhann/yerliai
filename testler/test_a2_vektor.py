"""sistem.md §1, §3; K-014, K-015, V-026: tamsayı HRR/VSA referans yolu (saf Python) ve SEKILLER tablosu.

Beklenen değerler kodun çıktısından değil, elle hesaplanmış örneklerden ve matematiksel özelliklerden gelir.
Testlerde ilişki adları anlamsızdır ("r0", "r1", ...).
"""
import ast
import hashlib
import json
import os
import random
import subprocess
import sys
import unittest

from cekirdek import vektor as V
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.sekiller import SEKILLER, SekilHatasi, sekil, sekil_dogrula
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")
D = AYAR.deger("vektor_boyutu")
KK = V.KodKitabi(AYAR.deger("vektor_tohum"), D)
SIGMA_SAYISI = 5  # V-026


class SekillerTesti(unittest.TestCase):
    def test_tablo_eksen_anlamlari(self):
        for eksen in ("boyut", "kayit", "aday"):
            self.assertIn(eksen, SEKILLER)
            self.assertTrue(SEKILLER[eksen])

    def test_sekil(self):
        self.assertEqual(sekil([]), (0,))
        self.assertEqual(sekil([[1, 2, 3]] * 7), (7, 3))
        self.assertEqual(sekil([[[0] * 13] * 11] * 7), (7, 11, 13))
        with self.assertRaises(SekilHatasi):
            sekil([[1, 2], [3]])

    def test_sekil_dogrula(self):
        x = [[0] * 13] * 11
        self.assertIs(sekil_dogrula(x, ("kayit", "boyut"), kayit=11, boyut=13), x)
        with self.assertRaises(SekilHatasi):
            sekil_dogrula(x, ("kayit", "boyut"), kayit=11, boyut=7)
        with self.assertRaises(SekilHatasi):
            sekil_dogrula(x, ("boyut",))
        with self.assertRaises(SekilHatasi):
            sekil_dogrula(x, ("kayit", "uydurma_eksen"))
        sekil_dogrula([], ("kayit", "boyut"), kayit=0, boyut=13)


class KodKitabiTesti(unittest.TestCase):
    def test_bagimsiz_turetim_ile_ayni(self):
        """Bitler SHAKE-256("tohum|tür|ad") çıktısından; 1 → +1, 0 → −1 (V-026). Test kendi başına türetir."""
        tohum = AYAR.deger("vektor_tohum")
        baytlar = hashlib.shake_256(f"{tohum}|varlik|7".encode("utf-8")).digest(D // 8)
        beklenen = tuple(1 if (baytlar[i // 8] >> (i % 8)) & 1 else -1 for i in range(D))
        self.assertEqual(KK.vektor("varlik", 7), beklenen)
        self.assertEqual(KK.vektor("varlik", "7"), beklenen)

    def test_pm1_uzunluk_denge(self):
        for i in range(13):
            v = KK.vektor("varlik", i)
            self.assertEqual(len(v), D)
            self.assertEqual(set(v), {-1, 1})
            self.assertLess(abs(sum(v)), SIGMA_SAYISI * D ** 0.5)

    def test_tur_ve_tohum_ayirt_edici(self):
        self.assertNotEqual(KK.vektor("varlik", 7), KK.vektor("iliski", 7))
        self.assertNotEqual(KK.vektor("varlik", 7), KK.vektor("varlik", 11))
        self.assertNotEqual(KK.vektor("varlik", 7), V.KodKitabi(AYAR.deger("vektor_tohum") + 1, D).vektor("varlik", 7))

    def test_surecten_surece_ayni(self):
        """Python'un hash() rastgeleliğine bağlı olmamalı: farklı PYTHONHASHSEED ile aynı vektör."""
        kod = ("import json,sys; from cekirdek import vektor as V; "
               f"print(json.dumps(V.KodKitabi({AYAR.deger('vektor_tohum')}, {D}).vektor('iliski', 'r3')))")
        for tohum in ("1", "7"):
            r = subprocess.run([sys.executable, "-c", kod], cwd=KOK, capture_output=True, text=True,
                               env=dict(os.environ, PYTHONHASHSEED=tohum), timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(tuple(json.loads(r.stdout)), KK.vektor("iliski", "r3"))

    def test_gecersiz_boyut_reddedilir(self):
        for boyut in (100, 72, 0, -64):
            with self.assertRaises(ValueError):
                V.KodKitabi(7, boyut)
        self.assertEqual(V.KodKitabi(7, 64).olcek, 8)
        self.assertEqual(KK.olcek, 16)


class EvrisimTesti(unittest.TestCase):
    def test_elle_hesaplanmis_ornekler(self):
        self.assertEqual(V.evrisim((1, 2, 3, 4), (1, 0, 0, 0)), (1, 2, 3, 4))
        self.assertEqual(V.evrisim((1, 2, 3, 4), (0, 1, 0, 0)), (4, 1, 2, 3))
        self.assertEqual(V.evrisim((1, -1, 1, 1), (1, 1, -1, 1)), (0, 0, 0, 4))
        self.assertEqual(V.ters((1, 2, 3, 4)), (1, 4, 3, 2))

    def test_cebirsel_ozellikler(self):
        a, b, c = (KK.vektor("varlik", i) for i in (7, 11, 13))
        self.assertEqual(V.evrisim(a, b), V.evrisim(b, a))
        self.assertEqual(V.evrisim(V.evrisim(a, b), c), V.evrisim(a, V.evrisim(b, c)))
        toplam = tuple(x + y for x, y in zip(b, c))
        self.assertEqual(V.evrisim(a, toplam), tuple(x + y for x, y in zip(V.evrisim(a, b), V.evrisim(a, c))))

    def test_ters_ile_tepe(self):
        a = KK.vektor("rol", "ozne")
        tepe = V.evrisim(V.ters(a), a)
        self.assertEqual(tepe[0], D)

    def test_uzunluk_uyusmazligi_reddedilir(self):
        with self.assertRaises(SekilHatasi):
            V.evrisim((1, 2, 3), (1, 2))


class BenzerlikTesti(unittest.TestCase):
    def test_kosinus(self):
        a = KK.vektor("varlik", 7)
        self.assertEqual(V.kosinus(a, a), 1.0)
        self.assertEqual(V.kosinus(a, tuple(-x for x in a)), -1.0)
        self.assertEqual(V.nokta((1, 2, 3), (4, -5, 6)), 12)
        with self.assertRaises(ValueError):
            V.kosinus((0, 0, 0), (1, 2, 3))

    def test_yari_diklik(self):
        vs = [KK.vektor("varlik", i) for i in range(100)]
        sinir = SIGMA_SAYISI / D ** 0.5
        en_buyuk = max(abs(V.kosinus(vs[i], vs[j])) for i in range(100) for j in range(i))
        self.assertLess(en_buyuk, sinir)

    def test_benzerlik_matrisi_sekil_ve_deger(self):
        A = V.kayit_matrisi(KK, [(i, "r0", i + 1) for i in range(7)])
        B = V.kayit_matrisi(KK, [(i, "r1", i + 2) for i in range(11)])
        M = V.benzerlik_matrisi(A, B)
        self.assertEqual(sekil(M), (7, 11))
        self.assertEqual(M[3][5], V.kosinus(A[3], B[5]))
        self.assertEqual(V.benzerlik_matrisi([], B), [])
        self.assertEqual(sekil(V.benzerlik_matrisi(A[:1], B[:1])), (1, 1))


class KayitVektoruTesti(unittest.TestCase):
    def test_tanim(self):
        s, r, o = 7, "r3", 11
        beklenen = tuple(KK.olcek * x + y + z for x, y, z in zip(
            KK.vektor("iliski", r),
            V.evrisim(KK.vektor("rol", "ozne"), KK.vektor("varlik", s)),
            V.evrisim(KK.vektor("rol", "nesne"), KK.vektor("varlik", o))))
        self.assertEqual(V.kayit_vektoru(KK, s, r, o), beklenen)

    def test_bilesen_olcekleri(self):
        R = tuple(KK.olcek * x for x in KK.vektor("iliski", "r0"))
        for i in range(7):
            pe = V.evrisim(KK.vektor("rol", "ozne"), KK.vektor("varlik", i))
            oran = V.nokta(pe, pe) / V.nokta(R, R)
            self.assertTrue(0.5 <= oran <= 2, oran)  # V-026

    def test_rol_bagi_asimetrik_ve_girdiye_duyarli(self):
        v = V.kayit_vektoru(KK, 7, "r3", 11)
        self.assertNotEqual(v, V.kayit_vektoru(KK, 11, "r3", 7))
        self.assertNotEqual(v, V.kayit_vektoru(KK, 7, "r4", 11))
        self.assertNotEqual(v, V.kayit_vektoru(KK, 7, "r3", 13))

    def test_ilgisiz_kayit_degisince_satir_sabit(self):
        uclular = [(i, f"r{i % 3}", i + 1) for i in range(13)]
        M1 = V.kayit_matrisi(KK, uclular)
        uclular[5] = (99, "r2", 98)
        M2 = V.kayit_matrisi(KK, uclular)
        for i in range(13):
            (self.assertNotEqual if i == 5 else self.assertEqual)(M1[i], M2[i])
        self.assertEqual(sekil(M1), (13, D))
        self.assertEqual(V.kayit_matrisi(KK, []), [])

    def test_cozme(self):
        """60 kayıtta özne, nesne ve ilişki %100 geri bulunur (V-026)."""
        rng = random.Random(13)
        varliklar = list(range(100))
        iliskiler = [f"r{i}" for i in range(21)]
        for _ in range(60):
            s, o = rng.sample(varliklar, 2)
            r = rng.choice(iliskiler)
            v = V.kayit_vektoru(KK, s, r, o)
            self.assertEqual(V.coz(KK, v, "ozne", varliklar), s)
            self.assertEqual(V.coz(KK, v, "nesne", varliklar), o)
            self.assertEqual(V.iliski_coz(KK, v, iliskiler), r)

    def test_bilinmeyen_rol_reddedilir(self):
        with self.assertRaises(ValueError):
            V.coz(KK, V.kayit_vektoru(KK, 7, "r0", 11), "uydurma", [7, 11])


class ReferansSafPythonTesti(unittest.TestCase):
    def test_referans_yol_yalniz_standart_kutuphane(self):
        for ad in ("vektor.py", "sekiller.py"):
            agac = ast.parse((KOK / "cekirdek" / ad).read_text(encoding="utf-8"))
            for d in ast.walk(agac):
                if isinstance(d, (ast.Import, ast.ImportFrom)):
                    adlar = [a.name for a in d.names] if isinstance(d, ast.Import) else [d.module or ""]
                    for a in adlar:
                        self.assertNotIn(a.split(".")[0], {"torch", "numpy"}, ad)


if __name__ == "__main__":
    unittest.main()
