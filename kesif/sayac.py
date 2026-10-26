"""sistem.md §3, §13; K-041, V-061 (ÖK-005 taslağı §7, §13.2): sembolik sayaç. Bir şablon gövdesinin bir olgu kümesinde
X ile Y'ye bağladığı (A, B) çiftleri tahmin kümesidir; her çift bir kez sayılır (tanık). Kapalı dünya: tahmin edilen
(A, r, B) olgu kümesinde varsa doğru, yoksa yanlıştır (yanlış = tahmin − doğru).

İki yol (KODLAMA_PROMPTU §4, önce referans):
- `referans_say`: açık geri izlemeli döngü, tek gövde.
- `sablon_say`: aynı biçimli gövdeler toplu tensörle. Bağlama sayıları float32'de tam sayıdır (2²⁴'ün altında), toplama
  sırası sonucu değiştirmez; bit-aynıdır.
OI (bütün değişkenler farklı kişi): birebir bağlama sayısı, değişken kümesinin bölüntüleri üzerinden Möbius
tersinmesiyle (μ(π) = Π (−1)^(|b|−1) (|b|−1)!) hesaplanır.
"""
import dataclasses
import math

import numpy as np
import torch

from cekirdek.sekiller import SEKILLER

HARFLER = "abcd"  # V-061: kişi ekseni harfleri (en çok 4 değişken; 'g' toplu eksen)
TOPLU = "g"  # V-061
EN_COK_ARA_EKSEN = 2  # V-061: ara sonuçta en çok iki kişi ekseni (bellek N² ile sınırlı)
OI_YOK = -1  # V-061: OI'nin anlamsız olduğu gövdede değer yok
KISI = (1, 2)  # V-061: [govde|iliski, kisi, kisi] tensörlerinde kişi eksenleri


@dataclasses.dataclass(frozen=True)
class SayimSonucu:
    tahmin: np.ndarray  # [govde]
    dogru: np.ndarray  # [govde, bas]
    tahmin_oi: np.ndarray  # [govde]; OI anlamsızsa OI_YOK
    dogru_oi: np.ndarray  # [govde, bas]


def _eksen_denetle(t, eksenler):
    for e in eksenler:
        if e not in SEKILLER:
            raise ValueError(f"SEKILLER tablosunda olmayan eksen: {e}")
    if t.dim() != len(eksenler):
        raise ValueError(f"beklenen eksenler {eksenler}, şekil {tuple(t.shape)}")


def iliski_tensoru(kisiler, olgular, iliski_adlari):
    """[iliski, kisi, kisi] float32; R[r, a, b] = 1 ⇔ (a, r, b) olgusu ("b, a'nın r'sidir")."""
    sira = {k: i for i, k in enumerate(kisiler)}
    if len(sira) != len(kisiler):
        raise ValueError("kişi listesinde yineleme")
    rs = {r: i for i, r in enumerate(iliski_adlari)}
    R = torch.zeros((len(iliski_adlari), len(kisiler), len(kisiler)), dtype=torch.float32)
    for a, r, b in olgular:
        if a not in sira or b not in sira:
            raise ValueError("olguda kişi listesinde olmayan kişi")
        if r not in rs:
            raise ValueError("olguda şemada olmayan ilişki")
        R[rs[r], sira[a], sira[b]] = 1
    _eksen_denetle(R, ("iliski", "kisi", "kisi"))
    return R


def referans_say(govde, oi, kisiler, olgular, iliski_adlari, degiskenler=("X", "Y")):
    """(tahmin sayısı, baş ilişkisi başına doğru sayısı). Açık döngü; yalnız küçük girdiler ve testler için."""
    x, y = degiskenler[0], degiskenler[1]
    olgu = set(olgular)
    cikis, giris = {}, {}
    for a, r, b in olgu:
        cikis.setdefault((r, a), set()).add(b)
        giris.setdefault((r, b), set()).add(a)
    halkalar = [(iliski_adlari[r], s, a) for r, s, a in govde]
    ciftler = set()

    def ara(i, bag):
        if i == len(halkalar):
            if not oi or len(set(bag.values())) == len(bag):
                ciftler.add((bag[x], bag[y]))
            return
        r, s, a = halkalar[i]
        if s in bag and a in bag:
            if (bag[s], r, bag[a]) in olgu:
                ara(i + 1, bag)
            return
        if s in bag:
            adaylar = [(bag[s], b) for b in sorted(cikis.get((r, bag[s]), ()))]
        elif a in bag:
            adaylar = [(b, bag[a]) for b in sorted(giris.get((r, bag[a]), ()))]
        else:
            adaylar = sorted((p, q) for p, rr, q in olgu if rr == r)
        for p, q in adaylar:
            if s == a and p != q:
                continue
            ara(i + 1, {**bag, s: p, a: q})

    ara(0, {})
    return len(ciftler), tuple(sum((p, r, q) in olgu for p, q in ciftler) for r in iliski_adlari)


def _bolunturler(ogeler):
    if not ogeler:
        yield []
        return
    ilk, kalan = ogeler[0], ogeler[1:]
    for b in _bolunturler(kalan):
        yield [[ilk]] + b
        for i in range(len(b)):
            yield b[:i] + [[ilk] + b[i]] + b[i + 1:]


def _mobius(bolunti):
    return math.prod((-1) ** (len(b) - 1) * math.factorial(len(b) - 1) for b in bolunti)  # V-061: Möbius tersinmesi


