"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A6 koduna kasıtlı hata sokar.

Kullanım: .venv/bin/python araclar/mutasyon_a6.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

H2 = "degerlendirme/h2.py"
DUN = "degerlendirme/dunya.py"
GEC = "cekirdek/bellek_gecidi.py"
BEL = "cekirdek/bellek.py"
ICD = "cekirdek/ic_dil.py"

MUTASYONLAR = [
    # K-032 §4: H2 kapısı
    ("V-053 durumu denetlenmiyor", H2, "    if karar is None:\n        _ret(", "    if False:\n        _ret("),
    ("kapatan kararda kullanıcı onayı aranmıyor", H2,
     ' or not re.search(r"^- \\*\\*Onaylayan:\\*\\* kullanıcı", kayit, re.M)', ""),
    ("kapatan kararda V-053 aranmıyor", H2, ' or "V-053" not in kayit', ""),
    ("ÖK-004 sonucu aranmıyor", H2, "    if sonuc is None or not yol.exists():", "    if not yol.exists():\n        sonuc = ''\n    if False:"),
    ("özet karşılaştırılmıyor", H2, "    if hashlib.sha256(baytlar).hexdigest() not in sonuc:", "    if False:"),
    ("eski tohum denetlenmiyor", H2, "    if not tohumlar or KULLANILMIS_H1_TOHUMLARI.intersection(tohumlar):",
     "    if not tohumlar:"),
    ("ÖK-003 tohumları kullanılmış sayılmıyor", H2, "frozenset(range(7, 18))", "frozenset(range(7, 12))"),
    ("tohumsuz özet kabul ediliyor", H2, "    if not tohumlar or KULLANILMIS_H1_TOHUMLARI",
     "    if KULLANILMIS_H1_TOHUMLARI"),
    ("komut kapıyı atlıyor", H2, "    try:\n        kapi_denetle(kok)\n", "    try:\n        pass\n"),
    # V-053: olgulardan çıkarılabilirlik
    ("çocuğun iki ebeveyni evlendirilmiyor", DUN, "            if len(u) == EBEVEYN_SAYISI:\n                a, b = sorted(u)",
     "            if False:\n                a, b = sorted(u)"),
    ("kardeşler birleştirilmiyor", DUN, "        sinif.birlestir(a, b)\n    degisti = True", "        sinif.bul(b)\n    degisti = True"),
    ("bir kişinin çocukları aynı çifte bağlanmıyor", DUN, "                    degisti |= sinif.birlestir(sinifi[e], k)",
     "                    pass"),
    ("ebeveynin eşi ebeveyn sayılmıyor", DUN, "                if e in es and es[e] not in u:", "                if False:"),
    ("olgu tipi alınmıyor", DUN, "            if tip.setdefault(y, t) != t:", "            if False:"),
    ("beklenen cevap karşılaştırılmıyor", DUN, "    if dunya.iliski(*sorgu_d, tanimlar) != cevap:\n        return False",
     "    if False:\n        return False"),
    ("aynı cinsten evli çift denetlenmiyor", DUN, "        if tipler[p] == tipler[q]:", "        if False:"),
    ("ikiden çok ebeveyn denetlenmiyor", DUN, "            if len(u) > EBEVEYN_SAYISI:", "            if False:"),
    # V-054: bellek geçidi
    ("destekte kök-ayrıklık aranmıyor", GEC, 'any(olgu_kimligi[u] not in v["kokler"] for v in vs)', "True"),
    ("olguyla karşıtlık çelişki sayılıyor", GEC, "(karsitlik if a in epitop or b in epitop else celiski)",
     "(celiski if a in epitop or b in epitop else karsitlik)"),
    ("soy türeyenleri kapsamıyor", GEC, ' or soy.intersection(v["ebeveynler"])', ""),
    ("en kötü ortam aranmıyor", GEC, "    if olculen and min(olculen) < esikler.dogruluk:", "    if False:"),
    ("çelişki denetlenmiyor", GEC, '    if sum(o["celiski"] for o in olcum.values()):', "    if False:"),
    ("katkı denetlenmiyor", GEC, '    if not sum(o["katki"] for o in olcum.values()):', "    if False:"),
    ("müdahale eşiği uygulanmıyor", GEC, "    if sum(puanlar) / len(puanlar) < esikler.mudahale:", "    if False:"),
    ("dış skor kanalı açık", GEC, "    if dis_kanit is not None:\n        raise NotImplementedError",
     "    if False:\n        raise NotImplementedError"),
    ("eşdeğerlikte halka sırası denenmiyor", GEC, "    for sira in itertools.permutations(hucre.halkalar):",
     "    for sira in [hucre.halkalar]:"),
    ("bellekteki kimlik denetlenmiyor", GEC, "    if aday.kimlik in {h.kimlik for h in bellek}:", "    if False:"),
    ("gözden geçirme geri almıyor", GEC, "            bellek_deposu.geri_al(h.kimlik, k.neden)\n", "            pass\n"),
    # V-056: bellek deposu
    ("geri alma aktiften düşürmüyor", BEL, '            self._aktif.pop(veri["kimlik"], None)', "            pass"),
    ("çift kabul denetlenmiyor", BEL, '        if hucre_verisi["kimlik"] in self._aktif:', "        if False:"),
    ("bellek kopya vermiyor", BEL, "copy.deepcopy(self._aktif[k])", "self._aktif[k]"),
    # V-055: iç dil
    ("iç dil özeti denetlenmiyor", ICD, '    if kayit["ozet"] != _ozet(kayit, algoritma):', "    if False:"),
    ("LLM karantinası yok", ICD, '    if kayit["kaynak"] == LLM_KAYNAGI:', "    if False:"),
    ("olumsuz kutup havuza giriyor", ICD, '    if kayit["kutup"] != OLUMLU or ', "    if "),
    ("onaysız ilişki kabul ediliyor", ICD, '    if kayit["iliski"] not in iliski_semasi:', "    if False:"),
]


def main(secilen=None):
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':40} {sayac}", flush=True)
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    kacan, liste = 0, [m for m in MUTASYONLAR if secilen is None or m[0] in secilen]
    for ad, dosya, eski, yeni in liste:
        if (KOK / dosya).read_text(encoding="utf-8").count(eski) != 1:
            print(f"ÇAPA YOK  {ad}")
            kacan += 1
            continue
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:40} {sayac}", flush=True)
    print(f"MUTASYON: toplam={len(liste)} yakalanan={len(liste) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
