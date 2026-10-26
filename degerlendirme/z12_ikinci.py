"""sistem.md §11, §13; K-041 (ÖK-005 taslağı §2.3: Z12-b ikinci üretici), V-066: Z12-b, bileşenlerden hesaplanan
ilişkiler (Çin kalan teoremi).

Ayrı koddur: doğrudan üreticiyi (`z12.py`) kullanmaz. Eleman, bileşen modülleri (ör. 3 ve 4) için kalanların demetidir;
öteleme her bileşene aynı farkla uygulanır, toplam sıfır her bileşende sıfırdır, "A ≡ B (mod m)" her bileşen q için
farkın ebob(m, q)'ya bölünmesidir. Modüller aralarında asal olduğundan sonuç doğrudan modüler aritmetiğin yeniden
adlandırmasıdır; kimlikler tohumla karıştırılır.
"""
import itertools
import math

from kesif import m0


def _elemanlar(moduller):
    return list(itertools.product(*(range(q) for q in moduller)))


def _fark(x, y, moduller, d):
    return all((b - a - d) % q == 0 for a, b, q in zip(x, y, moduller))


def tutar_mi(tanim, x, y, moduller):
    t = tanim["tur"]
    if t == "oteleme":
        return _fark(x, y, moduller, tanim["fark"])
    if t == "iki_yonlu_oteleme":
        return _fark(x, y, moduller, tanim["fark"]) or _fark(x, y, moduller, -tanim["fark"])
    if t == "toplam_sifir":
        return x != y and all((a + b) % q == 0 for a, b, q in zip(x, y, moduller))
    if t == "kalan_esit":
        return x != y and all((a - b) % math.gcd(tanim["modul"], q) == 0 for a, b, q in zip(x, y, moduller))
    raise ValueError("bilinmeyen tanım türü")


def dunya(aile, moduller, tanimlar, rng):
    elemanlar = _elemanlar(moduller)
    kimlik = dict(zip(elemanlar, rng.sample(range(len(elemanlar)), len(elemanlar))))
    olg = sorted((kimlik[x], r, kimlik[y]) for r, t in tanimlar.items() for x in elemanlar for y in elemanlar
                 if x != y and tutar_mi(t, x, y, moduller))
    return m0.Dunya(aile, tuple(range(len(elemanlar))), tuple(olg))
