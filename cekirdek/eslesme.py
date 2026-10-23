"""sistem.md §3, V-032, K-016: sembolik bağlama maskesi × kosinüs afinitesi > θ, yarı-naif eşleşme (saf Python).

Her halka ilişki dizininden kendi genindeki kayıtlara bakar; halkalar farklı kayıtlara bağlanır, aynı değişken
her yerde aynı varlığa bağlanır, en az bir halka `yeni` kümesindeki (önceki turda yazılmış) bir kayda bağlanır.
Afinite = kırp(kosinüs(alıcı, kayıt)·√3, 0, 1); güven = min(afiniteler, ebeveyn güvenleri) × hücre güvenilirliği.
"""
import math
from collections import namedtuple
from itertools import product

from cekirdek.vektor import TUR_ILISKI, kosinus

Baglama = namedtuple("Baglama", "kayitlar degiskenler")
Eslesme = namedtuple("Eslesme", "hucre baglama uclu afiniteler guven")
AFINITE_OLCEGI = math.sqrt(3)  # K-016: kayıt vektörü üç eşit büyüklükte bileşen (K-014), tam uyumda kosinüs ≈ 1/√3


def _bagla(hucre, kayitlar):
    degiskenler = {}
    for halka, kayit in zip(hucre.halkalar, kayitlar):
        ozne, _iliski, nesne = kayit.uclu
        for degisken, varlik in ((halka.sol, ozne), (halka.sag, nesne)):
            if degiskenler.setdefault(degisken, varlik) != varlik:
                return None
    return degiskenler


def baglamalar(hucre, havuz, yeni):
    """Hücrenin havuzdaki tüm tutarlı bağlamaları, kayıt kimlikleri sırasıyla (belirlenimli)."""
    adaylar = [havuz.iliski_dizini(h.gen) for h in hucre.halkalar]
    sonuc = []
    for kimlikler in product(*adaylar):
        if len(set(kimlikler)) != len(kimlikler) or not yeni.intersection(kimlikler):
            continue
        degiskenler = _bagla(hucre, [havuz.kayit(k) for k in kimlikler])
        if degiskenler is not None:
            sonuc.append(Baglama(tuple(kimlikler), tuple(sorted(degiskenler.items()))))
    return sorted(sonuc)


def sonuc_uclusu(hucre, baglama):
    d = dict(baglama.degiskenler)
    return (d[hucre.sonuc.sol], hucre.sonuc.gen, d[hucre.sonuc.sag])


def alici(kk, gen):
    """Elle yazılan hücrenin alıcı vektörü: √d·R[gen] (K-016). Öğrenilen alıcılar H2'de."""
    return tuple(kk.olcek * x for x in kk.vektor(TUR_ILISKI, gen))


def afinite(alici_vektoru, kayit_vektoru):
    return max(0.0, min(1.0, kosinus(alici_vektoru, kayit_vektoru) * AFINITE_OLCEGI))


def eslesmeler(hucre, havuz, yeni, kk, esik_carpani):
    """Sembolik bağlamalardan her halkası afinite > θ·çarpan olanlar, güvenleriyle (K-016, K-017)."""
    alicilar = [alici(kk, h.gen) for h in hucre.halkalar]
    sonuc = []
    for b in baglamalar(hucre, havuz, yeni):
        kayitlar = [havuz.kayit(k) for k in b.kayitlar]
        afiniteler = tuple(afinite(a, k.vektor) for a, k in zip(alicilar, kayitlar))
        if any(af <= h.esik * esik_carpani for af, h in zip(afiniteler, hucre.halkalar)):
            continue
        guven = min(afiniteler + tuple(k.guven for k in kayitlar)) * hucre.guvenilirlik
        sonuc.append(Eslesme(hucre.kimlik, b, sonuc_uclusu(hucre, b), afiniteler, guven))
    return sonuc
