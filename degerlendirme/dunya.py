"""sistem.md §11, K-007: soyut soy ağacı (tamsayı kişi, iki tip, yukarı/aşağı/evlilik bağı) ve gizli yapısal tanımlar.

Kodda hiçbir ilişki adı yoktur. Bir ilişki, A'dan B'ye kişi tekrarlamayan bir yürüyüş tanımdaki adımlara
uyuyorsa vardır (V-019). Tanımlar yalnız degerlendirme/ tarafından okunur (kâhin).
"""
import json

from cekirdek.altyapi.sema_dogrulayici import sema_yukle

YUKARI, ASAGI, ES = "U", "D", "E"


class TanimHatasi(ValueError):
    pass


class CokluIliskiHatasi(ValueError):
    pass


class Tanimlar:
    def __init__(self, adlar, secenekler, olgu_iliskileri):
        self.adlar = tuple(adlar)
        self.secenekler = dict(secenekler)
        self.olgu_iliskileri = tuple(olgu_iliskileri)

    def takasli(self, a, b):
        """İki ilişkinin tanımını yer değiştirir (yalnız testlerde sahte kod denetimi için)."""
        yeni = dict(self.secenekler)
        yeni[a], yeni[b] = self.secenekler[b], self.secenekler[a]
        return Tanimlar(self.adlar, yeni, self.olgu_iliskileri)


def tanimlar_yukle(yol, bicim_yolu, iliski_semasi):
    with open(yol, encoding="utf-8") as f:
        veri = json.load(f)
    hatalar = sema_yukle(bicim_yolu).hatalar(veri)
    if hatalar:
        raise TanimHatasi("tanım dosyası biçime uymuyor: " + "; ".join(hatalar))
    adlar = [t["ad"] for t in veri["tanimlar"]]
    if len(set(adlar)) != len(adlar):
        raise TanimHatasi("yinelenen tanım")
    if set(adlar) != set(iliski_semasi.adlar):
        raise TanimHatasi("tanımlar onaylı ilişki şemasıyla birebir örtüşmüyor")
    if not set(veri["olgu_iliskileri"]) <= set(adlar):
        raise TanimHatasi("olgu ilişkisi tanımlarda yok")
    secenekler = {t["ad"]: tuple(tuple((a["yon"], a["tip"]) for a in s) for s in t["secenekler"])
                  for t in veri["tanimlar"]}
    return Tanimlar(adlar, secenekler, veri["olgu_iliskileri"])


class Dunya:
    def __init__(self, tip, ebeveynler, es):
        self.tip = tuple(tip)
        self.ebeveynler = dict(ebeveynler)
        self.es = dict(es)
        cocuklar = {}
        for cocuk in sorted(self.ebeveynler):
            for e in self.ebeveynler[cocuk]:
                cocuklar.setdefault(e, []).append(cocuk)
        self.cocuklar = {k: tuple(v) for k, v in cocuklar.items()}

    @property
    def kisi_sayisi(self):
        return len(self.tip)

    @classmethod
    def uret(cls, rng, nesil_sayisi, cocuk_en_az, cocuk_en_cok):
        """Kök çift; her çiftin cocuk_en_az..cocuk_en_cok çocuğu; son nesil dışındaki her çocuk ağaç dışından
        karşı tipte biriyle evlenir (V-017). Akraba evliliği yoktur, her çocuğun iki ebeveyni birbiriyle evlidir."""
        tip, ebeveynler, es = [], {}, {}

        def yeni(t):
            tip.append(t)
            return len(tip) - 1

        kok_a, kok_b = yeni(1), yeni(0)
        es[kok_a], es[kok_b] = kok_b, kok_a
        ciftler = [(kok_a, kok_b)]
        for nesil in range(nesil_sayisi - 1):
            sonraki = []
            for a, b in ciftler:
                for _ in range(rng.randint(cocuk_en_az, cocuk_en_cok)):
                    cocuk = yeni(rng.randint(0, 1))
                    ebeveynler[cocuk] = (a, b)
                    if nesil < nesil_sayisi - 2:  # V-017: son nesil (sonuncu çocuklar) evlenmez
                        eslik = yeni(1 - tip[cocuk])
                        es[cocuk], es[eslik] = eslik, cocuk
                        sonraki.append((cocuk, eslik))
            ciftler = sonraki
        return cls(tip, ebeveynler, es)

    def _komsular(self, kisi, yon):
        if yon == YUKARI:
            return self.ebeveynler.get(kisi, ())
        if yon == ASAGI:
            return self.cocuklar.get(kisi, ())
        return (self.es[kisi],) if kisi in self.es else ()

    def uclar(self, a, secenek):
        """a'dan başlayıp seçeneğin adımlarına uyan, kişi tekrarlamayan yürüyüşlerin bitiş noktaları."""
        sonuc = set()

        def yuru(kisi, adim, gorulen):
            if adim == len(secenek):
                sonuc.add(kisi)
                return
            yon, tip = secenek[adim]
            for sonraki in self._komsular(kisi, yon):
                if sonraki in gorulen or (tip is not None and self.tip[sonraki] != tip):
                    continue
                yuru(sonraki, adim + 1, gorulen | {sonraki})

        yuru(a, 0, frozenset([a]))
        return sonuc

    def iliskiler(self, a, tanimlar, adlar=None):
        """a'dan her b'ye olan ilişki adı. Bir çifte birden fazla ilişki uyarsa tanımlar hatalıdır: durur."""
        sonuc = {}
        for ad in (tanimlar.adlar if adlar is None else adlar):
            for secenek in tanimlar.secenekler[ad]:
                for b in self.uclar(a, secenek):
                    if sonuc.get(b, ad) != ad:
                        raise CokluIliskiHatasi(f"{a} ile {b} arasında birden fazla ilişki: {sonuc[b]}, {ad}")
                    sonuc[b] = ad
        return dict(sorted(sonuc.items()))

    def iliski(self, a, b, tanimlar):
        return self.iliskiler(a, tanimlar).get(b)

    def komsular(self, kisi):
        return tuple(self.ebeveynler.get(kisi, ())) + tuple(self.cocuklar.get(kisi, ())) + \
            ((self.es[kisi],) if kisi in self.es else ())

    def yol_kisileri(self, a, b, en_cok):
        """a'dan b'ye en çok `en_cok` adımlı, kişi tekrarlamayan bütün yürüyüşlerdeki kişiler (tip gözetilmez)."""
        sonuc = set()

        def yuru(kisi, yol):
            if kisi == b and len(yol) > 1:
                sonuc.update(yol)
                return
            if len(yol) > en_cok:
                return
            for s in self.komsular(kisi):
                if s not in yol:
                    yuru(s, yol + (s,))

        yuru(a, (a,))
        return frozenset(sonuc)

    def olgu_baglari(self, tanimlar):
        """Her kişiden doğrudan bağlarla (olgu ilişkileri) ulaşılan (kişi, ilişki) listesi, sıralı."""
        return {a: tuple(self.iliskiler(a, tanimlar, tanimlar.olgu_iliskileri).items())
                for a in range(self.kisi_sayisi)}


