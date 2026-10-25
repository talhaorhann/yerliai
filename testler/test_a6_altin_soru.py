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


def kayit(adet=3, kaynaklar=None, **ek):
    k = {"parca": 2, "kaynak": "deneme", "onaylayan": "kullanıcı", "bagimsiz_insan_cevabi": False,
         "cevaplar": {str(n): "?" for n in range(1, adet + 1)}}
    if kaynaklar is not None:
        k["cevap_kaynaklari"] = {str(n): kaynaklar[(n - 1) % len(kaynaklar)] for n in range(1, adet + 1)}
    return {**k, **ek}


class CevapDenetimTesti(unittest.TestCase):
    """K-039: kullanıcı cevap dosyası biçimi kodla denetlenir; içerik yazdırılmaz. Kayıtlar sentetiktir."""
    LLM, KUL = altin.CEVAP_KAYNAKLARI[1], altin.CEVAP_KAYNAKLARI[0]

    def test_gecerli_kayit_ve_llm_sayisi(self):
        o = altin.kullanici_cevaplarini_denetle(kayit(kaynaklar=[self.LLM, self.KUL]), 2, 3)
        self.assertEqual((o["n"], o["llm_taslagi"]), (3, 2))
        o = altin.kullanici_cevaplarini_denetle(kayit(), 2, 3)  # eski biçim: cevap başına kaynak yok
        self.assertEqual((o["n"], o["llm_taslagi"]), (3, None))

    def test_bicim_hatalari_reddedilir(self):
        kotuler = [
            kayit(adet=2),  # eksik soru
            kayit(adet=4),  # fazla soru
            dict(kayit(), cevaplar={"1": "A", "2": "E", "3": "B"}),  # geçersiz harf
            kayit(kaynaklar=["başka"]),  # geçersiz kaynak
            dict(kayit(kaynaklar=[self.LLM]), cevap_kaynaklari={"1": self.LLM}),  # anahtarlar farklı
            kayit(kaynaklar=[self.LLM], bagimsiz_insan_cevabi=True),  # LLM taslağı varken bağımsız denmiş
            kayit(parca=1),  # yanlış parça
            {k: v for k, v in kayit().items() if k != "onaylayan"},  # alan eksik
            dict(kayit(), bagimsiz_insan_cevabi="hayır"),  # mantıksal değer değil
        ]
        for k in kotuler:
            with self.subTest(kayit=k), self.assertRaises(ValueError):
                altin.kullanici_cevaplarini_denetle(k, 2, 3)

    def test_hata_mesajinda_cevap_yok(self):
        k = dict(kayit(), cevaplar={"1": "A", "2": "E", "3": "B"})
        with self.assertRaises(ValueError) as h:
            altin.kullanici_cevaplarini_denetle(k, 2, 3)
        self.assertNotIn("'A'", str(h.exception))

    def test_altin_ozeti_llm_taslagini_acikca_yazar(self):
        from degerlendirme import h1
        kullanici = {2: kayit(kaynaklar=[self.LLM])}
        satir = {"parca": 2, "kullaniciyla_ayni": True, "kullanici_harfi": "A", "uretecle_ayni": True, "cekirdek_harfi": "A"}
        ozet = h1.altin_ozeti([satir], kullanici)["2"]
        self.assertEqual(ozet["llm_taslagi"], 3)
        self.assertIn("3/3 cevap LLM taslağı, kullanıcı onaylı", ozet["etiket"])
        self.assertIn("LLM taslağı", h1.altin_rapor_metni(h1.altin_ozeti([satir], kullanici)))


class AltinYuklemeTesti(unittest.TestCase):
    """H1 altın koşusu, cevap dosyasını yüklerken biçimini denetler (K-039)."""

    def test_bozuk_cevap_dosyasi_altin_kosusunu_durdurur(self):
        from degerlendirme import h1
        sorular = [{"parca": 2, "no": n} for n in range(1, 4)]
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "kullanici_cevaplari_2.json").write_text(json.dumps(kayit(adet=2)), encoding="utf-8")
            with self.assertRaises(ValueError):
                h1.kullanici_cevaplari_yukle(Path(d), 2, sorular)
            (Path(d) / "kullanici_cevaplari_2.json").write_text(json.dumps(kayit(adet=3)), encoding="utf-8")
            self.assertEqual(set(h1.kullanici_cevaplari_yukle(Path(d), 2, sorular)), {2})


if __name__ == "__main__":
    unittest.main()
