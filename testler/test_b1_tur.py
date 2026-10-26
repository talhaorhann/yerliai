"""K-041, K-043 (ÖK-005 taslağı §4 madde 2–4, 13; §5; §7 yedeklilik), V-065: H2 tur koşucusu.

Sentetik blorp dünyaları (`test_b1_gecit`): obiter adayın indirgenmiş kuralı sıraya girer (görülmüşse girmez), yedek
aday uyutulur ve bütçe harcamaz, turda en çok `aday_siniri` aday sorgulanır (sorgu defteri), taze dünya yinelenirse koşu
durur, kesilen koşu kaldığı yerden aynı sonuçla sürer, kalibrasyon kipinde hüküm verilmez ama çekirdek ölçülür.
"""
import copy
import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from degerlendirme import h2_butce, h2_gecit as G, h2_tur
from kesif import aday
from testler import test_b1_gecit as tg

SABIT = dataclasses.replace(tg.SABIT, mudahale_en_az_kanit=1, fwer=0.6)  # 20 çekilişte en küçük p 1/21 ≤ 0,6/12
ESIK = G.Esikler(tau=0.5, mudahale=0.9, T=0.04, sigma=0.01)
ZINDLE_YOLU = tg.k([(tg.ZN, "Z", "X"), (tg.B, "Z", "Y")], (tg.V, "X", "Y"))  # tanıkları DOGRU'nunkilerin altkümesi


def kayit(k):
    r = {"sema_surumu": "1", "kimlik": "x", "halkalar": [{"gen": g, "sol": s, "sag": a} for g, s, a in k.halkalar],
         "sonuc": {"gen": k.bas[0], "sol": k.bas[1], "sag": k.bas[2]}, "farkli": [sorted(c) for c in k.farkli],
         "oi": False, "kaynak": {"tur": "m0", "aile": None, "tohum": None, "ust": []}, "tanik_ozeti": None, "surum": 1}
    r["kimlik"] = "k" + aday.kanonik_kimlik(r, "sha256")
    return r


def taze_fn(basamak, tur):
    sira = {"B1": 1, "B2b": 2, "B2a": 3}[basamak]
    return [G.dunya_kaydi(f"taze|{basamak}|{tur}|{a}|{j}", tg.dunya(a, 30, 10000 * sira + 100 * tur + 10 * i + j))
            for i, a in enumerate(("F1", "F2", "F3")) for j in (1, 2)]


