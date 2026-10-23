"""sistem.md §9, KODLAMA_PROMPTU §5–§6, K-021, V-038: müdahale testi (kopya kâğıdı yok).

Yalnız çekirdeğin kendi zincirleri kullanılır; etiket, kâhin, kalibrasyon ve LLM bu hesaba girmez.
(a) Cevabın her kök epitopu silinir; kök kümesinde o epitop olan kayıtlar düşer (yalnız etkilenen köken alt grafı),
    cevabın güveni plazmayla yeniden hesaplanır. a = güveni düşüren silmelerin oranı.
(b) Sorgu yolundaki varlıklarla kenar paylaşmayan her epitop tür uyumlu yedekle (aynı ilişki ve güven, yeni varlıklar)
    değiştirilip çekirdek yeniden koşar. b = cevabın (ilişki ve güven) değişmediği oran. İlgisiz epitop yoksa
    soru "sınanamadı" olur: b ve puan boş kalır, başarı sayılmaz (K-021 kullanıcı şartı).
(c) Ters sorgu cevaplanıyorsa ters adaylarından biri olmalı ve cevabın köken alt grafına çelişki dokunmamalı.
Puan = a·b·c. Karşı-olgusal koşular bellekteki defterle yapılır; ana deftere yalnız `MUDAHALE` özeti yazılır.
"""
from dataclasses import dataclass

from cekirdek.defter import KAYNAK, Defter
from cekirdek.dongu import calistir
from cekirdek.havuz import EPITOP, Havuz
from cekirdek.plazma import cevapla, kok_kumesi

MUDAHALE = "MUDAHALE"  # KODLAMA_PROMPTU §5
PUANLI, SINANAMADI, CEVAPSIZ = "puanli", "sinanamadi", "cevapsiz"  # K-021


@dataclass(frozen=True)
class MudahaleSonucu:
    sorgu: tuple
    cevap: object
    guven: object
    silmeler: tuple
    a: object
    degisiklikler: tuple
    b: object
    sinanamadi: bool
    ters_cevap: object
    ters_tutarli: object
    celiski_var: object
    c: object
    puan: object
    durum: str


class BudanmisHavuz:
    """Bir epitop silinmiş gibi görünüm: kök kümesinde o epitop olan kayıtlar yok, diğerleri aynen (salt okunur)."""

    def __init__(self, havuz, silinen_epitop):
        self._havuz = havuz
        self._kalan = [k for k in havuz.kayitlar() if silinen_epitop not in kok_kumesi(havuz, k.kimlik)]

    def kayitlar(self):
        return list(self._kalan)

    def kayit(self, kimlik):
        return self._havuz.kayit(kimlik)


def _bellek_defteri(defter):
    return Defter(None, defter.algoritma, defter.sema_surumu, defter.izinli_kaynaklar)


def _yeniden_cevapla(olgular, hucreler, kk, prm, iliski_semasi, sorgu, defter):
    """Değiştirilmiş olgularla çekirdeği baştan koşturur (bellekteki defterle) ve cevabı döndürür."""
    havuz = Havuz(prm.kapasite, kk)
    for s, r, o, g in olgular:
        havuz.epitop_ekle(s, r, o, guven=g)
    bellek = _bellek_defteri(defter)
    calistir(hucreler, havuz, kk, prm, bellek, iliski_semasi=iliski_semasi, sorgu=sorgu)
    return cevapla(havuz, sorgu, bellek)


def _oran(degerler):
    return sum(1 for d in degerler if d) / len(degerler)


def _koken_alt_grafi(havuz, kimlikler):
    gorulen, yigin = set(), list(kimlikler)
    while yigin:
        k = havuz.kayit(yigin.pop())
        if k.kimlik not in gorulen:
            gorulen.add(k.kimlik)
            yigin.extend(k.ebeveynler)
    return gorulen


