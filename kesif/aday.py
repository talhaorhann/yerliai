"""sistem.md §3, §13; K-041: tek aday şeması (baş, gövde, kaynak, tanık, sürüm), kanonik kimlik ve kırmızı takım dosyası
denetimi (ÖK-005 taslağı §4 madde 19, §13.1).

Gizli kırmızı takım dosyası açılıp gösterilmez: denetim yalnız sayı ve özet döndürür; hata iletilerinde kayıt değeri
(ilişki adı, kimlik, aile adı) geçmez, yalnız yer (alan yolu) geçer.
Kullanım: python3 -m kesif.aday <dosya> <kirmizi_gizli|kirmizi_gorunur>  (yalnız sayıları ve özeti yazar)
"""
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json, ozet
from cekirdek.altyapi.sema_dogrulayici import sema_yukle
from cekirdek.bellek_gecidi import kanonik_bicim
from cekirdek.dna import Halka, Hucre, Sonuc
from cekirdek.iliski_semasi import iliski_semasi_yukle

KOK = Path(__file__).resolve().parents[1]
ADAY_SEMASI = KOK / "sema" / "aday_v1.schema.json"  # K-041
KIRMIZI_SEMASI = KOK / "sema" / "kirmizi_dosyasi_v1.schema.json"  # K-041
ILISKI_SEMASI = (KOK / "sema" / "iliskiler_v1.json", KOK / "kilit" / "sema_onayi.json",
                 KOK / "sema" / "iliski_semasi_v1.schema.json")  # V-013: onaylı şema, onay kaydı, biçim
KIRMIZI_TURLERI = ("kirmizi_gorunur", "kirmizi_gizli")  # ÖK-005 taslağı §4 madde 19 (K-041)


class AdayHatasi(ValueError):
    pass


_SEMALAR = {}


def _sema(yol):
    if yol not in _SEMALAR:
        _SEMALAR[yol] = sema_yukle(yol)
    return _SEMALAR[yol]


def _degiskenler(kayit):
    return {d for h in kayit["halkalar"] for d in (h["sol"], h["sag"])}


def aday_hatalari(kayit, iliski_adlari, yer="aday"):
    """Hata iletileri listesi (boşsa geçerli). İletilerde değer yoktur."""
    hatalar = [f"{yer}.{h}" for h in _sema(ADAY_SEMASI).hatalar(kayit)]
    if hatalar:
        return hatalar
    for i, h in enumerate(kayit["halkalar"]):
        if h["gen"] not in iliski_adlari:
            hatalar.append(f"{yer}.halkalar[{i}].gen: onaylı şemada yok")
        if h["sol"] == h["sag"]:
            hatalar.append(f"{yer}.halkalar[{i}]: iki ucu aynı değişken")
    s = kayit["sonuc"]
    if s["gen"] not in iliski_adlari:
        hatalar.append(f"{yer}.sonuc.gen: onaylı şemada yok")
    govde = _degiskenler(kayit)
    if not {s["sol"], s["sag"]} <= govde:
        hatalar.append(f"{yer}.sonuc: baş değişkenleri gövdede geçmiyor")
    if s["sol"] == s["sag"]:
        hatalar.append(f"{yer}.sonuc: baş değişkenleri farklı olmalı")
    for i, (a, b) in enumerate(kayit["farkli"]):
        if a == b or not {a, b} <= govde:
            hatalar.append(f"{yer}.farkli[{i}]: gövdedeki iki ayrı değişkeni göstermeli")
    if kayit["oi"] and kayit["farkli"]:
        hatalar.append(f"{yer}: oi açıkken farkli boş olmalı")
    kirmizi = kayit["kaynak"]["tur"] in KIRMIZI_TURLERI
    if kirmizi != (kayit["kaynak"]["aile"] is not None):
        hatalar.append(f"{yer}.kaynak.aile: yalnız kırmızı takım adaylarında ve onlarda zorunlu")
    return hatalar


def aday_denetle(kayit, iliski_adlari):
    hatalar = aday_hatalari(kayit, iliski_adlari)
    if hatalar:
        raise AdayHatasi("; ".join(hatalar))


def _farkli_ciftleri(kayit):
    """OI: gövdedeki bütün değişken çiftleri farklı kişi (ÖK-005 taslağı §6)."""
    if kayit["oi"]:
        return tuple(itertools.combinations(sorted(_degiskenler(kayit)), 2))  # K-041: OI = bütün değişken çiftleri
    return tuple(tuple(c) for c in kayit["farkli"])


