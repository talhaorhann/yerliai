"""sistem.md §6, K-018, KODLAMA_PROMPTU §5 (Sayısal): plazma hücresi.

Sorgu (A, B) çıkarım katmanıyla eşleştirilir. Aynı ilişkiye giden ispatlar kök kümelerine (katman 0 ataları) göre
bileşenlere ayrılır: kesişen kök kümeleri aynı bileşendir (ortak atalılar tek sayılır). Bileşen içi MAX, bileşenler
arası noisy-OR (log1p/expm1, sızıntı 0). İspat yoksa ya da en yüksekte eşitlik varsa cevap "bilmiyorum" (None).
Güven bir olasılık değildir.
"""
import math
from dataclasses import dataclass

from cekirdek.havuz import CIKARIM, EPITOP


@dataclass(frozen=True)
class Cevap:
    iliski: object
    guven: object
    birlesik: tuple
    celiski: bool
    gerekce: tuple


def kok_kumesi(havuz, kimlik):
    kokler, yigin, gorulen = set(), [kimlik], set()
    while yigin:
        k = havuz.kayit(yigin.pop())
        if k.kimlik in gorulen:
            continue
        gorulen.add(k.kimlik)
        if k.katman == EPITOP:
            kokler.add(k.kimlik)
        else:
            yigin.extend(k.ebeveynler)
    return frozenset(kokler)


def noisy_or(guvenler):
    """1 − Π(1 − g), log1p/expm1 ile; [0,1]'e kırpılır."""
    if not guvenler:
        return 0.0
    if any(g >= 1 for g in guvenler):
        return 1.0
    return max(0.0, min(1.0, -math.expm1(sum(math.log1p(-g) for g in guvenler))))


def _bilesen_maksimumlari(havuz, ispatlar):
    kokler = [kok_kumesi(havuz, k.kimlik) for k in ispatlar]
    ebeveyn = list(range(len(ispatlar)))

    def kok(i):
        while ebeveyn[i] != i:
            ebeveyn[i] = ebeveyn[ebeveyn[i]]
            i = ebeveyn[i]
        return i
    for i in range(len(ispatlar)):
        for j in range(i):
            if kokler[i] & kokler[j]:
                ebeveyn[kok(i)] = kok(j)
    maks = {}
    for i, k in enumerate(ispatlar):
        r = kok(i)
        maks[r] = max(maks.get(r, k.guven), k.guven)
    return [maks[r] for r in sorted(maks)]


def _agac(havuz, kimlik):
    k = havuz.kayit(kimlik)
    return {"kimlik": k.kimlik, "uclu": list(k.uclu), "katman": k.katman, "guven": k.guven, "zincir": k.zincir,
            "ebeveynler": [_agac(havuz, e) for e in k.ebeveynler]}


def cevapla(havuz, sorgu):
    a, b = sorgu
    ispatlar = {}
    for k in havuz.kayitlar():
        ozne, iliski, nesne = k.uclu
        if k.katman == CIKARIM and (ozne, nesne) == (a, b):
            ispatlar.setdefault(iliski, []).append(k)
    if not ispatlar:
        return Cevap(None, None, (), False, ())
    birlesik = {r: noisy_or(_bilesen_maksimumlari(havuz, liste)) for r, liste in ispatlar.items()}
    en_yuksek = max(birlesik.values())
    kazananlar = sorted(r for r, g in birlesik.items() if g == en_yuksek)
    ozet = tuple(sorted(birlesik.items()))
    celiski = len(birlesik) > 1
    if len(kazananlar) > 1:
        return Cevap(None, None, ozet, celiski, ())
    r = kazananlar[0]
    return Cevap(r, en_yuksek, ozet, celiski, tuple(_agac(havuz, k.kimlik) for k in ispatlar[r]))
