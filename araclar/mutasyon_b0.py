"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): H2 B0 koduna kasıtlı hata sokar (V-064).

Her mutant önce ilgili test modülleriyle (B0 + yapı testleri + H1 üreteç testleri) bir kopyada sınanır; orada kaçarsa
bütün test takımıyla yeniden sınanır. İkisinde de yeşil kalırsa KAÇTI.
Kullanım: .venv/bin/python araclar/mutasyon_b0.py [mutant adı ...]
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import ZAMAN_SINIRI, kopyada_kostur  # noqa: E402

MODULLER = ("testler.test_b0_aday", "testler.test_b0_sablon", "testler.test_b0_sayac", "testler.test_b0_m0",
            "testler.test_b0_dunyalar", "testler.test_b0_butce_bagla", "testler.test_b0_m0_kosucu",
            "testler.test_a0_yapi", "testler.test_a0_yasak_kaliplar", "testler.test_a0_kilit",
            "testler.test_a1_dil_veridir", "testler.test_a1_uretec")  # V-064: hızlı ilk eleme

ADY, TOH, SAB, SAY, M0 = "kesif/aday.py", "kesif/tohum.py", "kesif/sablon.py", "kesif/sayac.py", "kesif/m0.py"
DUN, IKI, HDU = "degerlendirme/dunya.py", "degerlendirme/ikinci_uretec.py", "degerlendirme/h2_dunya.py"
BUT, BAG, HM0 = "degerlendirme/h2_butce.py", "degerlendirme/h2_bagla.py", "degerlendirme/h2_m0.py"
CEK, KIL = "araclar/cekirdek_ozeti.py", "araclar/kilitle.py"

