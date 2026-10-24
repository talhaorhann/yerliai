"""sistem.md §10, §11; K-007, K-008: sentetik soy ağacı üreteci, bölmeler ve kelime çantası kapısı (V-017, V-018).

Bölüm dosyası (çekirdeğin göreceği) yalnız olgular + sorgu içerir. Bölme adı, k ve cevap ayrı kâhin kaydındadır.
Kullanım: python3 -m degerlendirme.uretec <cikti_klasoru>
"""
import copy
import dataclasses
import hashlib
import json
import random
import sys
from collections import Counter, deque
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json, ozet
from cekirdek.bilgi_tabani import uclu_kaydi
from cekirdek.iliski_semasi import iliski_semasi_yukle
from degerlendirme.dunya import Dunya, cikarilabilir_mi, tanimlar_yukle
from degerlendirme.kilitli_kumeler import KilitliKumeHatasi, kesisim_denetle, kilitli_ozetler
from degerlendirme.kisa_yol import NaiveBayes, kapi_denetle, ozellikler

BOLMELER = ("egitim", "uzunluk", "zincir_bozuk", "yon_ters", "yeniden_adlandirma", "onsel_ters")  # sistem.md §10
KUMELER = ("dedektor", "ana", "treg", "bozuk")  # K-008
SURUM = "1"  # V-017
KAYNAK = "üreteç"  # KODLAMA_PROMPTU §5
TAM_GUVEN = 1.0  # V-017: üreteç olgusu gerçek ağaçtan gelir
HARFLER = "abcdefghijklmnopqrstuvwxyz"  # V-017: anlamsız ad alfabesi
GENEL_OKUMA = "(A, r, B) = B, A'nın r'sidir."  # V-013


class UretimDurduHatasi(RuntimeError):
    pass


@dataclasses.dataclass(frozen=True)
class Parametreler:
    tohum: int
    nesil_sayisi: int
    cocuk_en_az: int
    cocuk_en_cok: int
    deneme_siniri: int
    dikkat_dagitici: int
    yeniden_ad_uzunlugu: int
    egitim_k: tuple
    test_k: tuple
    ana_kume_sayisi: int
    aday_siniri: int
    dedektor_egitim_sayisi: int
    laplace: float
    sans_payi: float
    algoritma: str
    cikarilabilirlik: bool = False  # K-029, V-048: cevap olgulardan çıkarılabilir olmalı (H1 yeniden denemesi)

    @classmethod
    def ayardan(cls, ayar):
        d = ayar.deger
        return cls(d("uretec_tohum"), d("uretec_nesil_sayisi"), d("uretec_cocuk_en_az"), d("uretec_cocuk_en_cok"),
                   d("uretec_deneme_siniri"), d("dikkat_dagitici_olgu_sayisi"), d("yeniden_ad_uzunlugu"),
                   tuple(d("egitim_k")), tuple(d("test_k")), d("ana_kume_sayisi"), d("aday_siniri"),
                   d("dedektor_egitim_sayisi"), d("dedektor_laplace"), d("kisa_yol_sans_payi"),
                   d("hash_algoritmasi"), d("uretec_cikarilabilirlik"))


@dataclasses.dataclass
class Aday:
    bolum: dict
    cevap: dict
    dunya: Dunya
    sorgu_ham: tuple
    kimlik_esleme: dict


def _yuru(rng, baglar, kisi_sayisi, k):
    yol = [rng.randrange(kisi_sayisi)]
    for _ in range(k):
        secenekler = [b for b, _ad in baglar[yol[-1]] if b not in yol]
        if not secenekler:
            return None
        yol.append(rng.choice(secenekler))
    return yol


def _en_kisa(olgular, bas, son):
    komsu = {}
    for x, _ad, y in olgular:
        komsu.setdefault(x, set()).add(y)
        komsu.setdefault(y, set()).add(x)
    uzaklik = {bas: 0}
    kuyruk = deque([bas])
    while kuyruk:
        x = kuyruk.popleft()
        for y in sorted(komsu.get(x, ())):
            if y not in uzaklik:
                uzaklik[y] = uzaklik[x] + 1
                kuyruk.append(y)
    return uzaklik.get(son)


