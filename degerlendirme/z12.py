"""sistem.md §11, §13; K-041 (ÖK-005 taslağı §2.3, §5 `havuzB3|<alan>|<havuz>|<aile>|<i>`), V-066: Z12/mod-n dünyaları,
doğrudan üretici (Z12-a ve parametre-kaydırılmış Z24).

Elemanlar 0..n−1; ilişkiler tanım dosyasından gelir (kodda ilişki adı yoktur). Tanım türleri: öteleme (B ≡ A + fark),
iki yönlü öteleme (B ≡ A ± fark), toplam sıfır (A + B ≡ 0, A ≠ B), kalan eşitliği (A ≡ B mod modül, A ≠ B).
Dünya, bütün eleman çiftleri arasındaki bütün olgulardır (kapalı dünya); kimlikler tohumla karıştırılır, çekirdek yalnız
rastgele kimlik görür. Aynı n'deki bütün dünyalar birbirinin yeniden adlandırmasıdır (dürüst not, ÖK §2.3).
"""
import json
from pathlib import Path

from kesif import m0

OTELEME, IKI_YONLU, TOPLAM_SIFIR, KALAN_ESIT = "oteleme", "iki_yonlu_oteleme", "toplam_sifir", "kalan_esit"  # V-066


def tanimlar_yukle(yol):
    return json.loads(Path(yol).read_text(encoding="utf-8"))


def tutar_mi(tanim, a, b, n):
    t = tanim["tur"]
    if t == OTELEME:
        return (b - a - tanim["fark"]) % n == 0
    if t == IKI_YONLU:
        return (b - a - tanim["fark"]) % n == 0 or (b - a + tanim["fark"]) % n == 0
    if t == TOPLAM_SIFIR:
        return a != b and (a + b) % n == 0
    if t == KALAN_ESIT:
        return a != b and (a - b) % tanim["modul"] == 0
    raise ValueError("bilinmeyen tanım türü")


def olgular(n, tanimlar):
    return sorted((a, r, b) for r, t in tanimlar.items() for a in range(n) for b in range(n)
                  if a != b and tutar_mi(t, a, b, n))


def dunya(aile, n, tanimlar, rng):
    kimlik = rng.sample(range(n), n)
    return m0.Dunya(aile, tuple(range(n)), tuple(sorted((kimlik[a], r, kimlik[b]) for a, r, b in olgular(n, tanimlar))))
