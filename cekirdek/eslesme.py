"""sistem.md §3, V-032: sembolik bağlama maskesi ve yarı-naif (delta) eşleşme, saf Python referans yolu.

Her halka ilişki dizininden kendi genindeki kayıtlara bakar; halkalar farklı kayıtlara bağlanır, aynı değişken
her yerde aynı varlığa bağlanır, en az bir halka `yeni` kümesindeki (önceki turda yazılmış) bir kayda bağlanır.
Kosinüs afinitesi ve θ süzgeci V-028 onayına bağlıdır, burada yoktur.
"""
from collections import namedtuple
from itertools import product

Baglama = namedtuple("Baglama", "kayitlar degiskenler")


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
