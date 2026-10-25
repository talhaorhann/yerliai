"""K-035, sistem.md §15, §16: bellek hattı. Adaylar sırayla geçitten geçer, kabul edilen belleğe yazılır. Doğruluk hesabı
çekirdek dışındadır ve kâhine dokunmaz. Bağımsızlık testi: aynı elle yazılmış gözlem akışı anlatıcısız (LLM'siz), sahte
(rastgele çıktılı) ve başka bir anlatıcıyla koşulur; kararlar, ölçümler, bellek baytları ve sürümü bit düzeyinde aynıdır.
İlişki adları anlamsızdır (blorp şeması)."""
import ast
import dataclasses
import random
from pathlib import Path

from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.bellek import Bellek
from cekirdek.bellek_gecidi import GEREKSIZ, KABUL, KISAYOL, RET, YANLIS
from degerlendirme.bellek_hatti import DOGRULANMADI, bellege_al
from testler.test_a5_h1 import GUNLUK
from testler.test_a6_bellek_gecidi import ESDEGER, ESIK, KISAYOL_ZZ, KK, ORTAMLAR, T1, T2, T3, YANLIS_SONUC
from testler.yardimci import KOK
import testler.test_a3_cekirdek as t3

DNA_V2 = KOK / "sema" / "dna_v2.schema.json"
ADAYLAR = [T1, YANLIS_SONUC, T2, KISAYOL_ZZ, ESDEGER, T3]
BEKLENEN = [(KABUL, None), (RET, YANLIS), (KABUL, None), (RET, KISAYOL), (RET, GEREKSIZ), (KABUL, None)]
KAHIN_MODULLERI = {"degerlendirme.uretec", "degerlendirme.dunya", "degerlendirme.altin", "degerlendirme.kilitli_kumeler",
                   "degerlendirme.kisa_yol", "degerlendirme.h1", "degerlendirme.h1_inceleme", "degerlendirme.h1_sinir"}


class SahteAnlatici:
    """Rastgele metin üretir ve aldığı kopyayı bozmaya çalışır."""

    def __init__(self, tohum):
        self.rng = random.Random(tohum)

    def __call__(self, karar):
        karar["karar"], karar["olcumler"] = KABUL, {}
        return "".join(self.rng.choice("abcçdefgğ ") for _ in range(self.rng.randint(1, 40)))


class BaskaAnlatici:
    """Başka bir anlatıcı: metin yerine sayı döndürür, iç listeleri değiştirir, son kararda hata verir."""

    def __init__(self, hata_kimligi=None):
        self.hata_kimligi = hata_kimligi

    def __call__(self, karar):
        for o in karar["olcumler"].values():
            if isinstance(o, dict):
                o["mudahale"].append(0.0)
        if karar["kimlik"] == self.hata_kimligi:
            raise RuntimeError("anlatıcı çöktü")
        return 42


