"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): A1 koduna kasıtlı hata sokar, test takımı kırmızıya dönmeli.

Kullanım: python3 araclar/mutasyon_a1.py
"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import kopyada_kostur  # noqa: E402

DOG = "cekirdek/altyapi/sema_dogrulayici.py"
SEM = "cekirdek/iliski_semasi.py"
BT = "cekirdek/bilgi_tabani.py"
DUN = "degerlendirme/dunya.py"
URE = "degerlendirme/uretec.py"
KY = "degerlendirme/kisa_yol.py"
KK = "degerlendirme/kilitli_kumeler.py"
ALT = "degerlendirme/altin.py"


def veri_iliskisi():
    """Kodda ilişki adı yazmamak için örnek ad veri dosyasından okunur (KODLAMA_PROMPTU §2.4)."""
    return json.loads((KOK / "sema" / "iliskiler_v1.json").read_text(encoding="utf-8"))["iliskiler"][0]["ad"]


def mutasyonlar():
    return [
        ("fazla alan denetimi silindi", DOG, "if alan not in ozellikler:", "if False:"),
        ("true/false tamsayı sayıldı", DOG, "isinstance(deger, int) and not isinstance(deger, bool)",
         "isinstance(deger, int)"),
        ("NaN denetimi silindi", DOG, "if isinstance(veri, float) and not math.isfinite(veri):", "if False:"),
        ("bilinmeyen şema anahtarına izin", DOG, "if bilinmeyen:", "if False:"),
        ("'$' gevşetildi", DOG, 'desen = desen[:-1] + r"\\Z"', "pass"),
        ("şema hash denetimi silindi", SEM, "if ozet != onay[\"ozet\"]:", "if False:"),
        ("ters karşılıklılık denetimi silindi", SEM, 'if i["ad"] not in ters[t]:', "if False:"),
        ("LLM kaydı ana tabana", BT, "if kopya[\"kaynak\"] == LLM_KAYNAGI:", "if False:"),
        ("onaylı şema denetimi silindi", BT, 'if kayit["iliski"] not in self.iliski_semasi:', "if False:"),
        ("kayıt hash denetimi silindi", BT, 'if kayit["ozet"] != beklenen:', "if False:"),
        ("yinelemeye izin", BT, 'elif kayit["ozet"] in self._ozetler:', "elif False:"),
        ("ret günlüğe yazılmıyor", BT, 'self.gunluk.ekle("KAYIT_REDDEDILDI"', '(lambda *a: None)("KAYIT_REDDEDILDI"'),
        ("kodda ilişki sözcüğü", BT, 'KABUL = "KABUL"\n', f'KABUL = "KABUL"  # {veri_iliskisi()}\n'),
        ("yürüyüşte kişi tekrarına izin", DUN, "if sonraki in gorulen or (", "if ("),
        ("tip kısıtı yok sayıldı", DUN, "(tip is not None and self.tip[sonraki] != tip)", "False"),
        ("cevap sabit: ilk zincir olgusu", URE, '"cevap": None if bozuk else adla(cevap)}',
         '"cevap": None if bozuk else adla(olgular[0][1])}'),
        ("en kısa yol denetimi silindi", URE, "if (uzaklik is not None) if bozuk else (uzaklik != k):", "if False:"),
        ("kimlikler karıştırılmıyor", URE, "rng.sample(range(dunya.kisi_sayisi), len(kisiler))", "kisiler"),
        ("olgular karıştırılmıyor", URE, "        rng.shuffle(hepsi)\n", ""),
        ("bozuk bölümde ek dikkat dağıtıcı yok", URE, "            dikkat_sayisi += 1", "            pass"),
        ("cevap bölüme sızdı", URE, '"sorgu": {"ozne": esleme[sorgu[0]], "nesne": esleme[sorgu[1]]}}',
         '"sorgu": {"ozne": esleme[sorgu[0]], "nesne": esleme[sorgu[1]]}, "cevap": cevap}'),
        ("Treg ayrımı ters", URE, 'if nb.tahmin(ozellikler(a.bolum)) == a.cevap["cevap"]:',
         'if nb.tahmin(ozellikler(a.bolum)) != a.cevap["cevap"]:'),
        ("kilitli küme kesişimi denetlenmiyor", URE, "    kesisim_denetle(yasakli, ozetler)\n", ""),
        ("kısa yol kapısı kapatıldı", KY, "if dogruluk > sans_ + pay:", "if False:"),
        ("kilitli küme hash denetimi silindi", KK, 'if hashlib.new(girdi["algoritma"], ham).hexdigest() != girdi["ozet"]:',
         "if False:"),
        ("önsel-ters reddetme yok", URE, "if kabul is not None and rng.random() >= kabul[a.cevap[\"cevap\"]]:",
         "if False:"),
        ("altın soruda cevap işaretli", ALT, 'satirlar.append("  ·  ".join(f"{h}) {_goster(sec)}"',
         'satirlar.append(s["dogru_harf"] + "  ·  ".join(f"{h}) {_goster(sec)}"'),
        ("altın küme üzerine yazılabiliyor", ALT, "        if KUME_ADI in kumeler:\n", "        if False:\n"),
        ("geçersiz cevap harfi kabul", ALT, "if harf is None or harf.upper() not in HARFLER + EMIN_DEGIL:",
         "if harf is None:"),
        ("bozuk soruda doğru seçenek D değil", ALT, "BILGI_YETMEZ if cevap is None else cevap)]",
         "secenekler[0] if cevap is None else cevap)]"),
    ]


def main():
    kod, sayac = kopyada_kostur()
    print(f"TABAN     {'değiştirilmemiş kopya':36} {sayac}")
    if kod != 0:
        print("Taban kırmızı; mutasyon sınaması anlamsız.")
        return 1
    liste = mutasyonlar()
    kacan = 0
    for ad, dosya, eski, yeni in liste:
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
        if kod == 0:
            kacan += 1
        print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:36} {sayac}")
    print(f"MUTASYON: toplam={len(liste)} yakalanan={len(liste) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main())
