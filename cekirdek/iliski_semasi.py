"""sistem.md §14, KODLAMA_PROMPTU §2.6: kullanıcının onayladığı tek sürümlü ilişki şeması (V-013).

Şema yalnız onay kaydındaki hash tutarsa yüklenir. Kodda hiçbir ilişki adı yoktur; adlar veridir.
İlişki tanımları (gizli kurallar) bu dosyada değildir ve çekirdek onları göremez.
"""
import hashlib
import json
import os
import re

from cekirdek.altyapi.sema_dogrulayici import SemaHatasi, sema_yukle

ONAY_ALANLARI = {"dosya", "algoritma", "ozet", "karar"}  # V-013
KARAR_DESENI = re.compile(r"^K-\d{3}$")  # V-002


class SemaOnayHatasi(ValueError):
    pass


class IliskiSemasi:
    def __init__(self, surum, okuma, iliskiler, dislayici_gruplar, ozet):
        self.surum = surum
        self.okuma = okuma
        self.ozet = ozet
        self.adlar = tuple(i["ad"] for i in iliskiler)
        self._ters = {i["ad"]: tuple(i["ters"]) for i in iliskiler}
        self._simetrik = {i["ad"]: i["simetrik"] for i in iliskiler}
        self._islevsel = {i["ad"]: i["islevsel"] for i in iliskiler}
        self._dislayici = frozenset(frozenset((a, b)) for grup in dislayici_gruplar
                                    for a in grup for b in grup if a != b)

    def __contains__(self, ad):
        return ad in self._ters

    def ters(self, ad):
        return self._ters[ad]

    def simetrik(self, ad):
        return self._simetrik[ad]

    def islevsel(self, ad):
        return self._islevsel[ad]

    def dislayici_mi(self, a, b):
        return frozenset((a, b)) in self._dislayici


def _dogrula_ve_kur(veri, bicim_yolu, ozet=None):
    hatalar = sema_yukle(bicim_yolu).hatalar(veri)
    if hatalar:
        raise SemaHatasi("ilişki şeması biçime uymuyor: " + "; ".join(hatalar))
    adlar = [i["ad"] for i in veri["iliskiler"]]
    if len(set(adlar)) != len(adlar):
        raise SemaHatasi("yinelenen ilişki adı")
    ters = {i["ad"]: i["ters"] for i in veri["iliskiler"]}
    for i in veri["iliskiler"]:
        for t in i["ters"]:
            if t not in ters:
                raise SemaHatasi(f"{i['ad']}: bilinmeyen ters ilişki {t}")
            if i["ad"] not in ters[t]:
                raise SemaHatasi(f"{i['ad']} ile {t} karşılıklı ters değil")
        if i["simetrik"] and i["ters"] != [i["ad"]]:
            raise SemaHatasi(f"{i['ad']}: simetrik ilişkinin tersi yalnız kendisi olmalı")
    for grup in veri["dislayici_gruplar"]:
        for ad in grup:
            if ad not in ters:
                raise SemaHatasi(f"dışlayıcı grupta bilinmeyen ilişki {ad}")
    return IliskiSemasi(veri["sema_surumu"], veri["okuma"], veri["iliskiler"], veri["dislayici_gruplar"], ozet)


def iliski_semasi_yukle(sema_yolu, onay_yolu, bicim_yolu):
    if not os.path.exists(onay_yolu):
        raise SemaOnayHatasi("ilişki şeması kullanıcı tarafından onaylanmamış (onay kaydı yok)")
    with open(onay_yolu, encoding="utf-8") as f:
        onay = json.load(f)
    if not isinstance(onay, dict) or set(onay) != ONAY_ALANLARI:
        raise SemaOnayHatasi(f"onay kaydı alanları tam olarak {sorted(ONAY_ALANLARI)} olmalı")
    if not isinstance(onay["karar"], str) or not KARAR_DESENI.match(onay["karar"]):
        raise SemaOnayHatasi("onay kaydında K-nnn karar kimliği yok")
    if onay["dosya"] != os.path.basename(sema_yolu) or onay["algoritma"] not in hashlib.algorithms_guaranteed:
        raise SemaOnayHatasi("onay kaydı bu şema dosyasına ait değil")
    with open(sema_yolu, "rb") as f:
        ham = f.read()
    ozet = hashlib.new(onay["algoritma"], ham).hexdigest()
    if ozet != onay["ozet"]:
        raise SemaOnayHatasi("şema dosyası onaydan sonra değişmiş; yeniden onay gerekir")
    return _dogrula_ve_kur(json.loads(ham.decode("utf-8")), bicim_yolu, ozet)
