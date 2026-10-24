"""sistem.md §13 (H1), ÖK-002 §6, V-047: H1 hatalarının incelemesi (yalnız teşhis; ayar, DNA, kapı sonucu değişmez).

Hatalı her bölüm, sınırlar gevşetilerek yeniden koşturulur: yalnız tur sınırı, yalnız havuz, ikisi birden. Cevap
doğrulaşırsa hata ilgili "sınır yetmedi" sınıfına girer; hiçbirinde doğrulaşmazsa "sınırdan bağımsız" olur ve elle
incelenir (DNA eksiği, olgulardan türetilemezlik ya da ara akrabalığın şemada adı olmaması). Kâhin tarafındadır.

Kullanım: .venv/bin/python -m degerlendirme.h1_inceleme <bölüm klasörü> <dna> <kapı çıkışı>
"""
import dataclasses
import json
import sys
from collections import Counter
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.defter import ATMA, Defter
from cekirdek.dongu import CekirdekParametreleri, calistir
from cekirdek.havuz import Havuz
from cekirdek.plazma import cevapla
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1

TUR_CARPANI = 4  # V-047: teşhiste tur sınırı bu kadar katlanır
HAVUZ_CARPANI = 32  # V-047: teşhiste havuz bu kadar katlanır
SINIR_TUR, SINIR_HAVUZ, SINIR_IKISI = "tur_yetmedi", "havuz_yetmedi", "tur_ve_havuz_yetmedi"  # ÖK-002 §6 (1)
SINIRDAN_BAGIMSIZ = "sinirdan_bagimsiz"  # ÖK-002 §6 (2)–(4): elle incelenir
OZET_ON_EKI = 12  # V-047: raporda bölüm özetinin gösterilen ilk karakter sayısı


def _cevap(bolum, hucreler, iliski_semasi, kk, prm, gunluk_ayari):
    havuz = Havuz(prm.kapasite, kk)
    for o in bolum["olgular"]:
        havuz.epitop_ekle(o["ozne"], o["iliski"], o["nesne"], guven=o["guven"])
    defter = Defter(None, **gunluk_ayari)
    sorgu = (bolum["sorgu"]["ozne"], bolum["sorgu"]["nesne"])
    calistir(hucreler, havuz, kk, prm, defter, iliski_semasi=iliski_semasi, sorgu=sorgu)
    return cevapla(havuz, sorgu, defter).iliski


def teshis(bolum, cevap_kaydi, hucreler, iliski_semasi, kk, prm, gunluk_ayari):
    if bolum["ozet"] != cevap_kaydi["bolum_ozeti"]:
        raise h1.H1Hatasi("cevap kaydı başka bölümün")
    tur = dataclasses.replace(prm, tur_siniri=prm.tur_siniri * TUR_CARPANI)
    havuz = dataclasses.replace(prm, kapasite=prm.kapasite * HAVUZ_CARPANI)
    ikisi = dataclasses.replace(tur, kapasite=havuz.kapasite)
    cevaplar = {ad: _cevap(bolum, hucreler, iliski_semasi, kk, p, gunluk_ayari)
                for ad, p in (("olagan", prm), ("genis_tur", tur), ("genis_havuz", havuz), ("ikisi", ikisi))}
    beklenen = cevap_kaydi["cevap"]
    sinif = next((s for ad, s in (("genis_tur", SINIR_TUR), ("genis_havuz", SINIR_HAVUZ), ("ikisi", SINIR_IKISI))
                  if cevaplar[ad] == beklenen), SINIRDAN_BAGIMSIZ)
    return dict(cevaplar, bolum_ozeti=bolum["ozet"], beklenen=beklenen, sinif=sinif)


def okunur(bolum):
    satirlar = [f"{o['ozne']} —{o['iliski']}→ {o['nesne']}" for o in bolum["olgular"]]
    return "\n".join(satirlar + [f"soru: {bolum['sorgu']['ozne']} → {bolum['sorgu']['nesne']}"])


def rapor_metni(kayitlar):
    sayim = Counter((k["bolme"], k["sinif"]) for k in kayitlar)
    satirlar = ["# H1 hata incelemesi (yalnız teşhis)", "",
                "Bu dosya test bölmelerinin cevaplarını içerir. DNA ve ayarlar buna bakılarak değiştirilmez (ÖK-002 §6).",
                "", "| Bölme | Sınıf | Sayı |", "|---|---|---|"]
    satirlar += [f"| {b} | {s} | {n} |" for (b, s), n in sorted(sayim.items())]
    for k in kayitlar:
        satirlar += ["", f"## {k['bolme']} / tohum {k['tohum']} / {k['bolum_ozeti'][:OZET_ON_EKI]}", "",
                     f"- beklenen: {k['beklenen']}; verilen: {k['cevap']}; durma: {k['durma']}, tur {k['tur']}, "
                     f"atma {k['atma']}; adaylar: {k['adaylar']}",
                     f"- teşhis: {k['sinif']} (tur ×{TUR_CARPANI}: {k['genis_tur']}; havuz ×{HAVUZ_CARPANI}: "
                     f"{k['genis_havuz']}; ikisi: {k['ikisi']})", "", "```", k["okunur"], "```"]
    return "\n".join(satirlar) + "\n"


def main(arg):
    if len(arg) != len(("klasor", "dna", "cikis")):
        print(__doc__)
        return 1
    klasor, dna_yolu, cikis = arg
    kok = Path(__file__).resolve().parents[1]
    ayar, sema, gunluk = h1._ortam(kok)
    hucreler = h1._dna(kok, dna_yolu, sema)
    kk = HizliKodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu"))
    prm = CekirdekParametreleri.ayardan(ayar)
    kayitlar = []
    for yol in sorted(Path(cikis).glob("*_t*.jsonl")):
        satirlar = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()]
        hatalar = [s for s in satirlar if not s["dogru"]]
        if not hatalar:
            continue
        bolme, tohum = hatalar[0]["bolme"], hatalar[0]["tohum"]
        bolumler, cevaplar = h1.bolme_dosyalari(klasor, tohum, bolme, gunluk["algoritma"])
        dizin = {b["ozet"]: (b, c) for b, c in zip(bolumler, cevaplar)}
        for s in hatalar:
            b, c = dizin[s["bolum_ozeti"]]
            t = teshis(b, c, hucreler, sema, kk, prm, gunluk)
            if t["olagan"] != s["cevap"]:
                raise h1.H1Hatasi(f"{s['bolum_ozeti']}: yeniden koşu aynı cevabı vermedi (belirlenim bozuk)")
            kayitlar.append(dict(t, bolme=bolme, tohum=tohum, cevap=s["cevap"], durma=s["durma"], tur=s["tur"],
                                 atma=s["atma"], adaylar=s["adaylar"], okunur=okunur(b)))
        print(f"{bolme} / tohum {tohum}: {len(hatalar)} hata incelendi")
    atomik_yaz(Path(cikis) / "hata_incelemesi.json", kanonik_json(kayitlar))
    atomik_yaz(Path(cikis) / "RAPOR_hatalar.md", rapor_metni(kayitlar).encode("utf-8"))
    sayim = Counter((k["bolme"], k["sinif"]) for k in kayitlar)
    print(json.dumps({f"{b}/{s}": n for (b, s), n in sorted(sayim.items())}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
