"""sistem.md §3 (vektörleştirilmiş maskeli matmul), K-015, K-022, V-040: tamsayı HRR/VSA hızlı yolu (PyTorch, CPU).

Referans yol `cekirdek/vektor.py` ile aynı girdide bit düzeyinde aynı çıktıyı verir. Tamsayı aşaması int64 ve tamdır;
tek kayan nokta adımı kosinüsteki son bölme ve köktür (float64, IEEE doğru yuvarlama). Hız iddiası yoktur; ölçüm
`araclar/hiz_olc.py` ile yapılır.
"""
import torch

from cekirdek.eslesme import AFINITE_OLCEGI
from cekirdek.sekiller import SEKILLER, SekilHatasi
from cekirdek.vektor import ROL_NESNE, ROL_OZNE, TUR_ILISKI, TUR_ROL, TUR_VARLIK

TAMSAYI = torch.int64
ONDALIK = torch.float64
TAM_SINIR = 2 ** 53  # V-040: float64'e tam çevrilebilen en büyük tamsayı aralığı


def tensor_sekli_dogrula(t, eksenler, **boyutlar):
    for eksen in tuple(eksenler) + tuple(boyutlar):
        if eksen not in SEKILLER:
            raise SekilHatasi(f"SEKILLER tablosunda olmayan eksen: {eksen}")
    if t.dim() != len(eksenler):
        raise SekilHatasi(f"beklenen eksenler {eksenler}, şekil {tuple(t.shape)}")
    for eksen, uzunluk in zip(eksenler, t.shape):
        if eksen in boyutlar and boyutlar[eksen] != uzunluk:
            raise SekilHatasi(f"{eksen} ekseni {boyutlar[eksen]} olmalı, {uzunluk} geldi")
    return t


def vektor_tensoru(kk, tur, adlar):
    """[aday × boyut] int64: her ad için kod kitabı vektörü (referans üretimle aynı bitler)."""
    t = torch.tensor([kk.vektor(tur, ad) for ad in adlar], dtype=TAMSAYI).reshape(len(adlar), kk.boyut)
    return tensor_sekli_dogrula(t, ("aday", "boyut"), aday=len(adlar), boyut=kk.boyut)


def donusum_matrisi(p):
    """Dairesel matris M[j,k] = p[(k−j) mod d]: E @ M satır satır p⊛E verir."""
    d = p.shape[0]
    sira = torch.arange(d)
    return p[(sira.unsqueeze(0) - sira.unsqueeze(1)) % d]


@torch.no_grad()
def evrisim_toplu(p, e):
    """[kayit × boyut]: her satır için p⊛E[satır], int64 tam."""
    tensor_sekli_dogrula(p, ("boyut",))
    tensor_sekli_dogrula(e, ("kayit", "boyut"), boyut=p.shape[0])
    if p.dtype != TAMSAYI or e.dtype != TAMSAYI:
        raise SekilHatasi("evrişim yalnız int64 ile yapılır")
    return tensor_sekli_dogrula(e @ donusum_matrisi(p), ("kayit", "boyut"), kayit=e.shape[0], boyut=p.shape[0])


@torch.no_grad()
def kayit_matrisi_hizli(kk, uclular):
    """[kayit × boyut] int64: v = √d·R[r] + P_s⊛E[s] + P_o⊛E[o] (K-014), referans `kayit_matrisi` ile aynı."""
    ozneler = [s for s, _r, _o in uclular]
    iliskiler = [r for _s, r, _o in uclular]
    nesneler = [o for _s, _r, o in uclular]
    p_s = torch.tensor(kk.vektor(TUR_ROL, ROL_OZNE), dtype=TAMSAYI)
    p_o = torch.tensor(kk.vektor(TUR_ROL, ROL_NESNE), dtype=TAMSAYI)
    v = (kk.olcek * vektor_tensoru(kk, TUR_ILISKI, iliskiler)
         + evrisim_toplu(p_s, vektor_tensoru(kk, TUR_VARLIK, ozneler))
         + evrisim_toplu(p_o, vektor_tensoru(kk, TUR_VARLIK, nesneler)))
    return tensor_sekli_dogrula(v, ("kayit", "boyut"), kayit=len(uclular), boyut=kk.boyut)


@torch.no_grad()
def benzerlik_matrisi_hizli(a, b):
    """[kayit × aday] float64 kosinüs; tamsayı nokta çarpımı, tek bölme. Referans `benzerlik_matrisi` ile bit-eşit."""
    tensor_sekli_dogrula(a, ("kayit", "boyut"))
    tensor_sekli_dogrula(b, ("aday", "boyut"), boyut=a.shape[1])
    if a.dtype != TAMSAYI or b.dtype != TAMSAYI:
        raise SekilHatasi("benzerlik yalnız int64 vektörlerle hesaplanır")
    noktalar = a @ b.T
    paydalar = (a * a).sum(dim=1).unsqueeze(1) * (b * b).sum(dim=1).unsqueeze(0)
    if bool((paydalar == 0).any()):
        raise ValueError("sıfır vektörün kosinüsü tanımsız")
    if bool((paydalar >= TAM_SINIR).any()) or bool((noktalar.abs() >= TAM_SINIR).any()):
        raise ValueError("tamsayılar float64'e tam çevrilemiyor (V-040)")
    sonuc = noktalar.to(ONDALIK) / torch.sqrt(paydalar.to(ONDALIK))
    return tensor_sekli_dogrula(sonuc, ("kayit", "aday"), kayit=a.shape[0], aday=b.shape[0])


@torch.no_grad()
def afinite_matrisi_hizli(kayitlar, alicilar):
    """[kayit × aday] afinite = kırp(kosinüs·√3, 0, 1) (K-016), referans `afinite` ile bit-eşit."""
    return torch.clamp(benzerlik_matrisi_hizli(kayitlar, alicilar) * AFINITE_OLCEGI, 0.0, 1.0)