MUTASYONLAR = [
    # tek aday şeması ve kırmızı takım dosyası
    ("şema dışı ilişki kabul", ADY, '        if h["gen"] not in iliski_adlari:', "        if False:"),
    ("baş değişkeni gövdede aranmıyor", ADY, '    if not {s["sol"], s["sag"]} <= govde:', "    if False:"),
    ("oi ile farklı birlikte kabul", ADY, '    if kayit["oi"] and kayit["farkli"]:', "    if False:"),
    ("kırmızı aile denetlenmiyor", ADY, '    if kirmizi != (kayit["kaynak"]["aile"] is not None):', "    if False:"),
    ("OI farklı çiftlerine açılmıyor", ADY, '    if kayit["oi"]:\n        return tuple(itertools.combinations',
     "    if False:\n        return tuple(itertools.combinations"),
    ("yinelenen kimlik kabul", ADY, "    if any(n > 1 for n in kimlikler.values()):", "    if False:"),
    ("görünür aile adı kabul", ADY, "    if set(adlar) & set(yasak_adlar):", "    if False:"),
    ("aile sayısı denetlenmiyor", ADY, "    if len(set(adlar)) < en_az_aile:", "    if False:"),
    ("aile boyu denetlenmiyor", ADY, "    if en_kucuk < aile_basina:", "    if False:"),
    # tohum
    ("etiket ayırıcısı denetlenmiyor", TOH, "    if any(AYIRICI in m for m in metinler):", "    if False:"),
    ("tohum öneki kullanılmıyor", TOH, '    metin = h2_ayar.deger("tohum_oneki") + etiket(*parcalar)',
     "    metin = etiket(*parcalar)"),
    # şablon
    ("gövde bağlılığı aranmıyor", SAB, "            if not _bagli(g, x) or (yalniz_zincir and not zincir_mi(g, degiskenler)):",
     "            if yalniz_zincir and not zincir_mi(g, degiskenler):"),
    ("ek değişken sırası aranmıyor", SAB,
     "            if any(ekler[i] in kullanilan and ekler[i - 1] not in kullanilan for i in range(1, len(ekler))):",
     "            if False:"),
    ("başı içeren gövde aday", SAB, "            if (bas, x, y) in g:\n                continue", "            if False:\n                continue"),
    ("OI anlamsız gövdede de aday", SAB, "        oi_secenekleri = (False, True) if oi_anlamli_mi(g) else (False,)",
     "        oi_secenekleri = (False, True)"),
    # sayaç
    ("tanık bağlama sayısıyla sayılıyor", SAY,
     "                B = (_bag_sayisi(bicim, parca, R, [[v] for v in degisken], degiskenler) > 0).float()",
     "                B = _bag_sayisi(bicim, parca, R, [[v] for v in degisken], degiskenler)"),
    ("Möbius işareti yok", SAY, "    return math.prod((-1) ** (len(b) - 1) * math.factorial(len(b) - 1) for b in bolunti)",
     "    return math.prod(math.factorial(len(b) - 1) for b in bolunti)"),
    ("OI yalnız boş gövdelerde hesaplanıyor", SAY, "dolu = torch.nonzero(B.sum(dim=KISI) > 0).flatten()",
     "dolu = torch.nonzero(B.sum(dim=KISI) == 0).flatten()"),
    ("referans OI'yi uygulamıyor", SAY, "            if not oi or len(set(bag.values())) == len(bag):", "            if True:"),
    ("bilinmeyen kişi kabul", SAY, "        if a not in sira or b not in sira:\n            raise",
     "        if False:\n            raise"),
    ("ilişki tensörü kare denetlenmiyor", SAY, "    if R.shape[KISI[0]] != R.shape[KISI[1]]:", "    if False:"),
    # M0
    ("M0 yanlış süzgeci yok", M0, "        uygun = (T[:, None] - D <= en_cok_yanlis) & (D >= en_az)", "        uygun = (D >= en_az)"),
    ("M0 tanık eşiği yok", M0, "        uygun = (T[:, None] - D <= en_cok_yanlis) & (D >= en_az)",
     "        uygun = (T[:, None] - D <= en_cok_yanlis) & (D >= 1)"),
    ("M0 sırası yok", M0, '    adaylar.sort(key=lambda a: (-sum(a["dogru"].values()), a["halka_sayisi"], a["kanonik_kimlik"]))',
     '    adaylar.sort(key=lambda a: a["kanonik_kimlik"])'),
    ("M0 OI'yi saymıyor", M0, '            hedef += np.maximum(getattr(s, alan), 0)', '            hedef += np.maximum(getattr(s, alan.replace("_oi", "")), 0)'),
    # dünyalar
    ("evlilik oranı 1'de de çekiliş", DUN, "(evlilik_orani >= 1 or rng.random() < evlilik_orani)",
     "(rng.random() < evlilik_orani or evlilik_orani >= 1)"),
    ("evlilik oranı yok sayılıyor", DUN, "(evlilik_orani >= 1 or rng.random() < evlilik_orani)", "(True)"),
    ("A3 aynı soydan evlendiriyor", IKI, " and tip[d] != tip[c] and not soy[d] & soy[c]]", " and tip[d] != tip[c]]"),
    ("A3 yorumlayıcısı kişi tekrarına izin veriyor", IKI, "            if k not in yol and (tip is None or n.tip[k] == tip):",
     "            if tip is None or n.tip[k] == tip:"),
    ("A3 yorumlayıcısı tip şartını yok sayıyor", IKI, "            if k not in yol and (tip is None or n.tip[k] == tip):",
     "            if k not in yol:"),
    ("A3 iki terimi durdurmuyor", IKI, "                    if terim.setdefault((a, b), ad) != ad:", "                    if False:"),
    ("havuz yinelemesi durdurmuyor", HDU, "    if len(set(hepsi)) != len(hepsi):", "    if False:"),
    ("havuz tohumu aileden bağımsız", HDU, "tohum.tohum(h2_ayar, HAVUZ, havuz_adi, aile, i)", "tohum.tohum(h2_ayar, HAVUZ, havuz_adi, i)"),
    # sorgu defteri
    ("tur sınırı yok", BUT, "        if self.tur >= self.tur_siniri:", "        if False:"),
    ("turda aday sınırı yok", BUT,
     "        if aday not in self._adaylar[self.tur] and len(self._adaylar[self.tur]) >= self.tur_basina:", "        if False:"),
    ("yanan dünya kabul", BUT, "        if self._dunya_turu.get(dunya, self.tur) != self.tur:", "        if False:"),
    ("grup sorgusu kabul", BUT, "        if not isinstance(aday, str) or not isinstance(dunya, str):", "        if False:"),
    ("P* tavanı yok", BUT, "    if p_yildiz is not None:", "    if False:"),
    # yeniden bağlama ve boş dünya
    ("kendine bağ kabul", BAG, "            if a == d or c == b or (tersleri_yaz", "            if (tersleri_yaz"),
    ("ters adı eşitliği aranmıyor", BAG,
     "            if a == d or c == b or (tersleri_yaz and ters_adi[(a, r)] != ters_adi[(c, r)]):", "            if a == d or c == b:"),
    ("dışlayıcı çakışma denetlenmiyor", BAG,
     "            if len(set(giren)) != len(giren) or any(_cakisir(cift, x, y, z, sema, cikan) for x, z, y in giren):",
     "            if len(set(giren)) != len(giren):"),
    ("boş dünyada tersler yazılmıyor", BAG, "    return yeniden_bagla(olgular, ileri_taraflar(sema), sema, rng, True, deneme_carpani)",
     "    return yeniden_bagla(olgular, ileri_taraflar(sema), sema, rng, False, deneme_carpani)"),
    ("ileri taraf yalnız ilk ilişki", BAG, "        secilen |= yan if ayrilir else sinif", "        secilen |= {ilk}"),
    ("okunabilir sınıfta yön aranmıyor", BAG, "    return ters_yon and (", "    return ("),
    ("sayaç okunabilir sınıfı da sayıyor", BAG,
     "any(not semadan_okunabilir_mi(a, self.sema) for a in kabul_edilenler)", "any(True for a in kabul_edilenler)"),
    # çekirdek özeti, kilit, M0 koşucusu
    ("çekirdek içeriği özetlenmiyor", CEK, "        icerik = hashlib.new(ALGORITMA, yol.read_bytes()).hexdigest()",
     '        icerik = ""'),
    ("config_h2 kilitlenmiyor", KIL, "    if h2.is_file():", "    if False:"),
    ("M0 final havuzunu açabiliyor", HM0, "    if havuz_adi != GELISTIRME:", "    if False:"),
]


