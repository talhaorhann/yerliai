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
GOZ = "degerlendirme/gozlem_puani.py"
HAT = "degerlendirme/bellek_hatti.py"
URE = "degerlendirme/uretec.py"
H1 = "degerlendirme/h1.py"
BAS = "degerlendirme/h1_baski.py"
ALT = "degerlendirme/altin.py"

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
    # V-054, K-035: bellek geçidi (çekirdek tarafı)
    ("maskelenen olgu çekirdeğe veriliyor", GEC, "    gorunen = [o for i, o in enumerate(olgular) if i != maske]",
     "    gorunen = list(olgular)"),
    ("soy türeyenleri kapsamıyor", GEC, ' or soy.intersection(v["ebeveynler"])', ""),
    ("olgu çelişkisi bellek çelişkisi sayılıyor", GEC, '        if epitop.intersection(k["veri"]["kayitlar"]):',
     '        if not epitop.intersection(k["veri"]["kayitlar"]):'),
    ("katkı belleksiz koşuyla karşılaştırılmıyor", GEC,
     "    katki = sum(1 for u in soy_uclu if u not in tur0 or tur1[u] < tur0[u])", "    katki = len(soy_uclu)"),
    ("az kanıtlı ortam ölçülmüş sayılıyor", GEC, 'if o["kanit"] >= esikler.en_az_kanit]', 'if o["kanit"]]'),
    ("en kötü ortam aranmıyor", GEC, "    if olculen and min(olculen) < esikler.dogruluk:", "    if False:"),
    ("çelişki denetlenmiyor", GEC, '    if sum(o["celiski"] for o in olcum.values()):', "    if False:"),
    ("eşleşme denetlenmiyor", GEC, '    if not sum(o["eslesme"] for o in olcum.values()):', "    if False:"),
    ("katkı denetlenmiyor", GEC, '    if not sum(o["katki"] for o in olcum.values()):', "    if False:"),
    ("geçit müdahalesinde (a) kullanılıyor", GEC, "mudahale, bilesenler = m.b * m.c,", "mudahale, bilesenler = m.puan,"),
    ("müdahale eşiği uygulanmıyor", GEC, "    if sum(puanlar) / len(puanlar) < esikler.mudahale:", "    if False:"),
    ("eşdeğerlikte halka sırası denenmiyor", GEC, "    for sira in itertools.permutations(hucre.halkalar):",
     "    for sira in [hucre.halkalar]:"),
    ("bellekteki kimlik denetlenmiyor", GEC, "    if aday.kimlik in {h.kimlik for h in bellek}:", "    if False:"),
    # K-035: doğruluk hesabı (çekirdek dışı)
    ("bütün gözlemler maskeleniyor", GOZ, " if o[1] == aday.sonuc.gen]", "]"),
    ("maskesiz koşu yapılmıyor", GOZ, "    for maske in [None] + maskelenecekler(aday, olgular):",
     "    for maske in maskelenecekler(aday, olgular):"),
    ("çelişki çifti tekilleştirilmiyor", GOZ, '        yanlis |= _ciftler(ham["olgu_celiskileri"])',
     '        yanlis |= {(len(yanlis), c) for c in _ciftler(ham["olgu_celiskileri"])}'),
    ("bellek çelişkisi toplanmıyor", GOZ, '        celiski |= _ciftler(ham["bellek_celiskileri"])', "        pass"),
    ("yanlış kanıta katılmıyor", GOZ, '    toplam["kanit"] = toplam["dogru"] + toplam["yanlis"]',
     '    toplam["kanit"] = toplam["dogru"]'),
    # K-035: bellek hattı ve bağımsızlık
    ("ortamsız değerlendirme kabul ediliyor", HAT, "    if not ortamlar:\n        raise ValueError",
     "    if False:\n        raise ValueError"),
    ("eşdeğer aday ölçülüyor", HAT, "    if esdeger_mi(aday, bellek):\n        return karar_ver(True, {}, esikler)",
     "    if esdeger_mi(aday, bellek) and False:\n        return karar_ver(True, {}, esikler)"),
    ("kabul edilen belleğe yazılmıyor", HAT, "            depo.kabul_et(veri, k.olcumler)\n", "            pass\n"),
    ("anlatıcıya kararın kendisi veriliyor", HAT, "**dataclasses.asdict(karar)}", "**vars(karar)}"),
    ("metin olmayan anlatıcı çıktısı alınıyor", HAT, "metin if isinstance(metin, str) else None", "metin"),
    ("gözden geçirme geri almıyor", HAT, "            depo.geri_al(h.kimlik, k.neden)\n", "            pass\n"),
    # K-035, V-057: gözlem bölümleri
    ("gözlemde türetilmiş ilişki yok", URE, "for y, r in dunya.iliskiler(x, tanimlar).items() if y in kisiler",
     "for y, r in dunya.iliskiler(x, tanimlar, tanimlar.olgu_iliskileri).items() if y in kisiler"),
    ("dikkat dağıtıcı kişiler alınmıyor", URE,
     "        kisiler = sorted(set(zincir) | {x for x, _r, y in dikkat} | {y for x, _r, y in dikkat})",
     "        kisiler = sorted(set(zincir))"),
    # K-034: V-053 üretece bağlı
    ("üreteç olgu tanımını kullanmıyor", URE, "    if prm.cikarilabilirlik_tanimi == OLGU_TANIMI:  # K-034",
     "    if False:  # K-034"),
    ("bilinmeyen çıkarılabilirlik tanımı kabul ediliyor", URE,
     "    if prm.cikarilabilirlik_tanimi not in (AGAC_TANIMI, OLGU_TANIMI):", "    if False:"),
    ("H1 üretimi tanımı config'ten almıyor", H1,
     ',\n                               cikarilabilirlik_tanimi=ayar.deger("h1_cikarilabilirlik_tanimi"))', ")"),
    ("gözlem ortamı tohuma girmiyor", URE, 'random.Random(f"{prm.tohum}:gozlem:{ortam}")',
     'random.Random(f"{prm.tohum}:gozlem")'),
    # ÖK-004 §4: baskı ölçümü
    ("tur sınırı sayılmıyor", BAS, '"tur_siniri": dongu.durma_nedeni == DURMA_TUR_SINIRI', '"tur_siniri": False'),
    ("atma doluluğu düşürmüyor", BAS, "            doluluk -= 1", "            pass"),
    ("kapı tohumları kayıttan alınmıyor", BAS,
     '        return h1.kapi_tohumlari(klasor, ayar.deger("h1_tohumlar"), ayar.deger("h1_tohum_degisim_siniri"),\n'
     '                                 h1._onaylar(ayar))',
     '        return ayar.deger("h1_tohumlar")'),
    # K-039: tohum değişimi onayı
    ("onaysız tohum değişiyor", H1, "                if tohum not in onayli:\n                    raise H1Hatasi",
     "                if False:\n                    raise H1Hatasi"),
    ("onaydaki yerine tohum denetlenmiyor", H1, "                if onayli[tohum] != siradaki:\n                    raise",
     "                if False:\n                    raise"),
    ("onay kaydında kalan hak denetlenmiyor", H1, '        if k["kalan_hak"] != sinir - len(harita) - 1:\n',
     "        if False:\n"),
    ("kayıttaki onaysız değişim kabul ediliyor", H1, "    if onaysiz:\n        raise H1Hatasi", "    if False:\n        raise H1Hatasi"),
    # K-039: altın küme soru dosyası
    ("JSON cevap biçimi eklenmiyor", ALT, "        satirlar += _json_bicimi(parca_no, len(sorular))", "        pass"),
    ("başka parçanın soruları alınıyor", ALT, ' if k["parca"] == parca_no]', "]"),
    ("cevap kaynağı LLM taslağı sayılmıyor", ALT, "    llm = sum(1 for k in kaynaklar.values() if k == LLM_TASLAGI)",
     "    llm = 0"),
    ("geçersiz cevap harfi kabul ediliyor", ALT, "    gecerli = tuple(HARFLER + EMIN_DEGIL)", "    gecerli = tuple(HARFLER + EMIN_DEGIL + 'E')"),
    ("H1 altın koşusu cevap dosyasını denetlemiyor", H1,
     '            kullanici_cevaplarini_denetle(kullanici[p], p, sum(1 for s in sorular if s["parca"] == p))  # K-039\n', ""),
    # V-056: bellek deposu
    ("geri alma aktiften düşürmüyor", BEL, '            self._aktif.pop(veri["kimlik"], None)', "            pass"),
    ("çift kabul denetlenmiyor", BEL, '        if hucre_verisi["kimlik"] in self._aktif:', "        if False:"),
    ("bellek kopya vermiyor", BEL, "copy.deepcopy(self._aktif[k])", "self._aktif[k]"),
    ("boş bellek DNA kurucuya gidiyor", BEL, " if veriler else ()", ""),
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
