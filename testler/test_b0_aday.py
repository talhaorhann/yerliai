"""K-041, v1 §2 (tek aday şeması), ÖK-005 taslağı §4 madde 19: aday kaydı biçimi, kanonik kimlik, kırmızı takım
dosyası denetimi. Gizli dosya açılmaz: denetim yalnız sayı ve özet döndürür, hata iletisinde değer yoktur.
Testlerde ilişki adı yazılmaz: anlamsız adlar ya da şemadan okunan adlar kullanılır."""
import copy
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path

from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.bellek_gecidi import kanonik_bicim
from kesif import aday as ad
from testler.yardimci import KOK

ADLAR = frozenset({"blorp", "quax", "vonk"})
ALGORITMA = "sha256"
ORNEK = KOK / "veri" / "h2" / "kirmizi_ornek_v1.json"
ISTEK = KOK / "raporlar" / "GIZLI_SAHTE_KURAL_ISTEGI.md"


def kayit(halkalar=(("blorp", "X", "Y"), ("blorp", "Y", "Z")), sonuc=("quax", "X", "Z"), farkli=(), oi=False,
          tur="m0", aile=None, kimlik="k1", **ek):
    k = {"sema_surumu": "1", "kimlik": kimlik,
         "halkalar": [{"gen": g, "sol": s, "sag": a} for g, s, a in halkalar],
         "sonuc": {"gen": sonuc[0], "sol": sonuc[1], "sag": sonuc[2]},
         "farkli": [list(c) for c in farkli], "oi": oi,
         "kaynak": {"tur": tur, "aile": aile, "tohum": None, "ust": []}, "tanik_ozeti": None, "surum": 1}
    k.update(ek)
    return k


def sema_adlari():
    veri = json.loads((KOK / "sema" / "iliskiler_v1.json").read_text(encoding="utf-8"))
    return frozenset(i["ad"] for i in veri["iliskiler"])


class AdayBicimiTesti(unittest.TestCase):
    def test_gecerli_kayit_kabul(self):
        ad.aday_denetle(kayit(), ADLAR)
        ad.aday_denetle(kayit(halkalar=(("blorp", "X", "Z"), ("vonk", "Z", "W"), ("quax", "W", "Y")),
                              sonuc=("quax", "X", "Y"), oi=True), ADLAR)
        ad.aday_denetle(kayit(tur="kirmizi_gizli", aile="H1x"), ADLAR)

    def test_bozuk_kayitlar_reddedilir(self):
        bozuklar = {
            "alan eksik": {k: v for k, v in kayit().items() if k != "oi"},
            "kapsam alanı (sistem türetir)": kayit(kapsam=["A1", "A2"]),
            "dört halka": kayit(halkalar=(("blorp", "X", "Y"), ("blorp", "Y", "Z"), ("blorp", "Z", "W"),
                                          ("blorp", "W", "V"))),
            "şemada olmayan ilişki": kayit(sonuc=("zzyok", "X", "Z")),
            "baş değişkeni gövdede yok": kayit(sonuc=("quax", "X", "Q")),
            "baş uçları aynı": kayit(sonuc=("quax", "X", "X")),
            "iki ucu aynı halka": kayit(halkalar=(("blorp", "X", "X"), ("blorp", "X", "Y")), sonuc=("quax", "X", "Y")),
            "yinelenen halka": kayit(halkalar=(("blorp", "X", "Y"), ("blorp", "X", "Y")), sonuc=("quax", "X", "Y")),
            "farklı çifti gövdede yok": kayit(farkli=(("X", "Q"),)),
            "farklı çifti aynı değişken": kayit(farkli=(("X", "X"),)),
            "oi ile farklı birlikte": kayit(farkli=(("X", "Z"),), oi=True),
            "kırmızı aday ailesiz": kayit(tur="kirmizi_gizli", aile=None),
            "kırmızı olmayan aday aileli": kayit(tur="m0", aile="G1"),
            "bilinmeyen kaynak": kayit(tur="llm"),
            "bozuk tanık özeti": kayit(tanik_ozeti="abc"),
            "sürüm sıfır": kayit(surum=0),
        }
        for neden, k in bozuklar.items():
            with self.subTest(neden=neden), self.assertRaises(ad.AdayHatasi):
                ad.aday_denetle(k, ADLAR)

    def test_hata_iletisinde_deger_yok(self):
        with self.assertRaises(ad.AdayHatasi) as h:
            ad.aday_denetle(kayit(sonuc=("zzgizliad", "X", "Z"), kimlik="zzgizlikimlik"), ADLAR)
        self.assertNotIn("zzgizliad", str(h.exception))
        self.assertNotIn("zzgizlikimlik", str(h.exception))


