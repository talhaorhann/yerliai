"""K-015, K-022, V-040, KODLAMA_PROMPTU §4–§5: PyTorch hızlı yolu = saf Python referans yolu, bit düzeyinde.

Tamsayılar doğrudan, kayan noktalılar `float.hex` ile karşılaştırılır (bit düzeyinde eşitlikte `==` kullanılmaz).
Eksen boyları bilerek farklıdır (7, 11, 13); boş ve tek öğe sınanır. İlişki adları anlamsızdır.
"""
import math
import random
import unittest

import torch

from cekirdek import vektor as V
from cekirdek import vektor_hizli as H
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.eslesme import afinite, alici
from cekirdek.sekiller import SekilHatasi
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")
D = AYAR.deger("vektor_boyutu")
KK = V.KodKitabi(AYAR.deger("vektor_tohum"), D)
ILISKILER = [f"r{i}" for i in range(5)]


def uclular(n, tohum):
    rng = random.Random(tohum)
    return [(rng.randrange(100), rng.choice(ILISKILER), rng.randrange(100)) for _ in range(n)]


def hexler(matris):
    return [[float(x).hex() for x in satir] for satir in matris]


class SurumTesti(unittest.TestCase):
    def test_sabit_surum_ve_cpu(self):
        self.assertEqual(torch.__version__, AYAR.deger("torch_surumu"))
        self.assertIsNone(torch.version.cuda)  # K-022: CPU tekerleği


class KodKitabiTesti(unittest.TestCase):
    def test_vektor_tensoru_referansla_ayni(self):
        adlar = list(range(13))
        t = H.vektor_tensoru(KK, "varlik", adlar)
        self.assertEqual(t.dtype, torch.int64)
        self.assertEqual(t.tolist(), [list(KK.vektor("varlik", a)) for a in adlar])
        self.assertEqual(tuple(H.vektor_tensoru(KK, "varlik", []).shape), (0, D))


class EvrisimTesti(unittest.TestCase):
    def test_elle_hesaplanmis_ornekler(self):
        e = torch.tensor([[1, 2, 3, 4]])
        self.assertEqual(H.evrisim_toplu(torch.tensor([1, 0, 0, 0]), e).tolist(), [[1, 2, 3, 4]])
        self.assertEqual(H.evrisim_toplu(torch.tensor([0, 1, 0, 0]), e).tolist(), [[4, 1, 2, 3]])
        self.assertEqual(H.evrisim_toplu(torch.tensor([1, -1, 1, 1]), torch.tensor([[1, 1, -1, 1]])).tolist(),
                         [[0, 0, 0, 4]])

    def test_referansla_ayni(self):
        p = KK.vektor("rol", "ozne")
        for n in (7, 11, 13, 1, 0):
            satirlar = [KK.vektor("varlik", i) for i in range(n)]
            e = torch.tensor(satirlar, dtype=torch.int64).reshape(n, D)
            hizli = H.evrisim_toplu(torch.tensor(p, dtype=torch.int64), e)
            self.assertEqual(hizli.tolist(), [list(V.evrisim(p, s)) for s in satirlar])

    def test_yalniz_int64_ve_dogru_sekil(self):
        with self.assertRaises(SekilHatasi):
            H.evrisim_toplu(torch.ones(D, dtype=torch.float64), torch.ones(7, D, dtype=torch.float64))
        with self.assertRaises(SekilHatasi):
            H.evrisim_toplu(torch.ones(D, dtype=torch.int64), torch.ones(7, D + 1, dtype=torch.int64))
        with self.assertRaises(SekilHatasi):
            H.evrisim_toplu(torch.ones(D, dtype=torch.int64), torch.ones(7, 11, D, dtype=torch.int64))
        with self.assertRaises(SekilHatasi):  # fazla eksen; son iki eksenin boyu tek başına doğru görünür
            H.evrisim_toplu(torch.ones(D, dtype=torch.int64), torch.ones(7, D, D, dtype=torch.int64))


class KayitMatrisiTesti(unittest.TestCase):
    def test_referansla_ayni(self):
        for n, tohum in ((13, 7), (7, 11), (1, 13)):
            u = uclular(n, tohum)
            hizli = H.kayit_matrisi_hizli(KK, u)
            self.assertEqual(hizli.dtype, torch.int64)
            self.assertEqual(hizli.tolist(), [list(v) for v in V.kayit_matrisi(KK, u)])
        self.assertEqual(tuple(H.kayit_matrisi_hizli(KK, []).shape), (0, D))


