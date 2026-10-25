"""V-057: A6 gösterim aracı. Bozma, sonucu temel ilişki olan kuralların sonucunu bir sonraki temel ilişkiyle değiştirir;
araç her kural için onaylı kararı ve V-058 önerisinin kararını yazar. Küçük bir koşuyla sınanır (bir bölüm, iki kural).
Testlerde ilişki adı yazılmaz: kurallar DNA dosyasından gelir."""
import json
import tempfile
import unittest
from pathlib import Path

from degerlendirme import a6_gosterim as g
from cekirdek.bellek_gecidi import KABUL, RET, SINANAMADI
from testler.yardimci import KOK
import testler.test_a1_uretec as t1

DNA = KOK / "veri" / "dna" / "akrabalik_dna_v8.json"


class GosterimTesti(unittest.TestCase):
    def test_bozuk_surumler(self):
        dna = json.loads(DNA.read_text(encoding="utf-8"))["hucreler"]
        temel = list(t1.TANIM.olgu_iliskileri)
        bozuk = g.bozuk_surumler(dna, temel)
        kaynak = [h for h in dna if h["sonuc"]["gen"] in temel]
        self.assertEqual(len(bozuk), len(kaynak))
        for b, h in zip(bozuk, kaynak):
            self.assertEqual((b["kimlik"], b["halkalar"]), (h["kimlik"] + "_bozuk", h["halkalar"]))
            self.assertEqual(b["sonuc"]["gen"], temel[(temel.index(h["sonuc"]["gen"]) + 1) % len(temel)])
            self.assertEqual({k: v for k, v in b["sonuc"].items() if k != "gen"},
                             {k: v for k, v in h["sonuc"].items() if k != "gen"})

    def test_kucuk_kosu(self):
        dna = json.loads(DNA.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            kucuk = Path(d) / "dna.json"
            kucuk.write_text(json.dumps(dict(dna, hucreler=dna["hucreler"][:1])), encoding="utf-8")
            self.assertEqual(g.main([str(kucuk), str(Path(d) / "c.json"), "1", "1"]), 0)
            rapor = json.loads((Path(d) / "c.json").read_text(encoding="utf-8"))
        self.assertEqual([k["etiket"] for k in rapor["kurallar"]], ["dna", "bozuk"])
        for k in rapor["kurallar"]:
            self.assertIn(k["karar"][0], {KABUL, RET, SINANAMADI})
            self.assertEqual(set(k["olcumler"]), {"olagan", "kaydirilmis"})
        self.assertEqual(rapor["bolum_sayisi"], 1)


if __name__ == "__main__":
    unittest.main()
