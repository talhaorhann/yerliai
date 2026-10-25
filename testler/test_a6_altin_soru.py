"""K-039, ÖK-001: altın küme parça soru dosyası, JSON cevap biçimiyle. Dosya yalnız soru kaydından
(`altin_sorular.jsonl`) üretilir; üretecin ve kullanıcının cevap dosyaları okunmaz. Dosyada doğru cevap yoktur.
Testlerde ilişki adı yazılmaz: sorular üretilmiş kayıttan gelir."""
import builtins
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from degerlendirme import altin
from testler.yardimci import KOK

KLASOR = KOK / "degerlendirme" / "altin"


def sorular(parca):
    kayitlar = [json.loads(s) for s in (KLASOR / "altin_sorular.jsonl").read_text(encoding="utf-8").splitlines()]
    return [k for k in kayitlar if k["parca"] == parca]


def ornek_kayit(metin):
    return json.loads(re.search(r"```json\n(.*?)```", metin, re.S).group(1))


class SoruDosyasiTesti(unittest.TestCase):
    def test_soru_govdesi_sohbet_kipiyle_ayni(self):
        s = sorular(2)
        json_metni = altin.parca_metni(2, s, altin.JSON_BICIMI)
        sohbet_metni = altin.parca_metni(2, s)
        govde = sohbet_metni[sohbet_metni.index("## Soru 1"):]
        self.assertIn(govde.rstrip("\n"), json_metni)
        self.assertNotIn("sohbete", json_metni)
        self.assertEqual(json_metni.count("## Soru "), len(s))

    def test_cevap_bicimi_ve_ornek_kayit(self):
        s = sorular(2)
        metin = altin.parca_metni(2, s, altin.JSON_BICIMI)
        self.assertIn("degerlendirme/altin/kullanici_cevaplari_2.json", metin)
        ornek = ornek_kayit(metin)
        self.assertEqual(set(ornek), set(altin.CEVAP_ALANLARI))
        self.assertEqual(ornek["parca"], 2)
        self.assertTrue(set(ornek["cevaplar"].values()) <= set(altin.HARFLER + altin.EMIN_DEGIL))
        self.assertTrue(set(ornek["cevap_kaynaklari"].values()) <= set(altin.CEVAP_KAYNAKLARI))
        self.assertEqual(set(ornek["cevaplar"]), set(ornek["cevap_kaynaklari"]))
        for alan in altin.CEVAP_ALANLARI:
            self.assertIn(f"`{alan}`", metin)
        self.assertIn(f"{len(s)} soru", metin)

    def test_dogru_cevap_kullanilmaz(self):
        """Soru kaydında cevap alanı yoktur; metin cevapsız kayıtla aynı çıkar."""
        s = sorular(2)
        self.assertFalse({"cevap", "dogru_harf", "k"} & {a for k in s for a in k})
        sahte = [dict(k, cevap="x", dogru_harf="A") for k in s]
        self.assertEqual(altin.parca_metni(2, sahte, altin.JSON_BICIMI), altin.parca_metni(2, s, altin.JSON_BICIMI))

    def test_cevap_dosyalari_okunmaz(self):
        asil = builtins.open
        acilan = []

        def izle(yol, *a, **kw):
            acilan.append(str(yol))
            return asil(yol, *a, **kw)
        with tempfile.TemporaryDirectory() as d, mock.patch("builtins.open", izle), \
                mock.patch.object(Path, "read_bytes", side_effect=AssertionError("read_bytes")):
            cikis = Path(d) / "soru.md"
            altin.soru_dosyasi_yaz(KLASOR, 2, cikis)
            yazilan = cikis.read_text(encoding="utf-8")
        self.assertFalse([y for y in acilan if "cevap" in Path(y).name], acilan)
        self.assertEqual(yazilan, altin.parca_metni(2, sorular(2), altin.JSON_BICIMI))

    def test_olmayan_parca_reddedilir(self):
        with tempfile.TemporaryDirectory() as d, self.assertRaises(ValueError):
            altin.soru_dosyasi_yaz(KLASOR, 9, Path(d) / "x.md")


if __name__ == "__main__":
    unittest.main()
