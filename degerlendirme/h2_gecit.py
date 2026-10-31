"""sistem.md §8, §10, §13, §18; K-041, K-043 (ÖK-005 taslağı §4 madde 4–14, §7, §13), V-065: H2 kabul geçidi.

Ucuzdan pahalıya; hepsi geçmeden KABUL yok. Önericiye yalnız hüküm (KABUL / RET / BİLMİYORUM) döner; ölçümler ve neden
denetçi kanalına (koşu dosyalarına) yazılır. Ölçüm ilk düşen aşamada durur; hüküm ölçümlerden aynı sırayla okunur.
1–3. Geliştirme havuzu (sembolik, kapalı dünya): yanlış 0 (kongrüans, işlevsellik ve ters ihlalleri kapalı dünyada
     yanlışın altkümesidir); obiter yok (bir halkası ya da farklılık şartları çıkarılmış kural da yanlış 0 ve en az aynı
     tanıkla geçiyorsa aday aşama 5'e gitmez, indirgenmiş kurallar sıraya girer); yol-kesme maskesiyle tanık ≥ en_az_tanik.
4.   Yeniden bağlı ikiz (geliştirme havuzu): yalnız baş ilişkisi derece koruyarak yeniden bağlanınca da tanık ≥
     en_az_tanik ve yanlış 0 → BİLMİYORUM. π-ikizi çekirdek adımında ölçülür (sembolik sayım adlardan bağımsızdır).
5.   Taze dünyalar (turun dünyaları: ailede `taze_aile_basina`, dünyada `bolum_sayisi` gövde-merkezli bölüm):
     - sembolik: ailede yanlış > 0 → o aile veto (≥ ret_aile_sayisi aile → RET, bir aile → BİLMİYORUM); kapsam ≥
       kapsam_en_az_aile; bölüm-düzeyi Wilson Thresholdout'la ≥ τ (T_gel: geliştirme havuzunda aynı biçimde, ailede ilk
       `taze_aile_basina` dünya); Westfall–Young düzeltilmiş p ≤ fwer / tur sınırı (aile: turda kapsamı geçenler);
     - çekirdek (bellek boş, V-065): her bölümde maskesiz koşu ve baş ilişkisindeki her gözlem için maskeli koşu;
       doğru = maskelenen gözlem adayın soyunca yeniden türetildi; yanlış = soyun gözlenmemiş tahmini ya da şema
       çelişkisi (kapalı dünya); müdahale b·c (K-037), en az `mudahale_en_az_kanit` ölçüm. Uyum: her bölümde çekirdek
       (doğru, yanlış) = sembolik. Olguları çekirdek havuzuna sığmayan bölüm (V-031) ölçülemez: uyum yok. π-ikizi: geliştirme bölümlerinde (dünya başına bir, en çok `pi_bolum_sayisi`)
       çekirdek sayıları ve müdahale hükmü π'li kopyayla aynı.
Sembolik doğru (ÖK-005 taslağı §13.2, tanık): maskelenen (A, r, B) için gövdenin, maske (yol-kesme maskesi) çıkarılmış
olgular üzerinde X → A, Y → B eşleşmesi var mı (tek adım; kuralın kendi türettiği olgu kullanılmaz, V-065).
"""
import dataclasses
import random

from cekirdek.bellek_gecidi import maskeli_kos
from cekirdek.havuz import HavuzHatasi
from cekirdek.dna import Halka, Hucre, Sonuc
from degerlendirme import h2_bagla, h2_bolum, h2_ikiz, istatistik, kural
from kesif import tohum

KABUL, RET, BILMIYORUM = "KABUL", "RET", "BİLMİYORUM"  # ÖK-005 taslağı §7
GOZLEM_GUVENI = 1.0  # V-017: gözlem güveni tam


@dataclasses.dataclass(frozen=True)
class Sabitler:
    """ÖK-005'te donan sayılar (config_h2 `gecit_sabitleri`); testler küçük değerlerle kurar."""
    en_az_tanik: int
    kapsam_en_az_aile: int
    ret_aile_sayisi: int
    wilson_z: float
    fwer: float
    tur_siniri: int
    wy_cekilis: int
    bolum_sayisi: int
    taze_aile_basina: int
    adim_araligi: tuple
    dikkat_sayisi: int
    pi_bolum_sayisi: int
    mudahale_en_az_kanit: int
    kapanis_tur_siniri: int
    bagla_deneme_carpani: int
    halka_esigi: float
    guvenilirlik: float

    @classmethod
    def ayardan(cls, h2):
        d = {**h2.deger("gecit_sabitleri"), **h2.deger("gecit_secimleri")}
        d["adim_araligi"] = tuple(d["adim_araligi"])
        return cls(**d, tur_siniri=h2.deger("sorgu_tur_siniri"), bagla_deneme_carpani=h2.deger("bagla_deneme_carpani"),
                   halka_esigi=h2.deger("aday_halka_esigi"), guvenilirlik=h2.deger("aday_guvenilirligi"))

    @property
    def alfa(self):
        return self.fwer / self.tur_siniri