def _kasilt(operandlar, cikti):
    """operandlar: [(harfler, tensör [G, N, ...])]; çıktı harfleri sırasıyla [G, N, ...]. Açgözlü çift kasılımı."""
    ops = []
    for harf, t in operandlar:
        if len(harf) == len(set(harf)) + 1:  # V-061: iki ucu aynı harf → köşegen
            t, harf = torch.diagonal(t, dim1=KISI[0], dim2=KISI[1]), harf[0]
        ops.append((harf, t))
    while True:
        yeni = []
        for i, (harf, t) in enumerate(ops):
            baska = set(cikti).union(*(set(h) for j, (h, _) in enumerate(ops) if j != i))
            kalan = "".join(c for c in harf if c in baska)
            if kalan != harf:
                t = torch.einsum(f"{TOPLU}{harf}->{TOPLU}{kalan}", t)
            yeni.append((kalan, t))
        ops = yeni
        if len(ops) == 1:
            break
        def sonuc_harfleri(i, j):
            digerleri = set(cikti).union(*(set(h) for k, (h, _) in enumerate(ops) if k not in (i, j)))
            return "".join(c for c in sorted(set(ops[i][0]) | set(ops[j][0])) if c in digerleri)
        i, j = min(((i, j) for i in range(len(ops)) for j in range(i + 1, len(ops))),
                   key=lambda c: (len(sonuc_harfleri(*c)), len(set(ops[c[0]][0]) | set(ops[c[1]][0])), c))
        sonuc = sonuc_harfleri(i, j)
        if len(sonuc) > EN_COK_ARA_EKSEN:
            raise ValueError("ara sonuç ikiden çok kişi ekseni ister")
        t = torch.einsum(f"{TOPLU}{ops[i][0]},{TOPLU}{ops[j][0]}->{TOPLU}{sonuc}", ops[i][1], ops[j][1])
        ops = [o for k, o in enumerate(ops) if k not in (i, j)] + [(sonuc, t)]
    harf, t = ops[0]
    if set(harf) != set(cikti):
        raise ValueError("çıktı eksenleri gövdede yok")
    return torch.einsum(f"{TOPLU}{harf}->{TOPLU}{cikti}", t)


def _bag_sayisi(bicim, parca, R, bolunti, degiskenler):
    """Bölüntüdeki her blok tek kişiye bağlanır; X'ten Y'ye bağlama sayısı [G, N, N]."""
    harf = {v: HARFLER[i] for i, blok in enumerate(bolunti) for v in blok}
    ops = [(harf[s] + harf[a], R[parca[:, k]]) for k, (s, a) in enumerate(bicim)]
    x, y = harf[degiskenler[0]], harf[degiskenler[1]]
    if x == y:
        return torch.diag_embed(_kasilt(ops, x))
    return _kasilt(ops, x + y)


def sablon_say(govde_listesi, R, parca_boyu, degiskenler=("X", "Y", "Z", "W")):
    """Gövde başına tahmin ve baş başına doğru sayıları (OI'siz ve OI'li). Aynı biçimli gövdeler toplu sayılır."""
    _eksen_denetle(R, ("iliski", "kisi", "kisi"))
    if R.shape[KISI[0]] != R.shape[KISI[1]]:
        raise ValueError("ilişki tensörü kare değil")
    m = R.shape[0]
    tahmin = np.zeros(len(govde_listesi), dtype=np.int64)
    dogru = np.zeros((len(govde_listesi), m), dtype=np.int64)
    tahmin_oi = np.full(len(govde_listesi), OI_YOK, dtype=np.int64)
    dogru_oi = np.full((len(govde_listesi), m), OI_YOK, dtype=np.int64)
    gruplar = {}
    for i, g in enumerate(govde_listesi):
        gruplar.setdefault(tuple((s, a) for _, s, a in g), []).append(i)
    H = R.reshape(m, -1).T
    with torch.no_grad():
        for bicim in sorted(gruplar):
            sira = gruplar[bicim]
            iliski = torch.tensor([[govde_listesi[i][k][0] for k in range(len(bicim))] for i in sira], dtype=torch.long)
            degisken = sorted({v for c in bicim for v in c}, key=degiskenler.index)
            oi = _oi_anlamli(bicim, degisken)
            for bas in range(0, len(sira), parca_boyu):
                parca = iliski[bas:bas + parca_boyu]
                yer = np.asarray(sira[bas:bas + parca_boyu])
                B = (_bag_sayisi(bicim, parca, R, [[v] for v in degisken], degiskenler) > 0).float()
                _eksen_denetle(B, ("govde", "kisi", "kisi"))
                tahmin[yer] = B.sum(dim=KISI).to(torch.int64).numpy()
                dogru[yer] = (B.reshape(len(parca), -1) @ H).to(torch.int64).numpy()
                if oi:
                    tahmin_oi[yer], dogru_oi[yer] = 0, 0
                    dolu = torch.nonzero(B.sum(dim=KISI) > 0).flatten()  # V-061: OI eşleşmesi OI'sizin altkümesidir
                    if len(dolu):
                        birebir = sum(_mobius(b) * _bag_sayisi(bicim, parca[dolu], R, b, degiskenler)
                                      for b in _bolunturler(degisken))
                        if (birebir < 0).any():
                            raise ValueError("birebir bağlama sayısı negatif")
                        B = (birebir > 0).float()
                        tahmin_oi[yer[dolu.numpy()]] = B.sum(dim=KISI).to(torch.int64).numpy()
                        dogru_oi[yer[dolu.numpy()]] = (B.reshape(len(dolu), -1) @ H).to(torch.int64).numpy()
    return SayimSonucu(tahmin, dogru, tahmin_oi, dogru_oi)


def _oi_anlamli(bicim, degisken):
    bitisik = {frozenset(c) for c in bicim}
    return any(frozenset((a, b)) not in bitisik for i, a in enumerate(degisken) for b in degisken[i + 1:])
