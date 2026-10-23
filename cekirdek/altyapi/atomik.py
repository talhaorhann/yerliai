"""KODLAMA_PROMPTU §5 (Uzun koşular): atomik dosya yazma ve tohum durumu dahil koşu durumu kaydı (V-010)."""
import json
import os
import random

from cekirdek.altyapi.kanonik import kanonik_json

GECICI_EK = ".gecici"  # V-010


def atomik_yaz(yol, baytlar):
    """Önce aynı klasörde geçici dosyaya yazar, diske zorlar, sonra yeniden adlandırır."""
    if not isinstance(baytlar, bytes):
        raise TypeError("atomik_yaz yalnız bytes kabul eder")
    yol = os.fspath(yol)
    gecici = yol + GECICI_EK
    with open(gecici, "wb") as f:
        f.write(baytlar)
        f.flush()
        os.fsync(f.fileno())
    os.replace(gecici, yol)
    if os.name == "nt":  # V-010: Windows klasör fsync desteklemez
        return
    klasor = os.open(os.path.dirname(os.path.abspath(yol)), os.O_RDONLY)
    try:
        os.fsync(klasor)
    finally:
        os.close(klasor)


def durum_kaydet(yol, durum):
    atomik_yaz(yol, kanonik_json(durum))


def durum_yukle(yol):
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def uretec_durumu(rng):
    """random.Random durumunu JSON'a yazılabilir listeye çevirir."""
    surum, ic_durum, gauss = rng.getstate()
    return [surum, list(ic_durum), gauss]


def uretec_kur(durum):
    surum, ic_durum, gauss = durum
    rng = random.Random()
    rng.setstate((surum, tuple(ic_durum), gauss))
    return rng