@dataclasses.dataclass(frozen=True)
class Esikler:
    """K değerleri (ÖK-005 taslağı §4 madde 9, 10, 12): B1'de kalibre edilir."""
    tau: float
    mudahale: float
    T: float
    sigma: float

    @classmethod
    def sozlukten(cls, d):
        return cls(d["tau"], d["mudahale"], d["T"], d["sigma"])


@dataclasses.dataclass
class Ortam:
    sema: object
    temel: tuple
    sabit: Sabitler
    h2: object  # tohum öneki için ayar
    gelistirme: list  # [(etiket, dunya, Indeks)], havuz sırasıyla
    bijeksiyonlar: list = None
    kk: object = None
    prm: object = None
    gunluk: dict = None


def dunya_kaydi(etiket, d):
    """Taze dünya kaydı: (etiket, aile, dünya, indeks)."""
    return etiket, d.aile, d, kural.Indeks(d.olgular)


def _tohum(ortam, ad, dunya_etiketi, *parcalar):
    """ÖK-005 taslağı §5: `<ad>|<dünya etiketi>|...`; dünya etiketi kendi parçalarıyla iç içe yazılır."""
    return tohum.tohum(ortam.h2, ad, *dunya_etiketi.split(tohum.AYIRICI), *parcalar)


def _ters_olgular(sema, olgu_kumesi, f):
    a, r, b = f
    return {(b, t, a) for t in sema.ters(r)} & olgu_kumesi


def _maske(k, sema, olgu_kumesi, f):
    """Yol-kesme maskesi (ÖK-005 taslağı §7): f ve, aday ters-dayanaklı değilse, f'nin gözlenen tersleri."""
    return frozenset({f} | (set() if k.ters_dayanakli else _ters_olgular(sema, olgu_kumesi, f)))


def kural_ozu(k):
    return {"halkalar": [list(h) for h in k.halkalar], "bas": list(k.bas), "farkli": sorted(sorted(c) for c in k.farkli)}


def ozunden(o):
    return kural.Kural([tuple(h) for h in o["halkalar"]], tuple(o["bas"]), o["farkli"])


# ---- aşama 1–3: geliştirme havuzu ----

def gelistirme_sayilari(k, ortam, yol_kesme=True):
    """Kapalı dünyada tanık (doğru tahmin), yanlış ve yol-kesmeli tanık (en_az_tanik'e ulaşınca sayım durur)."""
    r = k.bas[0]
    tanik = yanlis = yolkesme = 0
    for _, _, idx in ortam.gelistirme:
        tah = sorted(k.tahminler(idx), key=repr)
        dogrular = [(a, b) for a, b in tah if (a, r, b) in idx.olgu]
        tanik += len(dogrular)
        yanlis += len(tah) - len(dogrular)
        for a, b in dogrular if yol_kesme else ():
            if yolkesme >= ortam.sabit.en_az_tanik:
                break
            yolkesme += k.turetir_mi(idx, a, b, haric=_maske(k, ortam.sema, idx.olgu, (a, r, b)))
    return {"tanik": tanik, "yanlis": yanlis, "yolkesme_tanik": yolkesme}


def bagli_mi(k):
    komsu = {}
    for _, s, a in k.halkalar:
        komsu.setdefault(s, set()).add(a)
        komsu.setdefault(a, set()).add(s)
    _, x, y = k.bas
    gorulen, yigin = {x}, [x]
    while yigin:
        for w in komsu.get(yigin.pop(), set()) - gorulen:
            gorulen.add(w)
            yigin.append(w)
    return gorulen == set(komsu) and y in gorulen


