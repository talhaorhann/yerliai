"""K-041 (ÖK-005 taslağı §13.6, §4 madde 7, 13), V-065: veto ikizi ve null için derece-koruyan yeniden bağlama.
Simetrik ilişkide kenar yönsüz alınır, iki yönü birlikte yazılır; tersler yazılmaz. `kenar_bagla` tek ilişkinin kenar
listesini, öteki ilişkiler sabitken bağlar (Westfall–Young çekilişlerinde dünya kopyalanmadan). İlişki adı yazılmaz."""
import random
import unittest
from collections import Counter

from cekirdek.altyapi.ayar import ayar_yukle
from degerlendirme import h1, h2_bagla, h2_dunya
from degerlendirme.dunya import tanimlar_yukle
from testler.yardimci import KOK

H2 = ayar_yukle(KOK / "config_h2.json")
_, SEMA, _ = h1._ortam(KOK)
TANIMLAR = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                          KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", SEMA)
DUNYA = h2_dunya.aile_dunyasi("A1", H2.deger("dunya_aileleri")["A1"], 77, TANIMLAR)
CARPAN = H2.deger("bagla_deneme_carpani")


def dereceler(kenarlar):
    return Counter(a for a, _ in kenarlar), Counter(b for _, b in kenarlar)


def iliski_kenarlari(olgular, r):
    return {(a, b) for a, rr, b in olgular if rr == r}


class VetoBaglamaTesti(unittest.TestCase):
    def test_simetrik_iliski_simetrik_kalir(self):
        s = next(a for a in SEMA.adlar if SEMA.simetrik(a) and iliski_kenarlari(DUNYA.olgular, a))
        yeni = h2_bagla.yeniden_bagla(DUNYA.olgular, {s}, SEMA, random.Random(4), False, CARPAN)
        k = iliski_kenarlari(yeni, s)
        self.assertEqual(k, {(b, a) for a, b in k})
        self.assertNotEqual(k, iliski_kenarlari(DUNYA.olgular, s))
        self.assertEqual(dereceler(k), dereceler(iliski_kenarlari(DUNYA.olgular, s)))
        self.assertEqual({o for o in yeni if o[1] != s}, {o for o in DUNYA.olgular if o[1] != s})


class KenarBaglaTesti(unittest.TestCase):
    def _kontrol(self, r):
        eski = sorted(iliski_kenarlari(DUNYA.olgular, r))
        dolu = h2_bagla.dolu_ciftler(DUNYA.olgular, r, SEMA)
        yeni = h2_bagla.kenar_bagla(eski, dolu, SEMA.simetrik(r), random.Random(9), CARPAN)
        self.assertEqual(dereceler(yeni), dereceler(eski))
        self.assertFalse(any(a == b for a, b in yeni))
        self.assertFalse(set(yeni) & dolu, "başka ilişkinin çiftine yazıldı")
        self.assertEqual(len(set(yeni)), len(eski))
        self.assertNotEqual(set(yeni), set(eski))
        return yeni

    def test_yonlu_ve_simetrik(self):
        r = max((a for a in SEMA.adlar if not SEMA.simetrik(a)), key=lambda a: len(iliski_kenarlari(DUNYA.olgular, a)))
        self._kontrol(r)
        s = max((a for a in SEMA.adlar if SEMA.simetrik(a)), key=lambda a: len(iliski_kenarlari(DUNYA.olgular, a)))
        k = set(self._kontrol(s))
        self.assertEqual(k, {(b, a) for a, b in k})

    def test_belirlenimci_ve_veto_ile_ayni(self):
        r = SEMA.adlar[0]
        eski = sorted(iliski_kenarlari(DUNYA.olgular, r))
        dolu = h2_bagla.dolu_ciftler(DUNYA.olgular, r, SEMA)
        a = h2_bagla.kenar_bagla(eski, dolu, False, random.Random(5), CARPAN)
        self.assertEqual(a, h2_bagla.kenar_bagla(eski, dolu, False, random.Random(5), CARPAN))
        veto = h2_bagla.yeniden_bagla(DUNYA.olgular, {r}, SEMA, random.Random(5), False, CARPAN)
        self.assertEqual(set(a), iliski_kenarlari(veto, r))


if __name__ == "__main__":
    unittest.main()
