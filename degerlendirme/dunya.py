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


class OlguTutarsizHatasi(ValueError):
    """Olgular dünya varsayımlarıyla bağdaşmıyor (V-053)."""


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

    def tipli_kisiler(self, a, b, secenekler):
        """a'dan b'ye, seçeneklerin yönlerine uyan (tipe bakmadan) kişi tekrarsız yürüyüşlerde tip şartı olan adımların
        hedef kişileri. a ile b arasındaki ilişki yalnız bu kişilerin tipine bağlıdır (V-048)."""
        sonuc = set()
        for secenek in secenekler:
            def yuru(kisi, adim, gorulen, tipliler):
                if adim == len(secenek):
                    if kisi == b:
                        sonuc.update(tipliler)
                    return
                yon, tip = secenek[adim]
                for s in self._komsular(kisi, yon):
                    if s not in gorulen:
                        yuru(s, adim + 1, gorulen | {s}, tipliler + ((s,) if tip is not None else ()))

            yuru(a, 0, frozenset([a]), ())
        return frozenset(sonuc)

    def olgu_baglari(self, tanimlar):
        """Her kişiden doğrudan bağlarla (olgu ilişkileri) ulaşılan (kişi, ilişki) listesi, sıralı."""
        return {a: tuple(self.iliskiler(a, tanimlar, tanimlar.olgu_iliskileri).items())
                for a in range(self.kisi_sayisi)}


def cikarilabilir_mi(dunya, tanimlar, olgular, sorgu):
    """K-029, ÖK-003 §3.1, V-048: ağaç yapısı sabitken, olguların izin verdiği bütün cinsiyet atamalarında (her olgu
    doğru kalır, eşler karşı cinstendir) sorgu çiftinin ilişkisi aynı mı. Çekirdek kullanılmaz.

    Evli çiftler birlikte çevrilir (karşı cins şartı); evli olmayan kişi tek başına çevrilir. Yalnız olguların ve
    sorgunun tanım yürüyüşlerinde tip şartı olan adımların hedef kişileri değişkendir (başka kişinin tipi hiçbir
    sonucu etkilemez). Geri izlemeyle aranır: olguyu bozan dal budanır, cevabı değişen ilk atamada aranma biter."""
    a, b = sorgu

    def bilesen(p):
        return min(p, dunya.es[p]) if p in dunya.es else p

    hepsi = [s for ad in tanimlar.adlar for s in tanimlar.secenekler[ad]]
    olgu_secenekleri = [s for ad in tanimlar.olgu_iliskileri for s in tanimlar.secenekler[ad]]
    olgu_bag = [(x, r, y, frozenset(map(bilesen, dunya.tipli_kisiler(x, y, olgu_secenekleri)))) for x, r, y in olgular]
    degiskenler = sorted(frozenset(map(bilesen, dunya.tipli_kisiler(a, b, hepsi))).union(*(d for *_, d in olgu_bag)))
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
        if d:  # tip şartı olmayan olgu hiçbir çevirmede bozulmaz
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


# --- V-053: olgulardan çıkarılabilirlik (dünya verilmez) ---------------------------------------------

EBEVEYN, COCUK, ESLIK, KARDES = "ebeveyn", "cocuk", "evlilik", "ortak_ebeveyn"  # V-053: olgu tanımlarının desenleri
EBEVEYN_SAYISI = 2  # V-053: dünya varsayımı (V-017): ebeveyni olan herkesin birbiriyle evli iki ebeveyni vardır


def olgu_bicimi(tanimlar, iliski):
    """Olgu ilişkisinin tanımındaki adım deseni: (biçim, hedefin tipi)."""
    secenekler = tanimlar.secenekler[iliski]
    if len(secenekler) != 1:
        raise NotImplementedError(f"tek seçenekli olmayan olgu tanımı desteklenmiyor: {iliski}")
    adimlar = secenekler[0]
    yonler = tuple(y for y, _ in adimlar)
    tip = adimlar[-1][1]
    if yonler == (YUKARI,):
        return EBEVEYN, tip
    if yonler == (ASAGI,):
        return COCUK, tip
    if yonler == (ES,) and tip is None:
        return ESLIK, None
    if yonler == (YUKARI, ASAGI) and adimlar[0][1] is None:
        return KARDES, tip
    raise NotImplementedError(f"olgu tanımının deseni desteklenmiyor: {iliski}")


class _Birlesim:
    def __init__(self):
        self.ust = {}

    def bul(self, x):
        self.ust.setdefault(x, x)
        while self.ust[x] != x:
            self.ust[x] = self.ust[self.ust[x]]
            x = self.ust[x]
        return x

    def birlestir(self, a, b):
        a, b = self.bul(a), self.bul(b)
        if a != b:
            self.ust[max(a, b)] = min(a, b)
        return a != b


