"""sistem.md §8, §18, EK A P7; K-035, K-036, V-057, V-058: A6 gösterimi (gerçek DNA, gözlemli veri).

DNA'nın her kuralı (bellek boş) ve sonucu bozulmuş sürümleri bellek geçidinden geçirilir. Bozma: sonucu temel bir ilişki
olan kuralın sonucu, temel ilişkiler listesinde bir sonrakiyle değiştirilir (A6 önceki ölçümüyle aynı). Gözlem bölümleri
iki ortamdan gelir: olağan (eğitim uzunluğu) ve kaydırılmış (test uzunluğu, sistem.md §10). Geçit etiket görmez:
"dna"/"bozuk" ayrımı yalnız rapordadır. Her kural için onaylı karar (müdahale a·b·c, K-021) ve V-058 önerisinin kararı
(müdahale b·c) birlikte yazılır; öneri uygulanmış sayılmaz.

Kullanım: .venv/bin/python -m degerlendirme.a6_gosterim <dna.json> <cikis.json> [bolum_sayisi] [is_sayisi]
"""
import json
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.bellek_gecidi import GecitEsikleri, karar_ver
from cekirdek.dna import dna_kur
from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1, uretec
from degerlendirme.bellek_hatti import degerlendir
from degerlendirme.dunya import tanimlar_yukle

KOK = Path(__file__).resolve().parents[1]

BOLUM_SAYISI = 8  # V-057: ortam başına gözlem bölümü (gösterim süresini sınırlar)
IS_SAYISI = 4  # V-057: paralel süreç sayısı (sonucu etkilemez: her kural ayrı koşar)
DNA_BICIMI = KOK / "sema" / "dna_v2.schema.json"
_DURUM = {}


def tanimlar(kok, sema):
    return tanimlar_yukle(kok / "degerlendirme" / "veri" / "tanimlar_v1.json",
                          kok / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)


def ortamlar(kok, sayi):
    ayar, sema, _ = h1._ortam(kok)
    t, prm = tanimlar(kok, sema), uretec.Parametreler.ayardan(ayar)
    return {"olagan": uretec.gozlem_bolumleri(t, prm, "olagan", sayi, prm.egitim_k),
            "kaydirilmis": uretec.gozlem_bolumleri(t, prm, "kaydirilmis", sayi, prm.test_k)}


def bozuk_surumler(hucreler, temel):
    temel = list(temel)
    return [dict(h, kimlik=h["kimlik"] + "_bozuk",
                 sonuc=dict(h["sonuc"], gen=temel[(temel.index(h["sonuc"]["gen"]) + 1) % len(temel)]))
            for h in hucreler if h["sonuc"]["gen"] in temel]


def _hazirla(kok, sayi):
    import torch
    torch.set_num_threads(1)  # V-057: süreç başına tek iş parçacığı
    ayar, sema, gunluk = h1._ortam(kok)
    _DURUM.update(kok=kok, sema=sema, gunluk=gunluk, ortamlar=ortamlar(kok, sayi), esik=GecitEsikleri.ayardan(ayar),
                  prm=h1.kosu_parametreleri(ayar, h1.KIP_KAPI),
                  kk=HizliKodKitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu")))


def kural_kos(is_):
    etiket, veri = is_
    d = _DURUM
    hucre = dna_kur({"sema_surumu": "2", "hucreler": [veri]}, DNA_BICIMI, d["sema"])[0]
    k = degerlendir(hucre, (), d["ortamlar"], d["sema"], d["kk"], d["prm"], d["gunluk"], d["esik"])
    oneri = k if "esdeger" in k.olcumler else karar_ver(
        False, {a: dict(o, mudahale=o["mudahale_bc"]) for a, o in k.olcumler.items()}, d["esik"])
    return {"etiket": etiket, "kimlik": veri["kimlik"], "karar": [k.karar, k.neden], "oneri": [oneri.karar, oneri.neden],
            "olcumler": k.olcumler}


def ozet(sonuclar):
    tablo = {}
    for alan in ("karar", "oneri"):
        for etiket in ("dna", "bozuk"):
            sayac = Counter("/".join(str(x) for x in s[alan] if x) for s in sonuclar if s["etiket"] == etiket)
            tablo[f"{alan}:{etiket}"] = dict(sorted(sayac.items()))
    return tablo


def main(arg):
    dna_yolu, cikis, *secenek = arg
    dna_yolu, cikis = Path(dna_yolu), Path(cikis)
    sayi, is_sayisi = map(int, secenek + [BOLUM_SAYISI, IS_SAYISI][len(secenek):])
    _, sema, _ = h1._ortam(KOK)
    dna = json.loads(dna_yolu.read_text(encoding="utf-8"))["hucreler"]
    isler = [("dna", h) for h in dna] + [("bozuk", h) for h in bozuk_surumler(dna, tanimlar(KOK, sema).olgu_iliskileri)]
    with ProcessPoolExecutor(is_sayisi, initializer=_hazirla, initargs=(KOK, sayi)) as havuz:
        sonuclar = list(havuz.map(kural_kos, isler))
    rapor = {"dna": dna_yolu.name, "bolum_sayisi": sayi, "ozet": ozet(sonuclar), "kurallar": sonuclar}
    atomik_yaz(cikis, kanonik_json(rapor))
    print(json.dumps(rapor["ozet"], ensure_ascii=False, indent=1))  # V-057: okunur çıktı
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
