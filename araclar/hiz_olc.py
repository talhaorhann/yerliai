"""KODLAMA_PROMPTU §4 (hız iddiasını ölçmeden yazma): referans ve PyTorch hızlı yolunun süresini ölçer, aynılığı denetler.

Kullanım: python3 araclar/hiz_olc.py [kayıt_sayısı]
"""
import random
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from cekirdek import vektor as V  # noqa: E402
from cekirdek import vektor_hizli as H  # noqa: E402
from cekirdek.altyapi.ayar import ayar_yukle  # noqa: E402

VARSAYILAN_KAYIT = 64  # sistem.md §2: havuz kapasitesi kadar


def olc(fonksiyon):
    bas = time.perf_counter()
    sonuc = fonksiyon()
    return sonuc, time.perf_counter() - bas


def main(arg):
    n = int(arg[0]) if arg else VARSAYILAN_KAYIT
    ayar = ayar_yukle(KOK / "config.json")
    kk = V.KodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu"))
    rng = random.Random(ayar.deger("vektor_tohum"))
    uclular = [(rng.randrange(n), f"r{rng.randrange(n)}", rng.randrange(n)) for _ in range(n)]
    ref_m, ref_t = olc(lambda: V.kayit_matrisi(kk, uclular))
    hiz_m, hiz_t = olc(lambda: H.kayit_matrisi_hizli(kk, uclular))
    ref_b, ref_bt = olc(lambda: V.benzerlik_matrisi(ref_m, ref_m))
    hiz_b, hiz_bt = olc(lambda: H.benzerlik_matrisi_hizli(hiz_m, hiz_m))
    ayni = hiz_m.tolist() == [list(v) for v in ref_m] and \
        [[float(x).hex() for x in s] for s in hiz_b.tolist()] == [[float(x).hex() for x in s] for s in ref_b]
    print(f"kayıt={n}  kayıt matrisi: referans {ref_t:.3f} sn, hızlı {hiz_t:.3f} sn  |  "
          f"{n}×{n} kosinüs: referans {ref_bt:.3f} sn, hızlı {hiz_bt:.3f} sn  |  bit-eşit: {ayni}")
    return 0 if ayni else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