def zorunlu_yapi(tanimlar, olgular, kisiler):
    """Olgular + dünya varsayımlarının zorunlu kıldığı yapı.

    Dönüş: (ebeveyni ortak kişi sınıfları, sınıf → adı geçen ebeveynler, evlilikler, olgularla sabitlenen tipler)."""
    tip, ebeveyn_olgusu, kardes, es = {}, [], [], {}
    for x, r, y in olgular:
        bicim, t = olgu_bicimi(tanimlar, r)
        if t is not None:
            if tip.setdefault(y, t) != t:
                raise OlguTutarsizHatasi(f"{y} için iki farklı tip")
        if bicim == EBEVEYN:
            ebeveyn_olgusu.append((x, y))
        elif bicim == COCUK:
            ebeveyn_olgusu.append((y, x))
        elif bicim == KARDES:
            kardes.append((x, y))
        else:
            for a, b in ((x, y), (y, x)):
                if es.setdefault(a, b) != b:
                    raise OlguTutarsizHatasi(f"{a} için iki farklı evlilik")
    sinif = _Birlesim()
    ebeveynli = set()
    for cocuk, _ in ebeveyn_olgusu:
        ebeveynli.add(cocuk)
        sinif.bul(cocuk)
    for a, b in kardes:
        if a == b:
            raise OlguTutarsizHatasi(f"{a} kendi kardeşi")
        ebeveynli |= {a, b}
        sinif.birlestir(a, b)
    degisti = True
    while degisti:
        degisti = False
        uyeler = {}
        for cocuk, e in ebeveyn_olgusu:
            uyeler.setdefault(sinif.bul(cocuk), set()).add(e)
        # bir kişinin bütün çocukları aynı çiftin çocuklarıdır (varsayım 1 + 2)
        sinifi = {}
        for k, u in uyeler.items():
            for e in u:
                if e in sinifi:
                    degisti |= sinif.birlestir(sinifi[e], k)
                sinifi.setdefault(e, k)
        if degisti:
            continue
        # adı geçen ebeveynin eşi de o sınıfın ebeveynidir; iki ebeveyn evlidir
        for k, u in list(uyeler.items()):
            for e in list(u):
                if e in es and es[e] not in u:
                    ebeveyn_olgusu.append((k, es[e]))
                    degisti = True
            if len(u) > EBEVEYN_SAYISI:
                raise OlguTutarsizHatasi(f"{sorted(u)}: ikiden çok ebeveyn")
            if len(u) == EBEVEYN_SAYISI:
                a, b = sorted(u)
                for p, q in ((a, b), (b, a)):
                    if es.setdefault(p, q) != q:
                        raise OlguTutarsizHatasi(f"{p} için iki farklı evlilik")
    uyeler = {}
    for cocuk, e in ebeveyn_olgusu:
        uyeler.setdefault(sinif.bul(cocuk), set()).add(e)
    siniflar = {}
    for k in ebeveynli:
        siniflar.setdefault(sinif.bul(k), set()).add(k)
    for k, cocuklar in siniflar.items():
        if cocuklar & uyeler.get(k, set()):
            raise OlguTutarsizHatasi("bir kişi kendi ebeveyni")
    return siniflar, {k: sorted(uyeler.get(k, ())) for k in siniflar}, es, tip


def zorunlu_dunya(tanimlar, olgular, sorgu):
    """Zorunlu yapıyı Dunya olarak kurar. Adı geçen kişiler 0..n-1, adsız ebeveynler n.. ; ilk tipler olgulardan,
    eşler karşı cinsten, gerisi keyfî (sonuç buna bağlı değildir: bütün atamalar denenir)."""
    adlar = sorted({x for x, _, y in olgular} | {y for x, _, y in olgular} | set(sorgu), key=repr)
    kimlik = {a: i for i, a in enumerate(adlar)}
    siniflar, uyeler, es, tip = zorunlu_yapi(tanimlar, olgular, adlar)
    sayi = len(adlar)
    es_d = {kimlik[a]: kimlik[b] for a, b in es.items()}
    ebeveynler = {}
    for k in sorted(siniflar, key=repr):
        u = [kimlik[e] for e in uyeler[k]]
        while len(u) < EBEVEYN_SAYISI:  # adı geçen ebeveynin evliliği zorunlu yapıda; eksik ebeveyn adsız düğümdür
            yeni = sayi
            sayi += 1
            if u:
                es_d[u[0]], es_d[yeni] = yeni, u[0]
            u.append(yeni)
        for c in siniflar[k]:
            ebeveynler[kimlik[c]] = tuple(u)
    tipler = [None] * sayi
    for a, t in tip.items():
        tipler[kimlik[a]] = t
    for p in range(sayi):  # eşler karşı cinsten; geri kalan keyfî
        if tipler[p] is None:
            q = es_d.get(p)
            tipler[p] = 1 - tipler[q] if q is not None and tipler[q] is not None else 0
        q = es_d.get(p)
        if q is not None and tipler[q] is None:
            tipler[q] = 1 - tipler[p]
    for p, q in es_d.items():
        if tipler[p] == tipler[q]:
            raise OlguTutarsizHatasi("eşler aynı cinsten")
    return Dunya(tipler, ebeveynler, es_d), kimlik


def olgudan_cikarilabilir_mi(tanimlar, olgular, sorgu, cevap):
    """V-053, K-032 §3: dünya verilmez. Olgular + dünya varsayımlarının zorunlu kıldığı yapıda, cinsiyetlerin olgulara
    uyan bütün atamalarında sorgu çiftinin ilişkisi `cevap` ise True. Varsayımlar: her kişinin ya hiç ebeveyni yoktur
    ya da birbiriyle evli iki ebeveyni vardır; en çok bir evlilik; evli çiftler karşı cinsten. Başka bilgi kullanılmaz."""
    dunya, kimlik = zorunlu_dunya(tanimlar, olgular, sorgu)
    olgular_d = [(kimlik[x], r, kimlik[y]) for x, r, y in olgular]
    sorgu_d = (kimlik[sorgu[0]], kimlik[sorgu[1]])
    if dunya.iliski(*sorgu_d, tanimlar) != cevap:
        return False
    return cikarilabilir_mi(dunya, tanimlar, olgular_d, sorgu_d)


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
