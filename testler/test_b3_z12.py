"""K-041 (ÖK-005 taslağı §2.3: Z12/mod-n, K-041 madde 6 ile onaylı on ilişki), K-043, V-066: Z12 dünyaları, iki ayrı
üretici (doğrudan ve Çin kalan teoremi), alan şeması, alan ortamı, aile başına kapanış geri bulması ve B3 onay şartı.
İlişki adları kodda yazılmaz: tanım dosyasından okunur ve tanım türüyle seçilir."""
import random
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.ayar import ayar_yukle
from degerlendirme import h2_aktarim as AK, h2_tur, kural, z12, z12_ikinci
from kesif import m0
from testler.yardimci import KOK

H2 = ayar_yukle(KOK / "config_h2.json")
TANIM = z12.tanimlar_yukle(KOK / H2.deger("z12_dosyalari")["tanimlar"])
T = TANIM["tanimlar"]


class Sirali:
    """Kimlikleri karıştırmayan üreteç (yalnız yapıyı karşılaştırmak için)."""

    @staticmethod
    def sample(seq, n):
        return list(seq)[:n]


def ad(tur, **ek):
    return next(r for r, t in T.items() if t["tur"] == tur and all(t.get(a) == v for a, v in ek.items()))


class DunyaTesti(unittest.TestCase):
    def say(self, d):
        s = {}
        for _, r, _ in d.olgular:
            s[r] = s.get(r, 0) + 1
        return s

    def test_n12_sayilar(self):
        s = self.say(z12.dunya("Z12-a", 12, T, Sirali))
        self.assertEqual(s[ad("oteleme", fark=1)], 12)
        self.assertEqual(s[ad("iki_yonlu_oteleme")], 12)  # n = 12'de A+6 ≡ A−6: işlevsel
        self.assertEqual(s[ad("toplam_sifir")], 10)  # 0 ve 6 kendi karşıtı: yazılmaz
        self.assertEqual(s[ad("kalan_esit", modul=3)], 36)
        self.assertEqual(s[ad("kalan_esit", modul=4)], 24)
        self.assertEqual(sum(s.values()), 154)

    def test_n24_alti_ote_islevsel_degil(self):
        s = self.say(z12.dunya("Z24", 24, T, Sirali))
        self.assertEqual(s[ad("iki_yonlu_oteleme")], 48)

    def test_cin_kalan_ureticisi_yeniden_adlandirma(self):
        a = z12.dunya("Z12-a", 12, T, Sirali)
        b = z12_ikinci.dunya("Z12-b", [3, 4], T, Sirali)
        elemanlar = [(x, y) for x in range(3) for y in range(4)]
        esle = {i: next(k for k in range(12) if k % 3 == x and k % 4 == y) for i, (x, y) in enumerate(elemanlar)}
        self.assertEqual(sorted((esle[p], r, esle[q]) for p, r, q in b.olgular), sorted(a.olgular))

    def test_tohumla_karisir(self):
        a = z12.dunya("Z12-a", 12, T, random.Random(1))
        self.assertEqual(self.say(a), self.say(z12.dunya("Z12-a", 12, T, Sirali)))
        self.assertNotEqual(a.olgular, z12.dunya("Z12-a", 12, T, random.Random(2)).olgular)


class AlanTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ortam, taze_fn = h2_tur.ortam_kur(h2_tur.Kurulum(str(KOK), alan=AK.ALAN))
        cls.taze_fn = staticmethod(taze_fn)

    def test_ortam(self):
        o = self.ortam
        self.assertEqual(set(o.sema.adlar), set(T))
        self.assertFalse(o.sema.islevsel(ad("iki_yonlu_oteleme")))  # alan şeması: n = 24'te işlevsel değil
        self.assertEqual(len(o.gelistirme), 12)
        self.assertEqual(o.sabit.dikkat_sayisi, 2)
        self.assertEqual(o.temel, tuple(TANIM["temel"]))
        self.assertEqual(o.gelistirme[0][0], "havuzB3|z12|gelistirme|Z12-a|1")
        taze = self.taze_fn("B3", 1)
        self.assertEqual([t[1] for t in taze], ["Z12-a", "Z12-a", "Z12-b", "Z12-b", "Z24", "Z24"])

    def test_m0_ve_aile_kirilimi(self):
        dunyalar = [d for _, d, _ in self.ortam.gelistirme]
        sonuc = m0.m0(dunyalar, tuple(self.ortam.sema.adlar), H2, kademe="K2")
        bir, iki = ad("oteleme", fark=1), ad("oteleme", fark=2)
        bilesim = kural.Kural([(bir, "X", "Z"), (bir, "Z", "Y")], (iki, "X", "Y"), ())
        kimlikler = {a["aday"]["kimlik"] for a in sonuc.adaylar}
        from degerlendirme import h2_olcum as O
        self.assertIn("k" + O.kanonik(bilesim), kimlikler)
        k = AK.aile_kirilimi([bilesim], [(d.aile, kural.Indeks(d.olgular)) for d in dunyalar[:1]], self.ortam.sema, 8)
        self.assertEqual(k["Z12-a"]["dogru"], 12)
        self.assertEqual(k["Z12-a"]["toplam"], 154)


class OnayTesti(unittest.TestCase):
    def test_b3_onaysiz_baslamaz(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "KARARLAR.md").write_text("## K-050 (2026-11-01): B3\n- **Onaylayan:** kodlayıcı.\n", encoding="utf-8")
            with self.assertRaises(AK.AktarimHatasi):
                AK.b3_onayi_denetle(d, "K-050")
            (Path(d) / "KARARLAR.md").write_text("## K-051 (2026-11-01): B3 başlar\n- **Onaylayan:** kullanıcı.\n",
                                                 encoding="utf-8")
            AK.b3_onayi_denetle(d, "K-051")
            with self.assertRaises(AK.AktarimHatasi):
                AK.b3_onayi_denetle(d, "K-052")


if __name__ == "__main__":
    unittest.main()
