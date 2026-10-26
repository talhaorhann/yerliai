"""sistem.md §13, §18; K-041, K-043 (ÖK-005 taslağı §4 madde 15–18 ve 21; §8), V-065: B2 ölçümü ve Goodhart makası.

Hedef kurallar (DNA v8) yalnız bu ölçümde ve sınıflamada kullanılır; arama, kalibrasyon ve sıralamaya girmez. Ölçüm
yalnız final havuzunda ve bir kez yapılır (B2b); B2a duman testidir ve geliştirme havuzunda ölçülür (V-065).
Maske: f ve, değerlendirilen kural ters-dayanaklı değilse, f'nin (gözlenen) tersleri. Kümeye uygulanan ölçülerde her
kural kendi maskesini görmez (V-065); kapanış-eşdeğerde kabul kümesine hedef kuralın maskesi uygulanır.
- Hedef kuralın sınıfı (öncelik sırası): özdeş (aynı kanonik kimlik, kabul ya da uyutulmuş) → daha genel (kabul
  kümesinde onu θ-kapsayan ve finalde yanlışsız kural) → finalde örneği yok (gövde 24 dünyanın hiçbirinde eşleşmiyor) →
  kapanış-eşdeğer (hedefin maskeli olgudan yeniden türettiği her olguyu kabul kümesi aynı maskeyle en çok 8 turda
  türetir) → bulunamadı.
- Kabul edilenin sınıfı: bozuk (kapsamındaki bir ailenin final dünyasında yanlış tahmin) → özdeş → daha genel →
  farklı-doğru; uyutulanlar fazlalık-doğru.
- Bilmiyorum ölçüsü: final dünyalarında her olgu maskelenir; kümenin türettiği olgulardan biri dünyada yoksa yanlış,
  değilse maskelenen olgu türetildiyse doğru, değilse bilmiyorum.
- Kapı (madde 16–18): geri bulma = (özdeş + daha genel + kapanış-eşdeğer) / 244; kümeli Wilson (küme = hedefin sonuç
  ilişkisi); yanlış kabul = bozuk / kabul, Clopper–Pearson tek yanlı üst sınır; bilmiyorum farkı.
- Makas (madde 21): ölçü kapanış geri bulmasıdır (bilmiyorum ölçüsündeki doğru oranı); sorgulanan taraf turlarda yanan
  taze dünyalar, kontrol tarafı kontrol havuzu; her taraftaki bütün olgular (≥ en_az_olgu); fark için dünya kümeli
  bootstrap alt sınırı > tetik → arama donar. Bootstrap tohumu `makas|<basamak>|<tur>` (V-065).
"""
from cekirdek.altyapi.kanonik import kanonik_json, ozet
from cekirdek.bellek_gecidi import kanonik_bicim
from degerlendirme import h2_gecit as G
from degerlendirme import istatistik, kural
from kesif import tohum

ALGORITMA = "sha256"  # V-007
OZDES, GENEL, ORNEKSIZ, KAPANIS, BULUNAMADI = "ozdes", "daha_genel", "finalde_ornegi_yok", "kapanis_esdeger", "bulunamadi"
BOZUK, FARKLI_DOGRU, FAZLALIK = "bozuk", "farkli_dogru", "fazlalik_dogru"
DOGRU, YANLIS, BILMIYORUM = "dogru", "yanlis", "bilmiyorum"
GECTI, ARA_BOLGE, DUR = "GECTI", "ARA_BOLGE", "DUR"  # ÖK-005 taslağı §4 madde 16–18


def kanonik(k):
    return ozet(kanonik_json(kanonik_bicim(G.hucre(k, "kanonik", _KIMLIKSIZ))), ALGORITMA)


class _Kimliksiz:
    halka_esigi = guvenilirlik = None


_KIMLIKSIZ = _Kimliksiz()


def dna_kurali(hucre):
    return kural.Kural([(h.gen, h.sol, h.sag) for h in hucre.halkalar], tuple(hucre.sonuc), hucre.farkli, hucre.kimlik)


def maske(sema, olgu_kumesi, f, k):
    return G._maske(k, sema, olgu_kumesi, f)


def yanlissiz_mi(k, dunyalar):
    """`dunyalar`: [(aile, Indeks)]."""
    return all((a, k.bas[0], b) in idx.olgu for _, idx in dunyalar for a, b in k.tahminler(idx))


