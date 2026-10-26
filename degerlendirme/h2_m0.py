"""sistem.md §13; K-041 (ÖK-005 taslağı §4 madde 22, §7; B0 bitişi: M0 üç kez bit-aynı), V-064: M0 koşucusu.

Geliştirme havuzunu (16 dünya) kurar, M0'ı şablon üretim kademesinde koşar, aday listesini ve özeti atomik yazar. Yalnız
geliştirme havuzu kullanılır; final ve kontrol havuzları açılmaz. Süre yalnız ekrana yazılır (dosyalar bit-aynı kalır).
Kullanım: python3 -m degerlendirme.h2_m0 <çıkış klasörü> [kademe]
"""
import json
import sys
import time
from pathlib import Path

import torch

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from degerlendirme import h1, h2_dunya
from degerlendirme.dunya import tanimlar_yukle
from kesif import m0

DOSYALAR = ("m0_adaylar.jsonl", "m0_ozet.json")  # V-064
GELISTIRME = "gelistirme"  # K-041: M0 yalnız geliştirme havuzunda
IS_PARCACIGI = 4  # V-057: süreç başına iş parçacığı (sonucu değiştirmez)


def kos(kok, cikis, kademe=None, havuz_adi=GELISTIRME):
    if havuz_adi != GELISTIRME:
        raise ValueError("M0 yalnız geliştirme havuzunda koşar")
    torch.set_num_threads(IS_PARCACIGI)
    h2 = ayar_yukle(Path(kok) / "config_h2.json")
    _, sema, _ = h1._ortam(Path(kok))
    tanimlar = tanimlar_yukle(Path(kok) / "degerlendirme" / "veri" / "tanimlar_v1.json",
                              Path(kok) / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
    dunyalar = h2_dunya.havuz(havuz_adi, h2, tanimlar)
    sonuc = m0.m0(dunyalar, tuple(sema.adlar), h2, kademe=kademe)
    ozet = {"havuz": havuz_adi, "m0": sonuc.ozet,
            "dunya_ozetleri": [h2_dunya.dunya_ozeti(d, m0.ALGORITMA) for d in dunyalar]}
    Path(cikis).mkdir(parents=True, exist_ok=True)
    atomik_yaz(Path(cikis) / DOSYALAR[0], sonuc.cikti)
    atomik_yaz(Path(cikis) / DOSYALAR[1], kanonik_json(ozet))
    return json.loads(kanonik_json(ozet))


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    baslangic = time.time()
    ozet = kos(kok, arg[0], kademe=arg[1] if len(arg) > 1 else None)
    print(json.dumps({**ozet["m0"], "sure_s": round(time.time() - baslangic)}, ensure_ascii=False))  # V-064: yalnız ekran
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