class KanonikKimlikTesti(unittest.TestCase):
    def test_degisken_adi_ve_halka_sirasi_kimligi_degistirmez(self):
        a = kayit(halkalar=(("blorp", "X", "Y"), ("vonk", "Y", "Z")), sonuc=("quax", "X", "Z"))
        b = kayit(halkalar=(("vonk", "B", "C"), ("blorp", "A", "B")), sonuc=("quax", "A", "C"), kimlik="baska")
        self.assertEqual(ad.kanonik_kimlik(a, ALGORITMA), ad.kanonik_kimlik(b, ALGORITMA))

    def test_bas_ya_da_govde_degisirse_kimlik_degisir(self):
        temel = ad.kanonik_kimlik(kayit(), ALGORITMA)
        self.assertNotEqual(temel, ad.kanonik_kimlik(kayit(sonuc=("vonk", "X", "Z")), ALGORITMA))
        self.assertNotEqual(temel, ad.kanonik_kimlik(kayit(sonuc=("quax", "Z", "X")), ALGORITMA))
        self.assertNotEqual(temel, ad.kanonik_kimlik(kayit(halkalar=(("blorp", "X", "Y"), ("blorp", "Z", "Y"))),
                                                     ALGORITMA))

    def test_oi_ve_farkli_kimlige_girer(self):
        temel = ad.kanonik_kimlik(kayit(), ALGORITMA)
        oili = ad.kanonik_kimlik(kayit(oi=True), ALGORITMA)
        self.assertNotEqual(temel, oili)
        hepsi = (("X", "Y"), ("X", "Z"), ("Y", "Z"))
        self.assertEqual(oili, ad.kanonik_kimlik(kayit(farkli=hepsi), ALGORITMA))

    def test_kimlik_depodaki_kanonik_bicimin_ozeti(self):
        k = kayit(farkli=(("X", "Z"),))
        h = ad.hucreye(k, 0.5, 1.0)
        beklenen = hashlib.sha256(kanonik_json(kanonik_bicim(h))).hexdigest()
        self.assertEqual(ad.kanonik_kimlik(k, ALGORITMA), beklenen)

    def test_hucreye(self):
        h = ad.hucreye(kayit(oi=True), 0.25, 0.75)
        self.assertEqual(h.kimlik, "k1")
        self.assertEqual({x.esik for x in h.halkalar}, {0.25})
        self.assertEqual(h.guvenilirlik, 0.75)
        self.assertEqual(set(h.farkli), {("X", "Y"), ("X", "Z"), ("Y", "Z")})
        self.assertEqual((h.sonuc.gen, h.sonuc.sol, h.sonuc.sag), ("quax", "X", "Z"))


def gizli_dosya(aile_sayisi=4, aile_basina=40, adlar=None):
    adlar = adlar or [f"S{i}" for i in range(aile_sayisi)]
    adaylar = [kayit(tur="kirmizi_gizli", aile=a, kimlik=f"m{a.lower()}_{j}") for a in adlar for j in range(aile_basina)]
    return {"sema_surumu": "1", "dosya_turu": "kirmizi_gizli", "yazan": "deneme", "tarih": "2026-10-26",
            "aileler": [{"ad": a, "aciklama": "x"} for a in adlar], "adaylar": adaylar}