def cikarilabilir_mi(dunya, tanimlar, olgular, sorgu):
    """K-029, ÖK-003 §3.1, V-048: ağaç yapısı sabitken, olguların izin verdiği bütün cinsiyet atamalarında (her olgu
    doğru kalır, eşler karşı cinstendir) sorgu çiftinin ilişkisi aynı mı. Çekirdek kullanılmaz.

    Evli çiftler birlikte çevrilir (karşı cins şartı); evli olmayan kişi tek başına çevrilir. Yalnız olguların ve
    sorgunun yürüyüşlerinde geçen kişilerin bileşenleri değişken sayılır (başka kişinin tipi hiçbir sonucu
    etkilemez). Geri izlemeyle aranır: olguyu bozan dal budanır, cevabı değişen ilk atamada aranma biter."""
    a, b = sorgu

    def bilesen(p):
        return min(p, dunya.es[p]) if p in dunya.es else p

    en_uzun = max(len(s) for secenekler in tanimlar.secenekler.values() for s in secenekler)
    olgu_en_uzun = max(len(s) for r in tanimlar.olgu_iliskileri for s in tanimlar.secenekler[r])
    olgu_bag = [(x, r, y, frozenset(map(bilesen, dunya.yol_kisileri(x, y, olgu_en_uzun)))) for x, r, y in olgular]
    degiskenler = sorted(frozenset(map(bilesen, dunya.yol_kisileri(a, b, en_uzun))).union(*(d for *_, d in olgu_bag)))
    sira = {c: i for i, c in enumerate(degiskenler)}

    def kur(cevrilen):
        return Dunya([t ^ (bilesen(p) in cevrilen) for p, t in enumerate(dunya.tip)], dunya.ebeveynler, dunya.es)

    def olgu_dogru(w, x, r, y):
        return w.iliskiler(x, tanimlar, tanimlar.olgu_iliskileri).get(y) == r

    if not all(olgu_dogru(dunya, x, r, y) for x, r, y, _ in olgu_bag):
        raise ValueError("olgular gerçek dünyaya uymuyor")
    hedef = dunya.iliski(a, b, tanimlar)
    # her olgu, bağımlı olduğu son değişken atanınca denetlenir
    denetim = {}
    for x, r, y, d in olgu_bag:
        denetim.setdefault(max(sira[c] for c in d), []).append((x, r, y))

    def ara(i, cevrilen):
        if i:
            w = kur(cevrilen)
            if not all(olgu_dogru(w, x, r, y) for x, r, y in denetim.get(i - 1, ())):
                return True  # olguların izin vermediği atama: karşı örnek değil
        if i == len(degiskenler):
            return kur(cevrilen).iliski(a, b, tanimlar) == hedef
        return ara(i + 1, cevrilen) and ara(i + 1, cevrilen | {degiskenler[i]})

    return ara(0, frozenset())


ADIM_METNI = {YUKARI: "ebeveyni", ASAGI: "çocuğu", ES: "evlendiği kişi"}  # V-019: okunur gösterim


def okunur_tanimlar(tanimlar):
    """Gizli tanımları kullanıcının okuyabileceği tabloya çevirir (yalnız degerlendirme/ içinde kullanılır)."""
    satirlar = ["| İlişki | B, A'nın ... (adım adım) |", "|---|---|"]
    for ad in tanimlar.adlar:
        secenekler = []
        for secenek in tanimlar.secenekler[ad]:
            adimlar = [ADIM_METNI[yon] + ("" if tip is None else f" (tip {tip})") for yon, tip in secenek]
            secenekler.append(" → ".join(adimlar))
        satirlar.append(f"| {ad} | {' ya da '.join(secenekler)} |")
    return "\n".join(satirlar)
