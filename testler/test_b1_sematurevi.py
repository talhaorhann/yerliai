"""K-044 (ÖK-005 eki §4): "şema-türevi" kural testi ve (c) tanısının cinsiyet karıştırması.

- Şema-türevi: tetik testinde kullanılmamış, birbirinden bağımsız en az 20 taze boş dünyanın hepsinde sıfır ihlal.
  Dünyalar önkayıtlı etiketlerden (`sematurevi|<aile>|<i>`, `bos|sematurevi|<aile>|<i>`) türer.
- Cinsiyet ikizi: tanımın son belirli cinsiyet adımı çevrilince elde edilen ilişki (tanım dosyasından, mekanik).
- Karıştırma: her olgu bağımsız olarak yarı olasılıkla cinsiyet ikiziyle değişir (tohumlu).
İlişki adı yazılmaz; sentetik testler blorp şemasıyla, gerçek tanım dosyası yalnız yapısıyla sınanır.
"""
import json
import random
import unittest

from degerlendirme import h2_sematurevi as ST
from degerlendirme import kural
from testler import test_b1_gecit as tg
from testler.yardimci import KOK


class CinsiyetIkiziTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tanimlar = json.loads((KOK / "degerlendirme" / "veri" / "tanimlar_v1.json").read_text(encoding="utf-8"))
        cls.ikiz = ST.cinsiyet_ikizleri(cls.tanimlar["tanimlar"])

    def test_gercek_tanimlarda_yedi_cift(self):
        self.assertEqual(len(self.ikiz), 14)
        for r, s in self.ikiz.items():
            self.assertEqual(self.ikiz[s], r)  # kendi tersi olan eşleme
            self.assertNotEqual(r, s)
        tanim = {t["ad"]: t["secenekler"] for t in self.tanimlar["tanimlar"]}
        for r, s in self.ikiz.items():
            fark = [(a, b) for sa, sb in zip(tanim[r], tanim[s]) for a, b in zip(sa, sb) if a != b]
            self.assertEqual(len(fark), 1)  # yalnız bir cinsiyet adımı farklı
            self.assertEqual({fark[0][0]["tip"], fark[0][1]["tip"]}, {0, 1})
        ikizsiz = [t["ad"] for t in self.tanimlar["tanimlar"] if t["ad"] not in self.ikiz]
        self.assertEqual(len(ikizsiz), 7)

    def test_yapay_tanimlar(self):
        tanimlar = [{"ad": "p", "secenekler": [[{"yon": "U", "tip": 0}]]},
                    {"ad": "q", "secenekler": [[{"yon": "U", "tip": 1}]]},
                    {"ad": "s", "secenekler": [[{"yon": "U", "tip": None}, {"yon": "U", "tip": 1}]]},
                    {"ad": "t", "secenekler": [[{"yon": "D", "tip": 1}, {"yon": "E", "tip": None}]]},
                    {"ad": "u", "secenekler": [[{"yon": "D", "tip": 0}, {"yon": "E", "tip": None}]]}]
        self.assertEqual(ST.cinsiyet_ikizleri(tanimlar), {"p": "q", "q": "p", "t": "u", "u": "t"})


class KaristirmaTesti(unittest.TestCase):
    def test_olgu_basina_bagimsiz_ve_tohumlu(self):
        ikiz = {tg.ZN: tg.Q, tg.Q: tg.ZN}
        d = tg.dunya("F1", 60, 3)
        a = ST.cinsiyet_karistir(d.olgular, ikiz, random.Random(1))
        self.assertEqual(a, ST.cinsiyet_karistir(d.olgular, ikiz, random.Random(1)))
        self.assertNotEqual(a, ST.cinsiyet_karistir(d.olgular, ikiz, random.Random(2)))
        self.assertEqual(len(a), len(d.olgular))
        eski, yeni = dict(((x, y), r) for x, r, y in d.olgular), dict(((x, y), r) for x, r, y in a)
        degisen = [c for c in eski if eski[c] != yeni[c]]
        aday = [c for c in eski if eski[c] in ikiz]
        self.assertTrue(all(eski[c] in ikiz and yeni[c] == ikiz[eski[c]] for c in degisen))
        self.assertTrue(0.3 * len(aday) < len(degisen) < 0.7 * len(aday))
        self.assertEqual({c for c in eski if eski[c] not in ikiz and eski[c] != yeni[c]}, set())


class SemaTureviTesti(tg.Ortak):
    def test_sifir_ihlal(self):
        dunyalar = [(e, idx) for e, _, idx in self.ortam.gelistirme]
        self.assertTrue(ST.sema_turevi_mi(tg.DOGRU, dunyalar))
        self.assertFalse(ST.sema_turevi_mi(tg.YANLIS, dunyalar))
        self.assertFalse(ST.sema_turevi_mi(tg.TERS, dunyalar))  # F3 dünyalarında ihlal
        hic = tg.k([(tg.Q, "X", "Y"), (tg.ZN, "X", "Y")], (tg.B, "Y", "X"))
        self.assertEqual(ST.ihlal(hic, dunyalar), {"tahmin": 0, "ihlal": 0})  # hiç tetiklenmez: sıfır ihlal
        self.assertTrue(ST.sema_turevi_mi(hic, dunyalar))


class DunyalarTesti(unittest.TestCase):
    def test_onkayitli_etiketler_ve_tekillik(self):
        from cekirdek.altyapi.ayar import ayar_yukle
        from degerlendirme import h1, h2_dunya
        from degerlendirme.dunya import tanimlar_yukle
        h2 = ayar_yukle(KOK / "config_h2.json")
        _, sema, _ = h1._ortam(KOK)
        tanimlar = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                                  KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
        kayitlar = ST.dunya_kayitlari(h2, tanimlar, sema)
        self.assertGreaterEqual(len(kayitlar), 20)  # K-044: en az 20
        self.assertEqual(kayitlar[0][0], "sematurevi|A1|1")
        self.assertEqual(sorted({e.split("|")[1] for e, _ in kayitlar}), ["A1", "A2", "A3"])
        ozetler = [h2_dunya.dunya_ozeti(d, "sha256") for _, d in kayitlar]
        self.assertEqual(len(set(ozetler)), len(ozetler))
        havuz = json.loads((KOK / "raporlar" / "h2_b0" / "havuz_ozetleri.json").read_text(encoding="utf-8"))
        self.assertFalse(set(ozetler) & {o for v in havuz.values() for o in v})
        self.assertEqual([e for e, _ in kayitlar], [e for e, _ in ST.dunya_kayitlari(h2, tanimlar, sema)])


if __name__ == "__main__":
    unittest.main()
