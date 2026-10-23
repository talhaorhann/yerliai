"""KODLAMA_PROMPTU §5 (Uzun koşular): öldür-devam testi için oyuncak koşu (yalnız testler kullanır).

Kullanım: python -m testler.yardimci_uzun_kosu <durum_yolu> <tohum> <adim_sayisi> [<olunecek_adim>]
Her adımda üreteçten tamsayı çekip toplar, durumu atomik kaydeder. <olunecek_adim> verilirse o adımın
kaydından hemen sonra süreç SIGKILL (Windows: SIGTERM) ile kendini öldürür (kesinti benzetimi).
"""
import os
import signal
import sys

from cekirdek.altyapi.atomik import durum_kaydet, durum_yukle, uretec_durumu, uretec_kur


def calistir(durum_yolu, tohum, adim_sayisi, olunecek_adim=None):
    if os.path.exists(durum_yolu):
        durum = durum_yukle(durum_yolu)
        rng = uretec_kur(durum["uretec"])
    else:
        import random
        durum = {"adim": 0, "toplam": 0, "izler": []}
        rng = random.Random(tohum)
    while durum["adim"] < adim_sayisi:
        sayi = rng.randrange(1000)
        durum["toplam"] += sayi
        durum["izler"].append(sayi)
        durum["adim"] += 1
        durum["uretec"] = uretec_durumu(rng)
        durum_kaydet(durum_yolu, durum)
        if olunecek_adim is not None and durum["adim"] == olunecek_adim:
            os.kill(os.getpid(), getattr(signal, "SIGKILL", signal.SIGTERM))
    return durum


if __name__ == "__main__":
    a = sys.argv[1:]
    sonuc = calistir(a[0], int(a[1]), int(a[2]), int(a[3]) if len(a) > 3 else None)
    print(sonuc["toplam"])
