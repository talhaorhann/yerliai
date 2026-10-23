"""KODLAMA_PROMPTU §5 (Kilitli kümeler): altın/kalibrasyon kümelerinin hash denetimi ve kesişim durdurucusu (V-021)."""
import hashlib
import json
import os


class KilitliKumeHatasi(RuntimeError):
    pass


GIRDI_ALANLARI = {"dosya", "algoritma", "ozet"}  # V-021


def kilitli_ozetler(kayit_yolu, kok):
    """Kayıtlı her küme dosyasının hash'ini doğrular ve içindeki bölüm özetlerini döndürür.
    Kayıt dosyası yoksa henüz kilitli küme yoktur (boş küme)."""
    if not os.path.exists(kayit_yolu):
        return frozenset()
    with open(kayit_yolu, encoding="utf-8") as f:
        kayit = json.load(f)
    if not isinstance(kayit, dict) or set(kayit) != {"kumeler"} or not isinstance(kayit["kumeler"], dict):
        raise KilitliKumeHatasi("kilitli küme kaydı biçimsiz")
    ozetler = set()
    for ad in sorted(kayit["kumeler"]):
        girdi = kayit["kumeler"][ad]
        if not isinstance(girdi, dict) or set(girdi) != GIRDI_ALANLARI:
            raise KilitliKumeHatasi(f"{ad}: girdi biçimsiz")
        with open(os.path.join(kok, girdi["dosya"]), "rb") as f:
            ham = f.read()
        if hashlib.new(girdi["algoritma"], ham).hexdigest() != girdi["ozet"]:
            raise KilitliKumeHatasi(f"{ad}: kilitli küme dosyası değişmiş, hat durdu")
        for satir in ham.splitlines():
            if satir.strip():
                ozetler.add(json.loads(satir)["ozet"])
    return frozenset(ozetler)


def kesisim_denetle(yasakli, ozetler):
    ortak = yasakli & set(ozetler)
    if ortak:
        raise KilitliKumeHatasi(f"{len(ortak)} bölüm kilitli kümeyle kesişiyor, hat durdu")