def _dikkat_dagiticilar(rng, baglar, zincir, kullanilan, adet):
    """Zincirde en fazla bir ucu olan, zincirde kullanılmamış doğrudan bağlardan rastgele olgular."""
    zincirde = set(zincir)
    havuz = sorted({(min(a, b), max(a, b)) for a in baglar for b, _ad in baglar[a]
                    if frozenset((a, b)) not in kullanilan and not (a in zincirde and b in zincirde)})
    if len(havuz) < adet:
        return None
    ad = {(a, b): r for a in baglar for b, r in baglar[a]}
    secilen = []
    for a, b in rng.sample(havuz, adet):
        if rng.randint(0, 1):
            a, b = b, a
        secilen.append((a, ad[(a, b)], b))
    return secilen


def aday_uret(rng, tanimlar, prm, bolme, ad_esleme=None, kume="ana", sayac=None):
    if bolme not in BOLMELER:
        raise ValueError(f"bilinmeyen bölme: {bolme}")
    k_araligi = prm.test_k if bolme == "uzunluk" else prm.egitim_k
    bozuk = bolme == "zincir_bozuk"
    for _ in range(prm.deneme_siniri):
        dunya = Dunya.uret(rng, prm.nesil_sayisi, prm.cocuk_en_az, prm.cocuk_en_cok)
        baglar = dunya.olgu_baglari(tanimlar)
        k = rng.randint(*k_araligi)
        zincir = _yuru(rng, baglar, dunya.kisi_sayisi, k)
        if zincir is None:
            continue
        sorgu = (zincir[-1], zincir[0]) if bolme == "yon_ters" else (zincir[0], zincir[-1])
        cevap = dunya.iliski(sorgu[0], sorgu[1], tanimlar)
        if cevap is None:
            continue
        olgular = [(x, dict(baglar[x])[y], y) for x, y in zip(zincir, zincir[1:])]
        kullanilan = {frozenset((x, y)) for x, _r, y in olgular}
        dikkat_sayisi = prm.dikkat_dagitici
        if bozuk:
            olgular.pop(rng.randrange(len(olgular)))
            dikkat_sayisi += 1  # V-017: olgu sayısı bozulmamış bölümle aynı kalsın
        dikkat = _dikkat_dagiticilar(rng, baglar, zincir, kullanilan, dikkat_sayisi)
        if dikkat is None:
            continue
        hepsi = olgular + dikkat
        uzaklik = _en_kisa(hepsi, sorgu[0], sorgu[1])
        if (uzaklik is not None) if bozuk else (uzaklik != k):
            continue
        kisiler = sorted({x for x, _r, y in hepsi} | {y for x, _r, y in hepsi})
        if sorgu[0] not in kisiler or sorgu[1] not in kisiler:
            continue  # V-017: sorgulanan kişi olgularda hiç geçmezse kolay bir kısa yol olur
        if prm.cikarilabilirlik and not bozuk and not cikarilabilir_mi(dunya, tanimlar, hepsi, sorgu):
            if sayac is not None:
                sayac["cikarilamaz"] += 1  # K-029: cevap olgulardan çıkarılamıyor, aday atılır
            continue
        esleme = dict(zip(kisiler, rng.sample(range(dunya.kisi_sayisi), len(kisiler))))
        rng.shuffle(hepsi)
        adla = (lambda r: ad_esleme[r]) if ad_esleme else (lambda r: r)
        bolum = {"sema_surumu": SURUM,
                 "olgular": [uclu_kaydi(ozne=esleme[x], iliski=adla(r), nesne=esleme[y], kaynak=KAYNAK,
                                        guven=TAM_GUVEN, adim=0, algoritma=prm.algoritma) for x, r, y in hepsi],
                 "sorgu": {"ozne": esleme[sorgu[0]], "nesne": esleme[sorgu[1]]}}
        bolum["ozet"] = ozet(kanonik_json(bolum), prm.algoritma)
        kayit = {"sema_surumu": SURUM, "bolum_ozeti": bolum["ozet"], "bolme": bolme,
                 "kume": "bozuk" if bozuk else kume, "k": k, "cevap": None if bozuk else adla(cevap)}
        return Aday(bolum, kayit, dunya, sorgu, esleme)
    raise UretimDurduHatasi(f"{bolme}: {prm.deneme_siniri} denemede uygun bölüm bulunamadı")


