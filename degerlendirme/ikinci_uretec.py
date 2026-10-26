"""sistem.md §11, §13; K-041 (ÖK-005 taslağı §2.1, A3 ailesi), V-062: ikinci, bağımsız dünya üreticisi (nüfus modeli).

`degerlendirme/dunya.py`'den hiçbir şey almaz: ayrı kod, aynı yazar. Ortak olan yalnız veridir (ilişki tanımları).
- Kurucu çiftler ayrı soylardır: kurucu çiftin tip-1 kişisi soyun ilk kişisi, eşi dışarıdandır. Çocuğun soyu, ebeveynlerinin soylarının
  birleşimidir; dışarıdan gelenin soyu boştur.
- Son nesil dışındaki çocuk, evlilik olasılığıyla evlenir. Evlendiği kişi önce aynı nesildeki, evlenmemiş, karşı tipten ve soyu ortak
  olmayan bir çocuktur (tohumla seçilir); yoksa dışarıdan biri. Akraba evliliği yoktur; boşanma ve yeniden evlilik yoktur.
- İlişkiler, tanım verisindeki adımlarla (yukarı, aşağı, evlilik bağı; adımın vardığı kişinin tipi) kişi tekrarlamayan yürüyüşlerle
  bulunur (V-019 ile aynı anlam, ayrı yorumlayıcı).
- Bir çifte iki terim düşerse üretim durur (tohum değişmez); akraba evliliği olmadığı için beklenmez.
"""
import dataclasses

YUKARI, ASAGI, ES = "U", "D", "E"  # V-019: tanım verisindeki adım harfleri


class CokluTerimHatasi(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class Nufus:
    tip: tuple
    ebeveynler: dict
    es: dict
    soy: dict


def uret(rng, kurucu_cift, nesil_sayisi, kurucu_cocuk, cocuk, evlilik_orani):
    tip, ebeveynler, es, soy = [], {}, {}, {}

    def yeni(t, s):
        tip.append(t)
        soy[len(tip) - 1] = frozenset(s)
        return len(tip) - 1

    ciftler = []
    for i in range(kurucu_cift):
        soydan, disaridan = yeni(1, {i}), yeni(0, ())
        es[soydan], es[disaridan] = disaridan, soydan
        ciftler.append((soydan, disaridan))
    for nesil in range(nesil_sayisi - 1):
        aralik = kurucu_cocuk if nesil == 0 else cocuk
        cocuklar = []
        for a, b in ciftler:
            for _ in range(rng.randint(*aralik)):
                c = yeni(rng.randint(0, 1), soy[a] | soy[b])
                ebeveynler[c] = (a, b)
                cocuklar.append(c)
        ciftler = []
        if nesil >= nesil_sayisi - 2:  # V-017: son nesil evlenmez
            continue
        for c in cocuklar:
            if c in es or rng.random() >= evlilik_orani:
                continue
            adaylar = [d for d in cocuklar if d not in es and d != c and tip[d] != tip[c] and not soy[d] & soy[c]]
            d = rng.choice(adaylar) if adaylar else yeni(1 - tip[c], ())
            es[c], es[d] = d, c
            ciftler.append((c, d))
    return Nufus(tuple(tip), dict(ebeveynler), dict(es), dict(soy))


def _cocuklar(n):
    sonuc = {}
    for c in sorted(n.ebeveynler):
        for e in n.ebeveynler[c]:
            sonuc.setdefault(e, []).append(c)
    return sonuc


def _uclar(n, cocuklar, bas, secenek):
    sonuc = set()
    yigin = [(bas, 0, (bas,))]
    while yigin:
        kisi, adim, yol = yigin.pop()
        if adim == len(secenek):
            sonuc.add(kisi)
            continue
        yon, tip = secenek[adim]
        if yon == YUKARI:
            komsu = n.ebeveynler.get(kisi, ())
        elif yon == ASAGI:
            komsu = cocuklar.get(kisi, ())
        else:
            komsu = (n.es[kisi],) if kisi in n.es else ()
        for k in komsu:
            if k not in yol and (tip is None or n.tip[k] == tip):
                yigin.append((k, adim + 1, yol + (k,)))
    return sonuc


def olgular(n, secenekler):
    """Bütün (a, ilişki, b) olguları ("b, a'nın ilişkisidir"), sıralı. Bir çifte iki terim düşerse durur."""
    cocuklar = _cocuklar(n)
    terim = {}
    for a in range(len(n.tip)):
        for ad in sorted(secenekler):
            for secenek in secenekler[ad]:
                for b in _uclar(n, cocuklar, a, secenek):
                    if terim.setdefault((a, b), ad) != ad:
                        raise CokluTerimHatasi("bir çifte iki terim düştü; üretim durdu")
    return sorted((a, r, b) for (a, b), r in terim.items())
