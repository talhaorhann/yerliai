"""sistem.md §13; K-041, K-042, K-043 (ÖK-005 taslağı §9 madde 1: "ön kayıt tutmazsa koşu başlamaz"), V-065.

Her H2 koşusu (B1, B2a, B2b, B3) başında ONKAYIT.md'nin "## ÖK-005" bölümüyle depo karşılaştırılır:
- taslak metnin özeti (`ONKAYIT_H2_TASLAK.md`, sha256 ...),
- çekirdek özeti ve keşif paketi özeti (`araclar/cekirdek_ozeti.py` ile),
- bölümdeki tablolarda "| `yol` | `özet` |" satırıyla yazılan her dosya: aynı yol birden çok ekte yazılmışsa sonuncusu
  geçerlidir (sonraki ek öncekinin yerine geçer),
- H2 ayarında gizli kırmızı takım dosyasının özeti yazılıysa dosyanın özeti.
Tutmayan her şey listelenir ve koşu başlamaz. H1'den kalan K-032 kapısı (`degerlendirme/h2.py`) ayrıca denetlenir.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from araclar.cekirdek_ozeti import ozet_al

ALGORITMA = "sha256"  # V-007
BASLIK = "## ÖK-005 (H2): mühür"  # K-042
OZET = r"`([0-9a-f]{64})`"


class OnkayitHatasi(RuntimeError):
    pass


def _ozet(yol):
    return hashlib.new(ALGORITMA, Path(yol).read_bytes()).hexdigest()


def bolum(metin):
    i = metin.find(BASLIK)
    if i < 0:
        raise OnkayitHatasi("ONKAYIT.md'de ÖK-005 mührü yok")
    sonraki = re.search(r"^## (?!ÖK-005)", metin[i + len(BASLIK):], re.M)
    return metin[i:] if sonraki is None else metin[i:i + len(BASLIK) + sonraki.start()]


def beklenenler(metin):
    b = bolum(metin)
    sonuc = {}
    m = re.search(r"`ONKAYIT_H2_TASLAK\.md`, sha256 " + OZET, b)
    if m:
        sonuc["ONKAYIT_H2_TASLAK.md"] = m.group(1)
    for ad, desen in (("cekirdek/", r"çekirdek özeti[^\n]*?" + OZET), ("kesif/", r"keşif paketi özeti[^\n]*?" + OZET)):
        bulunan = re.findall(desen, b)
        if bulunan:
            sonuc[ad] = bulunan[-1]
    for yol, oz in re.findall(r"^\s*\|\s*`([^`]+)`\s*\|\s*" + OZET + r"\s*\|", b, re.M):
        sonuc[yol] = oz
    return sonuc


def denetle(kok, h2_ayar=None):
    kok = Path(kok)
    hatalar = []
    for yol, oz in sorted(beklenenler((kok / "ONKAYIT.md").read_text(encoding="utf-8")).items()):
        if yol.endswith("/"):
            gercek = ozet_al(kok / yol.rstrip("/"))
        elif (kok / yol).is_file():
            gercek = _ozet(kok / yol)
        else:
            hatalar.append(f"{yol}: dosya yok")
            continue
        if gercek != oz:
            hatalar.append(f"{yol}: özet tutmuyor")
    if h2_ayar is not None and "kirmizi_gizli_dosyasi" in h2_ayar.degerler:
        g = h2_ayar.deger("kirmizi_gizli_dosyasi")
        if not (kok / g["yol"]).is_file() or _ozet(kok / g["yol"]) != g["ozet"]:
            hatalar.append(f"{g['yol']}: gizli dosyanın özeti tutmuyor")
    if hatalar:
        raise OnkayitHatasi("ön kayıt tutmuyor: " + "; ".join(hatalar))
    return True


def tam_denetim(kok, h2_ayar):
    from degerlendirme import h2
    h2.kapi_denetle(kok)
    return denetle(kok, h2_ayar)


def dosya_ozetleri(kok, yollar):
    """Ek tablosu için (yol, özet) satırları."""
    return [(y, _ozet(Path(kok) / y)) for y in yollar]


def tablo(satirlar):
    return "\n".join(["   | Dosya | sha256 |", "   |---|---|"] + [f"   | `{y}` | `{o}` |" for y, o in satirlar])


def main():
    from cekirdek.altyapi.ayar import ayar_yukle
    kok = Path(__file__).resolve().parents[1]
    tam_denetim(kok, ayar_yukle(kok / "config_h2.json"))
    print(json.dumps({"onkayit": "tutuyor"}, ensure_ascii=False))  # V-057: okunur çıktı
    return 0


if __name__ == "__main__":
    sys.exit(main())
