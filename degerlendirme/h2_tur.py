"""sistem.md §13, §18; K-041, K-043 (ÖK-005 taslağı §3, §4 madde 2–4, 13; §5; §7 yedeklilik), V-065: H2 tur koşucusu.

Bir tur: sıradaki adaylar (M0 sırası) aşama 1–4'ten (geliştirme havuzu) geçer; geçenlerden kabul kümesince zaten
türetilenler uyutulur (yedeklilik, bütçe harcamaz), kalanlardan en çok `aday_siniri` tanesi turun taze dünyalarında
sorgulanır (sorgu defteri) ve aşama 5'in sembolik ölçümüne girer. Sonra turun Westfall–Young ailesi (K'dan bağımsız
aşamaları geçenler) için null çekilişleri, sonra çekirdek adımı yapılır ve hüküm verilir.
- Obiter adayın indirgenmiş kuralları sırada hemen arkasına girer (daha önce görülmediyse).
- Yedeklilik ve tabu (V-065): adayın geliştirme havuzundaki tanıklarının hepsi kabul kümesinin (uyutulanlar hariç) tek
  adımlık tahminleriyle zaten türetiliyorsa aday uyutulur. Tur sonunda yeni kabul edilenler, kabul sırasının tersiyle,
  kendileri çıkarılınca da tanıkları türetiliyorsa uyutulur.
- Kalibrasyon kipinde (`esik` yok) çekirdek, K'dan bağımsız aşamaları ve null'ı geçen her aday için koşar; hüküm ızgarada
  sonradan verilir (`h2_kalibrasyon`).
- Taze dünyanın özeti havuz özetlerinde ya da önceki turlarda görülmüşse koşu durur (ÖK-005 taslağı §9 madde 7).
- Her ölçüm aday kimliğiyle JSONL dosyalarına yazılır; koşu kesilirse kaldığı yerden devam eder (hesap tohumludur,
  sonuç iş bölüşümünden bağımsızdır).
"""
import dataclasses
import functools
import json
import os
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json, ozet
from degerlendirme import h2_bagla, h2_dunya, h2_gecit as G, kural
from kesif import aday, tohum

HAVUZ, TAZE, BOS = "havuz", "taze", "bos"  # ÖK-005 taslağı §5: tohum etiketlerinin ilk parçaları
GELISTIRME = "gelistirme"
UYUTULDU = "UYUTULDU"  # ÖK-005 taslağı §7: yedeklilik (hüküm değildir; bütçe harcamaz)
ALGORITMA = "sha256"  # V-007
ON, TAZE_DOSYASI, WY, CEKIRDEK, OZET = "asama1_4.jsonl", "asama5.jsonl", "wy.json", "cekirdek.jsonl", "tur.json"  # V-065
ON_PARCA = 64  # V-065: aşama 1–4 paralel ön hesap parçası (sonucu değiştirmez)
KOD_KITABI_ONBELLEGI = 32768  # V-065: süreç başına önbellekteki vektör sayısı (sonucu değiştirmez)
WY_PARCA = 250  # V-065: null çekilişlerinin iş parçası (sonucu değiştirmez)


class DurmaHatasi(RuntimeError):
    """ÖK-005 taslağı §9: koşu durur ve kullanıcıya bildirilir."""


# ---- dünyalar ----

def havuz_kayitlari(h2, tanimlar, havuz_adi):
    dagilim, aileler = h2.deger("havuz_dagilimi")[havuz_adi], h2.deger("dunya_aileleri")
    return [(tohum.etiket(HAVUZ, havuz_adi, a, i),
             h2_dunya.aile_dunyasi(a, aileler[a], tohum.tohum(h2, HAVUZ, havuz_adi, a, i), tanimlar))
            for a in sorted(dagilim) for i in range(1, dagilim[a] + 1)]


def taze_kayitlari(h2, tanimlar, basamak, tur, aile_basina):
    aileler = h2.deger("dunya_aileleri")
    return [(tohum.etiket(TAZE, basamak, tur, a, j),
             h2_dunya.aile_dunyasi(a, aileler[a], tohum.tohum(h2, TAZE, basamak, tur, a, j), tanimlar))
            for a in sorted(aileler) for j in range(1, aile_basina + 1)]


def bos_kaydi(h2, sema, k, etiket, d):
    """Boş dünya (ÖK-005 taslağı §2.2, §5 `bos|<k>|<dünya etiketi>`): ileri taraflar yeniden bağlanır, tersler yazılır."""
    rng = random.Random(tohum.tohum(h2, BOS, k, *etiket.split(tohum.AYIRICI)))
    return etiket, dataclasses.replace(d, olgular=tuple(h2_bagla.bos_dunya(d.olgular, sema, rng,
                                                                           h2.deger("bagla_deneme_carpani"))))


