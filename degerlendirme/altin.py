"""KODLAMA_PROMPTU §5 (Kilitli kümeler), sistem.md §17, K-011: altın küme soruları (V-023).

Sorular üreteçten ayrı tohumla hazırlanır, kullanıcı üretecin cevabını görmeden A/B/C/D ile cevaplar.
Altın kümede "beklenen" cevap kullanıcının cevabıdır; kodun cevabı yalnız karşılaştırma içindir.
JSON cevap biçimi (K-039): parça soru dosyası yalnız soru kaydından (`altin_sorular.jsonl`) yeniden yazılır; cevap
dosyaları okunmaz. Kullanım: python3 -m degerlendirme.altin uret | soru <parça_no>
"""
import dataclasses
import hashlib
import json
import os
import random
import re
import sys
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.iliski_semasi import iliski_semasi_yukle
from degerlendirme.dunya import tanimlar_yukle
from degerlendirme.kilitli_kumeler import KilitliKumeHatasi
from degerlendirme.uretec import Parametreler, UretimDurduHatasi, aday_uret

HARFLER = "ABCD"  # K-011
BILGI_YETMEZ = "Bilgi yetmez"  # V-023
EMIN_DEGIL = "?"  # V-023
ALGORITMA = "sha256"  # V-007
KUME_ADI = "altin"  # V-023
SOHBET_BICIMI, JSON_BICIMI = "sohbet", "json"  # V-023 (1. parça), K-039: cevap biçimi
CEVAP_ALANLARI = ("parca", "kaynak", "onaylayan", "bagimsiz_insan_cevabi", "cevaplar", "cevap_kaynaklari")  # K-039
CEVAP_KAYNAKLARI = ("kullanıcı", "LLM taslağı, kullanıcı onaylı")  # K-039: cevap başına kaynak
ORNEK_GIRINTISI = 2  # V-023: soru dosyasındaki örnek JSON okunur girintiyle


@dataclasses.dataclass(frozen=True)
class AltinParametreleri:
    tohum: int
    parca_sayisi: int
    normal_sayisi: int
    bozuk_sayisi: int
    dikkat_dagitici: int

    @classmethod
    def ayardan(cls, ayar):
        d = ayar.deger
        return cls(d("altin_tohum"), d("altin_parca_sayisi"), d("altin_normal_sayisi"), d("altin_bozuk_sayisi"),
                   d("altin_dikkat_dagitici"))


def _soru(rng, aday, iliski_semasi):
    cevap = aday.cevap["cevap"]
    adlar = list(iliski_semasi.adlar)
    if cevap is None:
        secim = rng.sample(adlar, len(HARFLER) - 1)
    else:
        secim = rng.sample([r for r in adlar if r != cevap], len(HARFLER) - 2) + [cevap]  # K-011: D hariç 2 çeldirici
        rng.shuffle(secim)
    secenekler = secim + [BILGI_YETMEZ]
    etiketler = {}
    for o in aday.bolum["olgular"]:
        for kisi in (o["ozne"], o["nesne"]):
            etiketler.setdefault(str(kisi), len(etiketler) + 1)
    return {"bolum": aday.bolum, "cevap": cevap, "k": aday.cevap["k"], "secenekler": secenekler,
            "dogru_harf": HARFLER[secenekler.index(BILGI_YETMEZ if cevap is None else cevap)],
            "etiketler": etiketler}


def altin_uret(ap, prm, tanimlar, iliski_semasi):
    rng = random.Random(f"{KUME_ADI}:{ap.tohum}")
    uprm = dataclasses.replace(prm, dikkat_dagitici=ap.dikkat_dagitici)
    parcalar, gorulen = [], set()
    for _ in range(ap.parca_sayisi):
        sorular = [_soru(rng, aday_uret(rng, tanimlar, uprm, "egitim"), iliski_semasi) for _ in range(ap.normal_sayisi)]
        sorular += [_soru(rng, aday_uret(rng, tanimlar, uprm, "zincir_bozuk"), iliski_semasi)
                    for _ in range(ap.bozuk_sayisi)]
        rng.shuffle(sorular)
        for s in sorular:
            if s["bolum"]["ozet"] in gorulen:
                raise UretimDurduHatasi("altın kümede yinelenen soru")
            gorulen.add(s["bolum"]["ozet"])
        parcalar.append(sorular)
    return parcalar


def _goster(ad):
    return ad.replace("_", " ")


