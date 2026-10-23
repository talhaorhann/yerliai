"""KODLAMA_PROMPTU §2.1, §5 (Defter); sistem.md §18; V-035: destek/çelişki defteri.

Sadece-ekleme, sıra numaralı, hash zincirli olay günlüğüdür (A0'ın alt sınıfı). Her ateşleme, yazma ve atma
kayıtlıdır. Dizin olaylardan kurulur (dosyadan yeniden açılınca yeniden oluşur): hangi çıkarım yazıldı, hangisi
atıldı, kök kümeleri. "Defterde izi olmayan sonuç yanıta giremez": plazma yalnız `yazildi_mi` olanları sayar.
Destek = bir üçlünün canlı ispatlarında kök kümeleri ayrık bileşen sayısı (K-018 ile aynı bileşen tanımı).
"""
from cekirdek.altyapi.olay_gunlugu import OlayGunlugu
from cekirdek.plazma import bilesenler

ATESLEME, YAZMA, ATMA = "ATESLEME", "YAZMA", "ATMA"  # KODLAMA_PROMPTU §5


class Defter(OlayGunlugu):
    def __init__(self, yol, algoritma, sema_surumu, izinli_kaynaklar):
        self._yazilan = {}
        self._atilan = set()
        super().__init__(yol, algoritma, sema_surumu, izinli_kaynaklar)

    def _eklendi(self, kayit):
        veri = kayit["veri"]
        if kayit["tur"] == YAZMA:
            self._yazilan[veri["kimlik"]] = (tuple(veri["uclu"]), frozenset(veri["kokler"]))
        elif kayit["tur"] == ATMA:
            self._atilan.add(veri["kimlik"])

    def yazildi_mi(self, kimlik):
        return kimlik in self._yazilan

    def kokler(self, kimlik):
        return self._yazilan[kimlik][1]

    def canli_ispatlar(self, uclu):
        uclu = tuple(uclu)
        return tuple(k for k in sorted(self._yazilan) if self._yazilan[k][0] == uclu and k not in self._atilan)

    def destek(self, uclu):
        return len(bilesenler([self.kokler(k) for k in self.canli_ispatlar(uclu)]))
