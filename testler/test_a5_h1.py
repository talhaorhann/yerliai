"""sistem.md §13 (H1), K-023 (ÖK-002), K-021, V-044: H1 koşturucusu.

Elle kurulmuş küçük bölümlerle (blorp şeması) sınanır: doğruluk kuralı (zincir-bozukta doğru = "bilmiyorum"),
hata sınıfları, sayımlar ve aralıklar, kapı kararı, ön kayıt kilidi, kâhin yalıtımı (cevap değişince çekirdek
satırları değişmez), dosya bütünlüğü ve yarıda kesilip sürdürülen koşunun kesintisizle aynı sonucu vermesi.
"""
import dataclasses
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1
from testler.test_a3_temel import dna_verisi, halka, hucre
import testler.test_a3_cekirdek as t3

AYAR = t3.AYAR
KK = HizliKodKitabi(AYAR.deger("vektor_tohum"), AYAR.deger("vektor_boyutu"))
GUNLUK = dict(algoritma=AYAR.deger("hash_algoritmasi"), sema_surumu=AYAR.deger("olay_sema_surumu"),
              izinli_kaynaklar=AYAR.deger("kaynaklar"))
DNA = [hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))]


def bolum(olgular, sorgu):
    b = {"sema_surumu": "1",
         "olgular": [{"sema_surumu": "1", "ozne": s, "iliski": r, "nesne": o, "kaynak": "üreteç", "guven": 1.0,
                      "adim": 0, "ozet": "0" * 64} for s, r, o in olgular],
         "sorgu": {"ozne": sorgu[0], "nesne": sorgu[1]}}
    b["ozet"] = hashlib.sha256(kanonik_json(b)).hexdigest()
    return b


def cevap(b, bolme, beklenen, kume="ana"):
    return {"sema_surumu": "1", "bolum_ozeti": b["ozet"], "bolme": bolme, "kume": kume, "k": 2, "cevap": beklenen}


ZINCIR = [(1, "blorp", 2), (2, "blorp", 3), (7, "frumb", 8)]
BOZUK = [(1, "blorp", 2), (5, "zindle", 6), (7, "frumb", 8)]
UZAK = [(1, "blorp", 2), (2, "zindle", 3), (7, "frumb", 8)]


def senaryo():
    """(bolme, bölüm, cevap kaydı): doğru, doğru bilmiyorum, yanlış ilişki, yanlış bilmiyorum."""
    a, b, c, d = bolum(ZINCIR, (1, 3)), bolum(BOZUK, (1, 6)), bolum(ZINCIR + [(3, "vonk", 9)], (1, 3)), \
        bolum(UZAK, (1, 3))
    return [("egitim", a, cevap(a, "egitim", "quax")), ("zincir_bozuk", b, cevap(b, "zincir_bozuk", None, "bozuk")),
            ("egitim", c, cevap(c, "egitim", "vonk")), ("egitim", d, cevap(d, "egitim", "quax"))]


def klasor_yaz(kok, tohum, bolmeler):
    """hepsini_uret çıktısının biçimi: bolumler/, kahin/, ozet.json (dosya özetleriyle)."""
    tk = Path(kok) / f"tohum_{tohum}"
    dosyalar = {}
    for (bolme, kume), satirlar in bolmeler.items():
        for alt, ad, kayitlar in (("bolumler", f"{bolme}_{kume}.jsonl", [b for b, _ in satirlar]),
                                  ("kahin", f"{bolme}_{kume}_cevap.jsonl", [c for _, c in satirlar])):
            baytlar = b"".join(kanonik_json(k) + b"\n" for k in kayitlar)
            (tk / alt).mkdir(parents=True, exist_ok=True)
            (tk / alt / ad).write_bytes(baytlar)
            dosyalar[f"{alt}/{ad}"] = hashlib.sha256(baytlar).hexdigest()
    (tk / "ozet.json").write_bytes(kanonik_json({"tohum": tohum, "dosyalar": dosyalar}))
    return tk


class Ortam(t3.Ortam):
    def hucreler_(self):
        return self.hucreler(*DNA)

    def kos(self, b):
        return h1.bolum_kos(b, self.hucreler_(), self.sema, KK, t3.PRM, GUNLUK)