def ad_eslemesi(rng, iliski_semasi, prm):
    """Her ilişkiye tutarlı, anlamsız, benzersiz bir ad (sistem.md §10 ilişki yeniden adlandırma)."""
    esleme, kullanilan = {}, set(iliski_semasi.adlar)
    for ad in iliski_semasi.adlar:
        while True:
            yeni = "".join(rng.choice(HARFLER) for _ in range(prm.yeniden_ad_uzunlugu))
            if yeni not in kullanilan:
                break
        esleme[ad] = yeni
        kullanilan.add(yeni)
    return esleme


def yeniden_adlandirilmis_sema(sema_verisi, esleme):
    yeni = copy.deepcopy(sema_verisi)
    yeni["okuma"] = GENEL_OKUMA
    for i in yeni["iliskiler"]:
        i["ad"] = esleme[i["ad"]]
        i["ters"] = [esleme[t] for t in i["ters"]]
    yeni["dislayici_gruplar"] = [[esleme[a] for a in g] for g in yeni["dislayici_gruplar"]]
    return yeni


def _kabul_olasiliklari(dedektor, adlar):
    """V-022: doğal dağılım p(r) (Laplace +1); q(r) ∝ 1/p(r) için reddetme örneklemesi kabul olasılığı (p_en_az/p)²."""
    sayac = Counter(a.cevap["cevap"] for a in dedektor)
    toplam = len(dedektor) + len(adlar)
    p = {r: (sayac[r] + 1) / toplam for r in adlar}
    p_en_az = min(p.values())
    return {r: (p_en_az / p[r]) ** 2 for r in adlar}  # V-022


def bolme_uret(bolme, prm, tanimlar, iliski_semasi, sema_yolu, yasakli=frozenset()):
    rng = random.Random(f"{prm.tohum}:{bolme}")
    esleme = ad_eslemesi(rng, iliski_semasi, prm) if bolme == "yeniden_adlandirma" else None
    sonuc = {k: [] for k in KUMELER}
    sayac = Counter()
    if bolme == "zincir_bozuk":
        # V-018: kapı, bozuk bölümler ile aynı dağılımdan bozulmamış bölümlerin karışımında ölçülür
        karisim = []
        for _ in range(prm.ana_kume_sayisi):
            karisim.append(aday_uret(rng, tanimlar, prm, "egitim", kume="dedektor", sayac=sayac))
            bozuk = aday_uret(rng, tanimlar, prm, bolme, sayac=sayac)
            karisim.append(bozuk)
            sonuc["bozuk"].append(bozuk)
        sonuc["kapi"] = kapi_denetle([a.bolum for a in karisim], [a.cevap for a in karisim], prm.laplace, prm.sans_payi)
    else:
        sonuc["dedektor"] = [aday_uret(rng, tanimlar, prm, bolme, esleme, kume="dedektor", sayac=sayac)
                             for _ in range(prm.dedektor_egitim_sayisi)]
        nb = NaiveBayes(prm.laplace)
        nb.egit([ozellikler(a.bolum) for a in sonuc["dedektor"]], [a.cevap["cevap"] for a in sonuc["dedektor"]])
        kabul = _kabul_olasiliklari(sonuc["dedektor"], iliski_semasi.adlar) if bolme == "onsel_ters" else None
        aday_sayisi = 0
        while len(sonuc["ana"]) < prm.ana_kume_sayisi:
            aday_sayisi += 1
            if aday_sayisi > prm.aday_siniri:
                raise UretimDurduHatasi(f"{bolme}: {prm.aday_siniri} adayda ana küme dolmadı "
                                        f"({len(sonuc['ana'])}/{prm.ana_kume_sayisi})")
            a = aday_uret(rng, tanimlar, prm, bolme, esleme, sayac=sayac)
            if kabul is not None and rng.random() >= kabul[a.cevap["cevap"]]:
                continue  # V-022: önsel-ters reddetme örneklemesi (ret edilen aday da sınıra sayılır)
            if nb.tahmin(ozellikler(a.bolum)) == a.cevap["cevap"]:
                a.cevap["kume"] = "treg"
                sonuc["treg"].append(a)
            else:
                sonuc["ana"].append(a)
        sonuc["kapi"] = kapi_denetle([a.bolum for a in sonuc["ana"]], [a.cevap for a in sonuc["ana"]],
                                     prm.laplace, prm.sans_payi)
    ozetler = [a.bolum["ozet"] for k in KUMELER for a in sonuc[k]]
    if len(set(ozetler)) != len(ozetler):
        raise UretimDurduHatasi(f"{bolme}: bölme içinde yinelenen bölüm")
    kesisim_denetle(yasakli, ozetler)
    sonuc["esleme"] = esleme
    sonuc["cikarilamaz_atilan"] = sayac["cikarilamaz"]
    if esleme:
        with open(sema_yolu, encoding="utf-8") as f:
            sonuc["sema"] = yeniden_adlandirilmis_sema(json.load(f), esleme)
    else:
        sonuc["sema"] = None
    return sonuc