class TurTesti(tg.Ortak):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.ortam = dataclasses.replace(type(self).ortam, sabit=SABIT)

    def tearDown(self):
        self._d.cleanup()

    def kosucu(self, defter=None, fn=taze_fn):
        return h2_tur.Kosucu(self._d.name, self.ortam, fn, defter=defter)

    def test_tur_akisi(self):
        kuyruk = [kayit(k) for k in (tg.YANLIS, tg.DOGRU, tg.FAZLA, tg.SIMETRIK)]
        dogru = kayit(tg.DOGRU)["kimlik"]
        defter = h2_butce.SorguDefteri(None, tg.H2, tur_basina_aday=1)
        bellek = h2_tur.Bellek()
        k = self.kosucu(defter)
        oz, olc = k.tur_kos(kuyruk, h2_tur.TurIsi("B1", 1, 1, ESIK), bellek)
        self.assertEqual(oz["hukumler"][kayit(tg.YANLIS)["kimlik"]], [G.RET, "gelistirme_yanlis"])
        self.assertEqual(oz["sorgulanan"], [dogru])
        self.assertEqual(oz["hukumler"][dogru][0], G.KABUL, olc[dogru])
        self.assertEqual(oz["kabul"], [dogru])
        self.assertEqual([x["kimlik"] for x in kuyruk], [kayit(c)["kimlik"] for c in (tg.FAZLA, tg.SIMETRIK)])  # sınır 1
        self.assertEqual(defter.turdaki_adaylar(), {dogru})
        self.assertEqual(defter.sayac(h2_butce.SORGU), 6)
        self.assertEqual(oz["wy"]["aile"], [dogru])
        # 2. tur: obiterin indirgenmişleri sıraya girer; DOGRU görülmüştür, girmez; ZINDLE_YOLU yedektir, uyutulur
        oz2, _ = k.tur_kos(kuyruk, h2_tur.TurIsi("B1", 2, 1, ESIK), bellek)
        self.assertEqual(oz2["hukumler"][kayit(tg.FAZLA)["kimlik"]], [G.BILMIYORUM, "obiter"])
        self.assertNotIn(dogru, oz2["hukumler"])
        self.assertEqual(oz2["hukumler"][kayit(ZINDLE_YOLU)["kimlik"]], [h2_tur.UYUTULDU, "yedeklilik"])
        self.assertIn(kayit(ZINDLE_YOLU)["kimlik"], bellek.uyuyan)
        self.assertEqual(oz2["hukumler"][kayit(tg.SIMETRIK)["kimlik"]], [G.BILMIYORUM, "bag_ikizi"])
        self.assertEqual(oz2["sorgulanan"], [])
        self.assertEqual(kuyruk, [])

    def test_kaldigi_yerden_ayni_sonuc(self):
        kuyruk = [kayit(k) for k in (tg.YANLIS, tg.DOGRU)]
        oz1, _ = self.kosucu().tur_kos(copy.deepcopy(kuyruk), h2_tur.TurIsi("B1", 1, 5, ESIK), h2_tur.Bellek())
        sayac = {"on": 0, "cekirdek": 0}
        on_is, cekirdek_is = h2_tur.on_is, h2_tur.cekirdek_is

        def say(ad, fn):
            def sarici(x):
                sayac[ad] += 1
                return fn(x)
            return sarici
        with mock.patch.object(h2_tur, "on_is", say("on", on_is)), \
                mock.patch.object(h2_tur, "cekirdek_is", say("cekirdek", cekirdek_is)):
            oz2, _ = self.kosucu().tur_kos(copy.deepcopy(kuyruk), h2_tur.TurIsi("B1", 1, 5, ESIK), h2_tur.Bellek())
        self.assertEqual(sayac, {"on": 0, "cekirdek": 0})  # hepsi dosyadan
        self.assertEqual(oz1, oz2)
        yol = Path(self._d.name) / "B1_tur01" / h2_tur.OZET
        self.assertEqual(json.loads(yol.read_text(encoding="utf-8"))["kabul"], oz1["kabul"])

    def test_tembel_kuyruk_listeyle_ayni(self):
        kayitlar = [kayit(k) for k in (tg.YANLIS, tg.FAZLA, tg.DOGRU)]
        oz1, _ = self.kosucu().tur_kos(list(kayitlar), h2_tur.TurIsi("B1", 1, 5, ESIK), h2_tur.Bellek())
        oz2, _ = h2_tur.Kosucu(self._d.name + "/t", self.ortam, taze_fn).tur_kos(
            h2_tur.TembelKuyruk(kayitlar), h2_tur.TurIsi("B1", 1, 5, ESIK), h2_tur.Bellek())
        self.assertEqual(oz1, oz2)

    def test_kalibrasyon_kipi(self):
        dogru = kayit(tg.DOGRU)
        oz, olc = self.kosucu().tur_kos([dogru], h2_tur.TurIsi("B1", 1, 5, None), h2_tur.Bellek())
        self.assertNotIn(dogru["kimlik"], oz["hukumler"])
        self.assertIn("cekirdek", olc[dogru["kimlik"]])
        self.assertEqual(G.hukum(olc[dogru["kimlik"]], ESIK, SABIT)[0], G.KABUL)

    def test_taze_dunya_yinelenirse_durur(self):
        k = self.kosucu(fn=lambda b, t: taze_fn(b, 1))
        k.tur_kos([], h2_tur.TurIsi("B1", 1, 5, ESIK), h2_tur.Bellek())
        with self.assertRaises(h2_tur.DurmaHatasi):
            k.tur_kos([], h2_tur.TurIsi("B1", 2, 5, ESIK), h2_tur.Bellek())
        ozet = h2_tur.h2_dunya.dunya_ozeti(taze_fn("B1", 1)[0][2], "sha256")
        with self.assertRaises(h2_tur.DurmaHatasi):
            h2_tur.Kosucu(self._d.name + "/b", self.ortam, taze_fn, yasak_ozetler=[ozet]).tur_kos(
                [], h2_tur.TurIsi("B1", 1, 5, ESIK), h2_tur.Bellek())

    def test_tabu(self):
        bellek = h2_tur.Bellek()
        bellek.kabul_et("a", tg.DOGRU)
        bellek.kabul_et("b", ZINDLE_YOLU)
        self.assertEqual(bellek.tabu(["a", "b"], self.ortam), ["b"])
        self.assertEqual(list(bellek.kabul), ["a"])


