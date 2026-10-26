"""K-041, ÖK-005 taslağı §2.1 (A1, A2, A3), §3 (havuzlar), §5 (tohumlar), V-062: H2 dünya aileleri ve havuzları.
A2 için üretece eklenen evlilik oranı 1,0'da H1 dünyalarını bit-aynı bırakır. A3 ayrı koddur (dunya.py'den bir şey
almaz, ≤300 satır); kendi tanım yorumlayıcısı aynı soy ağacında eski yorumlayıcıyla aynı olguları vermelidir.
Testlerde ilişki adı yazılmaz; şema ve tanımlar veri dosyasından okunur."""
import ast
import random
import unittest

from cekirdek.altyapi.ayar import ayar_yukle
from degerlendirme import h1, h2_dunya, ikinci_uretec
from degerlendirme.dunya import Dunya, tanimlar_yukle
from testler.yardimci import KOK

H2 = ayar_yukle(KOK / "config_h2.json")
_, SEMA, _ = h1._ortam(KOK)
TANIMLAR = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                          KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", SEMA)


def ozellik(d):
    return d.tip, d.ebeveynler, d.es


class EvlilikOraniTesti(unittest.TestCase):
    def test_oran_bir_h1_dunyalarini_degistirmez(self):
        for t in range(20):
            a = Dunya.uret(random.Random(t), 4, 2, 4)
            b = Dunya.uret(random.Random(t), 4, 2, 4, evlilik_orani=1.0)
            self.assertEqual(ozellik(a), ozellik(b))

    def test_oran_sifirda_kok_cocuklari_evlenmez(self):
        d = Dunya.uret(random.Random(3), 4, 2, 4, evlilik_orani=0.0)
        self.assertEqual(len(d.es), 2)  # yalnız kök çift
        self.assertEqual(d.kisi_sayisi, 2 + sum(1 for c in d.ebeveynler))

    def test_oran_kesirde_kimi_evlenmez(self):
        evli = toplam = 0
        for t in range(40):
            d = Dunya.uret(random.Random(t), 5, 1, 4, evlilik_orani=0.8)
            derinlik = {}
            for c in sorted(d.ebeveynler):
                derinlik[c] = 1 + max(derinlik.get(e, 0) for e in d.ebeveynler[c])
            for c, k in derinlik.items():
                if k < 5 - 1:  # son nesil dışındaki çocuklar
                    toplam += 1
                    evli += c in d.es
        self.assertGreater(evli, toplam / 2)
        self.assertLess(evli, toplam)


class IkinciUretecTesti(unittest.TestCase):
    PRM = H2.deger("dunya_aileleri")["A3"]["parametreler"]

    def test_bagimsiz_kod(self):
        yol = KOK / "degerlendirme" / "ikinci_uretec.py"
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for d in ast.walk(agac):
            if isinstance(d, ast.ImportFrom):
                self.assertNotIn(d.module, ("degerlendirme.dunya", "degerlendirme.uretec", "dunya"))
            if isinstance(d, ast.Import):
                self.assertFalse(any(a.name.startswith("degerlendirme") for a in d.names))
        self.assertLessEqual(len(yol.read_text(encoding="utf-8").splitlines()), 300)

    def test_belirlenimci_ve_akraba_evliligi_yok(self):
        a = ikinci_uretec.uret(random.Random(5), **self.PRM)
        b = ikinci_uretec.uret(random.Random(5), **self.PRM)
        self.assertEqual((a.tip, a.ebeveynler, a.es), (b.tip, b.ebeveynler, b.es))
        for t in range(10):
            n = ikinci_uretec.uret(random.Random(t), **self.PRM)
            for x, y in n.es.items():
                self.assertFalse(n.soy[x] & n.soy[y], "aynı soydan evlilik")
                self.assertNotEqual(n.tip[x], n.tip[y])

    def test_soylar_arasi_evlilik_olur(self):
        ici = 0
        for t in range(20):
            n = ikinci_uretec.uret(random.Random(t), **self.PRM)
            ici += sum(1 for x, y in n.es.items() if x in n.ebeveynler and y in n.ebeveynler)
        self.assertGreater(ici, 0)

    def test_yorumlayici_eskisiyle_ayni(self):
        """Aynı soy ağacında (A1 dünyası) ikinci üretecin yorumlayıcısı eski yorumlayıcıyla aynı olguları verir."""
        for t in range(3):
            d = Dunya.uret(random.Random(t), 4, 2, 4)
            eski = sorted((x, r, y) for x in range(d.kisi_sayisi) for y, r in d.iliskiler(x, TANIMLAR).items())
            n = ikinci_uretec.Nufus(d.tip, d.ebeveynler, d.es, {k: frozenset() for k in range(d.kisi_sayisi)})
            self.assertEqual(ikinci_uretec.olgular(n, TANIMLAR.secenekler), eski)

    def test_olgular_tek_terimli_ve_ters_tutarli(self):
        for t in range(5):
            n = ikinci_uretec.uret(random.Random(t), **self.PRM)
            olg = ikinci_uretec.olgular(n, TANIMLAR.secenekler)
            ciftler = [(x, y) for x, _, y in olg]
            self.assertEqual(len(ciftler), len(set(ciftler)))
            var = {(x, r, y) for x, r, y in olg}
            for x, r, y in olg:
                self.assertTrue(any((y, t2, x) in var for t2 in SEMA.ters(r)))


class HavuzTesti(unittest.TestCase):
    def test_aile_dagilimi_ve_tohumlar(self):
        dag = H2.deger("havuz_dagilimi")
        self.assertEqual({h: sum(v.values()) for h, v in dag.items()}, {"gelistirme": 16, "final": 24, "kontrol": 8})
        dunyalar = h2_dunya.havuz("kontrol", H2, TANIMLAR)
        self.assertEqual([d.aile for d in dunyalar], ["A1"] * 3 + ["A2"] * 3 + ["A3"] * 2)
        self.assertEqual(h2_dunya.havuz("kontrol", H2, TANIMLAR), dunyalar)

    def test_dunya_olgulari_tam(self):
        d = Dunya.uret(random.Random(1), 4, 2, 4)
        olg = h2_dunya.dunya_olgulari(d, TANIMLAR)
        self.assertEqual(len(olg), sum(len(d.iliskiler(x, TANIMLAR)) for x in range(d.kisi_sayisi)))

    def test_ozetler_tekil(self):
        ozetler = h2_dunya.havuz_ozetleri(H2, TANIMLAR, ("kontrol",))
        self.assertEqual(len(ozetler["kontrol"]), 8)
        self.assertEqual(len(set(ozetler["kontrol"])), 8)

    def test_yinelenen_dunya_durdurur(self):
        from unittest import mock
        tek = h2_dunya.havuz("kontrol", H2, TANIMLAR)[:1]
        with mock.patch.object(h2_dunya, "havuz", return_value=tek * 2), self.assertRaises(ValueError):
            h2_dunya.havuz_ozetleri(H2, TANIMLAR, ("kontrol",))

    def test_bilinmeyen_uretec_reddedilir(self):
        with self.assertRaises(ValueError):
            h2_dunya.aile_dunyasi("A9", {"uretec": "yok", "parametreler": {}}, 1, TANIMLAR)


if __name__ == "__main__":
    unittest.main()
