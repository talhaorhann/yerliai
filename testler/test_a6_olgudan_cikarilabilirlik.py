"""V-053, K-032 §3: olgulardan çıkarılabilirlik. Dünya verilmez: yalnız olgular, sorgu ve beklenen cevap.

Dünya varsayımları: her kişinin ya hiç ebeveyni yoktur ya da birbiriyle evli iki ebeveyni vardır; en çok bir evlilik;
eşler karşı cinsten. Bunların ve olguların zorunlu kıldığı yapı kurulur (çocuğun iki ebeveyni eştir, bir kişinin
bütün çocukları aynı çiftindir, kardeşlerin ebeveynleri ortaktır); cinsiyetlerin olgulara uyan bütün atamalarında
cevap aynıysa soru çıkarılabilirdir. Bağımsız denetim: küçük örneklerde varsayımlara uyan BÜTÜN dünyaları sayan
kaba kuvvet. Testlerde ilişki adı yazılmaz (KODLAMA_PROMPTU §2.4): anlamsız adlı tanım kümesi.
"""
import dataclasses
import itertools
import random
import unittest
from unittest import mock

from degerlendirme import uretec
from degerlendirme.dunya import (ASAGI, ES, YUKARI, CokluIliskiHatasi, Dunya, OlguTutarsizHatasi,
                                 olgudan_cikarilabilir_mi)
from testler.test_a5_cikarilabilirlik import TANIM
import testler.test_a1_uretec as t1


class ElleTesti(unittest.TestCase):
    def bak(self, olgular, sorgu, cevap):
        return olgudan_cikarilabilir_mi(TANIM, olgular, sorgu, cevap)

    def test_olgularda_gorunmeyen_evlilik_kullanilmaz(self):
        """ÖK-003'teki örnek: 15'in cinsiyetini yalnız 14 ile evliliği belirler, ama bu evlilik olgularda yok."""
        olgular = [(15, "alt0", 30), (30, "kar0", 29), (12, "kar1", 14)]
        self.assertFalse(self.bak(olgular, (29, 15), "ust0"))
        self.assertFalse(self.bak(olgular, (29, 15), "ust1"))
        self.assertTrue(self.bak(olgular + [(14, "ess", 15)], (29, 15), "ust0"))

    def test_cocugun_iki_ebeveyni_estir(self):
        self.assertTrue(self.bak([(3, "ust1", 1), (2, "alt1", 3)], (3, 2), "ust0"))
        self.assertFalse(self.bak([(2, "alt1", 3)], (3, 2), "ust0"))

    def test_kardeslerin_ebeveynleri_ortak_ve_evli(self):
        olgular = [(1, "ust0", 7), (1, "kar1", 2), (8, "alt1", 2)]
        self.assertTrue(self.bak(olgular, (2, 7), "ust0"))
        self.assertTrue(self.bak(olgular, (2, 8), "ust1"))  # 8, 7 ile evli olmak zorunda: tip 1
        self.assertFalse(self.bak([(1, "ust0", 7), (8, "alt1", 2)], (2, 8), "ust1"))

    def test_bir_kisinin_cocuklari_ayni_ciftin(self):
        olgular = [(5, "alt1", 1), (5, "alt0", 2), (1, "ust1", 6)]
        self.assertTrue(self.bak(olgular, (2, 6), "ust1"))
        self.assertTrue(self.bak(olgular, (2, 5), "ust0"))

    def test_zorunlu_yapi_tek_evlilik(self):
        """Bir kişinin çocukları aynı çiftindir: eşi bilinmese de iki çocuğun ebeveyn çifti aynıdır, evlilik bakışımlıdır."""
        from degerlendirme.dunya import zorunlu_dunya
        dunya, kimlik = zorunlu_dunya(TANIM, [(5, "alt1", 1), (5, "alt0", 2)], (1, 2))
        self.assertEqual(dunya.ebeveynler[kimlik[1]], dunya.ebeveynler[kimlik[2]])
        self.assertTrue(all(dunya.es[dunya.es[p]] == p for p in dunya.es))

    def test_cinsiyet_baska_olgudan(self):
        """ÖK-003'teki açıklanamayan 6 hatanın deseni: kişinin cinsiyeti zincir dışındaki bir olgudan gelir."""
        olgular = [(27, "alt0", 12), (13, "ess", 27), (8, "alt1", 27)]
        self.assertTrue(self.bak(olgular, (12, 13), "ust0"))
        self.assertFalse(self.bak(olgular[:2], (12, 13), "ust0"))

    def test_yanlis_cevap_cikarilamaz(self):
        self.assertFalse(self.bak([(3, "ust1", 1)], (3, 1), "ust0"))

    def test_bagli_olmayan_sorgu_cikarilamaz(self):
        self.assertFalse(self.bak([(3, "ust1", 1), (5, "ust1", 4)], (3, 4), "buyuk1"))

    def test_tutarsiz_olgu_reddedilir(self):
        for olgular in ([(3, "ust1", 1), (4, "ust0", 1)], [(1, "ess", 2), (1, "ess", 3)],
                        [(3, "ust1", 1), (3, "ust1", 2), (3, "ust0", 4)], [(1, "ess", 2), (5, "alt1", 1), (6, "alt1", 2)]):
            with self.subTest(olgular=olgular), self.assertRaises(OlguTutarsizHatasi):
                self.bak(olgular, (olgular[0][0], olgular[0][2]), "ust1")

    def test_dunya_ve_cekirdek_kullanilmaz(self):
        with mock.patch("cekirdek.dongu.calistir", side_effect=AssertionError("çekirdek çağrıldı")), \
                mock.patch.object(Dunya, "uret", side_effect=AssertionError("gerçek dünya kuruldu")):
            self.assertTrue(self.bak([(3, "ust1", 1), (2, "alt1", 3)], (3, 2), "ust0"))


