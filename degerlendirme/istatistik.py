"""KODLAMA_PROMPTU §5 (İstatistik), ÖK-002 §5, V-044: Clopper–Pearson aralığı ve yüzdelik bootstrap (saf Python).

Rastgelelik yalnız verilen tohumdan gelir. Bu sayılar raporlama içindir; H1 kapı kararı tamsayı sayımlarla verilir
(ÖK-002 §6).
"""
import math
import random

YARILAMA_ADIMI = 200  # V-044: ikiye bölme adımı; aralık 2^-200'e iner, float64 çözünürlüğünden çok daha ince
KUYRUK = 2  # V-044: iki yanlı aralık; 1 − güven iki kuyruğa eşit bölünür


def _binom_kdf(x, n, p):
    """P(X ≤ x), X ~ Binom(n, p); terimler log uzayında toplanır."""
    if x < 0:
        return 0.0
    if x >= n or p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    lp, lq = math.log(p), math.log1p(-p)
    terimler = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq
                for i in range(x + 1)]
    en_buyuk = max(terimler)
    return math.exp(en_buyuk) * math.fsum(math.exp(t - en_buyuk) for t in terimler)


def _yarila(artan_mi, fonksiyon, hedef):
    """[0, 1]'de tekdüze `fonksiyon` için fonksiyon(p) = hedef noktası (ikiye bölme)."""
    alt, ust = 0.0, 1.0
    for _ in range(YARILAMA_ADIMI):
        orta = (alt + ust) / KUYRUK  # V-044: ikiye bölme (orta nokta)
        if (fonksiyon(orta) < hedef) == artan_mi:
            alt = orta
        else:
            ust = orta
    return (alt + ust) / KUYRUK  # V-044: orta nokta


def clopper_pearson(x, n, guven):
    """n denemede x başarı için iki yanlı kesin (Clopper–Pearson) güven aralığı."""
    if n <= 0 or not 0 <= x <= n:
        raise ValueError(f"geçersiz sayım: {x}/{n}")
    if not 0 < guven < 1:
        raise ValueError(f"güven düzeyi (0, 1) aralığında olmalı: {guven}")
    yari = (1 - guven) / KUYRUK
    alt = 0.0 if x == 0 else _yarila(True, lambda p: 1 - _binom_kdf(x - 1, n, p), yari)
    ust = 1.0 if x == n else _yarila(False, lambda p: _binom_kdf(x, n, p), yari)
    return alt, ust


def bootstrap_araligi(degerler, tekrar, guven, tohum):
    """Ortalamanın yüzdelik bootstrap güven aralığı; boş listede None."""
    if not degerler:
        return None
    rng = random.Random(tohum)
    n = len(degerler)
    ortalamalar = sorted(math.fsum(rng.choices(degerler, k=n)) / n for _ in range(tekrar))
    yari = (1 - guven) / KUYRUK
    return ortalamalar[math.floor(yari * tekrar)], ortalamalar[math.ceil((1 - yari) * tekrar) - 1]
