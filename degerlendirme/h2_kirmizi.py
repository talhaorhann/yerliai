"""sistem.md §13, §18; K-041, K-043 (ÖK-005 taslağı §4 madde 19, görünür aileler tablosu; §5 `kirmizi|<aile>|<i>`), V-065:
kırmızı takım.

Görünür aileler (kodlayıcı yazar, DNA kullanılmaz; her aile `kirmizi_aile_basina` mutant, tohum `kirmizi|<aile>|<i>`):
- G1 bozuk sonuç: M0 listesinden tohumla seçilen adayın baş ilişkisi, aynı dışlayıcı gruptan tohumla seçilen başka bir
  ilişkiyle değiştirilir.
- G2 aşırı genel: M0 listesinden tohumla seçilen ≥2 halkalı adaydan tohumla bir halka silinir; kalan kural bağlı, X ile
  Y'yi içeren ve geliştirme havuzunda yanlış > 0 olmalı (değilse sonraki çekiliş).
- G3 kapsam artefaktı: ilk ailede (A1) yanlış 0 ve tanık ≥ en_az_tanik, öteki ailelerin birinde yanlış > 0 olan T
  adayları (şablon sayacıyla bulunur) arasından tohumla seçilir.
- G4 gizli ters: t(Z,X) ∧ s(Z,W) ∧ s(W,Y) → r(X,Y); t ∈ ters(r), ters(t) birden çok, s simetrik ve işlevsel; OI kapalı.
  Şemadan çıkan bütün üçlüler sıralanır, tohumla seçilir; 40'tan azsa hepsi alınır, eksik G1'den (sıra 41'den) doldurulur.
Aynı kanonik kimlik bir kez alınır (yinelenirse aynı üreteçle yeni çekiliş).
Gizli aileler (danışman): dosya yalnız `kesif.aday` denetiminden geçer; içerik yazdırılmaz. Sayım yalnız aile başına sayı
döner (aile adı da dönmez; aileler adlarının sırasıyla 1..n diye anılır): kural, geliştirme havuzunda yanlış veren ve
hiç tahmin üretmeyen.
"""
import json
import random
from pathlib import Path

import numpy as np

from degerlendirme.h2_gecit import bagli_mi
from kesif import aday as ad
from degerlendirme import kural
from kesif import m0, sablon, tohum

KIRMIZI = "kirmizi"  # ÖK-005 taslağı §5
G2_EN_AZ_HALKA = 2  # K-041: G2 ≥2 halkalı adaylardan
DENEME_SINIRI = 100000  # V-065: bir mutant için en çok çekiliş (aşılırsa üretim durur ve bildirilir)


class UretimHatasi(RuntimeError):
    pass


def _cekilisler(aile, i):
    for _ in range(DENEME_SINIRI):
        yield
    raise UretimHatasi(f"{aile} mutantı {i} üretilemedi")
GORUNUR, GIZLI = ad.KIRMIZI_TURLERI
ALGORITMA = "sha256"  # V-007


def _kayit(halkalar, bas, oi, farkli, aile, tohum_degeri, ust):
    gen, sol, sag = bas
    k = {"sema_surumu": "1", "kimlik": "x", "halkalar": [{"gen": r, "sol": s, "sag": a} for r, s, a in halkalar],
         "sonuc": {"gen": gen, "sol": sol, "sag": sag}, "farkli": [] if oi else sorted(sorted(c) for c in farkli),
         "oi": oi, "kaynak": {"tur": GORUNUR, "aile": aile, "tohum": tohum_degeri, "ust": ust}, "tanik_ozeti": None,
         "surum": 1}
    k["kimlik"] = "k" + ad.kanonik_kimlik(k, ALGORITMA)
    return k


def _parca(kayit):
    halkalar = [(h["gen"], h["sol"], h["sag"]) for h in kayit["halkalar"]]
    s = kayit["sonuc"]
    return halkalar, (s["gen"], s["sol"], s["sag"])


def _bas_govdede(halkalar, bas):
    return tuple(bas) in set(halkalar)


class M0Listesi:
    """M0 aday satırları (bayt); yalnız seçilenler çözülür."""

    def __init__(self, satirlar):
        self.satirlar = satirlar

    @classmethod
    def dosyadan(cls, yol):
        return cls(Path(yol).read_bytes().splitlines())

    def __len__(self):
        return len(self.satirlar)

    def __getitem__(self, i):
        return json.loads(self.satirlar[i])["aday"]