def indirgenmisler(k):
    """Bir halkası ya da farklılık şartları çıkarılmış, bağlı, X ile Y'yi içeren ve başı gövdede olmayan kurallar."""
    sonuc = []
    _, x, y = k.bas
    for i in range(len(k.halkalar)):
        kalan = k.halkalar[:i] + k.halkalar[i + 1:]
        degisken = {d for _, s, a in kalan for d in (s, a)}
        if kalan and {x, y} <= degisken:
            sonuc.append(kural.Kural(kalan, k.bas, [c for c in k.farkli if c <= degisken]))
    if k.farkli:
        sonuc.append(kural.Kural(k.halkalar, k.bas, ()))
    return [i for i in sonuc if bagli_mi(i) and tuple(i.bas) not in i.halkalar]


def obiterler(k, tanik, ortam):
    """Aşama 2: geliştirme havuzunda yanlış 0 ve en az `tanik` tanıkla geçen indirgenmiş kurallar."""
    sonuc = []
    for i in indirgenmisler(k):
        d = gelistirme_sayilari(i, ortam, yol_kesme=False)
        if d["yanlis"] == 0 and d["tanik"] >= tanik:
            sonuc.append(kural_ozu(i))
    return sonuc


# ---- aşama 4: yeniden bağlı ikiz ----

def bag_ikizi(k, kimlik, ortam):
    r = k.bas[0]
    tanik = yanlis = 0
    for etiket, d, _ in ortam.gelistirme:
        rng = random.Random(_tohum(ortam, "bag", etiket, kimlik))
        olg = h2_bagla.yeniden_bagla(d.olgular, {r}, ortam.sema, rng, False, ortam.sabit.bagla_deneme_carpani)
        idx = kural.Indeks(olg)
        tah = k.tahminler(idx)
        dogru = sum((a, r, b) in idx.olgu for a, b in tah)
        tanik += dogru
        yanlis += len(tah) - dogru
    return {"tanik": tanik, "yanlis": yanlis}


# ---- aşama 5: sembolik ----

def sembolik_bolum(k, bolum, ortam):
    idx = kural.Indeks(bolum.olgular)
    r = k.bas[0]
    tah = sorted(k.tahminler(idx), key=repr)
    yanlis = sum((a, r, b) not in idx.olgu for a, b in tah)
    dogru = 0
    for f in sorted((o for o in bolum.olgular if o[1] == r), key=repr):
        a, _, b = f
        dogru += k.turetir_mi(idx, a, b, haric=_maske(k, ortam.sema, idx.olgu, f))  # §13.2: tek adım
    geri = {v: w for w, v in bolum.esleme.items()}
    return {"dogru": dogru, "yanlis": yanlis, "tahmin": [[geri[a], geri[b]] for a, b in tah]}


def bolumler(k, kimlik, kayit, sayi, ortam):
    etiket, _, d, idx = kayit
    sonuc = []
    for m in range(1, sayi + 1):
        rng = random.Random(_tohum(ortam, "bolum", etiket, kimlik, m))
        b = h2_bolum.govde_merkezli(d, k, ortam.temel, rng, ortam.sabit.adim_araligi, ortam.sabit.dikkat_sayisi,
                                    f"{etiket}|{m}", idx)
        if b is None:  # gövde bu dünyada eşleşmiyor: kanıt yok
            break
        sonuc.append(b)
    return sonuc


def wilson_ozeti(olcumler, z):
    kanitli = [o for o in olcumler if o["dogru"] + o["yanlis"] > 0]
    basarili = sum(o["yanlis"] == 0 for o in kanitli)
    return {"kanitli": len(kanitli), "basarili": basarili, "wilson": istatistik.wilson_alt(basarili, len(kanitli), z)}


def taze_sembolik(k, kimlik, taze, ortam):
    """Aile başına sayılar ve bölüm ölçümleri. `ret_aile_sayisi` ailede yanlış görülünce durur (RET kesinleşir)."""
    aileler, olcumler = {}, []
    for kayit in taze:
        etiket, aile = kayit[0], kayit[1]
        a = aileler.setdefault(aile, {"dogru": 0, "yanlis": 0, "bolum": 0})
        for b in bolumler(k, kimlik, kayit, ortam.sabit.bolum_sayisi, ortam):
            o = dict(sembolik_bolum(k, b, ortam), dunya=etiket, aile=aile, bolum=b.etiket)
            olcumler.append(o)
            a["dogru"] += o["dogru"]
            a["yanlis"] += o["yanlis"]
            a["bolum"] += 1
        if sum(v["yanlis"] > 0 for v in aileler.values()) >= ortam.sabit.ret_aile_sayisi:
            break
    return {"aileler": aileler, "bolumler": olcumler, **wilson_ozeti(olcumler, ortam.sabit.wilson_z)}


