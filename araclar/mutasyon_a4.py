"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A4 (defter, çelişki, müdahale) koduna kasıtlı hata sokar.

Kullanım: python3 araclar/mutasyon_a4.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

DEF = "cekirdek/defter.py"
DON = "cekirdek/dongu.py"
PLA = "cekirdek/plazma.py"
MUD = "cekirdek/mudahale.py"
GUN = "cekirdek/altyapi/olay_gunlugu.py"

MUTASYONLAR = [
    ("iz kuralı yok", PLA, " and defter.yazildi_mi(k.kimlik):", ":"),
    ("ateşleme kaydedilmiyor", DON, "        for e in es:\n            olaylar.append((ATESLEME",
     "        for e in []:\n            olaylar.append((ATESLEME"),
    ("yazmada kök kümesi boş", DON, '"kokler": sorted(kok_kumesi(havuz, k.kimlik))', '"kokler": []'),
    ("atma dizine işlenmiyor", DEF, '            self._atilan.add(veri["kimlik"])', "            pass"),
    ("toplu yazım dosyaya yazmıyor", GUN, "        if self.yol is not None and satirlar:", "        if False:"),
    ("defter tipi denetimi yok", DON, "    if not isinstance(gunluk, Defter):", "    if False:"),
    ("dışlayıcı denetimi yok", DEF, "and r1 != r2 and iliski_semasi.dislayici_mi(r1, r2):", "and False:"),
    ("işlevsel denetimi yok", DEF, "and o1 != o2 and iliski_semasi.islevsel(r1):", "and False:"),
    ("ters denetimi yok", DEF, "            and r2 not in iliski_semasi.ters(r1):", "            and False:"),
    ("tanımsız ters koşulu yok", DEF, "and s1 != o1 and iliski_semasi.ters(r1) and iliski_semasi.ters(r2) \\",
     "and s1 != o1 \\"),
    ("ortak destek birleşim", DEF, "kok_kumesi(havuz, a.kimlik) & kok_kumesi(havuz, b.kimlik)",
     "kok_kumesi(havuz, a.kimlik) | kok_kumesi(havuz, b.kimlik)"),
    ("turda çelişki denetimi yok", DON, "        gunluk.celiski_denetle(havuz, iliski_semasi, tur)\n", ""),
    ("çelişki yinelemesi süzülmüyor", DEF, "                    if (tur_adi, a.kimlik, b.kimlik) in self._celiskiler:",
     "                    if False:"),
    ("(a) eşitlik düşüş sayılıyor", MUD, '"dustu": yeni < cevap.guven', '"dustu": yeni <= cevap.guven'),
    ("(a) budama yok", MUD, "if silinen_epitop not in kok_kumesi(havuz, k.kimlik)]", "]"),
    ("(b) ilgisiz tanımı yok", MUD, "        if s in yol_varliklari or o in yol_varliklari:\n            continue\n", ""),
    ("(b) sınanamadı başarı sayılıyor", MUD, "    b = None if sinanamadi else", "    b = 1.0 if sinanamadi else"),
    ("(b) yedek varlık çakışıyor", MUD, "yeni_ozne, yeni_nesne = en_buyuk + 1, en_buyuk + 2",
     "yeni_ozne, yeni_nesne = en_buyuk, en_buyuk + 1"),
    # Not: c formülünden yalnız ters_tutarli'yı çıkaran mutant eşdeğerdir (K-020'ye göre ters tutarsızlık her zaman
    # ters çelişkisi olarak da deftere düşer); bu yüzden raporlanan ters_tutarli alanı bozulur.
    ("(c) ters tutarlılığı hep doğru", MUD, "    ters_tutarli = ters.iliski is None or tanimsiz or ters.iliski in adaylar",
     "    ters_tutarli = True"),
    ("(c) çelişki puana girmiyor", MUD, "    c = 1 if ters_tutarli and not celiski_var else 0", "    c = 1 if ters_tutarli else 0"),
    ("puan çarpım yerine ortalama", MUD, "puan = None if sinanamadi else a * b * c",
     "puan = None if sinanamadi else (a + b + c) / 3"),
    ("karşı-olgusal koşu ana deftere yazıyor", MUD, "    bellek = _bellek_defteri(defter)\n", "    bellek = defter\n"),
]


def main():
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':40} {sayac}")
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    kacan = 0
    for ad, dosya, eski, yeni in MUTASYONLAR:
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:40} {sayac}")
    print(f"MUTASYON: toplam={len(MUTASYONLAR)} yakalanan={len(MUTASYONLAR) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
