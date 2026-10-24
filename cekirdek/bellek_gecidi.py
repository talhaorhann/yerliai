"""sistem.md §8 (bellek hücresi: müdahale + karşı-kısayol), §18 (kabul/ret çekirdeğin kendi kurallarıyla), EK A P7
(mutlak bellek kapısı, kaydırılmış doğrulama, en kötü ortam); V-054: bellek geçidi.

Geçit bir aday kuralı (hücre) yalnız veriyle sınar; etiket ve kâhin yoktur. Her ortamın her bölümünde çekirdek iki kez
koşar: bellekle (R0) ve bellek + adayla (R1). Adayın soyu = adayın yazdığı kayıtlar ve onlardan türeyenler.
- Destek: soydan bir kaydın üçlüsü bölümde gözlenmiş bir olguyla aynı ve o olgu kaydın kök kümesinde değil (kendini
  doğrulamıyor, kök-ayrık).
- Karşıtlık: soydan bir kayıt ile bir olgu arasında şema çelişkisi (dışlayıcı / işlevsel / ters; defterin CELISKI'si).
- Çelişki: soydan bir kayıt ile bellekten türemiş (soy dışı) bir çıkarım ya da soyun kendi içinde şema çelişkisi.
- Katkı: soyun yazdığı, R0'da hiç olmayan ya da R0'da daha geç turda çıkan üçlüler.
- Müdahale: cevabı soydan gelen sorularda müdahale testinin puanı ("sınanamadı" sayılmaz, K-021).
Ortam doğruluğu = destek / (destek + karşıtlık), en az `en_az_kanit` gözlemle. Karar sırası:
1. Bellekteki bir kuralla yapıca aynı (değişken adı ve halka sırası dışında) → ret: gereksiz.
2. Ölçülen her ortamda doğruluk < eşik → ret: yanlış. Bazı ortamlarda eşiği geçip en kötü ortamda geçmiyor → ret: kısayol.
3. Çelişki > 0 → ret: çelişkili.
4. Katkı = 0 → ret: gereksiz.
5. Bir ortam gözlemle ölçülemedi ya da müdahale kanıtı `en_az_kanit`'ten az → sınanamadı (kabul de ret de değil).
6. Müdahale ortalaması < eşik → ret: kısayol. Değilse kabul.
Gözlenmeyen ilişkiler için doğruluk kanıtı yoktur; dışarıdan skor (kâhin) kanalı kullanıcı kararıdır (V-054).
"""
import itertools
from dataclasses import dataclass

from cekirdek.defter import CELISKI, YAZMA, Defter
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


def _kos(hucreler, olgular, sorgu, iliski_semasi, kk, prm, gunluk_ayari):
    havuz = Havuz(prm.kapasite, kk)
    for s, r, o, g in olgular:
        havuz.epitop_ekle(s, r, o, guven=g)
    defter = Defter(None, **gunluk_ayari)
    calistir(hucreler, havuz, kk, prm, defter, iliski_semasi=iliski_semasi, sorgu=sorgu)
    return havuz, defter


def _ilk_turlar(havuz, defter):
    """Üçlü → ilk çıktığı tur (olgular 0)."""
    tur = {k.uclu: 0 for k in havuz.kayitlar() if k.katman == EPITOP}
    for k in defter.kayitlar():
        if k["tur"] == YAZMA:
            tur.setdefault(tuple(k["veri"]["uclu"]), k["veri"]["tur"])
    return tur


def bolum_kaniti(aday, bellek, bolum, iliski_semasi, kk, prm, gunluk_ayari):
    olgular = [(o["ozne"], o["iliski"], o["nesne"], o["guven"]) for o in bolum["olgular"]]
    sorgu = (bolum["sorgu"]["ozne"], bolum["sorgu"]["nesne"]) if bolum.get("sorgu") else None
    havuz0, defter0 = _kos(tuple(bellek), olgular, sorgu, iliski_semasi, kk, prm, gunluk_ayari)
    hucreler = tuple(bellek) + (aday,)
    havuz1, defter1 = _kos(hucreler, olgular, sorgu, iliski_semasi, kk, prm, gunluk_ayari)
    olaylar = defter1.kayitlar()
    epitop = {k.kimlik: k.uclu for k in havuz1.kayitlar() if k.katman == EPITOP}
    olgu_kimligi = {u: k for k, u in epitop.items()}
    soy, soy_uclu = set(), {}
    for k in olaylar:
        v = k["veri"]
        if k["tur"] == YAZMA and (v["zincir"] == aday.kimlik or soy.intersection(v["ebeveynler"])):
            soy.add(v["kimlik"])
            soy_uclu.setdefault(tuple(v["uclu"]), []).append(v)
    destek = sorted(u for u, vs in soy_uclu.items()
                    if u in olgu_kimligi and any(olgu_kimligi[u] not in v["kokler"] for v in vs))
    karsitlik, celiski = set(), set()
    for k in olaylar:
        if k["tur"] != CELISKI:
            continue
        a, b = k["veri"]["kayitlar"]
        if not soy.intersection((a, b)):
            continue
        cift = (k["veri"]["tur_adi"],) + tuple(sorted(map(tuple, k["veri"]["uclular"])))
        (karsitlik if a in epitop or b in epitop else celiski).add(cift)
    tur0, tur1 = _ilk_turlar(havuz0, defter0), _ilk_turlar(havuz1, defter1)
    katki = sorted(u for u in soy_uclu if u not in tur0 or tur1[u] < tur0[u])
    mudahale = None
    if sorgu is not None:
        cevap = cevapla(havuz1, sorgu, defter1)
        if cevap.iliski is not None and soy.intersection(a["kimlik"] for a in cevap.gerekce):
            m = mudahale_testi(havuz1, defter1, hucreler, olgular, kk, prm, iliski_semasi, sorgu)
            mudahale = m.puan if m.durum == PUANLI else None
    return {"destek": len(destek), "karsitlik": len(karsitlik), "celiski": len(celiski), "katki": len(katki),
            "mudahale": mudahale}


