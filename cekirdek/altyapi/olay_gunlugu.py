"""KODLAMA_PROMPTU §5 (Defter, Hata yutma yok): sadece-ekleme, sıra numaralı, hash zincirli olay günlüğü.

Bu genel kayıt altyapısıdır. Destek/çelişki defteri (sistem.md §8–§9, Ek A) A4'te bunun üstüne kurulur.
Zaman damgası alanı yok (VARSAYIM V-006).
"""
import json
import os
import re

from cekirdek.altyapi.kanonik import kanonik_json, ozet

YEDEK_KULLANILDI = "YEDEK_KULLANILDI"  # KODLAMA_PROMPTU §5
KAYIT_ALANLARI = {"sema_surumu", "sira", "tur", "kaynak", "veri", "onceki_ozet", "ozet"}
TUR_DESENI = re.compile(r"^[A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ0-9_]*$")
ILK_ONCEKI_OZET = ""


class KayitHatasi(ValueError):
    pass


class ZincirHatasi(ValueError):
    pass


class OlayGunlugu:
    def __init__(self, yol, algoritma, sema_surumu, izinli_kaynaklar):
        self.yol = os.fspath(yol)
        self.algoritma = algoritma
        self.sema_surumu = sema_surumu
        self.izinli_kaynaklar = frozenset(izinli_kaynaklar)
        self._kayitlar = self._oku_ve_dogrula()

    def _oku_ve_dogrula(self):
        if not os.path.exists(self.yol):
            return []
        with open(self.yol, "rb") as f:
            ham = f.read()
        if ham and not ham.endswith(b"\n"):
            raise ZincirHatasi(f"{self.yol}: son satır yarım")
        kayitlar = []
        onceki = ILK_ONCEKI_OZET
        for no, satir in enumerate(ham.splitlines()):
            try:
                kayit = json.loads(satir.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as hata:
                raise ZincirHatasi(f"{self.yol}:{no}: okunamıyor") from hata
            if not isinstance(kayit, dict) or set(kayit) != KAYIT_ALANLARI:
                raise ZincirHatasi(f"{self.yol}:{no}: alanlar hatalı")
            if kayit["sira"] != no or kayit["onceki_ozet"] != onceki:
                raise ZincirHatasi(f"{self.yol}:{no}: sıra ya da zincir bağı kopuk")
            if kayit["ozet"] != self._ozet(kayit) or kanonik_json(kayit) != satir:
                raise ZincirHatasi(f"{self.yol}:{no}: özet tutmuyor")
            onceki = kayit["ozet"]
            kayitlar.append(kayit)
        return kayitlar

    def _ozet(self, kayit):
        return ozet(kanonik_json({a: d for a, d in kayit.items() if a != "ozet"}), self.algoritma)

    def ekle(self, tur, kaynak, veri):
        if not isinstance(tur, str) or not TUR_DESENI.match(tur):
            raise KayitHatasi(f"olay türü büyük harfli ad olmalı: {tur!r}")
        if kaynak not in self.izinli_kaynaklar:
            raise KayitHatasi(f"kaynaksız ya da bilinmeyen kaynak: {kaynak!r}")
        if not isinstance(veri, dict):
            raise KayitHatasi("veri bir nesne olmalı")
        kayit = {
            "sema_surumu": self.sema_surumu,
            "sira": len(self._kayitlar),
            "tur": tur,
            "kaynak": kaynak,
            "veri": veri,
            "onceki_ozet": self._kayitlar[-1]["ozet"] if self._kayitlar else ILK_ONCEKI_OZET,
        }
        kayit["ozet"] = self._ozet(kayit)
        satir = kanonik_json(kayit) + b"\n"
        kayit = json.loads(satir)  # çağıranın sözlüğünden bağımsız kopya
        with open(self.yol, "ab") as f:
            f.write(satir)
            f.flush()
            os.fsync(f.fileno())
        self._kayitlar.append(kayit)
        return kayit

    def yedek_kullanildi(self, kaynak, yer, neden):
        return self.ekle(YEDEK_KULLANILDI, kaynak, {"yer": yer, "neden": neden})

    def sayac(self, tur):
        return sum(1 for k in self._kayitlar if k["tur"] == tur)

    def kayitlar(self):
        return [json.loads(kanonik_json(k)) for k in self._kayitlar]
