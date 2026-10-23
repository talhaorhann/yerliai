"""sistem.md §1, §3; K-014: tamsayı HRR/VSA vektörleri, saf Python referans yolu.

v = √d·R[ilişki] + P_s⊛E[özne] + P_o⊛E[nesne]; öğeler ±1, ⊛ tamsayıyla tam dairesel evrişim.
Yuvarlama yoktur; tek kayan nokta işlemi kosinüsteki son bölmedir (CPU, float64). Hızlı yol K-015 ile ertelendi.
"""
import hashlib
import math

from cekirdek.sekiller import SekilHatasi, sekil_dogrula

TUR_VARLIK, TUR_ILISKI, TUR_ROL = "varlik", "iliski", "rol"
ROL_OZNE, ROL_NESNE = "ozne", "nesne"
BAYT_BITI = 8  # V-026: SHAKE-256 baytı başına 8 bit


class KodKitabi:
    """(tohum, tür, ad) → ±1 vektör. Durumsuzdur: ekleme sırası ve Python hash() sonucu etkilemez (V-026)."""

    def __init__(self, tohum, boyut):
        olcek = math.isqrt(boyut) if boyut > 0 else 0
        if boyut <= 0 or boyut % BAYT_BITI or olcek * olcek != boyut:
            raise ValueError(f"vektör boyutu 8'in katı ve tam kare olmalı: {boyut}")
        self.tohum = tohum
        self.boyut = boyut
        self.olcek = olcek  # K-014: √d, ilişki bileşenini bağlı bileşenlerle aynı büyüklüğe getirir

    def vektor(self, tur, ad):
        baytlar = hashlib.shake_256(f"{self.tohum}|{tur}|{ad}".encode("utf-8")).digest(self.boyut // BAYT_BITI)
        v = tuple(1 if (baytlar[i // BAYT_BITI] >> (i % BAYT_BITI)) & 1 else -1 for i in range(self.boyut))
        return sekil_dogrula(v, ("boyut",), boyut=self.boyut)


def _ayni_uzunluk(a, b):
    if len(a) != len(b):
        raise SekilHatasi(f"boyut uyuşmuyor: {len(a)} ile {len(b)}")
    return len(a)


def evrisim(a, b):
    """Dairesel evrişim: c[k] = Σ_j a[j]·b[(k−j) mod d]. Tamsayıyla tam."""
    d = _ayni_uzunluk(a, b)
    return tuple(sum(a[j] * b[(k - j) % d] for j in range(d)) for k in range(d))


def ters(a):
    """Yaklaşık ters (involüsyon): a†[k] = a[−k mod d]. ±1 vektörde (a†⊛a)[0] = d."""
    d = len(a)
    return tuple(a[(-k) % d] for k in range(d))


def nokta(a, b):
    _ayni_uzunluk(a, b)
    return sum(x * y for x, y in zip(a, b))


def kosinus(a, b):
    paydalar = nokta(a, a) * nokta(b, b)
    if paydalar == 0:
        raise ValueError("sıfır vektörün kosinüsü tanımsız")
    return nokta(a, b) / math.sqrt(paydalar)


def kayit_vektoru(kk, ozne, iliski, nesne):
    r = kk.vektor(TUR_ILISKI, iliski)
    s = evrisim(kk.vektor(TUR_ROL, ROL_OZNE), kk.vektor(TUR_VARLIK, ozne))
    o = evrisim(kk.vektor(TUR_ROL, ROL_NESNE), kk.vektor(TUR_VARLIK, nesne))
    v = tuple(kk.olcek * x + y + z for x, y, z in zip(r, s, o))
    return sekil_dogrula(v, ("boyut",), boyut=kk.boyut)


def kayit_matrisi(kk, uclular):
    """[kayit × boyut]: her (özne, ilişki, nesne) için kayıt vektörü; satırlar birbirinden bağımsız."""
    m = [kayit_vektoru(kk, s, r, o) for s, r, o in uclular]
    return sekil_dogrula(m, ("kayit", "boyut"), kayit=len(uclular), boyut=kk.boyut)


def benzerlik_matrisi(a, b):
    """[kayit × aday] kosinüs matrisi."""
    m = [[kosinus(x, y) for y in b] for x in a]
    return sekil_dogrula(m, ("kayit", "aday"), kayit=len(a), aday=len(b))


def _en_iyi(puanlar):
    """En yüksek puanlı aday; eşitlikte ilk aday (sıra çağıranın verdiği sıradır)."""
    en_iyi, en_iyi_puan = None, None
    for aday, puan in puanlar:
        if en_iyi_puan is None or puan > en_iyi_puan:
            en_iyi, en_iyi_puan = aday, puan
    return en_iyi


def coz(kk, v, rol, adaylar):
    """Rolün tersiyle çözüp en yakın varlığı (temizleme) döndürür."""
    if rol not in (ROL_OZNE, ROL_NESNE):
        raise ValueError(f"bilinmeyen rol: {rol}")
    u = evrisim(ters(kk.vektor(TUR_ROL, rol)), v)
    return _en_iyi((a, nokta(u, kk.vektor(TUR_VARLIK, a))) for a in adaylar)


def iliski_coz(kk, v, adaylar):
    return _en_iyi((a, nokta(v, kk.vektor(TUR_ILISKI, a))) for a in adaylar)