def gecit(aday, bellek, ortamlar, iliski_semasi, kk, prm, gunluk_ayari, esikler, dis_kanit=None):
    """`ortamlar`: {ad: [bölüm]}; bölümde yalnız olgular ve isteğe bağlı sorgu kullanılır (cevap okunmaz)."""
    if dis_kanit is not None:
        raise NotImplementedError("dışarıdan doğruluk skoru (kâhin kanalı) kullanıcı kararı bekliyor (V-054)")
    if not ortamlar:
        raise ValueError("bellek geçidi en az bir ortam ister")
    if aday.kimlik in {h.kimlik for h in bellek}:
        raise ValueError(f"aday kimliği bellekte var: {aday.kimlik}")
    if any(kanonik_bicim(aday) == kanonik_bicim(h) for h in bellek):
        return GecitKarari(RET, GEREKSIZ, {"esdeger": True})
    olcum = {}
    for ad in sorted(ortamlar):
        kanitlar = [bolum_kaniti(aday, bellek, b, iliski_semasi, kk, prm, gunluk_ayari) for b in ortamlar[ad]]
        toplam = {a: sum(k[a] for k in kanitlar) for a in ("destek", "karsitlik", "celiski", "katki")}
        gozlem = toplam["destek"] + toplam["karsitlik"]
        toplam["dogruluk"] = toplam["destek"] / gozlem if gozlem >= esikler.en_az_kanit else None
        toplam["mudahale"] = [k["mudahale"] for k in kanitlar if k["mudahale"] is not None]
        olcum[ad] = toplam
    olculen = [o["dogruluk"] for o in olcum.values() if o["dogruluk"] is not None]
    if olculen and max(olculen) < esikler.dogruluk:
        return GecitKarari(RET, YANLIS, olcum)
    if olculen and min(olculen) < esikler.dogruluk:
        return GecitKarari(RET, KISAYOL, olcum)
    if sum(o["celiski"] for o in olcum.values()):
        return GecitKarari(RET, CELISKILI, olcum)
    if not sum(o["katki"] for o in olcum.values()):
        return GecitKarari(RET, GEREKSIZ, olcum)
    puanlar = [p for o in olcum.values() for p in o["mudahale"]]
    if len(olculen) < len(olcum) or len(puanlar) < esikler.en_az_kanit:
        return GecitKarari(SINANAMADI, None, olcum)
    if sum(puanlar) / len(puanlar) < esikler.mudahale:
        return GecitKarari(RET, KISAYOL, olcum)
    return GecitKarari(KABUL, None, olcum)


def gozden_gecir(bellek_deposu, bicim_yolu, ortamlar, iliski_semasi, kk, prm, gunluk_ayari, esikler):
    """EK A P7 (geri alınabilir statü): her aktif bellek hücresi öteki bellek hücreleriyle yeniden sınanır; yanlış,
    kısayol ya da çelişkili çıkan geri alınır (silinmez, olay yazılır). Geri alınan kimlikler döner."""
    geri = []
    for h in bellek_deposu.hucreler(bicim_yolu, iliski_semasi):
        oteki = [x for x in bellek_deposu.hucreler(bicim_yolu, iliski_semasi) if x.kimlik != h.kimlik]
        k = gecit(h, oteki, ortamlar, iliski_semasi, kk, prm, gunluk_ayari, esikler)
        if k.karar == RET and k.neden in (YANLIS, KISAYOL, CELISKILI):
            bellek_deposu.geri_al(h.kimlik, k.neden)
            geri.append(h.kimlik)
    return geri
