"""sistem.md §3, §5; K-016, K-017, V-032, V-034: çekirdek döngüsü (eşzamanlı turlar) ve durma.

Her turda bütün hücreler turun başındaki havuza yarı-naif bakar. Hücre başına en iyi `hucre_yazma_siniri`
eşleşme, sonra tur bütçesi uygulanır; atılanlar günlüğe yazılır. Yazmalar (hücre sırası, kayıt kimlikleri)
sırasıyla yapılır. Durma: yeni kayıt yok (sorgu cevaplıysa ya da sorgu yoksa), tur sınırı, ya da ikinci
impasse. İlk impasse'te bütün θ'lar bir kez `impasse_carpani` ile çarpılır ve tüm havuz yeniden denenir.
τ ile durma kalibrasyon kümesi oluşana kadar kapalıdır (K-017).
Günlük destek/çelişki defteridir (V-035): her ateşleme, yazma (kök kümesiyle) ve atma kayıtlıdır; bir turun
olayları sırası korunarak tur sonunda tek seferde yazılır.
"""
from dataclasses import dataclass

from cekirdek.altyapi.olay_gunlugu import YEDEK_KULLANILDI
from cekirdek.defter import ATESLEME, ATMA, KAYNAK, YAZMA, Defter
from cekirdek.eslesme import eslesmeler
from cekirdek.havuz import HavuzDoluHatasi
from cekirdek.plazma import cevapla, kok_kumesi

DURMA_YENI_YOK, DURMA_TUR_SINIRI, DURMA_IMPASSE = "yeni_kayit_yok", "tur_siniri", "impasse"


@dataclass(frozen=True)
class CekirdekParametreleri:
    kapasite: int
    tur_siniri: int
    hucre_yazma_siniri: int
    butce: int
    impasse_carpani: float

    @classmethod
    def ayardan(cls, ayar):
        d = ayar.deger
        return cls(d("havuz_kapasitesi"), d("tur_siniri"), d("hucre_tur_yazma_siniri"), d("eslesme_butcesi"),
                   d("impasse_esik_carpani"))


@dataclass(frozen=True)
class DonguSonucu:
    tur: int
    durma_nedeni: str
    esik_dusurme: int
    yazilan: int


def _skor(eslesme):
    """K-016: afinite × güven (afinite = halkaların en küçüğü)."""
    return min(eslesme.afiniteler) * eslesme.guven


def _tur_adaylari(hucreler, havuz, yeni, kk, prm, carpan, olaylar, tur):
    adaylar = []
    for sira, hucre in enumerate(hucreler):
        es = sorted(eslesmeler(hucre, havuz, yeni, kk, carpan), key=lambda e: (-_skor(e), e.baglama.kayitlar))
        for e in es:
            olaylar.append((ATESLEME, KAYNAK, {"tur": tur, "hucre": hucre.kimlik, "kayitlar": list(e.baglama.kayitlar),
                                               "uclu": list(e.uclu), "afiniteler": list(e.afiniteler),
                                               "guven": e.guven}))
        if len(es) > prm.hucre_yazma_siniri:
            olaylar.append(("ESLESME_ATILDI", KAYNAK, {"tur": tur, "neden": "hucre_siniri", "hucre": hucre.kimlik,
                                                        "sayi": len(es) - prm.hucre_yazma_siniri}))
        adaylar += [(sira, e) for e in es[:prm.hucre_yazma_siniri]]
    if len(adaylar) > prm.butce:
        adaylar.sort(key=lambda x: (-_skor(x[1]), x[0], x[1].baglama.kayitlar))
        olaylar.append(("ESLESME_ATILDI", KAYNAK, {"tur": tur, "neden": "butce", "sayi": len(adaylar) - prm.butce}))
        adaylar = adaylar[:prm.butce]
    return sorted(adaylar, key=lambda x: (x[0], x[1].baglama.kayitlar))


def _yaz(hucreler, havuz, adaylar, olaylar, tur):
    yazilanlar = []
    for sira, e in adaylar:
        try:
            k = havuz.cikarim_ekle(e.uclu, hucreler[sira].kimlik, e.baglama.kayitlar, e.guven)
        except HavuzDoluHatasi:
            olaylar.append((YEDEK_KULLANILDI, KAYNAK, {"yer": "cekirdek/dongu.py",
                                                       "neden": f"tur {tur}: havuz dolu, {list(e.uclu)} yazılamadı"}))
            continue
        for a in havuz.atilanlari_al():
            olaylar.append((ATMA, KAYNAK, {"tur": tur, "kimlik": a.kimlik, "uclu": list(a.uclu), "guven": a.guven}))
        if k is not None:
            yazilanlar.append(k.kimlik)
            olaylar.append((YAZMA, KAYNAK, {"tur": tur, "kimlik": k.kimlik, "uclu": list(k.uclu), "zincir": k.zincir,
                                            "ebeveynler": list(k.ebeveynler), "guven": k.guven,
                                            "kokler": sorted(kok_kumesi(havuz, k.kimlik))}))
    return yazilanlar


def calistir(hucreler, havuz, kk, prm, gunluk, *, iliski_semasi, sorgu=None):
    """`gunluk` destek/çelişki defteri olmalıdır (V-035); çelişki denetimi onaylı şemayla her turda yapılır (K-020)."""
    if not isinstance(gunluk, Defter):
        raise TypeError("çekirdek döngüsü Defter ister (defterde izi olmayan sonuç yanıta giremez)")
    gunluk.celiski_denetle(havuz, iliski_semasi, tur=0)
    yeni = frozenset(k.kimlik for k in havuz.kayitlar())
    carpan, dusurme, tur, toplam = 1.0, 0, 0, 0
    while True:
        tur += 1
        olaylar = []
        adaylar = _tur_adaylari(hucreler, havuz, yeni, kk, prm, carpan, olaylar, tur)
        yazilanlar = _yaz(hucreler, havuz, adaylar, olaylar, tur)
        gunluk.ekle_toplu(olaylar)
        gunluk.celiski_denetle(havuz, iliski_semasi, tur)
        toplam += len(yazilanlar)
        havuz.tur_ilerlet()
        canli = {k.kimlik for k in havuz.kayitlar()}
        yeni = frozenset(k for k in yazilanlar if k in canli)
        neden = None
        if not yeni:
            if sorgu is None or cevapla(havuz, sorgu, gunluk).iliski is not None:
                neden = DURMA_YENI_YOK
            elif dusurme == 0:
                dusurme, carpan, yeni = 1, prm.impasse_carpani, frozenset(canli)
                gunluk.ekle("ESIK_DUSURME", KAYNAK, {"tur": tur, "carpan": carpan})
            else:
                neden = DURMA_IMPASSE
        if neden is None and tur >= prm.tur_siniri:
            neden = DURMA_TUR_SINIRI
        if neden is not None:
            gunluk.ekle("DURMA", KAYNAK, {"tur": tur, "neden": neden, "esik_dusurme": dusurme})
            return DonguSonucu(tur, neden, dusurme, toplam)
