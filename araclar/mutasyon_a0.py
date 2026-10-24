"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): koda kasıtlı hata sokar, test takımı kırmızıya dönmeli.

Kullanım: python3 araclar/mutasyon_a0.py
Önce değiştirilmemiş kopya yeşil olmalı, sonra her satır YAKALANDI olmalı. KAÇTI çıkarsa ilgili test
değersizdir. Proje geçici bir kopyada değiştirilir, asıl dosyalara dokunulmaz.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
OLAY = "cekirdek/altyapi/olay_gunlugu.py"
AYAR = "cekirdek/altyapi/ayar.py"
KANONIK = "cekirdek/altyapi/kanonik.py"
ATOMIK = "cekirdek/altyapi/atomik.py"

ZAMAN_SINIRI = 600  # V-039: bir kopya koşusunun üst sınırı (normal koşu ~25 sn)

# (ad, dosya, eski metin, yeni metin)
MUTASYONLAR = [
    ("zincir bağı denetimi silindi", OLAY,
     'if kayit["sira"] != no or kayit["onceki_ozet"] != onceki:', 'if kayit["sira"] != no:'),
    ("özet denetimi silindi", OLAY,
     'if kayit["ozet"] != self._ozet(kayit) or kanonik_json(kayit) != satir:', "if False:"),
    ("kaynak denetimi silindi", OLAY, "if kaynak not in self.izinli_kaynaklar:", "if False:"),
    ("riskli bayrak denetimi silindi", AYAR, "if bayraklar[ad] is not False:", "if False:"),
    ("kaynak deseni gevşetildi", AYAR, 'not KAYNAK_DESENI.match(girdi["kaynak"])', 'not girdi["kaynak"]'),
    ("bayrak sınırı gevşetildi", AYAR, "EN_FAZLA_BAYRAK = 5  #", "EN_FAZLA_BAYRAK = 9  #"),
    ("NaN kabul edildi", KANONIK, "allow_nan=False", "allow_nan=True"),
    ("üreteç durumu yok sayıldı", ATOMIK, "rng.setstate((surum, tuple(ic_durum), gauss))", "pass"),
    ("yeniden adlandırma yerine kopya", ATOMIK, "    os.replace(gecici, yol)\n",
     "    open(yol, 'wb').write(open(gecici, 'rb').read())\n"),
    ("çekirdeğe ağ importu", KANONIK, "import json\n", "import json\nimport socket\n"),
    ("çekirdeğe tercüman importu", KANONIK, "import json\n", "import json\nimport tercuman\n"),
    ("etiketsiz sihirli sayı", KANONIK, "import json\n", "import json\nESIK = 0.95\n"),
    ("modül başlığı silindi", KANONIK,
     '"""KODLAMA_PROMPTU §5 (Determinizm, Şema ve veri): kanonik JSON ve hash (V-007)."""', '"""kanonik"""'),
    ("riskli bayrak açıldı", "config.json", '"kahin": {"deger": false', '"kahin": {"deger": true'),
    ("tercüman kâhine bağlandı", "tercuman/__init__.py", '"""\n', '"""\nimport degerlendirme\n'),
]


def kopyada_kostur(degisiklik=None):
    with tempfile.TemporaryDirectory() as d:
        kopya = Path(d) / "proje"
        shutil.copytree(KOK, kopya, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "uretilen"))
        if degisiklik:
            dosya, eski, yeni = degisiklik
            yol = kopya / dosya
            metin = yol.read_text(encoding="utf-8")
            if eski not in metin:
                raise SystemExit(f"mutasyon uygulanamadı, metin bulunamadı: {dosya}")
            yol.write_text(metin.replace(eski, yeni, 1), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, os.path.join("araclar", "kostur.py")], cwd=kopya,
                               capture_output=True, text=True, timeout=ZAMAN_SINIRI)
        except subprocess.TimeoutExpired:
            return 1, f"ZAMAN AŞIMI ({ZAMAN_SINIRI} sn): test takımı bitmedi, mutasyon yakalandı sayılır (V-039)"
        sayac = [s for s in r.stdout.splitlines() if s.startswith("SAYAÇ")]
        return r.returncode, (sayac[0] if sayac else r.stderr.strip().splitlines()[-1])


def main():
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':32} {sayac}")
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    kacan = 0
    for ad, dosya, eski, yeni in MUTASYONLAR:
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:32} {sayac}")
    print(f"MUTASYON: toplam={len(MUTASYONLAR)} yakalanan={len(MUTASYONLAR) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
