"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A6 koduna kasıtlı hata sokar.

Kullanım: .venv/bin/python araclar/mutasyon_a6.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

H2 = "degerlendirme/h2.py"

MUTASYONLAR = [
    # K-032 §4: H2 kapısı
    ("V-053 durumu denetlenmiyor", H2, "    if karar is None:\n        _ret(", "    if False:\n        _ret("),
    ("kapatan kararda kullanıcı onayı aranmıyor", H2,
     ' or not re.search(r"^- \\*\\*Onaylayan:\\*\\* kullanıcı", kayit, re.M)', ""),
    ("kapatan kararda V-053 aranmıyor", H2, ' or "V-053" not in kayit', ""),
    ("ÖK-004 sonucu aranmıyor", H2, "    if sonuc is None or not yol.exists():", "    if not yol.exists():\n        sonuc = ''\n    if False:"),
    ("özet karşılaştırılmıyor", H2, "    if hashlib.sha256(baytlar).hexdigest() not in sonuc:", "    if False:"),
    ("eski tohum denetlenmiyor", H2, "    if not tohumlar or KULLANILMIS_H1_TOHUMLARI.intersection(tohumlar):",
     "    if not tohumlar:"),
    ("ÖK-003 tohumları kullanılmış sayılmıyor", H2, "frozenset(range(7, 18))", "frozenset(range(7, 12))"),
    ("tohumsuz özet kabul ediliyor", H2, "    if not tohumlar or KULLANILMIS_H1_TOHUMLARI",
     "    if KULLANILMIS_H1_TOHUMLARI"),
    ("komut kapıyı atlıyor", H2, "    try:\n        kapi_denetle(kok)\n", "    try:\n        pass\n"),
]


def main(secilen=None):
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':40} {sayac}", flush=True)
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    kacan, liste = 0, [m for m in MUTASYONLAR if secilen is None or m[0] in secilen]
    for ad, dosya, eski, yeni in liste:
        if (KOK / dosya).read_text(encoding="utf-8").count(eski) != 1:
            print(f"ÇAPA YOK  {ad}")
            kacan += 1
            continue
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:40} {sayac}", flush=True)
    print(f"MUTASYON: toplam={len(liste)} yakalanan={len(liste) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