class HatTesti(t3.Ortam):
    def kos(self, ad, anlatici=None, adaylar=ADAYLAR):
        yol = Path(self._d.name) / ad
        depo = Bellek(yol, **GUNLUK)
        sonuc = bellege_al(depo, adaylar, ORTAMLAR, DNA_V2, self.sema, KK, t3.PRM, GUNLUK, ESIK, anlatici=anlatici)
        return sonuc, depo, yol

    @staticmethod
    def kararlar_bayti(sonuc):
        return kanonik_json([[kimlik, dataclasses.asdict(k)] for kimlik, k in sonuc.kararlar])

    def test_adaylar_sirayla_degerlendirilir_kabul_edilen_bellege_girer(self):
        sonuc, depo, _ = self.kos("bellek.jsonl")
        self.assertEqual([(k.karar, k.neden) for _, k in sonuc.kararlar], BEKLENEN)
        self.assertEqual([h["kimlik"] for h in depo.aktif_veriler()], ["t_bb", "t_qb", "t_ff"])
        self.assertEqual(depo.kayitlar()[1]["veri"]["kanit"], dict(sonuc.kararlar)["t_qb"].olcumler)
        for o in depo.kayitlar()[1]["veri"]["kanit"].values():  # K-037: (a) ve a·b·c kanıtta saklanır
            self.assertEqual(len(o["mudahale_a"]), len(o["mudahale"]))
            self.assertEqual(len(o["mudahale_abc"]), len(o["mudahale"]))
        self.assertEqual(sonuc.anlatimlar, [])

    def test_bagimsizlik_anlaticisiz_sahte_ve_baska_ayni(self):
        yok, depo0, yol0 = self.kos("yok.jsonl")
        sahte, depo1, yol1 = self.kos("sahte.jsonl", SahteAnlatici(7))
        baska, depo2, yol2 = self.kos("baska.jsonl", BaskaAnlatici())
        for sonuc, depo, yol in ((sahte, depo1, yol1), (baska, depo2, yol2)):
            self.assertEqual(self.kararlar_bayti(sonuc), self.kararlar_bayti(yok))
            self.assertEqual(yol.read_bytes(), yol0.read_bytes())
            self.assertEqual(depo.surum, depo0.surum)
            self.assertEqual(kanonik_json(depo.aktif_veriler()), kanonik_json(depo0.aktif_veriler()))
        self.assertEqual([a["kimlik"] for a in sahte.anlatimlar], [h["kimlik"] for h in ADAYLAR])
        self.assertTrue(all(a["durum"] == DOGRULANMADI and isinstance(a["metin"], str) for a in sahte.anlatimlar))
        self.assertTrue(all(a["metin"] is None for a in baska.anlatimlar))  # metin olmayan çıktı alınmaz

    def test_anlatici_coktugunde_bellek_yine_ayni(self):
        """Anlatıcı bütün kararlar yazıldıktan sonra çağrılır: çökmesi belleği değiştirmez."""
        _, depo0, yol0 = self.kos("yok.jsonl")
        with self.assertRaises(RuntimeError):
            self.kos("coken.jsonl", BaskaAnlatici(hata_kimligi=T1["kimlik"]))
        coken = Bellek(Path(self._d.name) / "coken.jsonl", **GUNLUK)
        self.assertEqual(((Path(self._d.name) / "coken.jsonl").read_bytes(), coken.surum), (yol0.read_bytes(), depo0.surum))

    def test_bellekteki_kimlikle_aday_reddedilir(self):
        with self.assertRaises(ValueError):
            self.kos("iki.jsonl", adaylar=[T1, dict(T2, kimlik=T1["kimlik"])])


class KahinYalitimTesti(t3.Ortam):
    def test_dogruluk_hesabi_kahine_dokunmaz(self):
        """Puanlayıcı ve hat üreteci, dünyayı, altın kümeyi ve H1 kâhin kayıtlarını içe aktarmaz (K-035)."""
        for ad in ("gozlem_puani.py", "bellek_hatti.py"):
            agac = ast.parse((KOK / "degerlendirme" / ad).read_text(encoding="utf-8"))
            for dugum in ast.walk(agac):
                if isinstance(dugum, ast.ImportFrom):
                    adlar = {dugum.module} | {f"{dugum.module}.{a.name}" for a in dugum.names}
                elif isinstance(dugum, ast.Import):
                    adlar = {a.name for a in dugum.names}
                else:
                    continue
                with self.subTest(dosya=ad, satir=dugum.lineno):
                    self.assertFalse(adlar & KAHIN_MODULLERI, adlar)

    def test_cekirdek_tarafi_degerlendirmeyi_bilmez(self):
        agac = ast.parse((KOK / "cekirdek" / "bellek_gecidi.py").read_text(encoding="utf-8"))
        moduller = {d.module for d in ast.walk(agac) if isinstance(d, ast.ImportFrom)}
        self.assertFalse({m for m in moduller if m.split(".")[0] in {"degerlendirme", "tercuman"}}, moduller)