def gelistirme_dunyalari(ortam):
    """T_gel dünyaları: her ailede havuz sırasıyla ilk `taze_aile_basina` dünya (taze akışla aynı biçim, V-065)."""
    sayac, secilen = {}, []
    for etiket, d, idx in ortam.gelistirme:
        if sayac.get(d.aile, 0) < ortam.sabit.taze_aile_basina:
            sayac[d.aile] = sayac.get(d.aile, 0) + 1
            secilen.append((etiket, d.aile, d, idx))
    return secilen


def gelistirme_wilson(k, kimlik, ortam):
    olcumler = [sembolik_bolum(k, b, ortam) for kayit in gelistirme_dunyalari(ortam)
                for b in bolumler(k, kimlik, kayit, ortam.sabit.bolum_sayisi, ortam)]
    return wilson_ozeti(olcumler, ortam.sabit.wilson_z)


def gurultu(kimlik, basamak, tur, ortam):
    """Thresholdout için iki standart Laplace(0, 1) çekilişi; ölçek eşiklerle uygulanır (ızgara aynı çekilişi kullanır)."""
    rng = random.Random(tohum.tohum(ortam.h2, "gurultu", basamak, tur, kimlik))
    return [istatistik.laplace(rng, 1.0), istatistik.laplace(rng, 1.0)]


def thresholdout(t_gel, t_taze, cekilis, esik):
    eta1, eta2 = (2 * esik.sigma) * cekilis[0], esik.sigma * cekilis[1]  # ÖK-005 taslağı §4 madde 12: Laplace(0, 2σ), Laplace(0, σ)
    return t_taze + eta2 if abs(t_gel - t_taze) > esik.T + eta1 else t_gel


def sembolik_olcum(k, kimlik, taze, basamak, tur, ortam):
    """Aşama 1–5'in sembolik ölçümleri; ilk düşen aşamada durur (Westfall–Young tur ailesiyle ayrıca)."""
    g = gelistirme_sayilari(k, ortam)
    o = {"gelistirme": g}
    if g["yanlis"] > 0:
        return o
    o["obiter"] = obiterler(k, g["tanik"], ortam)
    if o["obiter"] or g["yolkesme_tanik"] < ortam.sabit.en_az_tanik:
        return o
    o["bag_ikizi"] = bag_ikizi(k, kimlik, ortam)
    if _bag_ikizi_vetosu(o, ortam.sabit):
        return o
    o["taze"] = taze_sembolik(k, kimlik, taze, ortam)
    if _taze_hukmu(o, ortam.sabit):
        return o
    o["gel_wilson"] = gelistirme_wilson(k, kimlik, ortam)
    o["gurultu"] = gurultu(kimlik, basamak, tur, ortam)
    return o


# ---- Westfall–Young ----

def _basarili_mi(tahmin, kenarlar):
    return all(tuple(c) in kenarlar for c in tahmin)


def wy_istatistigi(aday, kenar_fn, z):
    kanitli = [b for b in aday["bolumler"] if b["tahmin"]]
    basarili = sum(_basarili_mi(b["tahmin"], kenar_fn(b["dunya"], aday["bas"])) for b in kanitli)
    return istatistik.wilson_alt(basarili, len(kanitli), z)


def wy_ailesi(adaylar):
    """adaylar: [(kimlik, kural, ölçüm)] → istatistik girdisi (yalnız tur ailesindekiler: aşama 1–5 sembolik geçen)."""
    return [{"kimlik": kimlik, "bas": k.bas[0], "bolumler": [{"dunya": b["dunya"], "tahmin": b["tahmin"]}
                                                           for b in o["taze"]["bolumler"]]} for kimlik, k, o in adaylar]


def wy_gozlenen(aile, taze, z):
    kenar = {}
    for et, _, d, _ in taze:
        for r in {a["bas"] for a in aile}:
            kenar[(et, r)] = {(x, y) for x, rr, y in d.olgular if rr == r}
    return {a["kimlik"]: wy_istatistigi(a, lambda dn, r: kenar[(dn, r)], z) for a in aile}