def g1(m0_listesi, sema, h2, sayi, ilk=1, gorulen=None):
    gorulen = set() if gorulen is None else gorulen
    sonuc = []
    for i in range(ilk, ilk + sayi):
        t = tohum.tohum(h2, KIRMIZI, "G1", i)
        rng = random.Random(t)
        for _ in _cekilisler("G1", i):
            ust = m0_listesi[rng.randrange(len(m0_listesi))]
            halkalar, bas = _parca(ust)
            secenek = sorted(r for r in sema.adlar if r != bas[0] and sema.dislayici_mi(r, bas[0]))
            if not secenek:
                continue
            yeni = (rng.choice(secenek), *bas[1:])
            if _bas_govdede(halkalar, yeni):
                continue
            k = _kayit(halkalar, yeni, ust["oi"], ust["farkli"], "G1", t, [ust["kimlik"]])
            if k["kimlik"] not in gorulen:
                break
        gorulen.add(k["kimlik"])
        sonuc.append(k)
    return sonuc


def _gelistirmede_yanlis(k, gelistirme):
    r = k.bas[0]
    return sum((a, r, b) not in idx.olgu for _, _, idx in gelistirme for a, b in k.tahminler(idx))


def g2(m0_listesi, gelistirme, h2, sayi, gorulen=None):
    """`gelistirme`: [(etiket, dünya, Indeks)]."""
    gorulen = set() if gorulen is None else gorulen
    sonuc = []
    for i in range(1, sayi + 1):
        t = tohum.tohum(h2, KIRMIZI, "G2", i)
        rng = random.Random(t)
        for _ in _cekilisler("G2", i):
            ust = m0_listesi[rng.randrange(len(m0_listesi))]
            halkalar, bas = _parca(ust)
            if len(halkalar) < G2_EN_AZ_HALKA:
                continue
            sil = rng.randrange(len(halkalar))
            kalan = halkalar[:sil] + halkalar[sil + 1:]
            degisken = {d for _, a, b in kalan for d in (a, b)}
            if not set(bas[1:]) <= degisken or _bas_govdede(kalan, bas):
                continue
            farkli = [c for c in ust["farkli"] if set(c) <= degisken]
            k = _kayit(kalan, bas, ust["oi"], farkli, "G2", t, [ust["kimlik"]])
            kk = kural.Kural.kayittan(k)
            if k["kimlik"] in gorulen or not bagli_mi(kk) or _gelistirmede_yanlis(kk, gelistirme) == 0:
                continue
            break
        gorulen.add(k["kimlik"])
        sonuc.append(k)
    return sonuc


def g3_listesi(dunyalar, iliski_adlari, h2, govdeler):
    """(gövde sırası, baş, OI) üçlüleri: ilk ailede yanlış 0 ve tanık ≥ en_az_tanik, öteki ailelerin birinde yanlış > 0."""
    aileler, toplam = m0._topla(dunyalar, govdeler, iliski_adlari, h2.deger("sayac_parca_boyu"))
    ana, digerleri = aileler[0], aileler[1:]  # K-041: G3 tanımında ilk aile (A1)
    en_az = h2.deger("m0_en_az_tanik")
    x, y = tuple(h2.deger("sablon_degiskenleri"))[:sablon.BAS]
    liste = []
    for oi, (t_i, d_i) in ((False, ("tahmin", "dogru")), (True, ("tahmin_oi", "dogru_oi"))):
        T, D = toplam[ana][t_i], toplam[ana][d_i]
        uygun = (T[:, None] - D == 0) & (D >= en_az)
        yanlis_baska = np.zeros_like(uygun)
        for a in digerleri:
            yanlis_baska |= toplam[a][t_i][:, None] - toplam[a][d_i] > 0
        for i, bas in zip(*np.nonzero(uygun & yanlis_baska)):
            g = govdeler[i]
            if (bas, x, y) in g or (oi and not sablon.oi_anlamli_mi(g)):
                continue
            liste.append((int(i), int(bas), oi))
    return liste


def g3(liste, govdeler, iliski_adlari, h2, sayi, gorulen=None):
    gorulen = set() if gorulen is None else gorulen
    degiskenler = tuple(h2.deger("sablon_degiskenleri"))
    sonuc = []
    for i in range(1, sayi + 1):
        t = tohum.tohum(h2, KIRMIZI, "G3", i)
        rng = random.Random(t)
        for _ in _cekilisler("G3", i):
            gi, bas, oi = liste[rng.randrange(len(liste))]
            ham = sablon.aday_kaydi(govdeler[gi], bas, oi, iliski_adlari, degiskenler)
            halkalar, b = _parca(ham)
            k = _kayit(halkalar, b, oi, [], "G3", t, [])
            if k["kimlik"] not in gorulen:
                break
        gorulen.add(k["kimlik"])
        sonuc.append(k)
    return sonuc


