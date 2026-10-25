"""sistem.md §8, §18, EK A P7; K-035, V-057: bellek geçidinin doğruluk hesabı (çekirdek dışı, kâhinsiz).

Yalnız bölümdeki gözlemleri (olgular) kullanır; sorgu ve cevap alanı okunmaz; üreteç, dünya ve altın küme içe
aktarılmaz. Her bölümde çekirdek bir kez maskesiz, sonra adayın sonuç ilişkisindeki her gözlem birer birer maskelenerek
koşar (`cekirdek.bellek_gecidi.maskeli_kos`). Karşılaştırma burada yapılır:
- doğru: maskelenen gözlem adayın soyunca yeniden türetildi (gözlem çekirdeğe verilmediği için kendini onaylama yok);
- yanlış: soydan bir tahmin görünen bir gözlemle şema çelişkisinde (çekirdeğin defteri). Aynı (tahmin, gözlem) çifti
  bölümde bir kez sayılır. Maskelenen gözlemle çelişki, maskesiz koşuda görünen gözlemle çelişki olarak sayılmış olur;
- çelişki: soydan bir tahmin bellekten türemiş bir kayıtla ya da soyun kendi içinde çelişiyor (bölümde tekil çiftler);
- katkı ve eşleşme: koşuların toplamı; müdahale: cevabı soydan gelen maskeli koşuların geçit puanları (b·c, K-037).
  Kanıt için `mudahale_a` ((a) bileşeni) ve `mudahale_abc` (K-021 puanı) de toplanır; bunlar eşiğe girmez.
Ortam: kanıt = doğru + yanlış, doğruluk = doğru / kanıt (kanıt yoksa yok). Eşikler çekirdekte (`karar_ver`).
"""
from cekirdek.bellek_gecidi import maskeli_kos

SAYILAR = ("dogru", "yanlis", "celiski", "katki", "eslesme")  # K-035: ortamda toplanan bölüm sayıları
MUDAHALE_ALANLARI = ("mudahale", "mudahale_a", "mudahale_abc")  # K-037: geçit puanı (b·c), (a), K-021 puanı


def bolum_olgulari(bolum):
    return [(o["ozne"], o["iliski"], o["nesne"], o["guven"]) for o in bolum["olgular"]]


def maskelenecekler(aday, olgular):
    """Adayın doğrudan tahmin ettiği ilişkideki gözlemler (V-057)."""
    return [i for i, o in enumerate(olgular) if o[1] == aday.sonuc.gen]


def _ciftler(liste):
    return {tuple(tuple(u) for u in cift) for cift in liste}


def bolum_olcumu(aday, bellek, bolum, iliski_semasi, kk, prm, gunluk_ayari):
    olgular = bolum_olgulari(bolum)
    bellek = tuple(bellek)
    dogru, yanlis, celiski, katki, eslesme = 0, set(), set(), 0, 0
    mudahale = {a: [] for a in MUDAHALE_ALANLARI}
    for maske in [None] + maskelenecekler(aday, olgular):
        ham = maskeli_kos(aday, bellek, olgular, maske, iliski_semasi, kk, prm, gunluk_ayari)
        yanlis |= _ciftler(ham["olgu_celiskileri"])
        celiski |= _ciftler(ham["bellek_celiskileri"])
        katki += ham["katki"]
        eslesme += ham["eslesme"]
        if maske is not None:
            ozne, iliski, nesne, _guven = olgular[maske]
            dogru += [ozne, iliski, nesne] in ham["tahminler"]
        if ham["mudahale"] is not None:
            a, _b, _c, abc = ham["mudahale_bilesenleri"]
            for alan, deger in zip(MUDAHALE_ALANLARI, (ham["mudahale"], a, abc)):
                mudahale[alan].append(deger)
    return {"dogru": dogru, "yanlis": len(yanlis), "celiski": len(celiski), "katki": katki, "eslesme": eslesme,
            **mudahale}


def ortam_olcumu(aday, bellek, bolumler, iliski_semasi, kk, prm, gunluk_ayari):
    olcumler = [bolum_olcumu(aday, bellek, b, iliski_semasi, kk, prm, gunluk_ayari) for b in bolumler]
    toplam = {a: sum(o[a] for o in olcumler) for a in SAYILAR}
    toplam["kanit"] = toplam["dogru"] + toplam["yanlis"]
    toplam["dogruluk"] = toplam["dogru"] / toplam["kanit"] if toplam["kanit"] else None
    for a in MUDAHALE_ALANLARI:
        toplam[a] = [p for o in olcumler for p in o[a]]
    return toplam
