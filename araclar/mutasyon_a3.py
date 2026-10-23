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
