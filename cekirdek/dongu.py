"""sistem.md §3, §5; K-016, K-017, V-032, V-034: çekirdek döngüsü (eşzamanlı turlar) ve durma.

Her turda bütün hücreler turun başındaki havuza yarı-naif bakar. Önce kopya kuralı C süzer (K-031), sonra
hücre başına en iyi `hucre_yazma_siniri` eşleşme, sonra tur bütçesi uygulanır; atılanlar günlüğe yazılır. Yazmalar (hücre sırası, kayıt kimlikleri)
sırasıyla yapılır. Durma: yeni kayıt yok (sorgu cevaplıysa ya da sorgu yoksa), tur sınırı, ya da ikinci
impasse. İlk impasse'te bütün θ'lar bir kez `impasse_carpani` ile çarpılır ve tüm havuz yeniden denenir.
τ ile durma kalibrasyon kümesi oluşana kadar kapalıdır (K-017).
Günlük destek/çelişki defteridir (V-035): her ateşleme, yazma (kök kümesiyle) ve atma kayıtlıdır; bir turun
olayları sırası korunarak tur sonunda tek seferde yazılır.
Kopya kuralı (K-028, V-046): aynı üçlünün yeni kökenli kaydı yalnız yeni dayanak getiriyorsa yazılır (`yeni_dayanak_mi`);
getirmeyen aday yazılmaz ve tur başına sayısı `ESLESME_ATILDI` (neden: dayanak_yok) olarak kaydedilir.
K-031 (V-051): C hücre sınırından önce uygulanır, böylece sınır yalnız yazılabilecek adayları sayar (§3 "≤8 yazma");
yazma sırasında C bir kez daha, bu turda yazılanlarla birlikte denetlenir.
"""
from dataclasses import dataclass

from cekirdek.altyapi.olay_gunlugu import YEDEK_KULLANILDI
from cekirdek.defter import ATESLEME, ATMA, KAYNAK, YAZMA, Defter
from cekirdek.eslesme import afinite_tablosu, eslesmeler
from cekirdek.havuz import CIKARIM, HavuzDoluHatasi
from cekirdek.plazma import cevapla, kok_kumesi

DURMA_YENI_YOK, DURMA_TUR_SINIRI, DURMA_IMPASSE = "yeni_kayit_yok", "tur_siniri", "impasse"
DAYANAK_YOK = "dayanak_yok"  # K-028


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


def _tur_adaylari(hucreler, havuz, yeni, kk, prm, carpan, olaylar, tur, ispat_mi):
    """Turun adayları ve C'nin (turun başındaki havuza göre) baştan attığı aday sayısı."""
    adaylar, dayanaksiz = [], 0
    tablo = afinite_tablosu(kk, havuz, [h.gen for hucre in hucreler for h in hucre.halkalar])  # V-042: tur başına bir kez
    for sira, hucre in enumerate(hucreler):
        es = sorted(eslesmeler(hucre, havuz, yeni, kk, carpan, tablo), key=lambda e: (-_skor(e), e.baglama.kayitlar))
        for e in es:
            olaylar.append((ATESLEME, KAYNAK, {"tur": tur, "hucre": hucre.kimlik, "kayitlar": list(e.baglama.kayitlar),
                                               "uclu": list(e.uclu), "afiniteler": list(e.afiniteler),
                                               "guven": e.guven}))
        yazilabilir = [e for e in es if yeni_dayanak_mi(havuz, e.uclu, e.baglama.kayitlar, ispat_mi)]  # K-031
        dayanaksiz += len(es) - len(yazilabilir)
        es = yazilabilir
        if len(es) > prm.hucre_yazma_siniri:
            olaylar.append(("ESLESME_ATILDI", KAYNAK, {"tur": tur, "neden": "hucre_siniri", "hucre": hucre.kimlik,
                                                        "sayi": len(es) - prm.hucre_yazma_siniri}))
        adaylar += [(sira, e) for e in es[:prm.hucre_yazma_siniri]]
    if len(adaylar) > prm.butce:
        adaylar.sort(key=lambda x: (-_skor(x[1]), x[0], x[1].baglama.kayitlar))
        olaylar.append(("ESLESME_ATILDI", KAYNAK, {"tur": tur, "neden": "butce", "sayi": len(adaylar) - prm.butce}))
        adaylar = adaylar[:prm.butce]
    return sorted(adaylar, key=lambda x: (x[0], x[1].baglama.kayitlar)), dayanaksiz


def yeni_dayanak_mi(havuz, uclu, ebeveynler, ispat_mi):
    """K-028 (C): adayın dayanağı, ebeveynlerinin kök kümelerinin birleşimidir (dayandığı olgular). Aynı üçlünün
    havuzdaki canlı bir ispatının kök kümesi bu dayanağın alt kümesiyse aday, o ispatın dayandığı her olguya zaten
    dayanıyordur: yeni dayanak getirmez. İspat = izli çıkarım (`ispat_mi`: defterde YAZMA izi var ya da bu turda
    döngü yazdı, V-035); epitoplar ve izsiz kayıtlar ispat sayılmaz (K-018)."""
    dayanak = frozenset().union(*(kok_kumesi(havuz, e) for e in ebeveynler))
    for kimlik in havuz.iliski_dizini(uclu[1]):
        k = havuz.kayit(kimlik)
        if k.katman == CIKARIM and k.uclu == tuple(uclu) and ispat_mi(kimlik) and kok_kumesi(havuz, kimlik) <= dayanak:
            return False
    return True


def _yaz(hucreler, havuz, adaylar, olaylar, tur, gunluk, dayanaksiz=0):
    yazilanlar = []
    for sira, e in adaylar:
        if not yeni_dayanak_mi(havuz, e.uclu, e.baglama.kayitlar,
                               lambda kimlik: gunluk.yazildi_mi(kimlik) or kimlik in yazilanlar):
            dayanaksiz += 1
            continue
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
    if dayanaksiz:
        olaylar.append(("ESLESME_ATILDI", KAYNAK, {"tur": tur, "neden": DAYANAK_YOK, "sayi": dayanaksiz}))
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
        adaylar, dayanaksiz = _tur_adaylari(hucreler, havuz, yeni, kk, prm, carpan, olaylar, tur, gunluk.yazildi_mi)
        yazilanlar = _yaz(hucreler, havuz, adaylar, olaylar, tur, gunluk, dayanaksiz)
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
