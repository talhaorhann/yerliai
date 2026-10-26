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


def wilson_alt(basari, n, z):
    """Wilson aralığının alt ucu; n tam sayı olmak zorunda değil (kümeli etkin n). n = 0 → 0."""
    if n <= 0:
        return 0.0
    p = basari / n
    payda = 1 + z * z / n
    merkez = p + z * z / (KUYRUK * n)
    yari = z * math.sqrt(max(p * (1 - p) / n + z * z / (KUYRUK * KUYRUK * n * n), 0.0))
    return max((merkez - yari) / payda, 0.0)


def kumeli_wilson_alt(kumeler, z):
    """ÖK-005 taslağı §4 madde 16: kümeler [(başarı, boy)]; ICC ANOVA (Fleiss) kestiricisi, negatifse 0;
    tasarım etkisi = 1 + (m₀ − 1)ρ̂, m₀ = (N − Σmᵢ²/N)/(k − 1); n_etkin = N / tasarım etkisi; Wilson(p̂, n_etkin)."""
    kumeler = [(x, m) for x, m in kumeler if m > 0]
    N = sum(m for _, m in kumeler)
    k = len(kumeler)
    if N == 0:
        return 0.0
    p = sum(x for x, _ in kumeler) / N
    if k < KUYRUK or N == k:  # V-065: tek küme ya da hepsi birer gözlem → küme etkisi kestirilemez, ρ̂ = 0
        return wilson_alt(p * N, N, z)
    msb = sum(m * (x / m - p) ** KUYRUK for x, m in kumeler) / (k - 1)  # V-065: ANOVA (Fleiss), kare
    msw = sum(x * (1 - x / m) for x, m in kumeler) / (N - k)
    m0 = (N - sum(m * m for _, m in kumeler) / N) / (k - 1)
    payda = msb + (m0 - 1) * msw
    rho = max((msb - msw) / payda, 0.0) if payda > 0 else 0.0
    n_etkin = N / (1 + (m0 - 1) * rho)
    return wilson_alt(p * n_etkin, n_etkin, z)


def laplace(rng, olcek):
    """Laplace(0, ölçek) çekilişi (Thresholdout gürültüsü, ÖK-005 taslağı §4 madde 12)."""
    u = rng.random() - 1 / KUYRUK
    return -olcek * math.copysign(1.0, u) * math.log(1 - KUYRUK * abs(u))


def kumeli_bootstrap_fark(kumeler_a, kumeler_b, tekrar, guven, tohum):
    """İki tarafın oranları farkı (a − b) için küme (dünya) yeniden örneklemeli yüzdelik aralık."""
    rng = random.Random(tohum)

    def oran(kumeler):
        n = sum(m for _, m in kumeler)
        return sum(x for x, _ in kumeler) / n if n else 0.0
    farklar = sorted(oran(rng.choices(kumeler_a, k=len(kumeler_a))) - oran(rng.choices(kumeler_b, k=len(kumeler_b)))
                     for _ in range(tekrar))
    yari = (1 - guven) / KUYRUK
    return farklar[math.floor(yari * tekrar)], farklar[math.ceil((1 - yari) * tekrar) - 1]