def _jsonl(kayitlar):
    return b"".join(kanonik_json(k) + b"\n" for k in kayitlar)


def hepsini_uret(klasor, prm, tanimlar, iliski_semasi, sema_yolu, kilit_kayit_yolu, kok):
    """Tüm bölmeleri üretir. Bölümler `bolumler/`, cevaplar ve eşlemeler `kahin/` altına yazılır (kâhin yalıtımı)."""
    yasakli = kilitli_ozetler(kilit_kayit_yolu, kok)
    klasor = Path(klasor)
    (klasor / "bolumler").mkdir(parents=True, exist_ok=True)
    (klasor / "kahin").mkdir(parents=True, exist_ok=True)
    yazilacak, kapilar, gorulen, atilan = {}, {}, set(), {}
    for bolme in BOLMELER:
        s = bolme_uret(bolme, prm, tanimlar, iliski_semasi, sema_yolu, yasakli)
        atilan[bolme] = s["cikarilamaz_atilan"]
        for kume in KUMELER:
            if not s[kume]:
                continue
            ozetler = {a.bolum["ozet"] for a in s[kume]}
            if ozetler & gorulen:
                raise KilitliKumeHatasi(f"{bolme}/{kume}: başka bölmeyle yinelenen bölüm")
            gorulen |= ozetler
            yazilacak[f"bolumler/{bolme}_{kume}.jsonl"] = _jsonl(a.bolum for a in s[kume])
            yazilacak[f"kahin/{bolme}_{kume}_cevap.jsonl"] = _jsonl(a.cevap for a in s[kume])
        if s["sema"] is not None:
            yazilacak[f"bolumler/{bolme}_sema.json"] = kanonik_json(s["sema"])
            yazilacak[f"kahin/{bolme}_esleme.json"] = kanonik_json(s["esleme"])
        kapilar[bolme] = {"dogruluk": s["kapi"][0], "sans": s["kapi"][1], "pay": prm.sans_payi}
    for yol, baytlar in yazilacak.items():
        atomik_yaz(klasor / yol, baytlar)
    manifest = {"sema_surumu": SURUM, "tohum": prm.tohum, "iliski_semasi_ozeti": iliski_semasi.ozet,
                "kilitli_bolum_sayisi": len(yasakli), "kapilar": kapilar,
                "dosyalar": {y: hashlib.new(prm.algoritma, b).hexdigest() for y, b in sorted(yazilacak.items())}}
    if prm.cikarilabilirlik:  # K-029: denetim kapalıyken manifest eskisiyle bayt bayt aynı kalır
        manifest["cikarilamaz_atilan"] = atilan
    atomik_yaz(klasor / "ozet.json", kanonik_json(manifest))
    return manifest


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    ayar = ayar_yukle(kok / "config.json")
    sema_yolu = kok / "sema" / "iliskiler_v1.json"
    sema = iliski_semasi_yukle(sema_yolu, kok / "kilit" / "sema_onayi.json", kok / "sema" / "iliski_semasi_v1.schema.json")
    tanimlar = tanimlar_yukle(kok / "degerlendirme" / "veri" / "tanimlar_v1.json",
                              kok / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
    manifest = hepsini_uret(Path(arg[0]), Parametreler.ayardan(ayar), tanimlar, sema, sema_yolu,
                            kok / "kilit" / "kilitli_kumeler.json", kok)
    print(json.dumps(manifest["kapilar"], ensure_ascii=False, indent=1))  # V-017: okunur çıktı
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
