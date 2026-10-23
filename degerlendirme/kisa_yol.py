"""sistem.md §10, KODLAMA_PROMPTU §6, K-008: kelime çantası kısa yol dedektörü ve kapısı (V-018).

Dedektör yapıya bakmaz: yalnız olgulardaki ilişki adı sayıları ve kişi kimlikleri ("isim").
"""
import math
from collections import Counter

YOK = "-"  # V-018: "cevap yok" sınıfının iç adı (ilişki adı deseni tire içermez)


class KisaYolHatasi(RuntimeError):
    pass


def ozellikler(bolum):
    jetonlar = []
    for o in bolum["olgular"]:
        jetonlar += ["r:" + o["iliski"], f"e:{o['ozne']}", f"e:{o['nesne']}"]
    jetonlar += [f"q:{bolum['sorgu']['ozne']}", f"q:{bolum['sorgu']['nesne']}"]
    return jetonlar


def _sinif(etiket):
    return YOK if etiket is None else etiket


class NaiveBayes:
    """Çok terimli Naive Bayes, Laplace düzeltmeli. Eşitlikte sözlük sırasında ilk sınıf seçilir."""

    def __init__(self, laplace):
        self.laplace = laplace

    def egit(self, ozellik_listeleri, etiketler):
        self.sinif_sayisi = Counter(_sinif(e) for e in etiketler)
        self.toplam = len(etiketler)
        self.jeton_sayisi = {c: Counter() for c in self.sinif_sayisi}
        for oz, e in zip(ozellik_listeleri, etiketler):
            self.jeton_sayisi[_sinif(e)].update(oz)
        self.sozluk = set()
        for sayac in self.jeton_sayisi.values():
            self.sozluk.update(sayac)
        self.sinif_toplami = {c: sum(s.values()) for c, s in self.jeton_sayisi.items()}

    def tahmin(self, ozellikler_):
        sayac = Counter(j for j in ozellikler_ if j in self.sozluk)
        payda_ek = self.laplace * len(self.sozluk)
        en_iyi, en_iyi_puan = None, None
        for c in sorted(self.sinif_sayisi):
            puan = math.log(self.sinif_sayisi[c] / self.toplam)
            payda = self.sinif_toplami[c] + payda_ek
            for j in sorted(sayac):
                puan += sayac[j] * math.log((self.jeton_sayisi[c][j] + self.laplace) / payda)
            if en_iyi_puan is None or puan > en_iyi_puan:
                en_iyi, en_iyi_puan = c, puan
        return None if en_iyi == YOK else en_iyi


def sans(etiketler):
    """K-008: şans = en sık cevabın oranı."""
    sayac = Counter(_sinif(e) for e in etiketler)
    return max(sayac.values()) / len(etiketler)


def kapi_olc(bolumler, cevaplar, laplace):
    """İlk yarıda sıfırdan eğitilen dedektörün ikinci yarıdaki doğruluğu ve o yarının şansı."""
    yari = len(bolumler) // 2  # K-008: ilk yarıda eğit, ikinci yarıda ölç
    nb = NaiveBayes(laplace)
    nb.egit([ozellikler(b) for b in bolumler[:yari]], [c["cevap"] for c in cevaplar[:yari]])
    etiketler = [c["cevap"] for c in cevaplar[yari:]]
    dogru = sum(1 for b, e in zip(bolumler[yari:], etiketler) if nb.tahmin(ozellikler(b)) == e)
    return dogru / len(etiketler), sans(etiketler)


def kapi_denetle(bolumler, cevaplar, laplace, pay):
    dogruluk, sans_ = kapi_olc(bolumler, cevaplar, laplace)
    if dogruluk > sans_ + pay:
        raise KisaYolHatasi(f"kelime çantası dedektörü {dogruluk:.3f} > şans {sans_:.3f} + {pay}: üretim durdu")
    return dogruluk, sans_
