"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A5 hızlı yol (PyTorch) koduna kasıtlı hata sokar.

Kullanım: .venv/bin/python araclar/mutasyon_a5.py  (torch gerekir; kopya aynı yorumlayıcıyla koşar)
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

HIZ = "cekirdek/vektor_hizli.py"
REF = "cekirdek/vektor.py"
ESL = "cekirdek/eslesme.py"
HAV = "cekirdek/havuz.py"
DNA = "cekirdek/dna.py"
H1 = "degerlendirme/h1.py"
IST = "degerlendirme/istatistik.py"

MUTASYONLAR = [
    ("dairesel matris yönü ters", HIZ, "p[(sira.unsqueeze(0) - sira.unsqueeze(1)) % d]",
     "p[(sira.unsqueeze(1) - sira.unsqueeze(0)) % d]"),
    ("ilişki ölçeği yok", HIZ, "v = (kk.olcek * vektor_tensoru(", "v = (vektor_tensoru("),
    ("özne yerine nesne bağlandı", HIZ, "evrisim_toplu(p_s, vektor_tensoru(kk, TUR_VARLIK, ozneler))",
     "evrisim_toplu(p_s, vektor_tensoru(kk, TUR_VARLIK, nesneler))"),
    ("kök torch.sqrt ile", HIZ, "/ dogru_kok(paydalar)", "/ torch.sqrt(paydalar.to(ONDALIK))"),
    ("ondalık float32", HIZ, "ONDALIK = torch.float64", "ONDALIK = torch.float32"),
    ("evrişimde int64 denetimi yok", HIZ, "if p.dtype != TAMSAYI or e.dtype != TAMSAYI:", "if False:"),
    ("benzerlikte int64 denetimi yok", HIZ, "if a.dtype != TAMSAYI or b.dtype != TAMSAYI:", "if False:"),
    ("öğe taşma denetimi yok", HIZ, "if t.numel() and int(t.abs().max()) ** 2 * t.shape[1] >= TAM_SINIR:",
     "if False:"),
    ("norm çarpımı taşma denetimi yok", HIZ,
     "if norm_a.numel() and norm_b.numel() and int(norm_a.max()) * int(norm_b.max()) >= TAM_SINIR:", "if False:"),
    ("sıfır payda denetimi yok", HIZ, "if bool((paydalar == 0).any()):", "if False:"),
    ("afinite kırpılmıyor", HIZ, "torch.clamp(benzerlik_matrisi_hizli(kayitlar, alicilar) * AFINITE_OLCEGI, 0.0, 1.0)",
     "benzerlik_matrisi_hizli(kayitlar, alicilar) * AFINITE_OLCEGI"),
    ("şekil denetimi yok", HIZ, "    if t.dim() != len(eksenler):\n", "    if False:\n"),
    # V-042: döngüye bağlama
    ("hızlı kayıt vektöründe özne/nesne ters", HIZ, "[(ozne, iliski, nesne)]", "[(nesne, iliski, ozne)]"),
    ("hızlı benzerlikte argümanlar ters", HIZ, "benzerlik_matrisi_hizli(self._matris(a), self._matris(b))",
     "benzerlik_matrisi_hizli(self._matris(b), self._matris(a))"),
    ("referans benzerlikte argümanlar ters", REF, "        return benzerlik_matrisi(a, b)\n",
     "        return benzerlik_matrisi(b, a)\n"),
    ("havuz referans yola dönüyor", HAV, "self.kod_kitabi.kayit_vektoru(*uclu)",
     "__import__('cekirdek.vektor').vektor.kayit_vektoru(self.kod_kitabi, *uclu)"),
    ("tabloda tek genin alıcısı", ESL, "[alici(kk, gen)]", "[alici(kk, min(genler))]"),
    ("tabloda kırpma yok", ESL, "tablo[(gen, kimlik)] = afinite_kosinustan(deger)", "tablo[(gen, kimlik)] = deger"),
    ("eşleşmede halka-kayıt eşlemesi ters", ESL, "for h, k in zip(hucre.halkalar, b.kayitlar))",
     "for h, k in zip(hucre.halkalar, reversed(b.kayitlar)))"),
    # Not: döngünün tabloyu eşleşmeye vermemesi eşdeğer mutanttır (her hücre aynı tabloyu kendisi kurar, sonuç aynı);
    # yalnız hızı etkiler, bu yüzden listede yok.
    # K-025, V-043: farklı kişi şartı
    ("farklı şartı uygulanmıyor", ESL, "    if any(degiskenler[a] == degiskenler[b] for a, b in hucre.farkli):",
     "    if False:"),
    ("farklı şartı ters", ESL, "degiskenler[a] == degiskenler[b] for a, b", "degiskenler[a] != degiskenler[b] for a, b"),
    ("farklı DNA'dan okunmuyor", DNA, 'farkli = tuple(tuple(cift) for cift in h.get("farkli", ()))', "farkli = ()"),
    ("farklı değişken denetimi yok", DNA, "if a == b or not {a, b} <= govde:", "if False:"),
    # V-044: H1 koşturucusu ve istatistik
    ("zincir-bozukta bilmiyorum yanlış", H1, "    dogru = verilen == beklenen\n",
     "    dogru = verilen == beklenen and beklenen is not None\n"),
    ("bilmiyorum sınıfı yok", H1, "        elif verilen is None:", "        elif False:"),
    ("cevap kaydı özeti denetlenmiyor", H1, '    if satir["bolum_ozeti"] != cevap_kaydi["bolum_ozeti"]:', "    if False:"),
    ("kapıda hata sayılmıyor", H1, '            if s["yanlis"]:', "            if False:"),
    ("kapıda bölüm sayısı denetlenmiyor", H1, '            if s["n"] != beklenen_sayi:', "            if False:"),
    ("kapıda eksik tohum geçiyor", H1, '                nedenler.append(f"{anahtar}: koşulmamış")\n', ""),
    ("ön kayıt eki aranmıyor", H1, "    ek = metin.split(EK_BASLIGI, 1)[1]", "    ek = metin"),
    ("manifest denetimi yok", H1, '        if _ozet(baytlar, algoritma) != manifest["dosyalar"].get(goreli):', "        if False:"),
    ("ara kayıt denetimi yok", H1,
     '        if i >= len(bolumler) or (s["bolum_ozeti"], s["bolme"], s["tohum"]) != (bolumler[i]["ozet"], bolme, tohum):',
     "        if False:"),
    ("emin değil cevaplı sayılıyor", H1, "kullaniciyla_ayni=None if k in (None, EMIN_DEGIL) else harf == k",
     "kullaniciyla_ayni=None if k is None else harf == k"),
    ("bağımsızlık etiketi yok", H1,
     '    return etiket + ("" if kayit.get("bagimsiz_insan_cevabi") else " (bağımsız insan cevabı değil, ÖK-001)")',
     "    return etiket"),
    ("Clopper–Pearson tek yanlı", IST, "    yari = (1 - guven) / KUYRUK\n    alt = 0.0", "    yari = 1 - guven\n    alt = 0.0"),
    ("yarılama yönü ters", IST, "if (fonksiyon(orta) < hedef) == artan_mi:", "if (fonksiyon(orta) < hedef) != artan_mi:"),
    ("bootstrap tohumsuz", IST, "    rng = random.Random(tohum)", "    rng = random.Random()"),
]


def main():
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':36} {sayac}")
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    kacan = 0
    for ad, dosya, eski, yeni in MUTASYONLAR:
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:36} {sayac}")
    print(f"MUTASYON: toplam={len(MUTASYONLAR)} yakalanan={len(MUTASYONLAR) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
