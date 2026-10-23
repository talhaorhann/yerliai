"""KODLAMA_PROMPTU §5 (Config): tek ayar dosyası, her değerin kaynağı, en fazla 5 bayrak, riskli bayraklar kapalı."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.ayar import RISKLI_BAYRAKLAR, AyarHatasi, ayar_yukle
from testler.yardimci import KOK, KIMLIK_DESENI, kayitli_kimlikler

GECERLI = {
    "surum": "1",
    "degerler": {"ornek": {"deger": "x", "kaynak": "V-001"}},
    "bayraklar": {ad: {"deger": False, "kaynak": "KODLAMA_PROMPTU §5"} for ad in RISKLI_BAYRAKLAR},
}


class GercekAyarTesti(unittest.TestCase):
    def test_gercek_ayar_yuklenir(self):
        ayar = ayar_yukle(KOK / "config.json")
        self.assertEqual(ayar.deger("hash_algoritmasi"), "sha256")

    def test_riskli_bayraklar_tanimli_ve_kapali(self):
        ayar = ayar_yukle(KOK / "config.json")
        for ad in ("deneysel", "kahin", "api_yedegi"):
            self.assertIn(ad, RISKLI_BAYRAKLAR)
            self.assertIs(ayar.bayrak(ad), False)

    def test_bilinmeyen_ad_varsayilan_donmez(self):
        ayar = ayar_yukle(KOK / "config.json")
        with self.assertRaises(KeyError):
            ayar.deger("olmayan_deger")
        with self.assertRaises(KeyError):
            ayar.bayrak("olmayan_bayrak")

    def test_kaynak_kimlikleri_kayitli(self):
        kayitli = kayitli_kimlikler()
        for kimlik in KIMLIK_DESENI.findall((KOK / "config.json").read_text(encoding="utf-8")):
            self.assertIn(kimlik, kayitli)


class BozukAyarTesti(unittest.TestCase):
    def yukle(self, veri):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "config.json"
            yol.write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
            return ayar_yukle(yol)

    def bozuk(self, degistir):
        veri = copy.deepcopy(GECERLI)
        degistir(veri)
        with self.assertRaises(AyarHatasi):
            self.yukle(veri)

    def test_gecerli_ornek_yuklenir(self):
        self.assertEqual(self.yukle(GECERLI).deger("ornek"), "x")

    def test_kaynaksiz_deger_reddedilir(self):
        self.bozuk(lambda v: v["degerler"]["ornek"].pop("kaynak"))

    def test_bos_kaynak_reddedilir(self):
        self.bozuk(lambda v: v["degerler"]["ornek"].update(kaynak=""))

    def test_bicimsiz_kaynak_reddedilir(self):
        for kaynak in ("makul varsayılan", "§2", "V-1", "sistem.md"):
            self.bozuk(lambda v, k=kaynak: v["degerler"]["ornek"].update(kaynak=k))

    def test_fazla_alan_reddedilir(self):
        self.bozuk(lambda v: v["degerler"]["ornek"].update(aciklama="ek"))
        self.bozuk(lambda v: v.update(fazla={}))

    def test_eksik_ust_alan_reddedilir(self):
        self.bozuk(lambda v: v.pop("bayraklar"))
        self.bozuk(lambda v: v.pop("surum"))

    def test_riskli_bayrak_acik_reddedilir(self):
        for ad in RISKLI_BAYRAKLAR:
            self.bozuk(lambda v, a=ad: v["bayraklar"][a].update(deger=True))

    def test_riskli_bayrak_eksik_reddedilir(self):
        self.bozuk(lambda v: v["bayraklar"].pop("kahin"))

    def test_bayrak_bool_olmali(self):
        self.bozuk(lambda v: v["bayraklar"]["kahin"].update(deger=0))

    def test_altidan_fazla_bayrak_reddedilir(self):
        def ekle(v):
            for i in range(6):
                v["bayraklar"][f"b{i}"] = {"deger": False, "kaynak": "V-001"}
        self.bozuk(ekle)

    def test_bes_bayrak_kabul(self):
        veri = copy.deepcopy(GECERLI)
        for i in range(5 - len(RISKLI_BAYRAKLAR)):
            veri["bayraklar"][f"b{i}"] = {"deger": True, "kaynak": "V-001"}
        self.assertEqual(len(self.yukle(veri).bayraklar), 5)

    def test_bozuk_json_reddedilir(self):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "config.json"
            yol.write_text("{bozuk", encoding="utf-8")
            with self.assertRaises(AyarHatasi):
                ayar_yukle(yol)

    def test_yinelenen_anahtar_reddedilir(self):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "config.json"
            metin = json.dumps(GECERLI)[:-1] + ', "surum": "2"}'
            yol.write_text(metin, encoding="utf-8")
            with self.assertRaises(AyarHatasi):
                ayar_yukle(yol)


if __name__ == "__main__":
    unittest.main()