class KirmiziDosyasiTesti(unittest.TestCase):
    SINIR = dict(tur="kirmizi_gizli", en_az_aile=4, aile_basina=40, yasak_adlar=("G1", "G2", "G3", "G4"))

    def test_ornek_dosya_gecerli(self):
        veri = json.loads(ORNEK.read_text(encoding="utf-8"))
        ozet = ad.kirmizi_dosyasi_denetle(veri, sema_adlari(), tur="kirmizi_gorunur", en_az_aile=1, aile_basina=0,
                                          yasak_adlar=())
        self.assertEqual(ozet, {"aile_sayisi": 4, "aday_sayisi": 3, "en_kucuk_aile": 0})

    def test_gizli_sinirlar(self):
        self.assertEqual(ad.kirmizi_dosyasi_denetle(gizli_dosya(), ADLAR, **self.SINIR),
                         {"aile_sayisi": 4, "aday_sayisi": 160, "en_kucuk_aile": 40})
        tek_kimlik = gizli_dosya()
        tek_kimlik["adaylar"][1]["kimlik"] = tek_kimlik["adaylar"][0]["kimlik"]
        listede_yok = gizli_dosya()
        listede_yok["adaylar"][0]["kaynak"]["aile"] = "Yok9"
        tur_farkli = gizli_dosya()
        tur_farkli["adaylar"][0]["kaynak"]["tur"] = "kirmizi_gorunur"
        bozuk_aday = gizli_dosya()
        bozuk_aday["adaylar"][5]["sonuc"]["gen"] = "zzyok"
        cift_aile = gizli_dosya(adlar=["S0", "S0", "S1", "S2"])
        kotuler = {"üç aile": gizli_dosya(aile_sayisi=3), "ailede 39": gizli_dosya(aile_basina=39),
                   "görünür aile adı": gizli_dosya(adlar=["G1", "S1", "S2", "S3"]), "yinelenen kimlik": tek_kimlik,
                   "listede olmayan aile": listede_yok, "dosya türüyle uyuşmayan aday": tur_farkli,
                   "bozuk aday": bozuk_aday, "yinelenen aile adı": cift_aile}
        for neden, veri in kotuler.items():
            with self.subTest(neden=neden), self.assertRaises(ad.AdayHatasi):
                ad.kirmizi_dosyasi_denetle(veri, ADLAR, **self.SINIR)

    def test_hata_iletisinde_icerik_yok(self):
        veri = gizli_dosya()
        veri["aileler"][0]["ad"] = "G2"
        veri["adaylar"][3]["sonuc"]["gen"] = "zzgizliad"
        with self.assertRaises(ad.AdayHatasi) as h:
            ad.kirmizi_dosyasi_denetle(veri, ADLAR, **self.SINIR)
        self.assertNotIn("zzgizliad", str(h.exception))
        self.assertNotIn("G2", str(h.exception))

    def test_ozet_yalniz_sayi_ve_hash(self):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "gizli.json"
            yol.write_text(json.dumps(gizli_dosya(), ensure_ascii=False), encoding="utf-8")
            ozet = ad.kirmizi_ozeti(yol, ADLAR, algoritma=ALGORITMA, **self.SINIR)
            self.assertEqual(set(ozet), {"aile_sayisi", "aday_sayisi", "en_kucuk_aile", "ozet"})
            self.assertEqual(ozet["ozet"], hashlib.sha256(yol.read_bytes()).hexdigest())

    def test_istek_belgesindeki_ornek_dosyayla_ayni(self):
        metin = ISTEK.read_text(encoding="utf-8")
        blok = re.search(r"```json\n(.*?)```", metin, re.S).group(1)
        self.assertEqual(json.loads(blok), json.loads(ORNEK.read_text(encoding="utf-8")))

    def test_arac_yalniz_sayi_ve_ozet_yazar(self):
        import contextlib
        import io
        cikti = io.StringIO()
        with contextlib.redirect_stdout(cikti):
            self.assertEqual(ad.main([str(ORNEK), "kirmizi_gorunur"]), 0)
        sonuc = json.loads(cikti.getvalue())
        self.assertEqual(set(sonuc), {"aile_sayisi", "aday_sayisi", "en_kucuk_aile", "ozet"})
        self.assertEqual(sonuc["ozet"], hashlib.sha256(ORNEK.read_bytes()).hexdigest())
        with self.assertRaises(ad.AdayHatasi):
            ad.main([str(ORNEK), "kirmizi_gizli"])  # örnek dosya gizli sınırlarını taşımaz

    def test_degistirilmis_ornek_reddedilir(self):
        veri = copy.deepcopy(json.loads(ORNEK.read_text(encoding="utf-8")))
        veri["adaylar"][0]["halkalar"][0]["gen"] = "zzyok"
        with self.assertRaises(ad.AdayHatasi):
            ad.kirmizi_dosyasi_denetle(veri, sema_adlari(), tur="kirmizi_gorunur", en_az_aile=1, aile_basina=0,
                                       yasak_adlar=())


if __name__ == "__main__":
    unittest.main()
