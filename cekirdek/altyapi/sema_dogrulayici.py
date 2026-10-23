"""KODLAMA_PROMPTU §5 (Şema ve veri): standart kütüphaneyle JSON Schema alt küme doğrulayıcısı (V-011).

Uymayan veri düzeltilmez. `hatalar()` nedenleri listeler, kararı çağıran verir.
"""
import json
import math
import re

DESTEKLENEN = {"$schema", "$id", "title", "description", "type", "properties", "required",
               "additionalProperties", "enum", "const", "pattern", "minLength", "maxLength", "minimum",
               "maximum", "items", "minItems", "maxItems", "uniqueItems"}  # V-011
TIPLER = {"object", "array", "string", "integer", "number", "boolean", "null"}


class SemaHatasi(ValueError):
    pass


def _tip_uyar(deger, tip):
    if tip == "object":
        return isinstance(deger, dict)
    if tip == "array":
        return isinstance(deger, list)
    if tip == "string":
        return isinstance(deger, str)
    if tip == "integer":
        return isinstance(deger, int) and not isinstance(deger, bool)
    if tip == "number":
        return isinstance(deger, (int, float)) and not isinstance(deger, bool)
    if tip == "boolean":
        return isinstance(deger, bool)
    return deger is None


def _desen_uyar(desen, metin):
    """JSON Schema'daki '$' metnin sonudur; Python'un sondaki satır sonunu kabul etmesine izin verilmez."""
    if desen.endswith("$") and not desen.endswith("\\$"):
        desen = desen[:-1] + r"\Z"
    return re.search(desen, metin) is not None


def _ayni(a, b):
    """JSON eşitliği: True ile 1 farklıdır."""
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


class SemaDogrulayici:
    def __init__(self, sema):
        self._denetle(sema, "#")
        self.sema = sema

    def _denetle(self, sema, yer):
        if not isinstance(sema, dict):
            raise SemaHatasi(f"{yer}: şema bir nesne olmalı")
        bilinmeyen = set(sema) - DESTEKLENEN
        if bilinmeyen:
            raise SemaHatasi(f"{yer}: desteklenmeyen anahtar {sorted(bilinmeyen)}")
        if "type" in sema:
            tipler = sema["type"] if isinstance(sema["type"], list) else [sema["type"]]
            if not tipler or any(t not in TIPLER for t in tipler):
                raise SemaHatasi(f"{yer}: bilinmeyen tip {sema['type']!r}")
        if sema.get("type") == "object" or "properties" in sema:
            if sema.get("additionalProperties") is not False:
                raise SemaHatasi(f"{yer}: nesne şemasında additionalProperties:false zorunlu")
            for ad, alt in sema.get("properties", {}).items():
                self._denetle(alt, f"{yer}.{ad}")
        if "items" in sema:
            self._denetle(sema["items"], f"{yer}[]")

    def hatalar(self, veri):
        sonuc = []
        self._dogrula(self.sema, veri, "", sonuc)
        return sonuc

    def _dogrula(self, sema, veri, yer, sonuc):
        ad = yer or "kayıt"
        if "type" in sema:
            tipler = sema["type"] if isinstance(sema["type"], list) else [sema["type"]]
            if not any(_tip_uyar(veri, t) for t in tipler):
                sonuc.append(f"{ad}: tip {'/'.join(tipler)} olmalı")
                return
        if isinstance(veri, float) and not math.isfinite(veri):
            sonuc.append(f"{ad}: sonlu sayı olmalı")
            return
        if "const" in sema and not _ayni(veri, sema["const"]):
            sonuc.append(f"{ad}: {sema['const']!r} olmalı")
        if "enum" in sema and not any(_ayni(veri, s) for s in sema["enum"]):
            sonuc.append(f"{ad}: izinli değerlerden biri olmalı")
        if isinstance(veri, str):
            if "minLength" in sema and len(veri) < sema["minLength"]:
                sonuc.append(f"{ad}: çok kısa")
            if "maxLength" in sema and len(veri) > sema["maxLength"]:
                sonuc.append(f"{ad}: çok uzun")
            if "pattern" in sema and not _desen_uyar(sema["pattern"], veri):
                sonuc.append(f"{ad}: biçim uymuyor")
        if _tip_uyar(veri, "number"):
            if "minimum" in sema and veri < sema["minimum"]:
                sonuc.append(f"{ad}: en az {sema['minimum']} olmalı")
            if "maximum" in sema and veri > sema["maximum"]:
                sonuc.append(f"{ad}: en çok {sema['maximum']} olmalı")
        if isinstance(veri, dict) and ("properties" in sema or sema.get("type") == "object"):
            ozellikler = sema.get("properties", {})
            for alan in sema.get("required", []):
                if alan not in veri:
                    sonuc.append(f"{ad}: eksik alan '{alan}'")
            for alan in veri:
                if alan not in ozellikler:
                    sonuc.append(f"{ad}: fazla alan '{alan}'")
            for alan, alt in ozellikler.items():
                if alan in veri:
                    self._dogrula(alt, veri[alan], f"{yer}.{alan}" if yer else alan, sonuc)
        if isinstance(veri, list):
            if "minItems" in sema and len(veri) < sema["minItems"]:
                sonuc.append(f"{ad}: çok az öğe")
            if "maxItems" in sema and len(veri) > sema["maxItems"]:
                sonuc.append(f"{ad}: çok fazla öğe")
            if sema.get("uniqueItems"):
                gorulen = [json.dumps(o, sort_keys=True) for o in veri]
                if len(set(gorulen)) != len(gorulen):
                    sonuc.append(f"{ad}: yinelenen öğe")
            if "items" in sema:
                for i, oge in enumerate(veri):
                    self._dogrula(sema["items"], oge, f"{yer}[{i}]", sonuc)


def sema_yukle(yol):
    with open(yol, encoding="utf-8") as f:
        return SemaDogrulayici(json.load(f))