def mudahale_testi(havuz, defter, hucreler, olgular, kk, prm, iliski_semasi, sorgu):
    """Ana koşunun (havuz, defter) cevabını müdahaleyle sınar. `olgular`, havuza aynı sırayla eklenen (s, r, o, güven)."""
    epitoplar = [k for k in havuz.kayitlar() if k.katman == EPITOP]
    if [k.uclu for k in epitoplar] != [(s, r, o) for s, r, o, _ in olgular]:
        raise ValueError("olgular havuzdaki epitoplarla aynı sırada değil")
    cevap = cevapla(havuz, sorgu, defter)
    if cevap.iliski is None:
        sonuc = MudahaleSonucu(tuple(sorgu), None, None, (), None, (), None, False, None, None, None, None, None,
                               CEVAPSIZ)
        return _kaydet(defter, sonuc)
    ispatlar = [a["kimlik"] for a in cevap.gerekce]
    kokler = sorted(set().union(*(kok_kumesi(havuz, k) for k in ispatlar)))

    silmeler = []
    for e in kokler:
        yeni = dict(cevapla(BudanmisHavuz(havuz, e), sorgu, defter).birlesik).get(cevap.iliski, 0.0)
        silmeler.append({"epitop": e, "uclu": list(havuz.kayit(e).uclu), "yeni_guven": yeni, "dustu": yeni < cevap.guven})
    a = _oran([s["dustu"] for s in silmeler])

    yol_varliklari = set()
    for e in kokler:
        ozne, _iliski, nesne = havuz.kayit(e).uclu
        yol_varliklari.update((ozne, nesne))
    en_buyuk = max(v for s, _r, o, _g in olgular for v in (s, o))
    yeni_ozne, yeni_nesne = en_buyuk + 1, en_buyuk + 2  # V-038: bölümde olmayan ilk iki varlık kimliği
    degisiklikler = []
    for i, k in enumerate(epitoplar):
        s, r, o = k.uclu
        if s in yol_varliklari or o in yol_varliklari:
            continue
        yedek = (yeni_ozne, r, yeni_ozne if s == o else yeni_nesne)
        _s, _r, _o, guven = olgular[i]
        degismis = list(olgular)
        degismis[i] = yedek + (guven,)
        yeni = _yeniden_cevapla(degismis, hucreler, kk, prm, iliski_semasi, sorgu, defter)
        degisiklikler.append({"epitop": k.kimlik, "uclu": list(k.uclu), "yedek": list(yedek),
                              "ayni": (yeni.iliski, yeni.guven) == (cevap.iliski, cevap.guven)})
    sinanamadi = not degisiklikler
    b = None if sinanamadi else _oran([d["ayni"] for d in degisiklikler])

    ters = cevapla(havuz, (sorgu[1], sorgu[0]), defter)
    adaylar = iliski_semasi.ters(cevap.iliski)
    tanimsiz = not adaylar or (ters.iliski is not None and not iliski_semasi.ters(ters.iliski))  # V-038
    ters_tutarli = ters.iliski is None or tanimsiz or ters.iliski in adaylar
    celiski_var = any(defter.celiskiye_karisti(k) for k in _koken_alt_grafi(havuz, ispatlar))
    c = 1 if ters_tutarli and not celiski_var else 0

    puan = None if sinanamadi else a * b * c
    sonuc = MudahaleSonucu(tuple(sorgu), cevap.iliski, cevap.guven, tuple(silmeler), a, tuple(degisiklikler), b,
                           sinanamadi, ters.iliski, ters_tutarli, celiski_var, c, puan,
                           SINANAMADI if sinanamadi else PUANLI)
    return _kaydet(defter, sonuc)


def _kaydet(defter, sonuc):
    defter.ekle(MUDAHALE, KAYNAK, {"sorgu": list(sonuc.sorgu), "cevap": sonuc.cevap, "a": sonuc.a, "b": sonuc.b,
                                   "c": sonuc.c, "puan": sonuc.puan, "durum": sonuc.durum,
                                   "silme_sayisi": len(sonuc.silmeler), "degisiklik_sayisi": len(sonuc.degisiklikler)})
    return sonuc


def mudahale_ozeti(sonuclar):
    """H1 raporu için: sınanamadı ve cevapsız sorular ayrı sayılır, ortalama yalnız puanlı sorulardan (K-021)."""
    puanlilar = [s.puan for s in sonuclar if s.durum == PUANLI]
    return {"toplam": len(sonuclar), "puanli": len(puanlilar),
            "sinanamadi": sum(1 for s in sonuclar if s.durum == SINANAMADI),
            "cevapsiz": sum(1 for s in sonuclar if s.durum == CEVAPSIZ),
            "ortalama_puan": sum(puanlilar) / len(puanlilar) if puanlilar else None}
