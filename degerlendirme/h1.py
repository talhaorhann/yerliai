"""sistem.md §13 (H1), K-023 (ÖK-002), K-021, V-044: H1 koşturucusu.

Kâhin yalıtımı: cevap kayıtlarını yalnız bu modül okur. Çekirdeğe (`bolum_kos`) yalnız bölümün olguları ve sorgusu
gider; cevap, çekirdek koştuktan sonra `degerlendir` ile karşılaştırılır. Kapı bölmeleri; config, DNA ve bölüm
dosyalarının özetleri ÖK-002 ekinde (ONKAYIT.md §9) yazılı değilse koşturulmaz.
Uzun koşu (KODLAMA_PROMPTU §5): her bölme-tohum sonucu aralıklarla atomik yazılır. Yarıda kesilen koşu kaldığı
yerden sürer ve duvar saati dışında kesintisiz koşuyla aynı satırları verir.

Kullanım (.venv/bin/python -m degerlendirme.h1 ...):
  uret <klasör>                    H1 tohumlarıyla bölümleri üretir (kapıda duran tohum değişir, K-030)
  ozetler <klasör> <dna>           ÖK-002 ekine yazılacak özetleri basar
  gelistir <klasör> <dna> <çıkış>  geliştirme bölmesini koşturur (ön kayıt gerekmez)
  kapi <klasör> <dna> <çıkış>      kapı bölmelerini koşturur ve kapı kararını verir (ön kayıt gerekir)
  yeni_egitim <klasör> <dna> <çıkış>  kapı tohumlarının eğitim bölmesi, ayrı satır, kapıya girmez (ÖK-003 §3.3)
  altin <dna> <çıkış>              altın küme, her parça kendi kaynak etiketiyle (ön kayıt gerekir)
"""
import dataclasses
import hashlib
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.altyapi.olay_gunlugu import YEDEK_KULLANILDI
from cekirdek.defter import ATMA, CELISKI, Defter
from cekirdek.dna import dna_yukle
from cekirdek.dongu import DURMA_TUR_SINIRI, CekirdekParametreleri, calistir
from cekirdek.havuz import Havuz
from cekirdek.iliski_semasi import iliski_semasi_yukle
from cekirdek.mudahale import PUANLI, mudahale_ozeti, mudahale_testi
from cekirdek.plazma import cevapla
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme.altin import BILGI_YETMEZ, EMIN_DEGIL, HARFLER, LLM_TASLAGI, kullanici_cevaplarini_denetle
from degerlendirme.istatistik import bootstrap_araligi, clopper_pearson
from degerlendirme.kisa_yol import KisaYolHatasi

BOZUK_BOLME = "zincir_bozuk"  # sistem.md §10
KUME_ANA, KUME_BOZUK = "ana", "bozuk"  # K-008
SURE = "sure_sn"  # V-044: duvar saati, belirlenim karşılaştırmasının dışında
DEGERLENDIRME_ALANLARI = ("beklenen", "dogru", "sinif", "bolme", "tohum")
SINIF_TUR, SINIF_HAVUZ, SINIF_BILMIYORUM, SINIF_YANLIS = "tur_siniri", "havuz", "bilmiyorum", "yanlis_iliski"  # ÖK-002 §6
EK_BASLIGI = "### 9. Koşu öncesi ek"  # ÖK-002 §9
DNA_BICIMLERI = {"1": "dna_v1.schema.json", "2": "dna_v2.schema.json"}  # V-032, V-043
TOHUM_KAYDI = "tohumlar.json"  # K-030: üretimde kullanılan tohumlar ve değişimler
KIP_GELISTIRME, KIP_KAPI, KIP_ALTIN, KIP_YENI_EGITIM = "gelistirme", "kapi", "altin", "yeni_egitim"  # ÖK-003 §3.3–§3.4


class H1Hatasi(RuntimeError):
    pass


class OnKayitHatasi(H1Hatasi):
    """Kapı bölmesi, özetleri ÖK-002 ekinde yazılı olmadan koşturulmak istendi."""