def g4_uclari(sema):
    return sorted((r, t, s) for r in sema.adlar for t in sema.ters(r) if len(sema.ters(t)) > 1
                  for s in sema.adlar if sema.simetrik(s) and sema.islevsel(s))


def g4(sema, h2, sayi, gorulen=None):
    """Dönüş: (G4 mutantları, eksik sayısı)."""
    gorulen = set() if gorulen is None else gorulen
    kalan = g4_uclari(sema)
    sonuc = []
    for i in range(1, min(sayi, len(kalan)) + 1):
        t = tohum.tohum(h2, KIRMIZI, "G4", i)
        r, tt, s = kalan.pop(random.Random(t).randrange(len(kalan)))
        k = _kayit([(tt, "Z", "X"), (s, "Z", "W"), (s, "W", "Y")], (r, "X", "Y"), False, [], "G4", t, [])
        gorulen.add(k["kimlik"])
        sonuc.append(k)
    return sonuc, sayi - len(sonuc)


def gorunur(m0_listesi, gelistirme, g3_liste, govdeler, sema, h2):
    """Dört görünür aile; G4 eksiği G1'den doldurulur. Dönüş: (mutantlar, aile başına sayılar)."""
    n = h2.deger("kirmizi_aile_basina")
    gorulen = set()
    a1 = g1(m0_listesi, sema, h2, n, gorulen=gorulen)
    a2 = g2(m0_listesi, gelistirme, h2, n, gorulen=gorulen)
    a3 = g3(g3_liste, govdeler, tuple(sema.adlar), h2, n, gorulen=gorulen)
    a4, eksik = g4(sema, h2, n, gorulen=gorulen)
    dolgu = g1(m0_listesi, sema, h2, eksik, ilk=n + 1, gorulen=gorulen)
    hepsi = a1 + a2 + a3 + a4 + dolgu
    sayilar = {"G1": len(a1) + len(dolgu), "G2": len(a2), "G3": len(a3), "G4": len(a4), "G4_eksigi_G1den": eksik}
    return hepsi, sayilar


def gizli_yukle(yol, iliski_adlari, h2):
    """Gizli dosyayı yalnız denetimden geçirip kayıtları döndürür (yazdırılmaz)."""
    veri = json.loads(Path(yol).read_bytes().decode("utf-8"))
    ad.kirmizi_dosyasi_denetle(veri, iliski_adlari, GIZLI, h2.deger("kirmizi_gizli_aile_sayisi"),
                               h2.deger("kirmizi_aile_basina"), h2.deger("kirmizi_gorunur_aileler"))
    return veri["adaylar"]


def gelistirme_sayimi(kayitlar, gelistirme):
    """Aile başına (adların sırasıyla 1..n): kural sayısı, geliştirme havuzunda yanlış veren, hiç tahmin üretmeyen.
    Dönüş yalnız sayılardır; ayrıca etkin (yanlış veren) kayıtların listesi ayrı döner (yazdırılmaz)."""
    aileler = sorted({k["kaynak"]["aile"] for k in kayitlar})
    sayim = {i: {"kural": 0, "yanlis": 0, "tetiklenmedi": 0} for i in range(1, len(aileler) + 1)}
    etkin = []
    for k in kayitlar:
        s = sayim[aileler.index(k["kaynak"]["aile"]) + 1]
        kk = kural.Kural.kayittan(k)
        tahmin = sum(len(kk.tahminler(idx)) for _, _, idx in gelistirme)
        yanlis = _gelistirmede_yanlis(kk, gelistirme)
        s["kural"] += 1
        s["yanlis"] += yanlis > 0
        s["tetiklenmedi"] += tahmin == 0
        if yanlis > 0:
            etkin.append(k)
    return sayim, etkin


def main(arg):
    """Gizli dosyanın geliştirme havuzundaki sayımı: yalnız aile sırası ve sayılar yazılır (K-043 adım 3)."""
    import sys
    from degerlendirme import h2_tur
    kok = Path(__file__).resolve().parents[1]
    ortam, _ = h2_tur.ortam_kur(h2_tur.Kurulum(str(kok)))
    kayitlar = gizli_yukle(arg[0], frozenset(ortam.sema.adlar), ortam.h2)
    sayim, _ = gelistirme_sayimi(kayitlar, ortam.gelistirme)
    sys.stdout.write(json.dumps({"aile_basina": sayim}, ensure_ascii=False) + "\n")  # V-057: yalnız sayılar
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