def hucreye(kayit, esik, guvenilirlik):
    """Çekirdek geçidine verilecek hücre (V-060: halka eşiği ve güvenilirlik ayardan)."""
    halkalar = tuple(Halka(h["gen"], h["sol"], h["sag"], esik) for h in kayit["halkalar"])
    s = kayit["sonuc"]
    return Hucre(kayit["kimlik"], halkalar, Sonuc(s["gen"], s["sol"], s["sag"]), guvenilirlik, _farkli_ciftleri(kayit))


def kanonik_kimlik(kayit, algoritma):
    """ÖK-005 taslağı §13.1: OI açılmış kuralın `kanonik_bicim` çıktısının kanonik JSON özeti; eşik ve güvenilirlik girmez."""
    return ozet(kanonik_json(kanonik_bicim(hucreye(kayit, None, None))), algoritma)


def kirmizi_dosyasi_denetle(veri, iliski_adlari, tur, en_az_aile, aile_basina, yasak_adlar):
    """Kırmızı takım dosyasının biçimi ve sayıları. Dönüş yalnız sayılardır (aile adları dönmez)."""
    hatalar = [f"dosya.{h}" for h in _sema(KIRMIZI_SEMASI).hatalar(veri)]
    if hatalar:
        raise AdayHatasi("; ".join(hatalar))
    if veri["dosya_turu"] != tur:
        hatalar.append("dosya.dosya_turu: beklenen tür değil")
    adlar = [a["ad"] for a in veri["aileler"]]
    if len(set(adlar)) != len(adlar):
        hatalar.append("dosya.aileler: yinelenen aile adı")
    if set(adlar) & set(yasak_adlar):
        hatalar.append("dosya.aileler: görünür aile adlarından biri kullanılmış")
    if len(set(adlar)) < en_az_aile:
        hatalar.append("dosya.aileler: aile sayısı yetersiz")
    sayac, kimlikler = Counter(), Counter()
    for i, k in enumerate(veri["adaylar"]):
        yer = f"dosya.adaylar[{i}]"
        alt = aday_hatalari(k, iliski_adlari, yer)
        hatalar.extend(alt)
        if alt or not isinstance(k, dict):
            continue
        kimlikler[k["kimlik"]] += 1
        if k["kaynak"]["tur"] != tur:
            hatalar.append(f"{yer}.kaynak.tur: dosya türüyle uyuşmuyor")
        if k["kaynak"]["aile"] not in adlar:
            hatalar.append(f"{yer}.kaynak.aile: dosyanın aile listesinde yok")
        else:
            sayac[k["kaynak"]["aile"]] += 1
    if any(n > 1 for n in kimlikler.values()):
        hatalar.append("dosya.adaylar: yinelenen kimlik")
    en_kucuk = min(sayac[a] for a in set(adlar))
    if en_kucuk < aile_basina:
        hatalar.append("dosya.adaylar: en az bir ailede aday sayısı yetersiz")
    if hatalar:
        raise AdayHatasi("; ".join(hatalar))
    return {"aile_sayisi": len(set(adlar)), "aday_sayisi": len(veri["adaylar"]), "en_kucuk_aile": en_kucuk}


def kirmizi_ozeti(yol, iliski_adlari, tur, en_az_aile, aile_basina, yasak_adlar, algoritma):
    """Dosyanın özeti ve sayıları. İçerik yazdırılmaz, döndürülmez."""
    baytlar = Path(yol).read_bytes()
    sayilar = kirmizi_dosyasi_denetle(json.loads(baytlar.decode("utf-8")), iliski_adlari, tur, en_az_aile,
                                      aile_basina, yasak_adlar)
    return {**sayilar, "ozet": ozet(baytlar, algoritma)}


def main(arg):
    yol, tur = arg
    ayar = ayar_yukle(KOK / "config.json")
    h2 = ayar_yukle(KOK / "config_h2.json")
    adlar = frozenset(iliski_semasi_yukle(*ILISKI_SEMASI).adlar)
    gizli = tur == KIRMIZI_TURLERI[1]
    sonuc = kirmizi_ozeti(yol, adlar, tur, h2.deger("kirmizi_gizli_aile_sayisi") if gizli else 1,
                          h2.deger("kirmizi_aile_basina") if gizli else 0,
                          h2.deger("kirmizi_gorunur_aileler") if gizli else (), ayar.deger("hash_algoritmasi"))
    print(json.dumps(sonuc, ensure_ascii=False))  # V-060: yalnız sayılar ve özet
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