def _json_bicimi(parca_no, adet):
    ornek = {"parca": parca_no, "kaynak": "danışman", "onaylayan": "kullanıcı", "bagimsiz_insan_cevabi": False,
             "cevaplar": {"1": EMIN_DEGIL, "2": EMIN_DEGIL},
             "cevap_kaynaklari": {"1": CEVAP_KAYNAKLARI[1], "2": CEVAP_KAYNAKLARI[0]}}
    return [
        "## Cevap biçimi (JSON)", "",
        f"Dosya: `degerlendirme/altin/kullanici_cevaplari_{parca_no}.json` (UTF-8). Alanlar:", "",
        f"- `parca`: {parca_no} (tamsayı).",
        "- `kaynak`: cevapları kim hazırladı (serbest metin).",
        "- `onaylayan`: cevapları kim onayladı.",
        "- `bagimsiz_insan_cevabi`: `true` yalnız her cevap kullanıcının kendi bağımsız cevabıysa; bir cevap bile "
        "LLM taslağıysa `false` (ÖK-001).",
        f"- `cevaplar`: `\"1\"`den `\"{adet}\"`e her soru numarası tam bir kez; değer "
        + ", ".join(f"`\"{h}\"`" for h in HARFLER + EMIN_DEGIL) + ".",
        "- `cevap_kaynaklari`: `cevaplar` ile aynı anahtarlar; değer "
        + " ya da ".join(f"`\"{k}\"`" for k in CEVAP_KAYNAKLARI) + ".", "",
        "Örnek (yalnız biçim; değerler gerçek cevap değildir, iki soru gösterilmiştir):", "",
        "```json", json.dumps(ornek, ensure_ascii=False, indent=ORNEK_GIRINTISI), "```", ""]


def parca_metni(parca_no, sorular, bicim=SOHBET_BICIMI):
    """Parça soru metni. Yalnız olgular, sorgu ve seçenekler yazılır; doğru cevap kullanılmaz."""
    if bicim not in (SOHBET_BICIMI, JSON_BICIMI):
        raise ValueError(f"bilinmeyen cevap biçimi: {bicim}")
    cevap_satiri = ("**Cevapları sohbete tek satırda yazın.** Örnek: `1B 2A 3D 4? 5C ...`" if bicim == SOHBET_BICIMI
                    else "**Cevaplar bir JSON dosyasıyla verilir;** biçimi dosyanın sonunda (Cevap biçimi).")
    satirlar = [
        f"# Altın küme: Parça {parca_no} ({len(sorular)} soru)", "",
        "**Nasıl okunur:** «Kişi 1 → r → Kişi 2» demek, Kişi 2, Kişi 1'in r'sidir.",
        "**Soru:** «Kişi 1 → ? → Kişi 3» demek, Kişi 3, Kişi 1'in nesidir?", "",
        f"Verilen bilgiler soruyu cevaplamaya yetmiyorsa **{HARFLER[-1]}** seçin. Emin değilseniz **{EMIN_DEGIL}** yazın.",
        "Her soru kendi içinde ayrı bir ailedir; kişi numaraları sorudan soruya değişir.", "",
        cevap_satiri, "",
    ]
    if bicim == JSON_BICIMI:
        satirlar[1:1] = ["", "Bu parça, çekirdeğin soy ağacı sorularına verdiği cevapların onaylı cevaplarla ne kadar "
                         "örtüştüğünü ölçer; sonuç ayrı satırda raporlanır, kapı kararına girmez (ÖK-002 §4)."]
    for no, s in enumerate(sorular, start=1):
        e = s["etiketler"]
        satirlar += [f"## Soru {no}", ""]
        for o in s["bolum"]["olgular"]:
            satirlar.append(f"- Kişi {e[str(o['ozne'])]} → {_goster(o['iliski'])} → Kişi {e[str(o['nesne'])]}")
        sorgu = s["bolum"]["sorgu"]
        satirlar += ["", f"**Kişi {e[str(sorgu['ozne'])]} → ? → Kişi {e[str(sorgu['nesne'])]}**", ""]
        satirlar.append("  ·  ".join(f"{h}) {_goster(sec)}" for h, sec in zip(HARFLER, s["secenekler"])))
        satirlar.append("")
    if bicim == JSON_BICIMI:
        satirlar += _json_bicimi(parca_no, len(sorular))
    return "\n".join(satirlar)


def soru_dosyasi_yaz(klasor, parca_no, cikis):
    """K-039: parçanın soru dosyasını JSON cevap biçimiyle yazar. Yalnız `altin_sorular.jsonl` okunur."""
    with open(Path(klasor) / "altin_sorular.jsonl", encoding="utf-8") as f:
        sorular = [k for k in map(json.loads, f.read().splitlines()) if k["parca"] == parca_no]
    if not sorular:
        raise ValueError(f"altın kümede {parca_no}. parça yok")
    atomik_yaz(Path(cikis), parca_metni(parca_no, sorular, JSON_BICIMI).encode("utf-8"))
    return len(sorular)


def _jsonl(kayitlar):
    return b"".join(kanonik_json(k) + b"\n" for k in kayitlar)