def wy_maksimumlar(aile, taze, basamak, tur, ortam, cekilisler):
    """Her çekilişte baş ilişkileri her taze dünyada öteki ilişkiler sabitken bağımsız yeniden bağlanır (V-065);
    gövde eşleşmeleri (tahminler) özgün dünyadan, baş doğruluğu yeniden bağlanmış dünyadan."""
    z = ortam.sabit.wilson_z
    hazir = {}
    for et, _, d, _ in taze:
        for r in sorted({a["bas"] for a in aile}):
            hazir[(et, r)] = (sorted((x, y) for x, rr, y in d.olgular if rr == r),
                              h2_bagla.dolu_ciftler(d.olgular, r, ortam.sema), ortam.sema.simetrik(r))
    maks = []
    for b in cekilisler:
        bagli = {}
        for (et, r), (kenarlar, dolu, simetrik) in hazir.items():
            rng = random.Random(tohum.tohum(ortam.h2, "null", basamak, tur, b, *et.split(tohum.AYIRICI), r))
            bagli[(et, r)] = set(h2_bagla.kenar_bagla(kenarlar, dolu, simetrik, rng, ortam.sabit.bagla_deneme_carpani))
        maks.append(max((wy_istatistigi(a, lambda dn, r: bagli[(dn, r)], z) for a in aile), default=0.0))
    return maks


def wy_p(T, maks, toplam_cekilis):
    """p_j = (1 + #{b : maxᵢ Tᵢᵇ ≥ T_j}) / (B + 1) (ÖK-005 taslağı §4, Westfall–Young çekilişi)."""
    return {k: (1 + sum(m >= t for m in maks)) / (toplam_cekilis + 1) for k, t in T.items()}


# ---- çekirdek ----

def hucre(k, kimlik, sabit):
    return Hucre(kimlik, tuple(Halka(r, s, a, sabit.halka_esigi) for r, s, a in k.halkalar), Sonuc(*k.bas),
                 sabit.guvenilirlik, tuple(tuple(sorted(c)) for c in sorted(k.farkli, key=sorted)))


def cekirdek_bolum(h, ters_dayanakli, olgular3, ortam):
    try:
        return _cekirdek_bolum(h, ters_dayanakli, olgular3, ortam)
    except HavuzHatasi:
        return {"dogru": None, "yanlis": None, "mudahale": [], "havuz_asimi": True}


def _cekirdek_bolum(h, ters_dayanakli, olgular3, ortam):
    olgular = [(a, r, b, GOZLEM_GUVENI) for a, r, b in olgular3]
    gozlenen = set(olgular3)
    ham = maskeli_kos(h, (), olgular, None, ortam.sema, ortam.kk, ortam.prm, ortam.gunluk)
    yanlis = {tuple(t) for t in ham["tahminler"] if tuple(t) not in gozlenen}
    yanlis |= {tuple(c[0]) for c in ham["olgu_celiskileri"]}
    dogru, mudahale = 0, []
    for i, (a, r, b, _) in enumerate(olgular):
        if r != h.sonuc.gen:
            continue
        ters = set() if ters_dayanakli else _ters_olgular(ortam.sema, gozlenen, (a, r, b))
        gorunen = [(p, q, s, g) for p, q, s, g in olgular if (p, q, s) not in ters]
        sonuc = maskeli_kos(h, (), gorunen, gorunen.index(olgular[i]), ortam.sema, ortam.kk, ortam.prm, ortam.gunluk)
        dogru += [a, r, b] in sonuc["tahminler"]
        if sonuc["mudahale"] is not None:
            mudahale.append(sonuc["mudahale"])
    return {"dogru": dogru, "yanlis": len(yanlis), "mudahale": mudahale}


def pi_olcumu(k, kimlik, ortam):
    h = hucre(k, kimlik, ortam.sabit)
    ayni, orijinal, ikiz, n = True, [], [], 0
    for etiket, d, idx in ortam.gelistirme:
        if n >= ortam.sabit.pi_bolum_sayisi:
            break
        bs = bolumler(k, kimlik, (etiket, d.aile, d, idx), 1, ortam)
        if not bs:
            continue
        n += 1
        pi = h2_ikiz.sec(ortam.bijeksiyonlar, random.Random(_tohum(ortam, "ikiz", etiket, kimlik)))
        k_pi = h2_ikiz.kurala(pi, k)
        c0 = cekirdek_bolum(h, k.ters_dayanakli, bs[0].olgular, ortam)
        c1 = cekirdek_bolum(hucre(k_pi, kimlik, ortam.sabit), k_pi.ters_dayanakli, h2_ikiz.dunyaya(pi, bs[0].olgular),
                            ortam)
        ayni &= (c0["dogru"], c0["yanlis"]) == (c1["dogru"], c1["yanlis"])
        orijinal += c0["mudahale"]
        ikiz += c1["mudahale"]
    return {"bolum": n, "sayilar_ayni": ayni, "mudahale_orijinal": orijinal, "mudahale_ikiz": ikiz}