def secili_kostur(degisiklik):
    with tempfile.TemporaryDirectory() as d:
        kopya = Path(d) / "proje"
        shutil.copytree(KOK, kopya, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "uretilen"))
        dosya, eski, yeni = degisiklik
        yol = kopya / dosya
        metin = yol.read_text(encoding="utf-8")
        yol.write_text(metin.replace(eski, yeni, 1), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-m", "unittest", *MODULLER], cwd=kopya, capture_output=True,
                               text=True, timeout=ZAMAN_SINIRI, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        except subprocess.TimeoutExpired:
            return 1, "ZAMAN AŞIMI (V-039)"
        return r.returncode, (r.stderr.strip().splitlines() or ["?"])[-1]


def main(secilen=None):
    liste = [m for m in MUTASYONLAR if not secilen or m[0] in secilen]
    capasiz = [ad for ad, dosya, eski, _ in liste if (KOK / dosya).read_text(encoding="utf-8").count(eski) != 1]
    for ad in capasiz:
        print(f"ÇAPA YOK  {ad}")
    if capasiz:
        return 1
    kacan = 0
    for ad, dosya, eski, yeni in liste:
        kod, sayac = secili_kostur((dosya, eski, yeni))
        if kod == 0:
            kod, sayac = kopyada_kostur((dosya, eski, yeni))
        kacan += kod == 0
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:48} {sayac}", flush=True)
    print(f"MUTASYON: toplam={len(liste)} yakalanan={len(liste) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