def bolum_kos(bolum, hucreler, iliski_semasi, kk, prm, gunluk_ayari):
    """Tek bölüm: çekirdek, plazma, müdahale testi. Cevap kaydı burada yoktur (kâhin yalıtımı)."""
    olgular = [(o["ozne"], o["iliski"], o["nesne"], o["guven"]) for o in bolum["olgular"]]
    sorgu = (bolum["sorgu"]["ozne"], bolum["sorgu"]["nesne"])
    bas = time.perf_counter()
    havuz = Havuz(prm.kapasite, kk)
    for s, r, o, g in olgular:
        havuz.epitop_ekle(s, r, o, guven=g)
    defter = Defter(None, **gunluk_ayari)
    dongu = calistir(hucreler, havuz, kk, prm, defter, iliski_semasi=iliski_semasi, sorgu=sorgu)
    c = cevapla(havuz, sorgu, defter)
    m = mudahale_testi(havuz, defter, hucreler, olgular, kk, prm, iliski_semasi, sorgu)
    return {"bolum_ozeti": bolum["ozet"], "cevap": c.iliski, "guven": c.guven,
            "adaylar": [list(a) for a in c.birlesik], "aday_celiskisi": c.celiski,
            "tur": dongu.tur, "durma": dongu.durma_nedeni, "esik_dusurme": dongu.esik_dusurme,
            "yazilan": dongu.yazilan, "atma": defter.sayac(ATMA), "yedek": defter.sayac(YEDEK_KULLANILDI),
            "celiski": defter.sayac(CELISKI),
            "mudahale": {"durum": m.durum, "a": m.a, "b": m.b, "c": m.c, "puan": m.puan},
            "defter_ozeti": defter.kayitlar()[-1]["ozet"], SURE: time.perf_counter() - bas}


def degerlendir(satir, cevap_kaydi):
    """Çekirdek satırını kâhin cevabıyla karşılaştırır. Zincir-bozukta doğru = "bilmiyorum" (ÖK-002 §5)."""
    if satir["bolum_ozeti"] != cevap_kaydi["bolum_ozeti"]:
        raise H1Hatasi(f"cevap kaydı başka bölümün: {cevap_kaydi['bolum_ozeti']}")
    beklenen, verilen = cevap_kaydi["cevap"], satir["cevap"]
    dogru = verilen == beklenen
    sinif = None
    if not dogru:  # ÖK-002 §6: otomatik ayrılabilen sınıflar; gerisi incelemede ayrılır
        if satir["durma"] == DURMA_TUR_SINIRI:
            sinif = SINIF_TUR
        elif satir["atma"] or satir["yedek"]:
            sinif = SINIF_HAVUZ
        elif verilen is None:
            sinif = SINIF_BILMIYORUM
        else:
            sinif = SINIF_YANLIS
    return dict(satir, beklenen=beklenen, dogru=dogru, sinif=sinif)


def cekirdek_kismi(satir):
    return {k: v for k, v in satir.items() if k not in DEGERLENDIRME_ALANLARI}


def belirlenimli(satir):
    return {k: v for k, v in satir.items() if k != SURE}


def _ozet_satiri(satirlar, guven, tekrar, tohum):
    n = len(satirlar)
    dogru = sum(1 for s in satirlar if s["dogru"])
    puanlar = [s["mudahale"]["puan"] for s in satirlar if s["mudahale"]["durum"] == PUANLI]
    mudahale = mudahale_ozeti([SimpleNamespace(**s["mudahale"]) for s in satirlar])
    mudahale["puan_araligi"] = bootstrap_araligi(puanlar, tekrar, guven, tohum)
    return {"n": n, "dogru": dogru, "yanlis": n - dogru, "dogruluk": dogru / n,
            "hata_ust_siniri": clopper_pearson(n - dogru, n, guven)[1],
            "bilmiyorum": sum(1 for s in satirlar if s["beklenen"] is not None and s["cevap"] is None),
            "yanlis_pozitif": sum(1 for s in satirlar if s["beklenen"] is None and s["cevap"] is not None),
            "siniflar": dict(sorted(Counter(s["sinif"] for s in satirlar if s["sinif"]).items())),
            "durma": dict(sorted(Counter(s["durma"] for s in satirlar).items())),
            "atma": sum(s["atma"] for s in satirlar), "yedek": sum(s["yedek"] for s in satirlar),
            "ortalama_tur": math.fsum(s["tur"] for s in satirlar) / n,
            SURE: math.fsum(s[SURE] for s in satirlar), "mudahale": mudahale}


