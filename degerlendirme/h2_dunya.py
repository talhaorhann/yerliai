"""sistem.md §11, §13; K-041 (ÖK-005 taslağı §2.1, §3, §5), V-062: H2 dünya aileleri ve havuzları (kâhin tarafı).

Bir dünya, üreticinin soy ağacındaki bütün kişiler arasındaki bütün olgulardır (kapalı dünya). Tohum etiketten türetilir
(`kesif.tohum`), seçilmez ve değiştirilmez. Havuzlardaki dünya özetleri tekildir; yineleme durdurur.
"""
import random

from cekirdek.altyapi.kanonik import kanonik_json, ozet
from degerlendirme import ikinci_uretec
from degerlendirme.dunya import Dunya
from kesif import m0, tohum

AGAC, NUFUS = "agac", "nufus"  # K-041: config_h2 dunya_aileleri üretici adları
HAVUZ = "havuz"  # K-041: tohum etiketinin ilk parçası (ÖK-005 taslağı §5)


def dunya_olgulari(d, tanimlar):
    return sorted((x, r, y) for x in range(d.kisi_sayisi) for y, r in d.iliskiler(x, tanimlar).items())


def aile_dunyasi(aile, aile_ayari, tohum_degeri, tanimlar):
    rng = random.Random(tohum_degeri)
    p = aile_ayari["parametreler"]
    if aile_ayari["uretec"] == AGAC:
        d = Dunya.uret(rng, p["nesil_sayisi"], p["cocuk_en_az"], p["cocuk_en_cok"], p["evlilik_orani"])
        return m0.Dunya(aile, tuple(range(d.kisi_sayisi)), tuple(dunya_olgulari(d, tanimlar)))
    if aile_ayari["uretec"] == NUFUS:
        n = ikinci_uretec.uret(rng, **p)
        return m0.Dunya(aile, tuple(range(len(n.tip))), tuple(ikinci_uretec.olgular(n, tanimlar.secenekler)))
    raise ValueError("bilinmeyen üretici")


def havuz(havuz_adi, h2_ayar, tanimlar):
    dagilim = h2_ayar.deger("havuz_dagilimi")[havuz_adi]
    aileler = h2_ayar.deger("dunya_aileleri")
    return [aile_dunyasi(aile, aileler[aile], tohum.tohum(h2_ayar, HAVUZ, havuz_adi, aile, i), tanimlar)
            for aile in sorted(dagilim) for i in range(1, dagilim[aile] + 1)]


def dunya_ozeti(d, algoritma):
    return ozet(kanonik_json([d.aile, list(d.kisiler), [list(o) for o in d.olgular]]), algoritma)


def havuz_ozetleri(h2_ayar, tanimlar, havuzlar, algoritma="sha256"):  # V-007
    sonuc = {h: [dunya_ozeti(d, algoritma) for d in havuz(h, h2_ayar, tanimlar)] for h in havuzlar}
    hepsi = [o for v in sonuc.values() for o in v]
    if len(set(hepsi)) != len(hepsi):
        raise ValueError("havuzlarda yinelenen dünya")
    return sonuc
