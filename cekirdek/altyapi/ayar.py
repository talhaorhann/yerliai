"""KODLAMA_PROMPTU §5 (Config): tek ayar dosyasını okur, yapısını ve her değerin kaynağını denetler (V-001, V-002)."""
import json
import re
from dataclasses import dataclass
from types import MappingProxyType

EN_FAZLA_BAYRAK = 5  # KODLAMA_PROMPTU §5
RISKLI_BAYRAKLAR = ("deneysel", "kahin", "api_yedegi")  # KODLAMA_PROMPTU §5: varsayılan KAPALI
UST_ALANLAR = {"surum", "degerler", "bayraklar"}  # V-001
GIRDI_ALANLARI = {"deger", "kaynak"}  # V-001
KAYNAK_DESENI = re.compile(r"^(sistem\.md §\d+|KODLAMA_PROMPTU §\d+|V-\d{3}|K-\d{3})$")  # V-002


class AyarHatasi(ValueError):
    pass


@dataclass(frozen=True)
class Ayar:
    surum: str
    degerler: MappingProxyType
    bayraklar: MappingProxyType

    def deger(self, ad):
        return self.degerler[ad]

    def bayrak(self, ad):
        return self.bayraklar[ad]


def _yinelenen_anahtar_yok(ciftler):
    sozluk = {}
    for anahtar, deger in ciftler:
        if anahtar in sozluk:
            raise AyarHatasi(f"yinelenen anahtar: {anahtar}")
        sozluk[anahtar] = deger
    return sozluk


def _girdileri_denetle(bolum, girdiler):
    if not isinstance(girdiler, dict):
        raise AyarHatasi(f"{bolum} bir nesne olmalı")
    sonuc = {}
    for ad, girdi in girdiler.items():
        if not isinstance(girdi, dict) or set(girdi) != GIRDI_ALANLARI:
            raise AyarHatasi(f"{bolum}.{ad}: alanlar tam olarak {sorted(GIRDI_ALANLARI)} olmalı")
        if not isinstance(girdi["kaynak"], str) or not KAYNAK_DESENI.match(girdi["kaynak"]):
            raise AyarHatasi(f"{bolum}.{ad}: kaynak '§N' ya da 'V-nnn' biçiminde olmalı")
        sonuc[ad] = girdi["deger"]
    return sonuc


def ayar_yukle(yol):
    try:
        with open(yol, encoding="utf-8") as f:
            veri = json.load(f, object_pairs_hook=_yinelenen_anahtar_yok)
    except json.JSONDecodeError as hata:
        raise AyarHatasi(f"ayar dosyası JSON değil: {hata}") from hata
    if not isinstance(veri, dict) or set(veri) != UST_ALANLAR:
        raise AyarHatasi(f"üst alanlar tam olarak {sorted(UST_ALANLAR)} olmalı")
    if not isinstance(veri["surum"], str) or not veri["surum"]:
        raise AyarHatasi("surum boş olmayan metin olmalı")
    degerler = _girdileri_denetle("degerler", veri["degerler"])
    bayraklar = _girdileri_denetle("bayraklar", veri["bayraklar"])
    if len(bayraklar) > EN_FAZLA_BAYRAK:
        raise AyarHatasi(f"en fazla {EN_FAZLA_BAYRAK} özellik bayrağı olabilir")
    for ad, deger in bayraklar.items():
        if not isinstance(deger, bool):
            raise AyarHatasi(f"bayraklar.{ad}: true/false olmalı")
    for ad in RISKLI_BAYRAKLAR:
        if ad not in bayraklar:
            raise AyarHatasi(f"bayraklar.{ad} tanımlı olmalı")
        if bayraklar[ad] is not False:
            raise AyarHatasi(f"bayraklar.{ad} varsayılan KAPALI olmalı")
    return Ayar(veri["surum"], MappingProxyType(degerler), MappingProxyType(bayraklar))
