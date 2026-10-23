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
