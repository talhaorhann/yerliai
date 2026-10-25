"""sistem.md §8 (bellek hücresi: müdahale + karşı-kısayol), §18 (kabul/ret çekirdeğin kendi kurallarıyla), EK A P7
(mutlak bellek kapısı, kaydırılmış doğrulama, en kötü ortam); V-054, K-035: bellek geçidi, çekirdek tarafı.

Çekirdek tarafı iki iş yapar; doğruluğu hesaplamaz (K-035, hesap `degerlendirme/gozlem_puani.py`'de):
1. `maskeli_kos`: bir bölümde bir gözlem maskelenmişken çekirdeği bellekle (R0) ve bellek + adayla (R1) koşar ve
   adayın soyunun (yazdıkları ve onlardan türeyenler) ham çıktısını verir: türettiği üçlüler, gözlenen (maskelenmemiş)
   olgularla ve bellekten türemiş kayıtlarla şema çelişkileri, katkı (R0'da olmayan ya da daha geç çıkan üçlüler),
   eşleşme sayısı ve maskelenen çiftin cevabı soydan geliyorsa müdahale ölçümü ("sınanamadı" sayılmaz, K-021).
   Geçidin müdahale puanı b·c'dir (K-037): cevap birden çok bağımsız yoldan çıkınca (a) düşer ama bu kısayol değildir.
   (a) ve K-021 puanı (a·b·c) ham çıktıda kalır, eşiğe girmez. H1'deki müdahale testi değişmez.
   Maskelenen olgu çekirdeğe hiç verilmez: kural onu kendi kendine onaylayamaz.
2. `karar_ver`: dışarıda hesaplanan ortam sayılarına eşikleri şu sırayla uygular:
   1. Bellekte yapıca aynı kural (değişken adı ve halka sırası dışında) → ret: gereksiz.
   2. Ölçülen (kanıtı `en_az_kanit`'e ulaşan) her ortamda doğruluk < eşik → ret: yanlış. Bir ortamda geçip en kötü
      ortamda geçmiyor → ret: kısayol.
   3. Bellekle çelişki → ret: çelişkili.
   4. Hiç eşleşme yok → sınanamadı. Eşleşip katkı yok → ret: gereksiz.
   5. Bir ortam ölçülemedi ya da müdahale kanıtı `en_az_kanit`'ten az → sınanamadı (kabul de ret de değil).
   6. Müdahale ortalaması < eşik → ret: kısayol. Değilse kabul.
Etiket ve kâhin yoktur: maskelenen şey bölümdeki bir gözlemdir (K-035).
"""
import itertools
from dataclasses import dataclass

from cekirdek.defter import ATESLEME, CELISKI, YAZMA, Defter
from cekirdek.dongu import calistir
from cekirdek.havuz import EPITOP, Havuz
from cekirdek.mudahale import PUANLI, mudahale_testi
from cekirdek.plazma import cevapla

KABUL, RET, SINANAMADI = "kabul", "ret", "sinanamadi"  # V-054
GEREKSIZ, YANLIS, KISAYOL, CELISKILI = "gereksiz", "yanlis", "kisayol", "celiskili"  # V-054: ret nedenleri


@dataclass(frozen=True)
class GecitEsikleri:
    dogruluk: float
    en_az_kanit: int
    mudahale: float

    @classmethod
    def ayardan(cls, ayar):
        d = ayar.deger
        return cls(d("bellek_dogruluk_esigi"), d("bellek_en_az_kanit"), d("bellek_mudahale_esigi"))


@dataclass(frozen=True)
class GecitKarari:
    karar: str
    neden: object
    olcumler: dict


def kanonik_bicim(hucre):
    """Değişken adları ve halka sırası dışında hücrenin yapısı (eşik ve güvenilirlik sayılmaz)."""
    en_iyi = None
    for sira in itertools.permutations(hucre.halkalar):
        ad = {}
        for h in sira:
            for d in (h.sol, h.sag):
                ad.setdefault(d, len(ad))
        bicim = (tuple((h.gen, ad[h.sol], ad[h.sag]) for h in sira), (hucre.sonuc.gen, ad[hucre.sonuc.sol],
                 ad[hucre.sonuc.sag]), tuple(sorted(tuple(sorted((ad[a], ad[b]))) for a, b in hucre.farkli)))
        en_iyi = bicim if en_iyi is None else min(en_iyi, bicim)
    return en_iyi


def esdeger_mi(aday, bellek):
    if aday.kimlik in {h.kimlik for h in bellek}:
        raise ValueError(f"aday kimliği bellekte var: {aday.kimlik}")
    return any(kanonik_bicim(aday) == kanonik_bicim(h) for h in bellek)


def _kos(hucreler, olgular, sorgu, iliski_semasi, kk, prm, gunluk_ayari):
    havuz = Havuz(prm.kapasite, kk)
    for s, r, o, g in olgular:
        havuz.epitop_ekle(s, r, o, guven=g)
    defter = Defter(None, **gunluk_ayari)
    calistir(hucreler, havuz, kk, prm, defter, iliski_semasi=iliski_semasi, sorgu=sorgu)
    return havuz, defter