def ornegi_var_mi(k, dunyalar):
    return any(next(k.baglamalar(idx), None) is not None for _, idx in dunyalar)


def kapanis_esdeger_mi(hedef, kume, dunyalar, sema, tur):
    """Hedefin maskeli olgudan yeniden türettiği her olguyu küme aynı maskeyle türetiyor mu (en az bir olgu olmalı)."""
    r, sayi = hedef.bas[0], 0
    for _, idx in dunyalar:
        for f in sorted((o for o in idx.olgu if o[1] == r), key=repr):
            a, _, b = f
            m = maske(sema, idx.olgu, f, hedef)
            if f not in kural.cift_kapanisi([hedef], idx, a, b, tur, m):
                continue
            sayi += 1
            if f not in kural.cift_kapanisi(kume, idx, a, b, tur, m):
                return False
    return sayi > 0


def hedef_siniflari(hedefler, kabul, uyuyan, dunyalar, sema, tur):
    """`hedefler`: {kimlik: Kural}; `kabul`, `uyuyan`: {kimlik: Kural}. Dönüş: {hedef kimliği: sınıf}."""
    kanonikler = {kanonik(k) for k in list(kabul.values()) + list(uyuyan.values())}
    yanlissiz = {kim: yanlissiz_mi(k, dunyalar) for kim, k in kabul.items()}
    kume = list(kabul.values())
    sonuc = {}
    for kim, d in sorted(hedefler.items()):
        if kanonik(d) in kanonikler:
            sonuc[kim] = OZDES
        elif any(yanlissiz[a] and kural.kapsar_mi(k, d) for a, k in kabul.items()):
            sonuc[kim] = GENEL
        elif not ornegi_var_mi(d, dunyalar):
            sonuc[kim] = ORNEKSIZ
        elif kapanis_esdeger_mi(d, kume, dunyalar, sema, tur):
            sonuc[kim] = KAPANIS
        else:
            sonuc[kim] = BULUNAMADI
    return sonuc


def kabul_siniflari(kabul, kapsamlar, uyuyan, hedefler, dunyalar):
    """`kapsamlar`: {kimlik: [aile]} (geçidin KABUL nedeni). Bozuk: kapsamındaki ailelerin final dünyasında yanlış."""
    hedef_kanonik = {kanonik(d) for d in hedefler.values()}
    sonuc = {kim: FAZLALIK for kim in uyuyan}
    for kim, k in sorted(kabul.items()):
        kendi = [(a, idx) for a, idx in dunyalar if a in kapsamlar[kim]]
        if not yanlissiz_mi(k, kendi):
            sonuc[kim] = BOZUK
        elif kanonik(k) in hedef_kanonik:
            sonuc[kim] = OZDES
        elif any(kural.kapsar_mi(k, d) for d in hedefler.values()):
            sonuc[kim] = GENEL
        else:
            sonuc[kim] = FARKLI_DOGRU
    return sonuc


def olgu_olcusu(kume, idx, sema, tur):
    """Bir dünyanın her olgusu için doğru / yanlış / bilmiyorum sayıları."""
    sayi = {DOGRU: 0, YANLIS: 0, BILMIYORUM: 0}
    for f in sorted(idx.olgu, key=repr):
        a, _, b = f
        turetilen = kural.cift_kapanisi(kume, idx, a, b, tur, maske=lambda k: maske(sema, idx.olgu, f, k))
        if any(t not in idx.olgu for t in turetilen):
            sayi[YANLIS] += 1
        elif f in turetilen:
            sayi[DOGRU] += 1
        else:
            sayi[BILMIYORUM] += 1
    return sayi


def aileye_gore(dunya_olculeri, aileler):
    """Dünya başına sayılar → aile başına sayılar ve kapanış geri bulması (doğru / toplam)."""
    sonuc = {}
    for o, aile in zip(dunya_olculeri, aileler):
        s = sonuc.setdefault(aile, {DOGRU: 0, YANLIS: 0, BILMIYORUM: 0})
        for a in s:
            s[a] += o[a]
    for s in sonuc.values():
        s["toplam"] = s[DOGRU] + s[YANLIS] + s[BILMIYORUM]
        s["geri_bulma"] = s[DOGRU] / s["toplam"] if s["toplam"] else 0.0
    return sonuc


