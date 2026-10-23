"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A3 çekirdek koduna kasıtlı hata sokar, test takımı kırmızıya dönmeli.

Kullanım: python3 araclar/mutasyon_a3.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

ESL = "cekirdek/eslesme.py"
HAV = "cekirdek/havuz.py"
DNA = "cekirdek/dna.py"
DON = "cekirdek/dongu.py"
PLA = "cekirdek/plazma.py"

MUTASYONLAR = [
    ("değişken tutarlılığı yok", ESL, "if degiskenler.setdefault(degisken, varlik) != varlik:",
     "if False and degiskenler.setdefault(degisken, varlik) != varlik:"),
    ("halkalar aynı kayda bağlanabiliyor", ESL, "if len(set(kimlikler)) != len(kimlikler) or not yeni.intersection(kimlikler):",
     "if not yeni.intersection(kimlikler):"),
    ("yarı-naif kural yok", ESL, "if len(set(kimlikler)) != len(kimlikler) or not yeni.intersection(kimlikler):",
     "if len(set(kimlikler)) != len(kimlikler):"),
    ("sonuç değişkenleri yer değiştirdi", ESL, "return (d[hucre.sonuc.sol], hucre.sonuc.gen, d[hucre.sonuc.sag])",
     "return (d[hucre.sonuc.sag], hucre.sonuc.gen, d[hucre.sonuc.sol])"),
    ("(üçlü, köken) tekilleştirmesi yok", HAV, "        if anahtar in self._kokenler:\n            return None\n", ""),
    ("ilişki dizini yanlış alan", HAV, "self._dizin.setdefault(k.uclu[1], [])", "self._dizin.setdefault(k.uclu[0], [])"),
    ("epitop kapasite denetimi yok", HAV, "        if len(self._kayitlar) >= self.kapasite:\n            raise HavuzHatasi(",
     "        if False:\n            raise HavuzHatasi("),
    ("güven aralık denetimi yok", HAV, "or not 0 <= guven <= 1:", ":"),
    ("DNA gen denetimi yok", DNA, "            if gen not in iliski_semasi:", "            if False:"),
    ("DNA sonuç değişkeni denetimi yok", DNA, "if not {sonuc.sol, sonuc.sag} <= govde:", "if False:"),
    ("afinite ölçeği yok", ESL, "AFINITE_OLCEGI = math.sqrt(3)", "AFINITE_OLCEGI = 1.0"),
    ("θ süzgeci yok", ESL, "if any(af <= h.esik * esik_carpani for af, h in zip(afiniteler, hucre.halkalar)):",
     "if False:"),
    ("ebeveyn güveni hesaba girmiyor", ESL, "guven = min(afiniteler + tuple(k.guven for k in kayitlar))",
     "guven = min(afiniteler)"),
    ("hücre güvenilirliği yok", ESL, ") * hucre.guvenilirlik", ") * 1.0"),
    ("hücre başına sınır yok", DON, "adaylar += [(sira, e) for e in es[:prm.hucre_yazma_siniri]]",
     "adaylar += [(sira, e) for e in es]"),
    ("tur bütçesi yok", DON, "    if len(adaylar) > prm.butce:\n", "    if False:\n"),
    ("impasse eşik düşürmesi yok", DON, "            elif dusurme == 0:", "            elif False:"),
    ("impasse sonrası yeniden deneme yok", DON, "prm.impasse_carpani, frozenset(canli)",
     "prm.impasse_carpani, frozenset()"),
    ("tur sınırı yok", DON, "if neden is None and tur >= prm.tur_siniri:", "if False:"),
    ("en yüksek güvenli kayıt atılıyor", HAV, "atilan = min(adaylar, key=", "atilan = max(adaylar, key="),
    ("mezar taşı tutulmuyor", HAV, "        self._mezar[atilan.kimlik] = atilan\n", ""),
    ("noisy-OR yerine MAX", PLA, "return max(0.0, min(1.0, -math.expm1(sum(math.log1p(-g) for g in guvenler))))",
     "return max(guvenler)"),
    ("ortak kökenli ispatlar ayrı sayılıyor", PLA, "            if kokler[i] & kokler[j]:", "            if False:"),
    ("eşitlikte ilk cevap seçiliyor", PLA, "    if len(kazananlar) > 1:\n        return Cevap(None, None, ozet, celiski, ())\n",
     ""),
    ("çelişki işareti yok", PLA, "    celiski = len(birlesik) > 1", "    celiski = False"),
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