def ozetle(satirlar, guven, tekrar, tohum):
    """Bölme-tohum başına ve bölme başına (tohumlar birleşik) ölçütler (ÖK-002 §5)."""
    gruplar, bolmeler = {}, {}
    for s in satirlar:
        gruplar.setdefault(f"{s['bolme']}/{s['tohum']}", []).append(s)
        bolmeler.setdefault(s["bolme"], []).append(s)
    return {"satirlar": {a: _ozet_satiri(g, guven, tekrar, tohum) for a, g in sorted(gruplar.items())},
            "bolmeler": {a: _ozet_satiri(g, guven, tekrar, tohum) for a, g in sorted(bolmeler.items())}}


def kapi_karari(ozet, kapi_bolmeleri, tohumlar, beklenen_sayi):
    """ÖK-002 §6: her kapı bölmesinde, her tohumda tam sayıda bölüm ve sıfır hata. Tolerans yok."""
    nedenler = []
    for bolme in kapi_bolmeleri:
        for tohum in tohumlar:
            anahtar = f"{bolme}/{tohum}"
            s = ozet["satirlar"].get(anahtar)
            if s is None:
                nedenler.append(f"{anahtar}: koşulmamış")
                continue
            if s["n"] != beklenen_sayi:
                nedenler.append(f"{anahtar}: {s['n']} bölüm, {beklenen_sayi} bekleniyordu")
            if s["yanlis"]:
                nedenler.append(f"{anahtar}: {s['yanlis']} hata")
    return not nedenler, nedenler


def on_kayit_denetle(metin, gerekli, ek_basligi=EK_BASLIGI):
    """Gerekli her özet ön kayıt ekinde (`ek_basligi`ndan sonra) yazılı olmalı (ÖK-002 §2, §3, §9; ÖK-003 §5)."""
    if ek_basligi not in metin:
        raise OnKayitHatasi(f"ön kayıt eki bulunamadı: {ek_basligi}")
    ek = metin.split(ek_basligi, 1)[1]
    eksik = sorted(ad for ad, o in gerekli.items() if o not in ek)
    if eksik:
        raise OnKayitHatasi("ön kayıt ekinde özeti yazılı olmayanlar: " + ", ".join(eksik))


def _ozet(baytlar, algoritma):
    return hashlib.new(algoritma, baytlar).hexdigest()


def _jsonl_oku(baytlar):
    return [json.loads(s) for s in baytlar.decode("utf-8").splitlines()]


def bolme_dosyalari(klasor, tohum, bolme, algoritma):
    """(bölümler, cevaplar); dosya özetleri üretecin manifestiyle (ozet.json) aynı olmalı."""
    kume = KUME_BOZUK if bolme == BOZUK_BOLME else KUME_ANA
    tk = Path(klasor) / f"tohum_{tohum}"
    manifest = json.loads((tk / "ozet.json").read_text(encoding="utf-8"))
    sonuc = []
    for goreli in (f"bolumler/{bolme}_{kume}.jsonl", f"kahin/{bolme}_{kume}_cevap.jsonl"):
        baytlar = (tk / goreli).read_bytes()
        if _ozet(baytlar, algoritma) != manifest["dosyalar"].get(goreli):
            raise H1Hatasi(f"tohum {tohum}: {goreli} özeti manifestle uyuşmuyor")
        sonuc.append(_jsonl_oku(baytlar))
    bolumler, cevaplar = sonuc
    if [b["ozet"] for b in bolumler] != [c["bolum_ozeti"] for c in cevaplar]:
        raise H1Hatasi(f"tohum {tohum}, {bolme}: bölümler ile cevaplar aynı sırada değil")
    return bolumler, cevaplar


