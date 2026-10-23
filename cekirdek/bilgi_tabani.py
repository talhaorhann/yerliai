"""sistem.md §1, §14; KODLAMA_PROMPTU §2.3, §5: üçlü olguların bilgi tabanı (V-012, V-014).

Kayıt şemaya, onaylı ilişki şemasına ve kendi hash'ine uymalıdır. Uymayan kayıt düzeltilmez, reddedilir
ve nedeni olay günlüğüne yazılır. kaynak=LLM olan kayıt ana tabana girmez, karantinada "kanıtlanmamış" kalır.
Bilgi tabanı güven birleştirmez, destek saymaz (A4, defter).
"""
import json

from cekirdek.altyapi.kanonik import KanonikHata, kanonik_json, ozet

KABUL = "KABUL"
KARANTINA = "KARANTINA"
RET = "RET"
LLM_KAYNAGI = "LLM"  # KODLAMA_PROMPTU §2.3
KAYIT_SURUMU = "1"  # V-012
GUNLUK_KAYNAGI = "çekirdek"  # KODLAMA_PROMPTU §5


def uclu_kaydi(ozne, iliski, nesne, kaynak, guven, adim, algoritma):
    kayit = {"sema_surumu": KAYIT_SURUMU, "ozne": ozne, "iliski": iliski, "nesne": nesne,
             "kaynak": kaynak, "guven": guven, "adim": adim}
    kayit["ozet"] = ozet(kanonik_json(kayit), algoritma)
    return kayit


class BilgiTabani:
    def __init__(self, iliski_semasi, uclu_dogrulayici, gunluk, algoritma):
        self.iliski_semasi = iliski_semasi
        self.dogrulayici = uclu_dogrulayici
        self.gunluk = gunluk
        self.algoritma = algoritma
        self._olgular = []
        self._karantina = []
        self._ozetler = set()

    def _nedenler(self, kayit):
        if not isinstance(kayit, dict):
            return ["kayıt bir nesne olmalı"]
        nedenler = self.dogrulayici.hatalar(kayit)
        if nedenler:
            return nedenler
        if kayit["iliski"] not in self.iliski_semasi:
            nedenler.append(f"iliski: '{kayit['iliski']}' onaylı şemada yok")
        try:
            beklenen = ozet(kanonik_json({a: d for a, d in kayit.items() if a != "ozet"}), self.algoritma)
        except KanonikHata as hata:
            return nedenler + [f"ozet hesaplanamıyor: {hata}"]
        if kayit["ozet"] != beklenen:
            nedenler.append("ozet: kaydın içeriğiyle tutmuyor")
        elif kayit["ozet"] in self._ozetler:
            nedenler.append("yineleme: birebir aynı kayıt zaten var")
        return nedenler

    def ekle(self, kayit):
        nedenler = self._nedenler(kayit)
        if nedenler:
            self.gunluk.ekle("KAYIT_REDDEDILDI", GUNLUK_KAYNAGI, {"nedenler": nedenler, "ham": repr(kayit)})
            return RET
        kopya = json.loads(kanonik_json(kayit))
        self._ozetler.add(kopya["ozet"])
        if kopya["kaynak"] == LLM_KAYNAGI:
            self._karantina.append(kopya)
            self.gunluk.ekle("KARANTINAYA_ALINDI", GUNLUK_KAYNAGI, {"ozet": kopya["ozet"]})
            return KARANTINA
        self._olgular.append(kopya)
        self.gunluk.ekle("KAYIT_EKLENDI", GUNLUK_KAYNAGI, {"ozet": kopya["ozet"]})
        return KABUL

    def olgular(self):
        return [dict(k) for k in self._olgular]

    def karantina(self):
        return [dict(k) for k in self._karantina]