def altin_yaz(klasor, parcalar, kayit_yolu, kok):
    """Soruları yazar ve altın kümeyi kilitli küme kaydına ekler. Kayıtta zaten altın küme varsa durur."""
    kumeler = {}
    if os.path.exists(kayit_yolu):
        with open(kayit_yolu, encoding="utf-8") as f:
            kumeler = json.load(f)["kumeler"]
        if KUME_ADI in kumeler:
            raise KilitliKumeHatasi("altın küme zaten kilitli; değiştirmek kullanıcı onayı ister")
    klasor = Path(klasor)
    klasor.mkdir(parents=True, exist_ok=True)
    for p_no, sorular in enumerate(parcalar, start=1):
        atomik_yaz(klasor / f"altin_soru_{p_no}.md", parca_metni(p_no, sorular).encode("utf-8"))
    hepsi = [(p_no, no, s) for p_no, sorular in enumerate(parcalar, start=1) for no, s in enumerate(sorular, start=1)]
    atomik_yaz(klasor / "altin_sorular.jsonl", _jsonl(
        {"parca": p, "no": n, "bolum": s["bolum"], "secenekler": s["secenekler"], "etiketler": s["etiketler"]}
        for p, n, s in hepsi))
    atomik_yaz(klasor / "uretec_cevaplari.jsonl", _jsonl(
        {"parca": p, "no": n, "bolum_ozeti": s["bolum"]["ozet"], "cevap": s["cevap"], "dogru_harf": s["dogru_harf"]}
        for p, n, s in hepsi))
    bolumler = _jsonl(s["bolum"] for _, _, s in hepsi)
    atomik_yaz(klasor / "altin_bolumler.jsonl", bolumler)
    kumeler[KUME_ADI] = {"dosya": Path(os.path.relpath(klasor / "altin_bolumler.jsonl", kok)).as_posix(),
                         "algoritma": ALGORITMA, "ozet": hashlib.new(ALGORITMA, bolumler).hexdigest()}
    metin = json.dumps({"kumeler": kumeler}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"  # V-008: okunur
    atomik_yaz(kayit_yolu, metin.encode("utf-8"))
    return kumeler[KUME_ADI]


CEVAP_DESENI = re.compile(r"(?P<no>\d+)\s*[-.):]*\s*(?P<harf>[A-Za-z?])?")


def kullanici_cevaplarini_coz(metin, adet):
    """'1B 2A 3? ...' biçimindeki cevabı {soru_no: harf} sözlüğüne çevirir. Eksik, fazla ya da biçimsiz cevap
    düzeltilmez, reddedilir."""
    cevaplar = {}
    for eslesme in CEVAP_DESENI.finditer(metin):
        no, harf = int(eslesme.group("no")), eslesme.group("harf")
        if harf is None or harf.upper() not in HARFLER + EMIN_DEGIL:
            raise ValueError(f"soru {no}: cevap A/B/C/D ya da ? olmalı")
        if no in cevaplar:
            raise ValueError(f"soru {no} iki kez cevaplanmış")
        cevaplar[no] = harf.upper()
    if set(cevaplar) != set(range(1, adet + 1)):
        raise ValueError(f"1..{adet} arası her soru tam bir kez cevaplanmalı")
    return cevaplar


def karsilastir(kullanici, uretec):
    """Kullanıcı ile üretecin ayrıştığı sorular ve kullanıcının emin olmadığı sorular."""
    farkli = sorted(n for n, h in kullanici.items() if h != EMIN_DEGIL and h != uretec[n])
    emin_degil = sorted(n for n, h in kullanici.items() if h == EMIN_DEGIL)
    return farkli, emin_degil


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    match arg:
        case ["soru", parca]:
            klasor = kok / "degerlendirme" / "altin"
            adet = soru_dosyasi_yaz(klasor, int(parca), klasor / f"altin_soru_{parca}.md")
            print(f"altin_soru_{parca}.md yazıldı: {adet} soru")
            return 0
    if arg != ["uret"]:
        print(__doc__)
        return 1
    ayar = ayar_yukle(kok / "config.json")
    sema = iliski_semasi_yukle(kok / "sema" / "iliskiler_v1.json", kok / "kilit" / "sema_onayi.json",
                               kok / "sema" / "iliski_semasi_v1.schema.json")
    tanimlar = tanimlar_yukle(kok / "degerlendirme" / "veri" / "tanimlar_v1.json",
                              kok / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", sema)
    parcalar = altin_uret(AltinParametreleri.ayardan(ayar), Parametreler.ayardan(ayar), tanimlar, sema)
    girdi = altin_yaz(kok / "degerlendirme" / "altin", parcalar, kok / "kilit" / "kilitli_kumeler.json", kok)
    print(f"altın küme yazıldı ve kilitlendi: {girdi['dosya']} {girdi['ozet']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
