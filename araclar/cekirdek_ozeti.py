"""sistem.md §13; K-041 (ÖK-005 taslağı §4 madde 27, çekirdek dondurma sözleşmesi), V-063: çekirdek kod özeti.

Özet, `cekirdek/` altındaki bütün .py dosyalarının (göreli yol, içerik özeti) sıralı listesinin özetidir; __pycache__
sayılmaz. B0 sonunda ÖK-005'e yazılır; sonra her H2 koşusu başında denetlenir.
Kullanım: python3 araclar/cekirdek_ozeti.py
"""
import hashlib
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ALGORITMA = "sha256"  # V-007


def ozet_al(klasor):
    klasor = Path(klasor)
    satirlar = []
    for yol in sorted(klasor.rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        icerik = hashlib.new(ALGORITMA, yol.read_bytes()).hexdigest()
        satirlar.append(f"{yol.relative_to(klasor).as_posix()} {icerik}\n")
    return hashlib.new(ALGORITMA, "".join(satirlar).encode("utf-8")).hexdigest()


def main():
    print(ozet_al(KOK / "cekirdek"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