def bolme_kos(klasor, tohum, bolme, hucreler, iliski_semasi, kk, prm, gunluk_ayari, cikis, ara_kayit, sinir=None):
    """Bir bölme-tohumu sırayla koşturur; ara kayıt varsa kaldığı yerden sürer. `sinir`: bu çağrıda en çok kaç bölüm."""
    bolumler, cevaplar = bolme_dosyalari(klasor, tohum, bolme, gunluk_ayari["algoritma"])
    cikis = Path(cikis)
    cikis.mkdir(parents=True, exist_ok=True)
    yol = cikis / f"{bolme}_t{tohum}.jsonl"
    satirlar = _jsonl_oku(yol.read_bytes()) if yol.exists() else []
    for i, s in enumerate(satirlar):
        if i >= len(bolumler) or (s["bolum_ozeti"], s["bolme"], s["tohum"]) != (bolumler[i]["ozet"], bolme, tohum):
            raise H1Hatasi(f"{yol}: ara kayıt {i}. satırda bu bölme-tohumla uyuşmuyor")
    son = len(bolumler) if sinir is None else min(len(bolumler), len(satirlar) + sinir)
    for i in range(len(satirlar), son):
        satir = degerlendir(bolum_kos(bolumler[i], hucreler, iliski_semasi, kk, prm, gunluk_ayari), cevaplar[i])
        satirlar.append(dict(satir, bolme=bolme, tohum=tohum))
        if (i + 1) % ara_kayit == 0 or i + 1 == son:
            atomik_yaz(yol, b"".join(kanonik_json(s) + b"\n" for s in satirlar))
    return satirlar


def rapor_metni(ozet, kapi=None):
    """İnsan için kısa rapor. Hepsi LLM'siz taban hattır (KODLAMA_PROMPTU §5)."""
    satirlar = ["# H1 raporu", "", "Bütün sonuçlar LLM'siz çekirdeğindir (LLM'siz taban hat).", ""]
    if kapi is not None:
        gecti, nedenler = kapi
        satirlar += [f"**Kapı (ÖK-002 §6): {'GEÇTİ' if gecti else 'GEÇMEDİ'}**", ""]
        satirlar += [f"- {n}" for n in nedenler] + ([""] if nedenler else [])
    satirlar += ["| Bölme / tohum | N | Doğru | Yanlış | Bilmiyorum | Hata %95 üst sınır | Müdahale: puanlı / "
                 "sınanamadı / cevapsız | Ortalama puan [aralık] |", "|---|---|---|---|---|---|---|---|"]
    for grup in ("satirlar", "bolmeler"):
        for ad, s in ozet[grup].items():
            m = s["mudahale"]
            ort = "—" if m["ortalama_puan"] is None else f"{m['ortalama_puan']:.3f}"
            aralik = "" if m["puan_araligi"] is None else " [{:.3f}, {:.3f}]".format(*m["puan_araligi"])
            satirlar.append(f"| {ad if grup == 'satirlar' else ad + ' (tümü)'} | {s['n']} | {s['dogru']} | "
                            f"{s['yanlis']} | {s['bilmiyorum']} | {s['hata_ust_siniri']:.4f} | {m['puanli']} / "
                            f"{m['sinanamadi']} / {m['cevapsiz']} | {ort}{aralik} |")
    satirlar += ["", "\"Sınanamadı\" sorular başarı sayılmaz, ayrı sayılır (K-021)."]
    return "\n".join(satirlar) + "\n"


def altin_harfi(cevap, secenekler):
    """Çekirdeğin cevabının seçenek harfi: "bilmiyorum" → "Bilgi yetmez"; seçeneklerde olmayan ilişki → None."""
    hedef = BILGI_YETMEZ if cevap is None else cevap
    return HARFLER[secenekler.index(hedef)] if hedef in secenekler else None


def altin_satiri(soru, satir, kullanici, uretec_kaydi):
    """Altın soru: çekirdeğin harfi, kullanıcının harfi (parçanın cevabı yoksa None), üretecin harfi (V-023)."""
    if not soru["bolum"]["ozet"] == satir["bolum_ozeti"] == uretec_kaydi["bolum_ozeti"]:
        raise H1Hatasi(f"altın soru {soru['parca']}/{soru['no']}: bölüm özetleri uyuşmuyor")
    harf = altin_harfi(satir["cevap"], soru["secenekler"])
    k = kullanici.get(soru["parca"], {}).get("cevaplar", {}).get(str(soru["no"]))
    return dict(satir, parca=soru["parca"], no=soru["no"], cekirdek_harfi=harf, kullanici_harfi=k,
                uretec_harfi=uretec_kaydi["dogru_harf"],
                kullaniciyla_ayni=None if k in (None, EMIN_DEGIL) else harf == k,
                uretecle_ayni=harf == uretec_kaydi["dogru_harf"])