class BenzerlikTesti(unittest.TestCase):
    def test_bit_duzeyinde_ayni(self):
        for (na, ta), (nb, tb) in (((7, 7), (11, 11)), ((1, 13), (1, 17)), ((13, 19), (13, 19))):
            ua, ub = uclular(na, ta), uclular(nb, tb)
            hizli = H.benzerlik_matrisi_hizli(H.kayit_matrisi_hizli(KK, ua), H.kayit_matrisi_hizli(KK, ub))
            self.assertEqual(hizli.dtype, torch.float64)
            self.assertEqual(hexler(hizli.tolist()), hexler(V.benzerlik_matrisi(V.kayit_matrisi(KK, ua),
                                                                               V.kayit_matrisi(KK, ub))))

    def test_bos_ve_sifir_vektor(self):
        b = H.kayit_matrisi_hizli(KK, uclular(11, 7))
        self.assertEqual(tuple(H.benzerlik_matrisi_hizli(torch.zeros(0, D, dtype=torch.int64), b).shape), (0, 11))
        with self.assertRaises(ValueError):
            H.benzerlik_matrisi_hizli(torch.zeros(1, D, dtype=torch.int64), b)

    def test_yalniz_int64_ve_dogru_sekil(self):
        b = H.kayit_matrisi_hizli(KK, uclular(11, 7))
        with self.assertRaises(SekilHatasi):
            H.benzerlik_matrisi_hizli(b.to(torch.float64), b.to(torch.float64))
        with self.assertRaises(SekilHatasi):
            H.benzerlik_matrisi_hizli(b, b.to(torch.float64))
        with self.assertRaises(SekilHatasi):
            H.benzerlik_matrisi_hizli(b.unsqueeze(0), b)


class DogruKokTesti(unittest.TestCase):
    def test_kok_dogru_yuvarlanmis(self):
        """torch.sqrt'ün 1 ulp saptığı ölçülmüş değer dahil: kök, kesin rasyonel hesapla doğru yuvarlanmış olmalı."""
        from fractions import Fraction
        degerler = [36912709632, 40243688448, 35965771776, 41261612032, 1, 2, 65536, 2 ** 52 - 1]
        kokler = H.dogru_kok(torch.tensor(degerler, dtype=torch.int64)).tolist()
        for x, k in zip(degerler, kokler):
            self.assertEqual(k.hex(), math.sqrt(x).hex())
            asagi, yukari = Fraction(math.nextafter(k, 0.0)), Fraction(math.nextafter(k, math.inf))
            self.assertLessEqual(((asagi + Fraction(k)) / 2) ** 2, x)
            self.assertGreaterEqual(((Fraction(k) + yukari) / 2) ** 2, x)
        self.assertEqual(tuple(H.dogru_kok(torch.zeros(0, 11, dtype=torch.int64)).shape), (0, 11))


class TasmaTesti(unittest.TestCase):
    def test_float64_tam_siniri_asilirsa_durur(self):
        """Taşma denetimi çarpımdan önce yapılır; int64 taşmasıyla yanlış sonuç sessizce üretilmez (V-040)."""
        b = H.kayit_matrisi_hizli(KK, uclular(7, 7))
        for ogeler in (2 ** 20, 2 ** 27):
            buyuk = torch.full((7, D), ogeler, dtype=torch.int64)
            with self.assertRaisesRegex(ValueError, "V-040"):
                H.benzerlik_matrisi_hizli(buyuk, b)
            with self.assertRaisesRegex(ValueError, "V-040"):
                H.benzerlik_matrisi_hizli(buyuk, buyuk)
        # int64 sarması: 2**32'nin karesi 2**64 ≡ 0 olur, norm küçük görünür; denetim yine durdurmalı.
        sarmali = torch.ones((1, D), dtype=torch.int64)
        sarmali[0, 0] = 2 ** 32
        with self.assertRaisesRegex(ValueError, "V-040"):
            H.benzerlik_matrisi_hizli(sarmali, b)


class AfiniteTesti(unittest.TestCase):
    def test_afinite_matrisi_bit_duzeyinde_ayni(self):
        u = uclular(13, 7)
        alicilar = [alici(KK, r) for r in ILISKILER]
        hizli = H.afinite_matrisi_hizli(H.kayit_matrisi_hizli(KK, u), torch.tensor(alicilar, dtype=torch.int64))
        referans = [[afinite(a, v) for a in alicilar] for v in V.kayit_matrisi(KK, u)]
        self.assertEqual(hexler(hizli.tolist()), hexler(referans))
        self.assertTrue(bool(((hizli >= 0) & (hizli <= 1)).all()))


class BelirlenimTesti(unittest.TestCase):
    def test_is_parcacigi_sayisi_sonucu_degistirmez(self):
        onceki = torch.get_num_threads()
        try:
            sonuclar = []
            for sayi in (1, 4):
                torch.set_num_threads(sayi)
                m = H.kayit_matrisi_hizli(KK, uclular(13, 7))
                sonuclar.append((m.tolist(), hexler(H.benzerlik_matrisi_hizli(m, m).tolist())))
            self.assertEqual(sonuclar[0], sonuclar[1])
        finally:
            torch.set_num_threads(onceki)

    def test_gradyan_izlenmez(self):
        m = H.kayit_matrisi_hizli(KK, uclular(7, 7))
        self.assertFalse(m.requires_grad)
        self.assertFalse(H.benzerlik_matrisi_hizli(m, m).requires_grad)


if __name__ == "__main__":
    unittest.main()
