"""sistem.md §13; K-044 (ÖK-005 eki §4), V-067: "şema-türevi" kural testi ve (c) tanısının cinsiyet karıştırması.

- Şema-türevi: bir kural, tetik testinde kullanılmamış, birbirinden bağımsız en az 20 taze boş dünyanın hepsinde sıfır
  ihlal veriyorsa şema-türevidir. İhlal kapalı dünyaya göre yanlış tahmindir (tahmin edilen çift dünyada o ilişkiyle
  gözlenmemiş). Dünyalar: her ailede `sema_turevi.aile_basina` taban dünya `sematurevi|<aile>|<i>` tohumuyla, boş
  dönüşümü `bos|sematurevi|<aile>|<i>` tohumuyla (önkayıtlı etiketler; sonuca bakılarak seçilmez). Hiç tetiklenmeyen
  kural da sıfır ihlal verir; sayısı ayrıca raporlanır.
- Cinsiyet ikizi: tanımın (her seçeneğin) son belirli cinsiyet adımının tipi çevrilince elde edilen tanım tanım
  dosyasında varsa o ilişki. Çevrilen tanım dosyada yoksa ilişkinin ikizi yoktur.
- Cinsiyet karıştırma (yalnız tanı, kapıya girmez): her olgu, ikizi varsa, bağımsız olarak yarı olasılıkla ikiziyle
  değişir. Böylece bir kişinin cinsiyeti olgudan olguya tutarsız olur; ters ilişki çifti ise geçerli kalır (gelen ve
  giden olgunun ikisi de cinsiyetin iki değerini kabul eden ters listelerindedir).
"""
import dataclasses
import random

from degerlendirme import h2_bagla, h2_dunya, kural
from kesif import tohum

SEMATUREVI, BOS = "sematurevi", "bos"  # K-044: önkayıtlı tohum etiketleri
CINSIYET = "cinsiyet"  # K-044: (c) tanısının tohum etiketi
CINSIYET_OLASILIGI = 1 / 2  # K-044: olgu başına ikizle değişme olasılığı


def _ceviri(secenekler):
    sonuc = []
    for adimlar in secenekler:
        belirli = [i for i, a in enumerate(adimlar) if a["tip"] is not None]
        if not belirli:
            return None
        i = belirli[-1]
        sonuc.append([dict(a, tip=1 - a["tip"]) if j == i else a for j, a in enumerate(adimlar)])
    return sonuc


def cinsiyet_ikizleri(tanimlar):
    """[{ad, secenekler}] → {ilişki: cinsiyet ikizi}."""
    tanim = {t["ad"]: t["secenekler"] for t in tanimlar}
    ikiz = {}
    for ad, secenekler in tanim.items():
        cevrik = _ceviri(secenekler)
        eslesen = [b for b, s in tanim.items() if b != ad and s == cevrik]
        if eslesen:
            ikiz[ad] = eslesen[0]
    return ikiz


def cinsiyet_karistir(olgular, ikiz, rng):
    return tuple((a, ikiz[r] if r in ikiz and rng.random() < CINSIYET_OLASILIGI else r, b) for a, r, b in olgular)


def ihlal(k, dunyalar):
    """`dunyalar`: [(etiket, Indeks)] → toplam tahmin ve ihlal sayısı."""
    r = k.bas[0]
    tahmin = ihlal_ = 0
    for _, idx in dunyalar:
        t = k.tahminler(idx)
        tahmin += len(t)
        ihlal_ += sum((a, r, b) not in idx.olgu for a, b in t)
    return {"tahmin": tahmin, "ihlal": ihlal_}


def sema_turevi_mi(k, dunyalar):
    return ihlal(k, dunyalar)["ihlal"] == 0


def dunya_kayitlari(h2, tanimlar, sema):
    """[(etiket, boş dünya)]: ailelerin sözlük sırasıyla, her ailede `aile_basina` dünya."""
    aileler, n = h2.deger("dunya_aileleri"), h2.deger("sema_turevi")["aile_basina"]
    carpan = h2.deger("bagla_deneme_carpani")
    sonuc = []
    for a in sorted(aileler):
        for i in range(1, n + 1):
            d = h2_dunya.aile_dunyasi(a, aileler[a], tohum.tohum(h2, SEMATUREVI, a, i), tanimlar)
            rng = random.Random(tohum.tohum(h2, BOS, SEMATUREVI, a, i))
            sonuc.append((tohum.etiket(SEMATUREVI, a, i),
                          dataclasses.replace(d, olgular=tuple(h2_bagla.bos_dunya(d.olgular, sema, rng, carpan)))))
    return sonuc


def dunyalar(h2, tanimlar, sema):
    return [(e, kural.Indeks(d.olgular)) for e, d in dunya_kayitlari(h2, tanimlar, sema)]