def _altin_etiketi(kayit):
    """ÖK-001: her parça kendi kaynağıyla; bağımsız insan cevabı değilse açıkça yazılır."""
    if kayit is None:
        return "kullanıcı cevap yok"
    etiket = f"kaynak={kayit['kaynak']}, onaylayan={kayit['onaylayan']}"
    if "cevap_kaynaklari" in kayit:  # K-039: cevap başına kaynak
        llm = sum(1 for k in kayit["cevap_kaynaklari"].values() if k == LLM_TASLAGI)
        etiket += f"; {llm}/{len(kayit['cevap_kaynaklari'])} cevap LLM taslağı, kullanıcı onaylı"
    return etiket + ("" if kayit.get("bagimsiz_insan_cevabi") else " (bağımsız insan cevabı değil, ÖK-001)")


def _llm_taslagi(kayit):
    if kayit is None or "cevap_kaynaklari" not in kayit:
        return None
    return sum(1 for k in kayit["cevap_kaynaklari"].values() if k == LLM_TASLAGI)


def altin_ozeti(satirlar, kullanici):
    parcalar = {}
    for s in satirlar:
        parcalar.setdefault(s["parca"], []).append(s)
    return {str(p): {"etiket": _altin_etiketi(kullanici.get(p)), "llm_taslagi": _llm_taslagi(kullanici.get(p)), "n": len(g),
                     "kullanici_cevapli": sum(1 for s in g if s["kullaniciyla_ayni"] is not None),
                     "kullaniciyla_ayni": sum(1 for s in g if s["kullaniciyla_ayni"]),
                     "emin_degil": sum(1 for s in g if s["kullanici_harfi"] == EMIN_DEGIL),
                     "uretecle_ayni": sum(1 for s in g if s["uretecle_ayni"]),
                     "secenek_disi": sum(1 for s in g if s["cekirdek_harfi"] is None)}
            for p, g in sorted(parcalar.items())}


# --- komut satırı ------------------------------------------------------------------------------------------------

def _ortam(kok):
    ayar = ayar_yukle(kok / "config.json")
    sema = iliski_semasi_yukle(kok / "sema" / "iliskiler_v1.json", kok / "kilit" / "sema_onayi.json",
                               kok / "sema" / "iliski_semasi_v1.schema.json")
    gunluk = dict(algoritma=ayar.deger("hash_algoritmasi"), sema_surumu=ayar.deger("olay_sema_surumu"),
                  izinli_kaynaklar=ayar.deger("kaynaklar"))
    return ayar, sema, gunluk


def _dna(kok, yol, sema):
    surum = json.loads(Path(yol).read_text(encoding="utf-8")).get("sema_surumu")
    if surum not in DNA_BICIMLERI:
        raise H1Hatasi(f"bilinmeyen DNA sürümü: {surum!r}")
    return dna_yukle(yol, kok / "sema" / DNA_BICIMLERI[surum], sema)


def gerekli_ozetler(kok, klasor, dna_yolu, tohumlar, algoritma):
    ozetler = {"config.json": _ozet((kok / "config.json").read_bytes(), algoritma),
               "dna": _ozet(Path(dna_yolu).read_bytes(), algoritma)}
    if klasor is not None and (Path(klasor) / TOHUM_KAYDI).exists():
        ozetler[TOHUM_KAYDI] = _ozet((Path(klasor) / TOHUM_KAYDI).read_bytes(), algoritma)
    for t in tohumlar:
        ozetler[f"tohum_{t}/ozet.json"] = _ozet((Path(klasor) / f"tohum_{t}" / "ozet.json").read_bytes(), algoritma)
    return ozetler


