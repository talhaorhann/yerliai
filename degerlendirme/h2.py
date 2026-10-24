"""sistem.md §13 (H2), K-032: H2 deneyi (klonal seçilim kuralı sıfırdan buluyor mu). Deneyin kendisi henüz yazılmadı.

Kapı (K-032 §4): V-053 kapanmadan ve H1 taze tohumlarla yeniden koşulmadan H2 çalışmaz. Kapı yalnız kayıtlara bakar:
1. VARSAYIMLAR.md'de V-053'ün durumu "KARARA BAĞLANDI (K-nnn" ile başlar; K-nnn, KARARLAR.md'de V-053'ü anan ve
   kullanıcının onayladığı bir karardır.
2. ONKAYIT.md'de "## ÖK-004 sonucu" başlığı altında H1 yeniden koşusunun kapı özeti (`H1_YENIDEN_OZETI`) sha256'sıyla
   yazılıdır; dosya vardır, özeti tutar ve tohumlarının hiçbiri ÖK-002/ÖK-003'te kullanılmamıştır.
Her ret "V-053 açık" ile başlar. Bu kapıyı kapatan ya da gevşeten kod yazılmaz (K-032).

Kullanım: .venv/bin/python -m degerlendirme.h2
"""
import hashlib
import json
import re
import sys
from pathlib import Path

H1_YENIDEN_OZETI = "raporlar/H1_v3_kapi_ozet.json"  # K-032: ÖK-004 kapı koşusunun özet dosyası
KULLANILMIS_H1_TOHUMLARI = frozenset(range(7, 18))  # ÖK-002 (7–11), ÖK-003 (12–16, yerine 17): bir daha taze sayılmaz
SONUC_BASLIGI = "## ÖK-004 sonucu"  # K-032
RET = "V-053 açık"  # K-032 §4


class H2KapiHatasi(RuntimeError):
    pass


def _bolum(metin, baslik_deseni):
    """`baslik_deseni` ile başlayan ilk "## " bölümünün metni (bir sonraki "## " başlığına kadar)."""
    m = re.search(rf"^{baslik_deseni}.*?(?=^## |\Z)", metin, re.M | re.S)
    return m.group(0) if m else None


def _ret(neden):
    raise H2KapiHatasi(f"{RET}: {neden}")


def kapi_denetle(kok):
    kok = Path(kok)
    v053 = _bolum((kok / "VARSAYIMLAR.md").read_text(encoding="utf-8"), re.escape("## V-053:"))
    durum = re.search(r"\*\*Durum:\*\*\s*(.*)", v053 or "")
    karar = re.match(r"KARARA BAĞLANDI \((K-\d{3})", durum.group(1)) if durum else None
    if karar is None:
        _ret("VARSAYIMLAR.md'de V-053 kapanmamış")
    kimlik = karar.group(1)
    kayit = _bolum((kok / "KARARLAR.md").read_text(encoding="utf-8"), re.escape(f"## {kimlik} "))
    if kayit is None or "V-053" not in kayit or not re.search(r"^- \*\*Onaylayan:\*\* kullanıcı", kayit, re.M):
        _ret(f"{kimlik}, V-053'ü kapatan kullanıcı onaylı bir karar değil")
    sonuc = _bolum((kok / "ONKAYIT.md").read_text(encoding="utf-8"), re.escape(SONUC_BASLIGI))
    yol = kok / H1_YENIDEN_OZETI
    if sonuc is None or not yol.exists():
        _ret("H1 taze tohumlarla yeniden koşulmadı (ÖK-004 sonucu yok)")
    baytlar = yol.read_bytes()
    if hashlib.sha256(baytlar).hexdigest() not in sonuc:
        _ret(f"{H1_YENIDEN_OZETI} özeti ÖK-004 sonucunda yazılı değil ya da tutmuyor")
    tohumlar = sorted({int(ad.rsplit("/", 1)[1]) for ad in json.loads(baytlar)["ozet"]["satirlar"]})
    if not tohumlar or KULLANILMIS_H1_TOHUMLARI.intersection(tohumlar):
        _ret(f"H1 yeniden koşusu taze tohumlarla değil: {tohumlar}")
    return {"karar": kimlik, "tohumlar": tohumlar}


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    try:
        kapi_denetle(kok)
    except H2KapiHatasi as h:
        print(h)
        return 1
    print("H2 kapısı açık; H2 deneyi henüz yazılmadı.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