def _ilk_turlar(olgular, defter):
    """Üçlü → ilk çıktığı tur (olgular 0)."""
    tur = {(s, r, o): 0 for s, r, o, _ in olgular}
    if defter is not None:
        for k in defter.kayitlar():
            if k["tur"] == YAZMA:
                tur.setdefault(tuple(k["veri"]["uclu"]), k["veri"]["tur"])
    return tur


def maskeli_kos(aday, bellek, olgular, maske, iliski_semasi, kk, prm, gunluk_ayari):
    """`olgular`: [(özne, ilişki, nesne, güven)]; `maske`: çekirdeğe verilmeyecek olgunun sırası ya da None.

    Ham çıktı döner; hiçbir şey maskelenen gözlemle karşılaştırılmaz (karşılaştırma çekirdek dışında). Çelişkiler
    üçlü çiftleridir: `olgu_celiskileri` [tahmin, gözlem], `bellek_celiskileri` sıralı [tahmin, kayıt]."""
    gorunen = [o for i, o in enumerate(olgular) if i != maske]
    if maske is None:
        sorgu = None
    else:
        ozne, _iliski, nesne, _guven = olgular[maske]
        sorgu = (ozne, nesne)
    bellek = tuple(bellek)
    defter0 = _kos(bellek, gorunen, sorgu, iliski_semasi, kk, prm, gunluk_ayari)[1] if bellek else None
    hucreler = bellek + (aday,)
    havuz1, defter1 = _kos(hucreler, gorunen, sorgu, iliski_semasi, kk, prm, gunluk_ayari)
    olaylar = defter1.kayitlar()
    epitop = {k.kimlik for k in havuz1.kayitlar() if k.katman == EPITOP}
    soy, soy_uclu = set(), set()
    for k in olaylar:
        v = k["veri"]
        if k["tur"] == YAZMA and (v["zincir"] == aday.kimlik or soy.intersection(v["ebeveynler"])):
            soy.add(v["kimlik"])
            soy_uclu.add(tuple(v["uclu"]))
    olgu_celiskisi, bellek_celiskisi = set(), set()
    for k in olaylar:
        if k["tur"] != CELISKI or not soy.intersection(k["veri"]["kayitlar"]):
            continue
        ciftler = list(zip(k["veri"]["kayitlar"], map(tuple, k["veri"]["uclular"])))
        if epitop.intersection(k["veri"]["kayitlar"]):
            olgu_celiskisi.add(tuple(u for _, u in sorted(ciftler, key=lambda c: c[0] in epitop)))
        else:
            bellek_celiskisi.add(tuple(sorted(u for _, u in ciftler)))
    tur0, tur1 = _ilk_turlar(gorunen, defter0), _ilk_turlar(gorunen, defter1)
    katki = sum(1 for u in soy_uclu if u not in tur0 or tur1[u] < tur0[u])
    mudahale = bilesenler = None
    if sorgu is not None:
        cevap = cevapla(havuz1, sorgu, defter1)
        if cevap.iliski is not None and soy.intersection(a["kimlik"] for a in cevap.gerekce):
            m = mudahale_testi(havuz1, defter1, hucreler, gorunen, kk, prm, iliski_semasi, sorgu)
            if m.durum == PUANLI:
                mudahale, bilesenler = m.b * m.c, [m.a, m.b, m.c, m.puan]  # K-037
    return {"tahminler": sorted(list(u) for u in soy_uclu),
            "olgu_celiskileri": sorted([list(t), list(o)] for t, o in olgu_celiskisi),
            "bellek_celiskileri": sorted([list(a), list(b)] for a, b in bellek_celiskisi), "katki": katki,
            "eslesme": sum(1 for k in olaylar if k["tur"] == ATESLEME and k["veri"]["hucre"] == aday.kimlik),
            "mudahale": mudahale, "mudahale_bilesenleri": bilesenler}


def karar_ver(esdeger, olcum, esikler):
    """`olcum`: {ortam: {"kanit", "celiski", "katki", "eslesme": sayı, "dogruluk": oran ya da None,
    "mudahale": [puan]}}, dışarıda hesaplanır (K-035). Yalnız eşikler uygulanır: doğruluk, kanıtı `en_az_kanit`'e
    ulaşan ortamda ölçülmüş sayılır."""
    if esdeger:
        return GecitKarari(RET, GEREKSIZ, {"esdeger": True})
    olculen = [o["dogruluk"] for o in olcum.values() if o["kanit"] >= esikler.en_az_kanit]
    if olculen and max(olculen) < esikler.dogruluk:
        return GecitKarari(RET, YANLIS, olcum)
    if olculen and min(olculen) < esikler.dogruluk:
        return GecitKarari(RET, KISAYOL, olcum)
    if sum(o["celiski"] for o in olcum.values()):
        return GecitKarari(RET, CELISKILI, olcum)
    if not sum(o["eslesme"] for o in olcum.values()):
        return GecitKarari(SINANAMADI, None, olcum)
    if not sum(o["katki"] for o in olcum.values()):
        return GecitKarari(RET, GEREKSIZ, olcum)
    puanlar = [p for o in olcum.values() for p in o["mudahale"]]
    if len(olculen) < len(olcum) or len(puanlar) < esikler.en_az_kanit:
        return GecitKarari(SINANAMADI, None, olcum)
    if sum(puanlar) / len(puanlar) < esikler.mudahale:
        return GecitKarari(RET, KISAYOL, olcum)
    return GecitKarari(KABUL, None, olcum)