class TembelKuyrukTesti(unittest.TestCase):
    def test_islemler(self):
        q = h2_tur.TembelKuyruk([{"kimlik": c} for c in "abcde"], atla=lambda k: k["kimlik"] == "c")
        self.assertEqual([k["kimlik"] for k in q[:3]], ["a", "b", "d"])
        self.assertEqual(q.pop(0)["kimlik"], "a")
        q[0:0] = [{"kimlik": "x"}]
        self.assertEqual(q[0]["kimlik"], "x")
        self.assertEqual([q.pop(0)["kimlik"] for _ in range(4)], ["x", "b", "d", "e"])
        self.assertFalse(q)


class KodKitabiTesti(tg.Ortak):
    def test_onbellek_sonucu_degistirmez(self):
        from cekirdek.bellek_gecidi import maskeli_kos
        kk = h2_tur.onbellekli_kod_kitabi(tg.t3.AYAR.deger("vektor_tohum"), tg.t3.AYAR.deger("vektor_boyutu"), sinir=64)
        b = G.bolumler(tg.TERS, "t", self.taze[0], 1, self.ortam)[0]
        olg = [(a, r, c, 1.0) for a, r, c in b.olgular]
        h = G.hucre(tg.TERS, "t", SABIT)
        for maske in [None] + [i for i, o in enumerate(olg) if o[1] == tg.ZN][:2]:
            beklenen = maskeli_kos(h, (), olg, maske, self.sema, self.ortam.kk, self.ortam.prm, self.ortam.gunluk)
            for _ in range(2):  # ikinci kez önbellekten
                self.assertEqual(maskeli_kos(h, (), olg, maske, self.sema, kk, self.ortam.prm, self.ortam.gunluk), beklenen)
        self.assertGreater(kk.kayit_vektoru.cache_info().hits, 0)
        self.assertEqual(kk.kayit_vektoru(1, tg.B, 2), self.ortam.kk.kayit_vektoru(1, tg.B, 2))


class DunyaKayitlariTesti(unittest.TestCase):
    def test_havuz_kayitlari_havuzla_ayni(self):
        from cekirdek.altyapi.ayar import ayar_yukle
        from degerlendirme import h1, h2_dunya
        from degerlendirme.dunya import tanimlar_yukle
        from testler.yardimci import KOK
        h2 = ayar_yukle(KOK / "config_h2.json")
        _, sema, _ = h1._ortam(KOK)
        tanimlar = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                                  KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
        kayitlar = h2_tur.havuz_kayitlari(h2, tanimlar, "gelistirme")
        self.assertEqual([d for _, d in kayitlar], h2_dunya.havuz("gelistirme", h2, tanimlar))
        self.assertEqual(kayitlar[0][0], "havuz|gelistirme|A1|1")
        ozetler = json.loads((KOK / "raporlar" / "h2_b0" / "havuz_ozetleri.json").read_text(encoding="utf-8"))
        self.assertEqual([h2_dunya.dunya_ozeti(d, "sha256") for _, d in kayitlar], ozetler["gelistirme"])


if __name__ == "__main__":
    unittest.main()
