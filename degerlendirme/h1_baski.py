"""sistem.md §2, §3, §5; ÖK-004 §4: havuz ve eşleşme bütçesi baskısı ölçümü (kapıya girmez, sınırlar değişmez).

Her bölümde çekirdek kapı sınırlarıyla (`h1.kosu_parametreleri`, KIP_KAPI: ÖK-003 eki §6) koşar; sayılar defterin
olaylarından okunur:
- tur: durma turu ve nedeni; tur sınırına ulaştı mı;
- havuz: en yüksek doluluk (kayıt sayısı), havuzdan atılan (ATMA), havuz dolu diye yazılamayan (YEDEK_KULLANILDI);
- eşleşme: bir turdaki en çok eşleşme (ateşleme), bütçeyle atılan, hücre sınırıyla atılan, yeni dayanak getirmediği
  için atılan (C, K-028).
Cevap ancak çekirdek koştuktan sonra kâhin cevabıyla karşılaştırılır. Doğru olmayan bölümde tur sınırına, havuz
sınırına ya da bütçeye ulaşıldıysa hata "sınırla ilişkili" sayılır.
Kullanım: .venv/bin/python -m degerlendirme.h1_baski <bölüm klasörü> <dna> <çıkış klasörü> [gelistirme|kapi]
(gelistirme: `h1_gelistirme_tohumlari`, varsayılan; kapi: kapı tohumları, tohum kaydından (K-030). Bölmeler:
geliştirme + kapı bölmeleri.)
"""
import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.altyapi.olay_gunlugu import YEDEK_KULLANILDI
from cekirdek.defter import ATESLEME, ATMA, YAZMA, Defter
from cekirdek.dongu import DAYANAK_YOK, DURMA_TUR_SINIRI, calistir
from cekirdek.havuz import Havuz
from cekirdek.plazma import cevapla
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1

ATILDI = "ESLESME_ATILDI"  # cekirdek/dongu.py olay türü
BUTCE, HUCRE = "butce", "hucre_siniri"  # cekirdek/dongu.py ESLESME_ATILDI nedenleri
IS_SAYISI = 4  # V-057: paralel süreç sayısı (sonucu etkilemez)
SINIR_ALANLARI = ("tur_siniri", "havuz_doldu", "butce_asildi")  # ÖK-004 §4: hata bunlardan biriyle "sınırla ilişkili"
GELISTIRME, KAPI = "gelistirme", "kapi"  # ölçülecek tohumlar


def bolum_baskisi(bolum, hucreler, iliski_semasi, kk, prm, gunluk_ayari):
    havuz = Havuz(prm.kapasite, kk)
    for o in bolum["olgular"]:
        havuz.epitop_ekle(o["ozne"], o["iliski"], o["nesne"], guven=o["guven"])
    sorgu = (bolum["sorgu"]["ozne"], bolum["sorgu"]["nesne"])
    defter = Defter(None, **gunluk_ayari)
    dongu = calistir(hucreler, havuz, kk, prm, defter, iliski_semasi=iliski_semasi, sorgu=sorgu)
    cevap = cevapla(havuz, sorgu, defter).iliski
    doluluk = en_cok = len(bolum["olgular"])
    eslesme, atilan = Counter(), Counter()
    for k in defter.kayitlar():
        if k["tur"] == YAZMA:
            doluluk += 1
            en_cok = max(en_cok, doluluk)
        elif k["tur"] == ATMA:
            doluluk -= 1
        elif k["tur"] == ATESLEME:
            eslesme[k["veri"]["tur"]] += 1
        elif k["tur"] == ATILDI:
            atilan[k["veri"]["neden"]] += k["veri"]["sayi"]
    return {"cevap": cevap, "tur": dongu.tur, "durma": dongu.durma_nedeni,
            "tur_siniri": dongu.durma_nedeni == DURMA_TUR_SINIRI, "en_cok_doluluk": en_cok,
            "atma": defter.sayac(ATMA), "yedek": defter.sayac(YEDEK_KULLANILDI),
            "en_cok_eslesme": max(eslesme.values(), default=0), "butce_atilan": atilan[BUTCE],
            "hucre_atilan": atilan[HUCRE], "dayanaksiz": atilan[DAYANAK_YOK]}


