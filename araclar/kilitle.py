"""KODLAMA_PROMPTU §5 (Kilitli kümeler): test ve eşik dosyalarının hash kilidini yeniden yazar (V-008).

Kullanım: python3 araclar/kilitle.py
Kilitli dosyalardaki her değişiklik kullanıcı onayı ister. Bu komutu yalnız onaydan sonra çalıştırın
ve commit mesajında hangi kilitli dosyanın neden değiştiğini yazın.
"""
import hashlib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from cekirdek.altyapi.atomik import atomik_yaz  # noqa: E402

ALGORITMA = "sha256"  # V-007
KILIT_YOLU = KOK / "kilit" / "kilitler.json"  # V-008


def kilitlenecekler():
    dosyalar = [p for p in (KOK / "testler").rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    dosyalar.append(KOK / "config.json")
    # K-009: onaylı veri dosyaları (ör. gizli tanımlar) config'teki listeden; araç yalnız hash alır, içeriği kullanmaz
    ayar = json.loads((KOK / "config.json").read_text(encoding="utf-8"))
    dosyalar.extend(KOK / y for y in ayar["degerler"]["kilitli_veri_dosyalari"]["deger"])
    h2 = KOK / "config_h2.json"  # V-060: H2 ayarı ve H2'nin kilitli veri dosyaları (ör. gizli kırmızı takım dosyası)
    if h2.is_file():
        dosyalar.append(h2)
        h2_ayar = json.loads(h2.read_text(encoding="utf-8"))
        dosyalar.extend(KOK / y for y in h2_ayar["degerler"]["h2_kilitli_veri_dosyalari"]["deger"])
    return sorted(p.relative_to(KOK).as_posix() for p in dosyalar)


def main():
    kilit = {
        "algoritma": ALGORITMA,
        "dosyalar": {y: hashlib.new(ALGORITMA, (KOK / y).read_bytes()).hexdigest() for y in kilitlenecekler()},
    }
    metin = json.dumps(kilit, ensure_ascii=False, indent=2, sort_keys=True) + "\n"  # V-008: okunur biçim
    atomik_yaz(KILIT_YOLU, metin.encode("utf-8"))
    for yol, deger in kilit["dosyalar"].items():
        print(deger, yol)


if __name__ == "__main__":
    main()
