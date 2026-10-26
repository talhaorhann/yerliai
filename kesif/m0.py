"""sistem.md §13; K-041 (ÖK-005 taslağı §4 madde 5 ve 22, §6): M0, şablon uzayının bütün adaylarını sembolik sayaçla
sayan referans yöntem (AMIE tarzı kaba kuvvet; KODLAMA_PROMPTU §2 istisnası K-041).

Girdi: dünya gözlemleri (aile etiketi, kişiler, olgular); kâhin yoktur. Her aday için aile başına tahmin ve doğru
sayısı toplanır. Süzgeç: toplam yanlış ≤ m0_en_cok_yanlis VE toplam doğru (tanık) ≥ m0_en_az_tanik. Sıra: tanık azalan,
halka sayısı artan, kanonik kimlik artan. Çıktı kanonik JSON satırlarıdır; aynı girdi bit-aynı çıktı verir (dünya ve
olgu sırasından bağımsız).
"""
import dataclasses

import numpy as np

from cekirdek.altyapi.kanonik import kanonik_json, ozet
from kesif import aday as ad
from kesif import sablon, sayac

ALGORITMA = "sha256"  # V-007: kanonik kimlik ve çıktı özeti


@dataclasses.dataclass(frozen=True)
class Dunya:
    aile: str
    kisiler: tuple
    olgular: tuple


@dataclasses.dataclass(frozen=True)
class M0Sonucu:
    adaylar: list
    cikti: bytes
    ozet: dict


def _topla(dunyalar, govdeler, iliski_adlari, parca_boyu):
    aileler = sorted({d.aile for d in dunyalar})
    G, m = len(govdeler), len(iliski_adlari)
    toplam = {a: {"tahmin": np.zeros(G, np.int64), "dogru": np.zeros((G, m), np.int64),
                  "tahmin_oi": np.zeros(G, np.int64), "dogru_oi": np.zeros((G, m), np.int64)} for a in aileler}
    for d in dunyalar:
        kisiler = tuple(sorted(d.kisiler))
        s = sayac.sablon_say(govdeler, sayac.iliski_tensoru(kisiler, d.olgular, iliski_adlari), parca_boyu)
        for alan, hedef in toplam[d.aile].items():
            hedef += np.maximum(getattr(s, alan), 0)  # V-061: OI'nin anlamsız olduğu gövdede değer yok (OI_YOK) → 0
    return aileler, toplam


def m0(dunyalar, iliski_adlari, h2_ayar, kademe=None):
    kademe = kademe or h2_ayar.deger("sablon_uretim_kademesi")
    en_cok, zincir = h2_ayar.deger("sablon_kademeleri")[kademe]
    degiskenler = tuple(h2_ayar.deger("sablon_degiskenleri"))
    govdeler = sablon.govdeler(len(iliski_adlari), degiskenler, en_cok, zincir)
    aileler, toplam = _topla(dunyalar, govdeler, iliski_adlari, h2_ayar.deger("sayac_parca_boyu"))
    en_az, en_cok_yanlis = h2_ayar.deger("m0_en_az_tanik"), h2_ayar.deger("m0_en_cok_yanlis")
    adaylar = []
    for oi, (t_i, d_i) in ((False, ("tahmin", "dogru")), (True, ("tahmin_oi", "dogru_oi"))):
        T = sum(toplam[a][t_i] for a in aileler)
        D = sum(toplam[a][d_i] for a in aileler)
        uygun = (T[:, None] - D <= en_cok_yanlis) & (D >= en_az)
        for i, bas in zip(*np.nonzero(uygun)):
            g = govdeler[i]
            if (bas, degiskenler[0], degiskenler[1]) in g or (oi and not sablon.oi_anlamli_mi(g)):
                continue
            kayit = sablon.aday_kaydi(g, int(bas), oi, iliski_adlari, degiskenler, tur="m0")
            kimlik = ad.kanonik_kimlik(kayit, ALGORITMA)
            kayit["kimlik"] = "k" + kimlik
            adaylar.append({"kanonik_kimlik": kimlik, "halka_sayisi": len(g), "aday": kayit,
                            "dogru": {a: int(toplam[a][d_i][i, bas]) for a in aileler},
                            "tahmin": {a: int(toplam[a][t_i][i]) for a in aileler}})
    adaylar.sort(key=lambda a: (-sum(a["dogru"].values()), a["halka_sayisi"], a["kanonik_kimlik"]))
    cikti = b"".join(kanonik_json(a) + b"\n" for a in adaylar)
    oz = {"kademe": kademe, "dunya_sayisi": len(dunyalar), "aileler": aileler,
          "aday_uzayi": sablon.sayim(govdeler, len(iliski_adlari), degiskenler)[1], "aday_sayisi": len(adaylar),
          "cikti_ozeti": ozet(cikti, ALGORITMA)}
    return M0Sonucu(adaylar, cikti, oz)
