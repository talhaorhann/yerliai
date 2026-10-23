"""sistem.md §3, V-032: hücre DNA'sı (1–3 halkalı değişkenli nedensellik zinciri), veri dosyasından yüklenir.

Kodda ilişki adı yoktur (KODLAMA_PROMPTU §2.4); genler onaylı ilişki şemasına karşı denetlenir.
"""
import json
from collections import namedtuple
from dataclasses import dataclass

from cekirdek.altyapi.sema_dogrulayici import sema_yukle

Halka = namedtuple("Halka", "gen sol sag esik")
Sonuc = namedtuple("Sonuc", "gen sol sag")


class DnaHatasi(ValueError):
    pass


@dataclass(frozen=True)
class Hucre:
    kimlik: str
    halkalar: tuple
    sonuc: Sonuc
    guvenilirlik: float


def dna_kur(veri, bicim_yolu, iliski_semasi):
    hatalar = sema_yukle(bicim_yolu).hatalar(veri)
    if hatalar:
        raise DnaHatasi("DNA biçime uymuyor: " + "; ".join(hatalar))
    hucreler, kimlikler = [], set()
    for h in veri["hucreler"]:
        if h["kimlik"] in kimlikler:
            raise DnaHatasi(f"yinelenen hücre kimliği: {h['kimlik']}")
        kimlikler.add(h["kimlik"])
        halkalar = tuple(Halka(x["gen"], x["sol"], x["sag"], x["esik"]) for x in h["halkalar"])
        sonuc = Sonuc(h["sonuc"]["gen"], h["sonuc"]["sol"], h["sonuc"]["sag"])
        for gen in [x.gen for x in halkalar] + [sonuc.gen]:
            if gen not in iliski_semasi:
                raise DnaHatasi(f"{h['kimlik']}: gen '{gen}' onaylı şemada yok")
        govde = {d for x in halkalar for d in (x.sol, x.sag)}
        if not {sonuc.sol, sonuc.sag} <= govde:
            raise DnaHatasi(f"{h['kimlik']}: sonuç değişkenleri gövdede geçmiyor")
        hucreler.append(Hucre(h["kimlik"], halkalar, sonuc, h["guvenilirlik"]))
    return tuple(hucreler)


def dna_yukle(yol, bicim_yolu, iliski_semasi):
    with open(yol, encoding="utf-8") as f:
        return dna_kur(json.load(f), bicim_yolu, iliski_semasi)