def cekirdek_olcum(k, kimlik, taze, ortam):
    """Taze bölümlerde çekirdek sayıları (uyum bozulunca durur) ve geliştirme bölümlerinde π-ikizi."""
    h = hucre(k, kimlik, ortam.sabit)
    olcumler = []
    for kayit in taze:
        for b in bolumler(k, kimlik, kayit, ortam.sabit.bolum_sayisi, ortam):
            c = cekirdek_bolum(h, k.ters_dayanakli, b.olgular, ortam)
            s = sembolik_bolum(k, b, ortam)
            olcumler.append(dict(c, bolum=b.etiket, sembolik=[s["dogru"], s["yanlis"]]))
            if [c["dogru"], c["yanlis"]] != olcumler[-1]["sembolik"]:
                return {"uyum": False, "bolumler": olcumler}
    return {"uyum": True, "bolumler": olcumler, "pi": pi_olcumu(k, kimlik, ortam)}


# ---- hüküm ----

def _ortalama_gecer(puanlar, esik):
    return bool(puanlar) and sum(puanlar) / len(puanlar) >= esik


def kapsam(o, sabit):
    return sorted(a for a, v in o["taze"]["aileler"].items() if v["dogru"] >= sabit.en_az_tanik and v["yanlis"] == 0)


def _gelistirme_hukmu(o, sabit):
    g = o["gelistirme"]
    if g["yanlis"] > 0:
        return RET, "gelistirme_yanlis"
    if o["obiter"]:
        return BILMIYORUM, "obiter"
    if g["yolkesme_tanik"] < sabit.en_az_tanik:
        return BILMIYORUM, "yol_kesme"
    return None


def _bag_ikizi_vetosu(o, sabit):
    b = o["bag_ikizi"]
    return (BILMIYORUM, "bag_ikizi") if b["tanik"] >= sabit.en_az_tanik and b["yanlis"] == 0 else None


def _taze_hukmu(o, sabit):
    veto = sum(a["yanlis"] > 0 for a in o["taze"]["aileler"].values())
    if veto >= sabit.ret_aile_sayisi:
        return RET, "taze_yanlis"
    if veto:
        return BILMIYORUM, "aile_vetosu"
    if len(kapsam(o, sabit)) < sabit.kapsam_en_az_aile:
        return BILMIYORUM, "kapsam"
    return None


def esiksiz_hukum(o, sabit):
    """K değerlerine bağlı olmayan aşamalar (Westfall–Young ailesi ve kalibrasyon bunlardan geçenlerle kurulur)."""
    return _gelistirme_hukmu(o, sabit) or _bag_ikizi_vetosu(o, sabit) or _taze_hukmu(o, sabit)


def sembolik_hukum(o, esik, sabit):
    h = esiksiz_hukum(o, sabit)
    if h:
        return h
    if thresholdout(o["gel_wilson"]["wilson"], o["taze"]["wilson"], o["gurultu"], esik) < esik.tau:
        return BILMIYORUM, "wilson"
    if o.get("wy_p") is None or o["wy_p"] > sabit.alfa:
        return BILMIYORUM, "null"
    return None


def hukum(o, esik, sabit):
    """Ölçümlerden hüküm ve neden (neden yalnız denetçi kanalına yazılır)."""
    h = sembolik_hukum(o, esik, sabit)
    if h:
        return h
    c = o.get("cekirdek")
    if c is None:
        return BILMIYORUM, "cekirdek_olculmedi"
    if not c["uyum"]:
        return BILMIYORUM, "uyum"
    mud = [m for b in c["bolumler"] for m in b["mudahale"]]
    if len(mud) < sabit.mudahale_en_az_kanit:
        return BILMIYORUM, "mudahale_kaniti"
    if not _ortalama_gecer(mud, esik.mudahale):
        return RET, "kisayol"
    pi = c["pi"]
    if not pi["sayilar_ayni"] or (_ortalama_gecer(pi["mudahale_orijinal"], esik.mudahale)
                                  != _ortalama_gecer(pi["mudahale_ikiz"], esik.mudahale)):
        return BILMIYORUM, "pi_ikizi"
    return KABUL, ",".join(kapsam(o, sabit))