def tohumlari_uret(uret, on_kayit, kullanilmis, sinir, onayli):
    """K-030: kısa yol kapısında (K-008) duran tohumun yerine kullanılmamış ilk tohum geçer; eşik değişmez, `uret`
    aynı ayarla çağrılır. En çok `sinir` değişim. Kapı dışındaki durmalar değişim sebebi değildir, olduğu gibi çıkar.
    K-039: değişim yalnız `onayli` (danışman ve kullanıcı onayı) içindeki tohum için yapılır; değilse üretim durur."""
    kullanilan, degisimler = [], []
    dolu = set(on_kayit) | set(kullanilmis)
    siradaki = max(dolu) + 1
    for tohum in on_kayit:
        while True:
            try:
                uret(tohum)
                break
            except KisaYolHatasi as h:
                if tohum not in onayli:
                    raise H1Hatasi(f"tohum {tohum} kısa yol kapısında durdu: {h}. Yerine tohum geçmesi danışman ve "
                                   f"kullanıcı onayı ister (K-039): onaylanırsa `h1_onayli_tohum_degisimleri`ne yazılır")
                if len(degisimler) == sinir:
                    raise H1Hatasi(f"en çok {sinir} tohum değişimi (K-030): tohum {tohum} de kapıda durdu: {h}")
                degisimler.append({"tohum": tohum, "yerine": siradaki, "neden": str(h)})
                tohum = siradaki
                siradaki += 1
        kullanilan.append(tohum)
    return kullanilan, degisimler


def kapi_tohumlari(klasor, on_kayit, sinir, onayli):
    """K-030, K-039: kapı koşusunun tohumları, üretim kaydı ön kayıtla, değişim sınırıyla ve onaylarla tutarlıysa."""
    yol = Path(klasor) / TOHUM_KAYDI
    if not yol.exists():
        raise H1Hatasi(f"{yol} yok: tohumlar `uret` ile üretilmeli")
    kayit = json.loads(yol.read_text(encoding="utf-8"))
    if kayit["on_kayit"] != list(on_kayit):
        raise H1Hatasi("tohum kaydı ön kayıttaki tohumlarla uyuşmuyor")
    degisimler = kayit["degisimler"]
    if len(degisimler) > sinir:
        raise H1Hatasi(f"tohum kaydında {len(degisimler)} değişim var, en çok {sinir} (K-030)")
    onaysiz = [d["tohum"] for d in degisimler if d["tohum"] not in onayli]
    if onaysiz:
        raise H1Hatasi(f"tohum kaydında onaysız değişim var (K-039): {onaysiz}")
    beklenen, yerine = [], {d["tohum"]: d["yerine"] for d in degisimler}
    for tohum in on_kayit:
        while tohum in yerine:
            tohum = yerine[tohum]
        beklenen.append(tohum)
    if kayit["kullanilan"] != beklenen:
        raise H1Hatasi("tohum kaydındaki kullanılan tohumlar değişimlerle tutarsız")
    return beklenen


def kosu_parametreleri(ayar, kip):
    """ÖK-003 §3.4: kapı, altın ve yeni tohumların eğitim satırı seçilen sınırlarla (`h1_tur_siniri`,
    `h1_havuz_kapasitesi`); eski eğitimde DNA denetimi (§3.3) olağan ayarla. Sınır seçilmemişse KeyError."""
    prm = CekirdekParametreleri.ayardan(ayar)
    if kip == KIP_GELISTIRME:
        return prm
    return dataclasses.replace(prm, tur_siniri=ayar.deger("h1_tur_siniri"), kapasite=ayar.deger("h1_havuz_kapasitesi"))


def uretim_parametreleri(ayar, tohum):
    """ÖK-003 §3.1, ÖK-004: H1 tohumunun üreteç ayarı; çıkarılabilirlik denetimi ve tanımı config'ten (K-029, K-034)."""
    from degerlendirme.uretec import Parametreler
    return dataclasses.replace(Parametreler.ayardan(ayar), tohum=tohum, cikarilabilirlik=ayar.deger("h1_cikarilabilirlik"),
                               cikarilabilirlik_tanimi=ayar.deger("h1_cikarilabilirlik_tanimi"))