# --- bağımsız kaba kuvvet ------------------------------------------------------------------------------------------

def _desen(tanimlar, iliski):
    adimlar = tanimlar.secenekler[iliski][0]
    return tuple(y for y, _ in adimlar), adimlar[-1][1]


def _eslesmeler(dugumler):
    if not dugumler:
        yield ()
        return
    ilk, kalan = dugumler[0], dugumler[1:]
    yield from _eslesmeler(kalan)
    for i, d in enumerate(kalan):
        for e in _eslesmeler(kalan[:i] + kalan[i + 1:]):
            yield ((ilk, d),) + e


def _atasi(ebeveyn, x):
    gorulen, yigin = set(), list(ebeveyn.get(x, ()))
    while yigin:
        a = yigin.pop()
        if a == x:
            return True
        if a not in gorulen:
            gorulen.add(a)
            yigin.extend(ebeveyn.get(a, ()))
    return False


def kaba_cevaplar(tanimlar, olgular, sorgu, adsiz):
    """Adlı kişiler + `adsiz` düğüm üzerinde varsayımlara uyan ve olguları tam doğrulayan bütün dünyalarda sorgu ilişkisi.

    Budama yalnız olgunun doğru olması için gerekli yapı koşullarıyladır; yeterlilik `iliskiler` ile denetlenir."""
    adlar = sorted({x for x, _, y in olgular} | {y for x, _, y in olgular} | set(sorgu))
    k = {a: i for i, a in enumerate(adlar)}
    n = len(adlar) + adsiz
    bic = [(k[x], *_desen(tanimlar, r), k[y], r) for x, r, y in olgular]
    cevaplar = set()
    for es_ciftleri in _eslesmeler(list(range(n))):
        es = {}
        for a, b in es_ciftleri:
            es[a], es[b] = b, a
        if any(yon == (ES,) and es.get(x) != y for x, yon, _t, y, _r in bic):
            continue
        ciftler = list(es_ciftleri)
        for secim in itertools.product(range(len(ciftler) + 1), repeat=n):
            ebeveyn = {x: ciftler[s - 1] for x, s in enumerate(secim) if s}
            if any(x in ebeveyn[x] for x in ebeveyn) or any(_atasi(ebeveyn, x) for x in ebeveyn):
                continue
            if not all((yon != (YUKARI,) or y in ebeveyn.get(x, ())) and (yon != (ASAGI,) or x in ebeveyn.get(y, ()))
                       and (yon != (YUKARI, ASAGI) or (x in ebeveyn and ebeveyn.get(y) == ebeveyn[x]))
                       for x, yon, _t, y, _r in bic):
                continue
            bekarlar = [d for d in range(n) if d not in es]
            for bitler in itertools.product((0, 1), repeat=len(ciftler) + len(bekarlar)):
                tip = [0] * n
                for (a, b), t in zip(ciftler, bitler):
                    tip[a], tip[b] = t, 1 - t
                for d, t in zip(bekarlar, bitler[len(ciftler):]):
                    tip[d] = t
                w = Dunya(tip, ebeveyn, es)
                try:
                    if all(w.iliskiler(x, tanimlar, tanimlar.olgu_iliskileri).get(y) == r for x, _y, _t, y, r in bic):
                        cevaplar.add(w.iliski(k[sorgu[0]], k[sorgu[1]], tanimlar))
                except CokluIliskiHatasi:
                    continue
    return cevaplar