def bilmiyorum_olcusu(kume, dunyalar, sema, tur):
    dunya = [olgu_olcusu(kume, idx, sema, tur) for _, idx in dunyalar]
    toplam = {a: sum(d[a] for d in dunya) for a in (DOGRU, YANLIS, BILMIYORUM)}
    n = sum(toplam.values())
    return {"dunyalar": dunya, **toplam, "toplam": n, "bilmiyorum_orani": toplam[BILMIYORUM] / n if n else 0.0}


def b2_karari(hedef_sinif, hedefler, kabul_sinif, bilmiyorum_kume, bilmiyorum_hedef, h2, z):
    k = h2.deger("b2_kapi")
    if len(hedefler) != k["hedef_sayisi"]:
        raise ValueError("hedef sayısı önkayıttakiyle aynı değil")
    bulunan = {kim for kim, s in hedef_sinif.items() if s in (OZDES, GENEL, KAPANIS)}
    nokta = len(bulunan) / len(hedefler)
    kumeler = {}
    for kim, d in hedefler.items():
        x, m = kumeler.get(d.bas[0], (0, 0))
        kumeler[d.bas[0]] = (x + (kim in bulunan), m + 1)
    kumeli = istatistik.kumeli_wilson_alt(sorted(kumeler.values()), z)
    kabuller = [s for s in kabul_sinif.values() if s != FAZLALIK]
    bozuk = sum(s == BOZUK for s in kabuller)
    cp_ust = istatistik.clopper_pearson(bozuk, len(kabuller), 1 - 2 * (1 - k["cp_guven"]))[1] if kabuller else 1.0  # K-041: tek yanlı %95 = iki yanlı %90
    fark = bilmiyorum_kume["bilmiyorum_orani"] - bilmiyorum_hedef["bilmiyorum_orani"]
    sartlar = {"geri_bulma": nokta >= k["geri_bulma"], "kumeli_wilson": kumeli >= k["kumeli_wilson"],
               "yanlis_kabul": cp_ust <= k["cp_ust"], "bilmiyorum": fark <= k["bilmiyorum_farki"]}
    if nokta < k["ara_bolge_alt"]:
        karar = DUR
    elif all(sartlar.values()):
        karar = GECTI
    else:
        karar = ARA_BOLGE
    say = {s: sum(v == s for v in hedef_sinif.values()) for s in (OZDES, GENEL, KAPANIS, ORNEKSIZ, BULUNAMADI)}
    return {"karar": karar, "sartlar": sartlar, "geri_bulma": nokta, "bulunan": len(bulunan),
            "bicimce": (say[OZDES] + say[GENEL]) / len(hedefler), "kumeli_wilson": kumeli, "kume_sayisi": len(kumeler),
            "kabul": len(kabuller), "bozuk": bozuk, "cp_ust": cp_ust, "bilmiyorum_farki": fark, "siniflar": say}


def makas(kume, sorgulanan, kontrol, sema, tur, h2, basamak, tur_no):
    """Taraf: [(aile, Indeks)]. Dönüş: ölçü, aralık ve tetik."""
    m = h2.deger("makas")

    def kumeler(dunyalar):
        return [(o[DOGRU], o[DOGRU] + o[YANLIS] + o[BILMIYORUM]) for o in (olgu_olcusu(kume, idx, sema, tur)
                                                                            for _, idx in dunyalar)]
    s, k = kumeler(sorgulanan), kumeler(kontrol)
    n_s, n_k = sum(x[1] for x in s), sum(x[1] for x in k)
    if min(n_s, n_k) < m["en_az_olgu"]:
        return {"yeterli": False, "sorgulanan_olgu": n_s, "kontrol_olgu": n_k, "tetik": False}
    alt, ust = istatistik.kumeli_bootstrap_fark(s, k, m["bootstrap"], m["guven"],
                                                tohum.tohum(h2, "makas", basamak, tur_no))
    oran = lambda c: sum(x for x, _ in c) / sum(n for _, n in c)  # noqa: E731
    return {"yeterli": True, "sorgulanan_olgu": n_s, "kontrol_olgu": n_k, "sorgulanan": oran(s), "kontrol": oran(k),
            "alt": alt, "ust": ust, "yari_genislik": (ust - alt) / istatistik.KUYRUK, "tetik": alt > m["tetik"]}