class BolumTesti(Ortam):
    def test_dogruluk_kurali_ve_siniflar(self):
        sonuclar = [h1.degerlendir(self.kos(b), c) for _, b, c in senaryo()]
        self.assertEqual([s["dogru"] for s in sonuclar], [True, True, False, False])
        self.assertEqual([s["cevap"] for s in sonuclar], ["quax", None, "quax", None])
        self.assertEqual([s["sinif"] for s in sonuclar], [None, None, "yanlis_iliski", "bilmiyorum"])

    def test_cekirdek_satiri_cevabi_icermez_ve_cevaptan_bagimsiz(self):
        _, b, c = senaryo()[0]
        satir = self.kos(b)
        self.assertNotIn("beklenen", satir)
        self.assertEqual(satir["bolum_ozeti"], b["ozet"])
        self.assertEqual(satir["mudahale"]["durum"], "puanli")
        degismis = dict(c, cevap="vonk")
        self.assertEqual(h1.cekirdek_kismi(h1.degerlendir(satir, c)), h1.cekirdek_kismi(h1.degerlendir(satir, degismis)))

    def test_bolum_ozeti_uyusmazsa_durur(self):
        (_, a, ca), (_, b, _cb) = senaryo()[:2]
        with self.assertRaises(h1.H1Hatasi):
            h1.degerlendir(self.kos(a), dict(ca, bolum_ozeti=b["ozet"]))


class OzetVeKapiTesti(Ortam):
    def satirlar(self, tohum=7):
        return [dict(h1.degerlendir(self.kos(b), c), bolme=bolme, tohum=tohum) for bolme, b, c in senaryo()]

    def test_sayimlar_ve_araliklar(self):
        ozet = h1.ozetle(self.satirlar(), guven=0.95, tekrar=101, tohum=7)
        e = ozet["satirlar"]["egitim/7"]
        self.assertEqual((e["n"], e["dogru"], e["yanlis"], e["bilmiyorum"]), (3, 1, 2, 1))
        self.assertEqual(e["siniflar"], {"bilmiyorum": 1, "yanlis_iliski": 1})
        self.assertGreater(e["hata_ust_siniri"], 2 / 3)
        z = ozet["satirlar"]["zincir_bozuk/7"]
        self.assertEqual((z["n"], z["dogru"], z["yanlis_pozitif"]), (1, 1, 0))
        m = e["mudahale"]
        self.assertEqual(m["toplam"], 3)
        self.assertEqual(m["toplam"], m["puanli"] + m["sinanamadi"] + m["cevapsiz"])
        self.assertEqual(m["cevapsiz"], 1)
        self.assertIn("egitim", ozet["bolmeler"])

    def test_kapi_karari(self):
        satirlar = self.satirlar(7) + self.satirlar(8)
        ozet = h1.ozetle(satirlar, guven=0.95, tekrar=101, tohum=7)
        gecti, nedenler = h1.kapi_karari(ozet, ["zincir_bozuk"], [7, 8], beklenen_sayi=1)
        self.assertTrue(gecti, nedenler)
        gecti, nedenler = h1.kapi_karari(ozet, ["egitim", "zincir_bozuk"], [7, 8], beklenen_sayi=1)
        self.assertFalse(gecti)
        self.assertTrue(any("egitim/7" in n for n in nedenler))
        gecti, nedenler = h1.kapi_karari(ozet, ["zincir_bozuk"], [7, 8, 9], beklenen_sayi=1)
        self.assertFalse(gecti)
        self.assertTrue(any("zincir_bozuk/9" in n for n in nedenler))
        gecti, _ = h1.kapi_karari(ozet, ["zincir_bozuk"], [7, 8], beklenen_sayi=400)
        self.assertFalse(gecti)

    def test_rapor_metni(self):
        ozet = h1.ozetle(self.satirlar(), guven=0.95, tekrar=101, tohum=7)
        m = ozet["satirlar"]["egitim/7"]["mudahale"]
        metin = h1.rapor_metni(ozet, h1.kapi_karari(ozet, ["egitim"], [7], beklenen_sayi=3))
        self.assertIn("GEÇMEDİ", metin)
        self.assertIn("egitim/7: 2 hata", metin)
        self.assertIn(f"| {m['puanli']} / {m['sinanamadi']} / {m['cevapsiz']} |", metin)
        self.assertIn("LLM'siz", metin)
        self.assertIn("Sınanamadı", metin.replace('"', "").replace("sınanamadı", "Sınanamadı", 1))