class KabaKuvvetTesti(unittest.TestCase):
    ORNEK = 24  # V-053: test süresini sınırlar (bütün dünyalar sayılır)
    DUGUM = 6  # V-053: kaba kuvvetin düğüm sınırı

    def test_elle_ornekler_kaba_kuvvetle_ayni(self):
        for olgular, sorgu, cevap, adsiz in [
                ([(15, "alt0", 30), (2, "alt1", 14)], (30, 15), "ust0", 2),
                ([(3, "ust1", 1), (2, "alt1", 3)], (3, 2), "ust0", 0),
                ([(1, "ust0", 7), (1, "kar1", 2), (8, "alt1", 2)], (2, 8), "ust1", 0)]:
            with self.subTest(olgular=olgular):
                self.assertEqual(kaba_cevaplar(TANIM, olgular, sorgu, adsiz) == {cevap},
                                 olgudan_cikarilabilir_mi(TANIM, olgular, sorgu, cevap))

    def test_kucuk_uretilmis_bolumlerde_kaba_kuvvetle_ayni(self):
        from degerlendirme.dunya import zorunlu_dunya
        prm = dataclasses.replace(uretec.Parametreler.ayardan(t1.AYAR), nesil_sayisi=3, cocuk_en_az=1, cocuk_en_cok=2,
                                  dikkat_dagitici=1)
        rng, sayac, ikisi = random.Random(53), 0, set()
        while sayac < self.ORNEK:
            a = uretec.aday_uret(rng, t1.TANIM, prm, rng.choice(["egitim", "yon_ters"]))
            olgular = [(o["ozne"], o["iliski"], o["nesne"]) for o in a.bolum["olgular"]]
            sorgu = (a.bolum["sorgu"]["ozne"], a.bolum["sorgu"]["nesne"])
            dunya, kimlik = zorunlu_dunya(t1.TANIM, olgular, sorgu)
            if dunya.kisi_sayisi > self.DUGUM:
                continue
            sayac += 1
            beklenen = kaba_cevaplar(t1.TANIM, olgular, sorgu, dunya.kisi_sayisi - len(kimlik)) == {a.cevap["cevap"]}
            ikisi.add(beklenen)
            with self.subTest(olgular=olgular, sorgu=sorgu):
                self.assertEqual(olgudan_cikarilabilir_mi(t1.TANIM, olgular, sorgu, a.cevap["cevap"]), beklenen)
        self.assertEqual(ikisi, {True, False})  # iki sonuç da sınandı


if __name__ == "__main__":
    unittest.main()
