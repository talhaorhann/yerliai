"""sistem.md §13 (H1), K-029, ÖK-003 §3.4, V-049: tur ve havuz sınırlarının geliştirme verisinde seçimi.

Kural (ÖK-003 §3.4, veriden önce yazıldı): önce en büyük havuzda, doğru sayısı en büyük turdakine eşit olan en küçük
tur; sonra o turla, doğru sayısı en büyük havuzdakine eşit olan en küçük havuz. Ölçüm yalnız çekirdek + plazmadır
(müdahale testi doğruluğu etkilemez). Ölçülen her değer tabloya yazılır; seçim kuralı harfiyen uygulanır.
Kâhin tarafındadır: cevaplar yalnız burada okunur.

Kullanım: .venv/bin/python -m degerlendirme.h1_sinir <eski bölüm klasörü> <dna> <çıkış>
"""
import dataclasses
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.defter import Defter
from cekirdek.dongu import CekirdekParametreleri, calistir
from cekirdek.havuz import Havuz
from cekirdek.plazma import cevapla
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1


def _cevap(bolum, hucreler, iliski_semasi, kk, prm, gunluk_ayari):
    havuz = Havuz(prm.kapasite, kk)
    for o in bolum["olgular"]:
        havuz.epitop_ekle(o["ozne"], o["iliski"], o["nesne"], guven=o["guven"])
    defter = Defter(None, **gunluk_ayari)
    sorgu = (bolum["sorgu"]["ozne"], bolum["sorgu"]["nesne"])
    calistir(hucreler, havuz, kk, prm, defter, iliski_semasi=iliski_semasi, sorgu=sorgu)
    return cevapla(havuz, sorgu, defter).iliski


def dogru_sayisi(klasor, tohumlar, bolmeler, hucreler, iliski_semasi, kk, prm, gunluk_ayari):
    toplam = 0
    for tohum in tohumlar:
        for bolme in bolmeler:
            bolumler, cevaplar = h1.bolme_dosyalari(klasor, tohum, bolme, gunluk_ayari["algoritma"])
            toplam += sum(1 for b, c in zip(bolumler, cevaplar)
                          if _cevap(b, hucreler, iliski_semasi, kk, prm, gunluk_ayari) == c["cevap"])
    return toplam


def sinirli(prm, tur, havuz):
    return dataclasses.replace(prm, tur_siniri=tur, kapasite=havuz)


def sec(olc, tur_adaylari, havuz_adaylari):
    """ÖK-003 §3.4. `olc(tur, havuz)` doğru sayısını verir; her ölçüm bir kez yapılır."""
    olcum = {}

    def bellekli(tur, havuz):
        if (tur, havuz) not in olcum:
            olcum[(tur, havuz)] = olc(tur, havuz)
        return olcum[(tur, havuz)]

    en_buyuk_havuz = max(havuz_adaylari)
    hedef = bellekli(max(tur_adaylari), en_buyuk_havuz)
    tur = next(t for t in sorted(tur_adaylari) if bellekli(t, en_buyuk_havuz) == hedef)
    hedef = bellekli(tur, en_buyuk_havuz)
    havuz = next(h for h in sorted(havuz_adaylari) if bellekli(tur, h) == hedef)
    return {"tur": tur, "havuz": havuz, "olcum": olcum}


def _is(arg):
    """Süreç işi: bir bölme-tohum dosyasının doğru sayısı (her süreç kendi DNA'sını ve kod kitabını kurar)."""
    import torch
    torch.set_num_threads(1)  # V-049: paralel süreçlerde iş parçacığı taşmasını önler; sonuç değişmez (V-040 testi)
    kok, klasor, dna_yolu, tohum, bolme, tur, havuz = arg
    ayar, sema, gunluk = h1._ortam(kok)
    hucreler = h1._dna(kok, dna_yolu, sema)
    kk = HizliKodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu"))
    prm = sinirli(CekirdekParametreleri.ayardan(ayar), tur, havuz)
    return dogru_sayisi(klasor, [tohum], [bolme], hucreler, sema, kk, prm, gunluk)


def rapor_metni(secim, toplam):
    satirlar = ["# H1 sınır seçimi (ÖK-003 §3.4)", "", f"Geliştirme verisi: ilk koşunun dört test bölmesi, {toplam} bölüm.",
                "", f"**Seçilen:** tur {secim['tur']}, havuz {secim['havuz']}", "", "| Tur | Havuz | Doğru |", "|---|---|---|"]
    satirlar += [f"| {t} | {h} | {n} |" for (t, h), n in sorted(secim["olcum"].items())]
    return "\n".join(satirlar) + "\n"


def main(arg):
    if len(arg) != len(("klasor", "dna", "cikis")):
        print(__doc__)
        return 1
    klasor, dna_yolu, cikis = arg
    kok = Path(__file__).resolve().parents[1]
    ayar, _, _ = h1._ortam(kok)
    tohumlar, bolmeler = ayar.deger("h1_gelistirme_tohumlari"), ayar.deger("h1_kapi_bolmeleri")
    with ProcessPoolExecutor() as havuz_isci:
        def olc(tur, havuz):
            isler = [(kok, klasor, dna_yolu, t, b, tur, havuz) for t in tohumlar for b in bolmeler]
            n = sum(havuz_isci.map(_is, isler))
            print(f"tur {tur}, havuz {havuz}: {n} doğru", flush=True)
            return n
        secim = sec(olc, ayar.deger("h1_tur_adaylari"), ayar.deger("h1_havuz_adaylari"))
    toplam = len(tohumlar) * len(bolmeler) * ayar.deger("ana_kume_sayisi")
    Path(cikis).mkdir(parents=True, exist_ok=True)
    atomik_yaz(Path(cikis) / "sinir_secimi.json",
               kanonik_json({"tur": secim["tur"], "havuz": secim["havuz"], "toplam": toplam,
                             "olcum": [[t, h, n] for (t, h), n in sorted(secim["olcum"].items())]}))
    atomik_yaz(Path(cikis) / "RAPOR_sinir.md", rapor_metni(secim, toplam).encode("utf-8"))
    print(rapor_metni(secim, toplam))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
