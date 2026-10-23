"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A2 vektör koduna kasıtlı hata sokar, test takımı kırmızıya dönmeli.

Kullanım: python3 araclar/mutasyon_a2.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

VEK = "cekirdek/vektor.py"
SEK = "cekirdek/sekiller.py"

MUTASYONLAR = [
    ("evrişim yerine korelasyon", VEK, "b[(k - j) % d]", "b[(k + j) % d]"),
    ("ilişki ölçeği yok", VEK, "kk.olcek * x + y + z", "x + y + z"),
    ("tohum Python hash() ile", VEK, 'hashlib.shake_256(f"{self.tohum}|{tur}|{ad}".encode("utf-8"))',
     'hashlib.shake_256(str(hash(f"{self.tohum}|{tur}|{ad}")).encode("utf-8"))'),
    ("iki rol aynı vektör", VEK, "kk.vektor(TUR_ROL, ROL_NESNE), kk.vektor(TUR_VARLIK, nesne)",
     "kk.vektor(TUR_ROL, ROL_OZNE), kk.vektor(TUR_VARLIK, nesne)"),
    ("ters işlemi yok", VEK, "return tuple(a[(-k) % d] for k in range(d))", "return tuple(a)"),
    ("kosinüste kök yok", VEK, "math.sqrt(paydalar)", "paydalar"),
    ("bit eşlemesi ters", VEK, "1 if (baytlar[i // BAYT_BITI] >> (i % BAYT_BITI)) & 1 else -1",
     "-1 if (baytlar[i // BAYT_BITI] >> (i % BAYT_BITI)) & 1 else 1"),
    ("sıfır vektör denetimi yok", VEK, "if paydalar == 0:", "if False:"),
    ("eksen sayısı denetimi kapalı", SEK, "if len(s) != len(eksenler):", "if False:"),
    ("düzensiz şekil kabul", SEK, "if any(s != alt[0] for s in alt):", "if False:"),
    ("eksen boyu denetimi kapalı", SEK, "if eksen in boyutlar and boyutlar[eksen] != uzunluk:", "if False:"),
]


def main():
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':32} {sayac}")
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    kacan = 0
    for ad, dosya, eski, yeni in MUTASYONLAR:
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:32} {sayac}")
    print(f"MUTASYON: toplam={len(MUTASYONLAR)} yakalanan={len(MUTASYONLAR) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