def ozetle(satirlar):
    ozet = {}
    for bolme in sorted({s["bolme"] for s in satirlar}):
        sec = [s for s in satirlar if s["bolme"] == bolme]
        for s in sec:
            s["havuz_doldu"] = bool(s["atma"] or s["yedek"])
            s["butce_asildi"] = bool(s["butce_atilan"])
        hatali = [s for s in sec if s["cevap"] != s["beklenen"]]
        ozet[bolme] = {"n": len(sec), "dogru": len(sec) - len(hatali),
                       "tur_siniri": sum(s["tur_siniri"] for s in sec),
                       "havuz_doldu": sum(s["havuz_doldu"] for s in sec),
                       "butce_asildi": sum(s["butce_asildi"] for s in sec),
                       "hucre_siniri_kesti": sum(1 for s in sec if s["hucre_atilan"]),
                       "en_cok_doluluk": max(s["en_cok_doluluk"] for s in sec),
                       "en_cok_eslesme": max(s["en_cok_eslesme"] for s in sec),
                       "en_cok_tur": max(s["tur"] for s in sec),
                       "sinirla_iliskili_hata": sum(1 for s in hatali if any(s[a] for a in SINIR_ALANLARI))}
    return ozet


def olcum_tohumlari(ayar, klasor, kip):
    if kip == GELISTIRME:
        return ayar.deger("h1_gelistirme_tohumlari")
    if kip == KAPI:
        return h1.kapi_tohumlari(klasor, ayar.deger("h1_tohumlar"), ayar.deger("h1_tohum_degisim_siniri"),
                                 ayar.deger("h1_onayli_tohum_degisimleri"))
    raise ValueError(f"bilinmeyen tohum kipi: {kip}")


def _bolme_olc(is_):
    import torch
    torch.set_num_threads(1)  # V-057: süreç başına tek iş parçacığı
    kok, klasor, dna_yolu, tohum, bolme = is_
    ayar, sema, gunluk = h1._ortam(kok)
    hucreler = h1._dna(kok, dna_yolu, sema)
    kk = HizliKodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu"))
    prm = h1.kosu_parametreleri(ayar, h1.KIP_KAPI)
    bolumler, cevaplar = h1.bolme_dosyalari(klasor, tohum, bolme, gunluk["algoritma"])
    return [dict(bolum_baskisi(b, hucreler, sema, kk, prm, gunluk), bolme=bolme, tohum=tohum, beklenen=c["cevap"])
            for b, c in zip(bolumler, cevaplar)]


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    klasor, dna_yolu, cikis, *kip = arg
    ayar, _, _ = h1._ortam(kok)
    tohumlar = olcum_tohumlari(ayar, klasor, kip[0] if kip else GELISTIRME)
    prm = h1.kosu_parametreleri(ayar, h1.KIP_KAPI)
    bolmeler = ayar.deger("h1_gelistirme_bolmeleri") + ayar.deger("h1_kapi_bolmeleri")
    isler = [(kok, klasor, dna_yolu, t, b) for t in tohumlar for b in bolmeler]
    with ProcessPoolExecutor(IS_SAYISI) as havuz:
        satirlar = [s for parca in havuz.map(_bolme_olc, isler) for s in parca]
    rapor = {"dna": Path(dna_yolu).name, "tohumlar": tohumlar, "sinirlar": {"tur": prm.tur_siniri, "havuz": prm.kapasite, "butce": prm.butce,
                                                      "hucre": prm.hucre_yazma_siniri},
             "ozet": ozetle(satirlar)}
    Path(cikis).mkdir(parents=True, exist_ok=True)
    atomik_yaz(Path(cikis) / "baski_ozet.json", kanonik_json(rapor))
    atomik_yaz(Path(cikis) / "baski_satirlari.jsonl", b"".join(kanonik_json(s) + b"\n" for s in satirlar))
    print(json.dumps(rapor, ensure_ascii=False, indent=1))  # V-057: okunur çıktı
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