def _uret(kok, klasor):
    from degerlendirme.dunya import tanimlar_yukle
    from degerlendirme.uretec import hepsini_uret
    ayar, sema, _ = _ortam(kok)
    tanimlar = tanimlar_yukle(kok / "degerlendirme" / "veri" / "tanimlar_v1.json",
                              kok / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)

    def uret(t):
        prm = uretim_parametreleri(ayar, t)
        manifest = hepsini_uret(Path(klasor) / f"tohum_{t}", prm, tanimlar, sema, kok / "sema" / "iliskiler_v1.json",
                                kok / "kilit" / "kilitli_kumeler.json", kok)
        print(f"tohum {t}: üretildi; çıkarılamadığı için atılan aday: {manifest.get('cikarilamaz_atilan')}", flush=True)

    on_kayit = ayar.deger("h1_tohumlar")
    kullanilan, degisimler = tohumlari_uret(uret, on_kayit, ayar.deger("h1_gelistirme_tohumlari"),
                                            ayar.deger("h1_tohum_degisim_siniri"), ayar.deger("h1_onayli_tohum_degisimleri"))
    for d in degisimler:
        print(f"tohum {d['tohum']} kapıda durdu, yerine {d['yerine']}: {d['neden']}")
    atomik_yaz(Path(klasor) / TOHUM_KAYDI,
               kanonik_json({"on_kayit": on_kayit, "kullanilan": kullanilan, "degisimler": degisimler}))


def _kos(kok, klasor, dna_yolu, cikis, kip):
    ayar, sema, gunluk = _ortam(kok)
    kapi_mi = kip == KIP_KAPI
    if kip == KIP_GELISTIRME:  # ÖK-003 §3.3
        tohumlar = ayar.deger("h1_gelistirme_tohumlari")
    else:  # ÖK-003 §3.2, K-030
        tohumlar = kapi_tohumlari(klasor, ayar.deger("h1_tohumlar"), ayar.deger("h1_tohum_degisim_siniri"),
                                  ayar.deger("h1_onayli_tohum_degisimleri"))
    bolmeler = ayar.deger("h1_kapi_bolmeleri" if kapi_mi else "h1_gelistirme_bolmeleri")
    if kip != KIP_GELISTIRME:
        on_kayit_denetle((kok / "ONKAYIT.md").read_text(encoding="utf-8"),
                         gerekli_ozetler(kok, klasor, dna_yolu, tohumlar, gunluk["algoritma"]), ayar.deger("h1_on_kayit_eki"))
    hucreler = _dna(kok, dna_yolu, sema)
    kk = HizliKodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu"))
    prm = kosu_parametreleri(ayar, kip)
    satirlar = []
    for t in tohumlar:
        for b in bolmeler:
            satirlar += bolme_kos(klasor, t, b, hucreler, sema, kk, prm, gunluk, cikis, ayar.deger("ara_kayit_araligi"))
            print(f"{b} / tohum {t}: {len(satirlar)} bölüm bitti")
    ozet = ozetle(satirlar, ayar.deger("guven_duzeyi"), ayar.deger("bootstrap_tekrar"), ayar.deger("istatistik_tohum"))
    kapi = kapi_karari(ozet, bolmeler, tohumlar, ayar.deger("ana_kume_sayisi")) if kapi_mi else None
    ad = kip
    atomik_yaz(Path(cikis) / f"rapor_{ad}.json", kanonik_json({"ozet": ozet, "kapi": kapi}))
    atomik_yaz(Path(cikis) / f"RAPOR_{ad}.md", rapor_metni(ozet, kapi).encode("utf-8"))
    print(rapor_metni(ozet, kapi))


def altin_rapor_metni(ozet):
    satirlar = ["# H1 altın küme (kapıya girmez, ÖK-002 §4)", "", "LLM'siz çekirdek.", "",
                "| Parça | Kaynak | LLM taslağı (kullanıcı onaylı) | N | Kullanıcı cevaplı | Kullanıcıyla aynı | "
                "Emin değil | Üreteçle aynı | Seçenek dışı |", "|---|---|---|---|---|---|---|---|---|"]
    for p, s in ozet.items():
        llm = "—" if s["llm_taslagi"] is None else s["llm_taslagi"]
        satirlar.append(f"| {p} | {s['etiket']} | {llm} | {s['n']} | {s['kullanici_cevapli']} | "
                        f"{s['kullaniciyla_ayni']} | {s['emin_degil']} | {s['uretecle_ayni']} | {s['secenek_disi']} |")
    return "\n".join(satirlar) + "\n"