class OnKayitTesti(unittest.TestCase):
    def test_ozetler_on_kayitta_yoksa_kapi_kosmaz(self):
        gerekli = {"config.json": "a" * 64, "dna": "b" * 64}
        metin = "## ÖK-002\n...\n### 9. Koşu öncesi ek\n"
        with self.assertRaises(h1.OnKayitHatasi):
            h1.on_kayit_denetle(metin, gerekli)
        with self.assertRaises(h1.OnKayitHatasi):
            h1.on_kayit_denetle(metin + "a" * 64 + "\n", gerekli)
        with self.assertRaises(h1.OnKayitHatasi):
            h1.on_kayit_denetle("a" * 64 + "b" * 64 + "\n" + metin, gerekli)
        h1.on_kayit_denetle(metin + "config `" + "a" * 64 + "`, DNA `" + "b" * 64 + "`\n", gerekli)


class DosyaKosusuTesti(Ortam):
    def setUp(self):
        super().setUp()
        senaryolar = senaryo()
        self.kok = Path(self._d.name) / "veri"
        egitim = [(b, c) for bolme, b, c in senaryolar if bolme == "egitim"]
        bozuk = [(b, c) for bolme, b, c in senaryolar if bolme == "zincir_bozuk"]
        self.tk = klasor_yaz(self.kok, 7, {("egitim", "ana"): egitim, ("zincir_bozuk", "bozuk"): bozuk})

    def kos_(self, cikis, sinir=None, ara=2):
        return h1.bolme_kos(self.kok, 7, "egitim", self.hucreler_(), self.sema, KK, t3.PRM, GUNLUK, cikis,
                            ara_kayit=ara, sinir=sinir)

    def test_bozuk_kume_ve_sayi(self):
        satirlar = h1.bolme_kos(self.kok, 7, "zincir_bozuk", self.hucreler_(), self.sema, KK, t3.PRM, GUNLUK,
                                Path(self._d.name) / "c0", ara_kayit=2)
        self.assertEqual([(s["bolme"], s["tohum"], s["dogru"]) for s in satirlar], [("zincir_bozuk", 7, True)])

    def test_yarida_kesilen_kosu_kesintisizle_ayni(self):
        tam = self.kos_(Path(self._d.name) / "c1")
        yarim_cikis = Path(self._d.name) / "c2"
        self.assertEqual(len(self.kos_(yarim_cikis, sinir=1)), 1)
        devam = self.kos_(yarim_cikis)
        self.assertEqual([h1.belirlenimli(s) for s in devam], [h1.belirlenimli(s) for s in tam])
        self.assertEqual(len(tam), 3)
        dosya = yarim_cikis / "egitim_t7.jsonl"
        self.assertEqual([json.loads(s)["bolum_ozeti"] for s in dosya.read_text(encoding="utf-8").splitlines()],
                         [s["bolum_ozeti"] for s in tam])

    def test_bozulmus_bolum_dosyasi_reddedilir(self):
        yol = self.tk / "bolumler" / "egitim_ana.jsonl"
        yol.write_bytes(yol.read_bytes() + b"\n")
        with self.assertRaises(h1.H1Hatasi):
            self.kos_(Path(self._d.name) / "c3")

    def test_baska_bolumun_ara_kaydi_reddedilir(self):
        cikis = Path(self._d.name) / "c4"
        self.kos_(cikis, sinir=1)
        dosya = cikis / "egitim_t7.jsonl"
        satir = json.loads(dosya.read_text(encoding="utf-8").splitlines()[0])
        dosya.write_bytes(kanonik_json(dict(satir, bolum_ozeti="f" * 64)) + b"\n")
        with self.assertRaises(h1.H1Hatasi):
            self.kos_(cikis)


if __name__ == "__main__":
    unittest.main()
