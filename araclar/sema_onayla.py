"""sistem.md §14, KODLAMA_PROMPTU §2.6: ilişki şemasını kullanıcıya okunur gösterir ve onay kaydını yazar (V-013).

Kullanım:
  python3 araclar/sema_onayla.py            # taslağı okunur tablo olarak gösterir
  python3 araclar/sema_onayla.py K-nnn      # kullanıcı onayından sonra: onay kaydını yazar
Onay kaydı yalnız kullanıcı "evet" dedikten ve karar KARARLAR.md'ye yazıldıktan sonra yazılır.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from cekirdek.altyapi.atomik import atomik_yaz  # noqa: E402

SEMA = KOK / "sema" / "iliskiler_v1.json"  # V-013
ONAY = KOK / "kilit" / "sema_onayi.json"  # V-013
ALGORITMA = "sha256"  # V-007


def onay_kaydi_yaz(sema_yolu, onay_yolu, karar):
    if not isinstance(karar, str) or not re.fullmatch(r"K-\d{3}", karar):
        raise ValueError("onay için KARARLAR.md'deki K-nnn kimliği gerekir")
    kayit = {"dosya": os.path.basename(sema_yolu), "algoritma": ALGORITMA,
             "ozet": hashlib.new(ALGORITMA, Path(sema_yolu).read_bytes()).hexdigest(), "karar": karar}
    metin = json.dumps(kayit, ensure_ascii=False, indent=2, sort_keys=True) + "\n"  # V-008: okunur biçim
    atomik_yaz(onay_yolu, metin.encode("utf-8"))
    return kayit


def okunur_tablo(sema_yolu):
    veri = json.loads(Path(sema_yolu).read_text(encoding="utf-8"))
    satirlar = [f"Okuma: {veri['okuma']}", "",
                "| İlişki | Tersi (adaylar) | Simetrik | Tek mi (işlevsel) |", "|---|---|---|---|"]
    for i in veri["iliskiler"]:
        satirlar.append(f"| {i['ad']} | {', '.join(i['ters']) or '-'} | {'evet' if i['simetrik'] else 'hayır'} | "
                        f"{'evet' if i['islevsel'] else 'hayır'} |")
    satirlar.append("")
    for grup in veri["dislayici_gruplar"]:
        satirlar.append("Aynı iki kişi arasında bunlardan en fazla biri olabilir: " + ", ".join(grup))
    return "\n".join(satirlar)


def main(arg):
    if not arg:
        print(okunur_tablo(SEMA))
        return 0
    kayit = onay_kaydi_yaz(SEMA, ONAY, arg[0])
    print(f"onay yazıldı: {kayit['dosya']} {kayit['ozet']} ({kayit['karar']})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