def _altin(kok, dna_yolu, cikis):
    from degerlendirme.kilitli_kumeler import kilitli_ozetler
    ayar, sema, gunluk = _ortam(kok)
    on_kayit_denetle((kok / "ONKAYIT.md").read_text(encoding="utf-8"),  # DNA altın kümeye bakılarak düzeltilemez
                     gerekli_ozetler(kok, None, dna_yolu, [], gunluk["algoritma"]), ayar.deger("h1_on_kayit_eki"))
    klasor = kok / "degerlendirme" / "altin"
    sorular = _jsonl_oku((klasor / "altin_sorular.jsonl").read_bytes())
    uretec = _jsonl_oku((klasor / "uretec_cevaplari.jsonl").read_bytes())
    kilitli = kilitli_ozetler(kok / "kilit" / "kilitli_kumeler.json", kok)
    if any(s["bolum"]["ozet"] not in kilitli for s in sorular):
        raise H1Hatasi("altın soru bölümü kilitli kümede yok")
    kullanici = {}
    for p in range(1, ayar.deger("altin_parca_sayisi") + 1):
        yol = klasor / f"kullanici_cevaplari_{p}.json"
        if yol.exists():
            kullanici[p] = json.loads(yol.read_text(encoding="utf-8"))
            kullanici_cevaplarini_denetle(kullanici[p], p, sum(1 for s in sorular if s["parca"] == p))  # K-039
    hucreler = _dna(kok, dna_yolu, sema)
    kk = HizliKodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu"))
    prm = kosu_parametreleri(ayar, KIP_ALTIN)
    satirlar = [altin_satiri(s, bolum_kos(s["bolum"], hucreler, sema, kk, prm, gunluk), kullanici, u)
                for s, u in zip(sorular, uretec)]
    ozet = altin_ozeti(satirlar, kullanici)
    Path(cikis).mkdir(parents=True, exist_ok=True)
    atomik_yaz(Path(cikis) / "altin_satirlari.jsonl", b"".join(kanonik_json(s) + b"\n" for s in satirlar))
    atomik_yaz(Path(cikis) / "RAPOR_altin.md", altin_rapor_metni(ozet).encode("utf-8"))
    print(altin_rapor_metni(ozet))


KOMUTLAR = {"uret": ("klasor",), "ozetler": ("klasor", "dna"), "gelistir": ("klasor", "dna", "cikis"),
            "kapi": ("klasor", "dna", "cikis"), "yeni_egitim": ("klasor", "dna", "cikis"), "altin": ("dna", "cikis")}
KIPLER = {"gelistir": KIP_GELISTIRME, "kapi": KIP_KAPI, "yeni_egitim": KIP_YENI_EGITIM}


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    komut, *degerler = arg or [None]
    if komut not in KOMUTLAR or len(degerler) != len(KOMUTLAR[komut]):
        print(__doc__)
        return 1
    d = dict(zip(KOMUTLAR[komut], degerler))
    if komut == "uret":
        _uret(kok, d["klasor"])
    elif komut == "ozetler":
        ayar, _, gunluk = _ortam(kok)
        kayitli = (Path(d["klasor"]) / TOHUM_KAYDI).exists()
        tohumlar = (kapi_tohumlari(d["klasor"], ayar.deger("h1_tohumlar"), ayar.deger("h1_tohum_degisim_siniri"),
                                   ayar.deger("h1_onayli_tohum_degisimleri"))
                    if kayitli else ayar.deger("h1_tohumlar"))
        for ad, o in gerekli_ozetler(kok, d["klasor"], d["dna"], tohumlar, gunluk["algoritma"]).items():
            print(f"- `{ad}`: `{o}`")
    elif komut == "altin":
        _altin(kok, d["dna"], d["cikis"])
    else:
        _kos(kok, d["klasor"], d["dna"], d["cikis"], KIPLER[komut])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