# ---- çalışan süreç ----

def onbellekli_kod_kitabi(tohum_, boyut, sinir=KOD_KITABI_ONBELLEGI):
    """Çekirdeğe verilen kod kitabı: `HizliKodKitabi`'nin aynısı, `vektor` ve `kayit_vektoru` sonuçları önbellekte.
    Kod kitabı durumsuz bir işlevdir (V-026); önbellek sonucu değiştirmez (test: bit-aynı). Çekirdek kodu değişmez."""
    from cekirdek.vektor_hizli import HizliKodKitabi
    kk = HizliKodKitabi(tohum_, boyut)
    kk.vektor = functools.lru_cache(maxsize=sinir)(kk.vektor)
    kk.kayit_vektoru = functools.lru_cache(maxsize=sinir)(kk.kayit_vektoru)
    return kk


@dataclasses.dataclass(frozen=True)
class Kurulum:
    """Çalışan süreçlerin ortamı: kök ve boş koşu sırası (None: gerçek dünyalar)."""
    kok: str
    bos: object = None


def ortam_kur(kurulum):
    """(ortam, taze dünya işlevi): gerçek depo ayarlarıyla."""
    from cekirdek.altyapi.ayar import ayar_yukle
    from cekirdek.dongu import CekirdekParametreleri
    from degerlendirme import h1, h2_ikiz
    from degerlendirme.dunya import tanimlar_yukle
    kok = Path(kurulum.kok)
    ayar, sema, gunluk = h1._ortam(kok)
    h2 = ayar_yukle(kok / "config_h2.json")
    tanimlar = tanimlar_yukle(kok / "degerlendirme" / "veri" / "tanimlar_v1.json",
                              kok / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
    sabit = G.Sabitler.ayardan(h2)
    gel = havuz_kayitlari(h2, tanimlar, GELISTIRME)
    if kurulum.bos is not None:
        gel = [bos_kaydi(h2, sema, kurulum.bos, e, d) for e, d in gel]
    temel = tuple(tanimlar.olgu_iliskileri)
    ortam = G.Ortam(sema, temel, sabit, h2, [(e, d, kural.Indeks(d.olgular)) for e, d in gel],
                    h2_ikiz.bijeksiyonlar(sema, temel),
                    onbellekli_kod_kitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu")),
                    CekirdekParametreleri.ayardan(ayar), gunluk)

    def taze_fn(basamak, tur):
        kayitlar = taze_kayitlari(h2, tanimlar, basamak, tur, sabit.taze_aile_basina)
        if kurulum.bos is not None:
            kayitlar = [bos_kaydi(h2, sema, kurulum.bos, e, d) for e, d in kayitlar]
        return [G.dunya_kaydi(e, d) for e, d in kayitlar]

    return ortam, taze_fn


_DURUM = {}


def _yerlestir(ortam, taze_fn):
    _DURUM.clear()
    _DURUM.update(ortam=ortam, taze_fn=taze_fn, taze={})


def _hazirla(kurulum):
    import torch
    torch.set_num_threads(1)  # V-057: süreç başına tek iş parçacığı (sonucu değiştirmez)
    _yerlestir(*ortam_kur(kurulum))


def _taze(basamak, tur):
    anahtar = (basamak, tur)
    if anahtar not in _DURUM["taze"]:
        _DURUM["taze"] = {anahtar: _DURUM["taze_fn"](basamak, tur)}
    return _DURUM["taze"][anahtar]


def on_is(kayit):
    """Aşama 1–4 (geliştirme havuzu); taze dünya kullanmaz. İlk düşen aşamada durur."""
    o = _DURUM["ortam"]
    k, kimlik = kural.Kural.kayittan(kayit), kayit["kimlik"]
    g = G.gelistirme_sayilari(k, o)
    sonuc = {"kimlik": kimlik, "gelistirme": g, "obiter": []}
    if g["yanlis"] == 0:
        sonuc["obiter"] = G.obiterler(k, g["tanik"], o)
        if not sonuc["obiter"] and g["yolkesme_tanik"] >= o.sabit.en_az_tanik:
            sonuc["bag_ikizi"] = G.bag_ikizi(k, kimlik, o)
    return sonuc


def taze_is(arg):
    kayit, basamak, tur = arg
    o = _DURUM["ortam"]
    k, kimlik = kural.Kural.kayittan(kayit), kayit["kimlik"]
    sonuc = {"kimlik": kimlik, "taze": G.taze_sembolik(k, kimlik, _taze(basamak, tur), o)}
    if not G._taze_hukmu(sonuc, o.sabit):
        sonuc["gel_wilson"] = G.gelistirme_wilson(k, kimlik, o)
        sonuc["gurultu"] = G.gurultu(kimlik, basamak, tur, o)
    return sonuc


def wy_is(arg):
    aile, basamak, tur, cekilisler = arg
    return G.wy_maksimumlar(aile, _taze(basamak, tur), basamak, tur, _DURUM["ortam"], cekilisler)


def cekirdek_is(arg):
    kayit, basamak, tur = arg
    k = kural.Kural.kayittan(kayit)
    return {"kimlik": kayit["kimlik"], "cekirdek": G.cekirdek_olcum(k, kayit["kimlik"], _taze(basamak, tur),
                                                                     _DURUM["ortam"])}


# ---- kayıt ----

class Kayitci:
    """Kimlik → ölçüm; JSONL'e eklenir, yeniden açılınca okunur (kaldığı yerden devam)."""

    def __init__(self, yol):
        self.yol = Path(yol)
        self.veri = {}
        if self.yol.exists():
            with open(self.yol, encoding="utf-8") as f:
                for satir in f:
                    if satir.endswith("\n"):  # yarım son satır (kesilmiş koşu) yok sayılır, yeniden hesaplanır
                        s = json.loads(satir)
                        self.veri[s["kimlik"]] = s

    def ekle(self, s):
        self.yol.parent.mkdir(parents=True, exist_ok=True)
        with open(self.yol, "a", encoding="utf-8") as f:
            f.write(kanonik_json(s).decode("utf-8") + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.veri[s["kimlik"]] = s


def _kimlik(i):
    return (i[0] if isinstance(i, tuple) else i)["kimlik"]


# ---- bellek (kabul kümesi) ----

@dataclasses.dataclass
class Bellek:
    """Kabul kümesi: kimlik → kural (kabul sırasıyla); uyutulanlar ayrı. Tahminler geliştirme havuzunda önbelleklenir."""
    kabul: dict = dataclasses.field(default_factory=dict)
    uyuyan: dict = dataclasses.field(default_factory=dict)
    sira: list = dataclasses.field(default_factory=list)
    _tahmin: dict = dataclasses.field(default_factory=dict)

    def _tahminler(self, kimlik, k, ortam):
        if kimlik not in self._tahmin:
            self._tahmin[kimlik] = {(e, a, b) for e, _, idx in ortam.gelistirme for a, b in k.tahminler(idx)}
        return self._tahmin[kimlik]

    def kapsar_mi(self, k, ortam, haric=None):
        """k'nin geliştirme tanıklarının hepsi kabul kümesince (uyuyanlar ve `haric` dışında) tahmin ediliyor mu."""
        tanik = {(e, a, b) for e, _, idx in ortam.gelistirme for a, b in k.tahminler(idx) if (a, k.bas[0], b) in idx.olgu}
        if not tanik:
            return False
        kalan = set(tanik)
        for kimlik in self.sira:
            diger = self.kabul.get(kimlik)
            if kimlik != haric and diger is not None and diger.bas[0] == k.bas[0]:
                kalan -= self._tahminler(kimlik, diger, ortam)
                if not kalan:
                    return True
        return False

    def kabul_et(self, kimlik, k):
        self.kabul[kimlik] = k
        self.sira.append(kimlik)

    def tabu(self, yeniler, ortam):
        uyutulan = []
        for kimlik in reversed(yeniler):
            if self.kapsar_mi(self.kabul[kimlik], ortam, haric=kimlik):
                self.uyuyan[kimlik] = self.kabul.pop(kimlik)
                uyutulan.append(kimlik)
        return uyutulan


# ---- koşucu ----

@dataclasses.dataclass
class TurIsi:
    basamak: str
    tur: int
    aday_siniri: int
    esik: object = None  # G.Esikler; None → kalibrasyon kipi


def obiter_kaydi(ust, oz):
    k = G.ozunden(oz)
    gen, sol, sag = k.bas
    kayit = {"sema_surumu": "1", "kimlik": "obiter",
             "halkalar": [{"gen": r, "sol": s, "sag": a} for r, s, a in k.halkalar],
             "sonuc": {"gen": gen, "sol": sol, "sag": sag}, "farkli": [list(c) for c in oz["farkli"]],
             "oi": False, "kaynak": {**ust["kaynak"], "ust": [ust["kimlik"]]}, "tanik_ozeti": None, "surum": 1}
    kayit["kimlik"] = "k" + aday.kanonik_kimlik(kayit, ALGORITMA)  # M0 kimlik biçimi
    return kayit


class Kosucu:
    """Bir basamağın turlarını koşar. `havuz` None ise her şey bu süreçte (testler)."""

    def __init__(self, klasor, ortam, taze_fn, havuz=None, defter=None, yasak_ozetler=(), obiter_sirala=True):
        """`obiter_sirala`: aramada obiterin indirgenmişleri sıraya girer; ölçüm akışlarında (B1) girmez."""
        self.klasor = Path(klasor)
        self.ortam, self.taze_fn, self.havuz, self.defter = ortam, taze_fn, havuz, defter
        self.yasak = set(yasak_ozetler)
        self.obiter_sirala = obiter_sirala
        self.on = Kayitci(self.klasor / ON)
        _yerlestir(ortam, taze_fn)

    @classmethod
    def paralel(cls, klasor, kurulum, is_sayisi, defter=None, yasak_ozetler=(), obiter_sirala=True):
        ortam, taze_fn = ortam_kur(kurulum)
        havuz = ProcessPoolExecutor(is_sayisi, initializer=_hazirla, initargs=(kurulum,))
        return cls(klasor, ortam, taze_fn, havuz, defter, yasak_ozetler, obiter_sirala)

    def kapat(self):
        if self.havuz is not None:
            self.havuz.shutdown()

    def _esle(self, fn, isler, kayitci):
        eksik = [i for i in isler if _kimlik(i) not in kayitci.veri]
        sonuclar = map(fn, eksik) if self.havuz is None else self.havuz.map(fn, eksik, chunksize=1)
        for s in sonuclar:
            kayitci.ekle(s)
        return [kayitci.veri[_kimlik(i)] for i in isler]

    def taze(self, is_):
        taze = self.taze_fn(is_.basamak, is_.tur)
        for et, _, d, _ in taze:
            if h2_dunya.dunya_ozeti(d, ALGORITMA) in self.yasak:
                raise DurmaHatasi(f"taze dünya özeti yinelendi: {et}")
        self.yasak |= {h2_dunya.dunya_ozeti(d, ALGORITMA) for _, _, d, _ in taze}
        return taze

    def on_eleme(self, kuyruk, is_, bellek):
        """Sıradan adayları aşama 1–4 ve yedeklilikten geçirir; sorgulanacakları (en çok aday_siniri) döner."""
        sabit = self.ortam.sabit
        gorulen = {k["kimlik"] for k in kuyruk} | set(self.on.veri)
        hukumler, sorgulanacak = {}, []
        while kuyruk and len(sorgulanacak) < is_.aday_siniri:
            parca = {k["kimlik"] for k in kuyruk[:ON_PARCA]}
            self._esle(on_is, kuyruk[:ON_PARCA], self.on)
            while kuyruk and kuyruk[0]["kimlik"] in parca and len(sorgulanacak) < is_.aday_siniri:
                kayit = kuyruk.pop(0)
                on = self.on.veri[kayit["kimlik"]]
                h = G._gelistirme_hukmu(on, sabit) or ("bag_ikizi" in on and G._bag_ikizi_vetosu(on, sabit))
                if h:
                    hukumler[kayit["kimlik"]] = list(h)
                    if h[1] == "obiter" and self.obiter_sirala:
                        yeni = [y for y in (obiter_kaydi(kayit, oz) for oz in on["obiter"]) if y["kimlik"] not in gorulen]
                        gorulen |= {y["kimlik"] for y in yeni}
                        kuyruk[0:0] = yeni
                    continue
                k = kural.Kural.kayittan(kayit)
                if bellek.kapsar_mi(k, self.ortam):
                    hukumler[kayit["kimlik"]] = [UYUTULDU, "yedeklilik"]
                    bellek.uyuyan[kayit["kimlik"]] = k  # ÖK-005 taslağı §8: fazlalık-doğru sınıfında görünür
                    continue
                sorgulanacak.append(kayit)
        return hukumler, sorgulanacak

    def _sorgula(self, is_, adaylar, taze):
        if self.defter is None:
            return
        while self.defter.tur < is_.tur:
            self.defter.tur_ac()
        if self.defter.tur != is_.tur:
            raise DurmaHatasi("sorgu defterinin turu koşunun turuyla uyuşmuyor")
        for kayit in adaylar:
            for et, _, _, _ in taze:
                if (is_.tur, kayit["kimlik"], et) not in self.defter._ciftler:
                    self.defter.sorgu(kayit["kimlik"], et)

    def _wy(self, is_, aile, taze, klasor):
        yol = klasor / WY
        anahtar = ozet(kanonik_json(aile), ALGORITMA)
        if yol.exists():
            kayit = json.loads(yol.read_text(encoding="utf-8"))
            if kayit["aile_ozeti"] == anahtar:
                return kayit
        klasor.mkdir(parents=True, exist_ok=True)
        T = G.wy_gozlenen(aile, taze, self.ortam.sabit.wilson_z)
        B = self.ortam.sabit.wy_cekilis
        parcalar = [(aile, is_.basamak, is_.tur, range(b, min(b + WY_PARCA, B + 1))) for b in range(1, B + 1, WY_PARCA)]
        maks = [m for p in (map(wy_is, parcalar) if self.havuz is None else self.havuz.map(wy_is, parcalar))
                for m in p] if aile else []
        kayit = {"aile_ozeti": anahtar, "T": T, "maks": maks, "p": G.wy_p(T, maks, B)}
        atomik_yaz(yol, kanonik_json(kayit))
        return kayit

    def olcum(self, kimlik, olc):
        """Hüküm için ölçüm: turda sorgulandıysa tam ölçüm, değilse aşama 1–4 ölçümü."""
        return olc.get(kimlik) or self.on.veri[kimlik]

    def tur_kos(self, kuyruk, is_, bellek):
        klasor = self.klasor / f"{is_.basamak}_tur{is_.tur:02d}"
        sabit = self.ortam.sabit
        hukumler, sorgulanacak = self.on_eleme(kuyruk, is_, bellek)
        taze = self.taze(is_)
        self._sorgula(is_, sorgulanacak, taze)
        olc = {}
        for kayit, t in zip(sorgulanacak, self._esle(taze_is, [(k, is_.basamak, is_.tur) for k in sorgulanacak],
                                                      Kayitci(klasor / TAZE_DOSYASI))):
            olc[kayit["kimlik"]] = {**self.on.veri[kayit["kimlik"]], **t}
        aile = G.wy_ailesi([(k["kimlik"], kural.Kural.kayittan(k), olc[k["kimlik"]]) for k in sorgulanacak
                            if G.esiksiz_hukum(olc[k["kimlik"]], sabit) is None])
        wy = self._wy(is_, aile, taze, klasor)
        for kimlik, p in wy["p"].items():
            olc[kimlik]["wy_p"] = p
        cekirdege = [k for k in sorgulanacak if self._cekirdege_mi(olc[k["kimlik"]], is_)]
        for kayit, c in zip(cekirdege, self._esle(cekirdek_is, [(k, is_.basamak, is_.tur) for k in cekirdege],
                                                   Kayitci(klasor / CEKIRDEK))):
            olc[kayit["kimlik"]]["cekirdek"] = c["cekirdek"]
        yeniler = []
        for kayit in sorgulanacak:
            if is_.esik is None:
                continue
            h = G.hukum(olc[kayit["kimlik"]], is_.esik, sabit)
            hukumler[kayit["kimlik"]] = list(h)
            if h[0] == G.KABUL:
                bellek.kabul_et(kayit["kimlik"], kural.Kural.kayittan(kayit))
                yeniler.append(kayit["kimlik"])
        uyutulan = bellek.tabu(yeniler, self.ortam)
        ozet_ = {"basamak": is_.basamak, "tur": is_.tur, "aday_siniri": is_.aday_siniri,
                 "taze": [[et, h2_dunya.dunya_ozeti(d, ALGORITMA)] for et, _, d, _ in taze],
                 "sorgulanan": [k["kimlik"] for k in sorgulanacak], "hukumler": hukumler,
                 "kabul": [k for k in yeniler if k not in uyutulan], "tabu_uyutulan": uyutulan,
                 "wy": {"aile": [a["kimlik"] for a in aile], "p": wy["p"]}}
        atomik_yaz(klasor / OZET, kanonik_json(ozet_))
        return ozet_, olc

    def _cekirdege_mi(self, o, is_):
        sabit = self.ortam.sabit
        if is_.esik is not None:
            return G.sembolik_hukum(o, is_.esik, sabit) is None
        return G.esiksiz_hukum(o, sabit) is None and o.get("wy_p") is not None and o["wy_p"] <= sabit.alfa
