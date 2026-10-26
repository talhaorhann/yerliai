"""sistem.md §3, §13; K-041 (ÖK-005 taslağı §6): tipli şablon ailesi T ve kademeleri.

Gövde: 1..en_cok_halka halka; her halka (ilişki sırası, sol, sağ). Değişkenler: ilk ikisi baş (X'ten Y'ye), kalanlar ek
değişken; ek değişkenler sırayla kullanılır (ikincisi birincisi olmadan geçmez). Gövde bağlıdır ve baş değişkenlerini
içerir; iki ucu aynı değişken olan halka yoktur; aynı halka iki kez geçmez. Kanonik biçim: halkalar sıralı, ek
değişkenlerin adlandırması sözlük sırasında en küçük olan. Baş, şemadaki ilişkilerden biridir; gövde başın kendisini
(aynı ilişki, X'ten Y'ye) içeriyorsa aday atılır. OI (bütün değişkenler farklı kişi) yalnız bitişik olmayan bir değişken çifti olan gövdede ayrı
adaydır. Akrabalık ve Z12'de tek tür olduğu için tip budaması yoktur (V-059).
"""
import itertools

BAS = 2  # K-041: baş iki değişkenlidir (X'ten Y'ye); değişken listesinin ilk ikisi


def _bagli(govde, bas):
    komsu = {}
    for _, a, b in govde:
        komsu.setdefault(a, set()).add(b)
        komsu.setdefault(b, set()).add(a)
    gorulen, yigin = {bas}, [bas]
    while yigin:
        for w in komsu[yigin.pop()] - gorulen:
            gorulen.add(w)
            yigin.append(w)
    return gorulen == set(komsu)


def zincir_mi(govde, degiskenler):
    """Baş uçları arasında dallanmasız yol (her ara değişken iki kez, baş uçları bir kez)."""
    x, y = degiskenler[:BAS]
    derece = {}
    for _, a, b in govde:
        derece[a] = derece.get(a, 0) + 1
        derece[b] = derece.get(b, 0) + 1
    return (len(derece) == len(govde) + 1 and derece.get(x) == 1 and derece.get(y) == 1
            and all(d == 2 for v, d in derece.items() if v not in (x, y)) and _bagli(govde, x))  # K-041: yol tanımı


def oi_anlamli_mi(govde):
    degisken = sorted({d for _, a, b in govde for d in (a, b)})
    bitisik = {frozenset((a, b)) for _, a, b in govde}
    return any(frozenset(c) not in bitisik for c in itertools.combinations(degisken, 2))  # K-041: değişken çifti


def _kanonik(govde, ekler):
    adlandirmalar = []
    for sira in itertools.permutations(ekler):
        esle = dict(zip(ekler, sira))
        adlandirmalar.append(tuple(sorted((r, esle.get(a, a), esle.get(b, b)) for r, a, b in govde)))
    return min(adlandirmalar)


def govdeler(iliski_sayisi, degiskenler, en_cok_halka, yalniz_zincir):
    """Kanonik gövdeler, sıralı ve tekil."""
    x, y = degiskenler[:BAS]
    ekler = tuple(degiskenler[BAS:])
    halkalar = [(r, a, b) for r in range(iliski_sayisi) for a in degiskenler for b in degiskenler if a != b]
    sonuc = set()
    for n in range(1, en_cok_halka + 1):
        for g in itertools.combinations(halkalar, n):
            kullanilan = {d for _, a, b in g for d in (a, b)}
            if not {x, y} <= kullanilan:
                continue
            if any(ekler[i] in kullanilan and ekler[i - 1] not in kullanilan for i in range(1, len(ekler))):
                continue
            if not _bagli(g, x) or (yalniz_zincir and not zincir_mi(g, degiskenler)):
                continue
            sonuc.add(_kanonik(g, tuple(e for e in ekler if e in kullanilan)))
    return sorted(sonuc)


def adaylar(govde_listesi, bas_sayisi, degiskenler=("X", "Y")):
    """(gövde, baş ilişkisi sırası, oi) üçlüleri; sıralı ve kesin."""
    x, y = degiskenler[:BAS]
    for g in govde_listesi:
        oi_secenekleri = (False, True) if oi_anlamli_mi(g) else (False,)
        for bas in range(bas_sayisi):
            if (bas, x, y) in g:
                continue
            for oi in oi_secenekleri:
                yield g, bas, oi


def sayim(govde_listesi, bas_sayisi, degiskenler=("X", "Y")):
    """(OI'siz kural sayısı, OI'li varyantlarla aday sayısı)."""
    kural = oili = 0
    for g, _, oi in adaylar(govde_listesi, bas_sayisi, degiskenler):
        oili += 1
        kural += not oi
    return kural, oili


def aday_kaydi(govde, bas, oi, iliski_adlari, degiskenler, tur="m0", tohum=None):
    """Tek aday şemasına (sema/aday_v1) uygun kayıt; kimlik sonradan kanonik kimlikle değiştirilebilir."""
    x, y = degiskenler[:BAS]
    return {"sema_surumu": "1", "kimlik": "sablon_adayi",
            "halkalar": [{"gen": iliski_adlari[r], "sol": a, "sag": b} for r, a, b in govde],
            "sonuc": {"gen": iliski_adlari[bas], "sol": x, "sag": y}, "farkli": [], "oi": oi,
            "kaynak": {"tur": tur, "aile": None, "tohum": tohum, "ust": []}, "tanik_ozeti": None, "surum": 1}
