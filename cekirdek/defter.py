"""KODLAMA_PROMPTU §2.1, §5 (Defter); sistem.md §18; V-035: destek/çelişki defteri.

Sadece-ekleme, sıra numaralı, hash zincirli olay günlüğüdür (A0'ın alt sınıfı). Her ateşleme, yazma ve atma
kayıtlıdır. Dizin olaylardan kurulur (dosyadan yeniden açılınca yeniden oluşur): hangi çıkarım yazıldı, hangisi
atıldı, kök kümeleri. "Defterde izi olmayan sonuç yanıta giremez": plazma yalnız `yazildi_mi` olanları sayar.
Destek = bir üçlünün canlı ispatlarında kök kümeleri ayrık bileşen sayısı (K-018 ile aynı bileşen tanımı).
Çelişki (K-020): dışlayıcı / işlevsel / ters, onaylı şemaya göre. Hiçbir kayıt silinmez; her çelişki bir kez
`CELISKI` olayıyla iki kayda bağlanır ve ortak destek kümesi (kök kümelerinin kesişimi) kalıcı kaydedilir.
"""
from cekirdek.altyapi.olay_gunlugu import OlayGunlugu
from cekirdek.plazma import bilesenler, kok_kumesi

ATESLEME, YAZMA, ATMA, CELISKI = "ATESLEME", "YAZMA", "ATMA", "CELISKI"  # KODLAMA_PROMPTU §5, K-020
DISLAYICI, ISLEVSEL, TERS = "dislayici", "islevsel", "ters"  # K-020
KAYNAK = "çekirdek"  # KODLAMA_PROMPTU §5


def celiski_turleri(birinci, ikinci, iliski_semasi):
    """İki üçlü arasındaki şema çelişkileri (K-020, V-038)."""
    (s1, r1, o1), (s2, r2, o2) = birinci, ikinci
    turler = []
    if (s1, o1) == (s2, o2) and r1 != r2 and iliski_semasi.dislayici_mi(r1, r2):
        turler.append(DISLAYICI)
    if s1 == s2 and r1 == r2 and o1 != o2 and iliski_semasi.islevsel(r1):
        turler.append(ISLEVSEL)
    if (s1, o1) == (o2, s2) and s1 != o1 and iliski_semasi.ters(r1) and iliski_semasi.ters(r2) \
            and r2 not in iliski_semasi.ters(r1):
        turler.append(TERS)
    return turler


class Defter(OlayGunlugu):
    def __init__(self, yol, algoritma, sema_surumu, izinli_kaynaklar):
        self._yazilan = {}
        self._atilan = set()
        self._celiskiler = {}
        self._celiskili = set()
        super().__init__(yol, algoritma, sema_surumu, izinli_kaynaklar)

    def _eklendi(self, kayit):
        veri = kayit["veri"]
        if kayit["tur"] == YAZMA:
            self._yazilan[veri["kimlik"]] = (tuple(veri["uclu"]), frozenset(veri["kokler"]))
        elif kayit["tur"] == ATMA:
            self._atilan.add(veri["kimlik"])
        elif kayit["tur"] == CELISKI:
            self._celiskiler[(veri["tur_adi"],) + tuple(veri["kayitlar"])] = veri["ortak_destek"]
            self._celiskili.update(veri["kayitlar"])

    def yazildi_mi(self, kimlik):
        return kimlik in self._yazilan

    def kokler(self, kimlik):
        return self._yazilan[kimlik][1]

    def canli_ispatlar(self, uclu):
        uclu = tuple(uclu)
        return tuple(k for k in sorted(self._yazilan) if self._yazilan[k][0] == uclu and k not in self._atilan)

    def destek(self, uclu):
        return len(bilesenler([self.kokler(k) for k in self.canli_ispatlar(uclu)]))

    def celiskiye_karisti(self, kimlik):
        return kimlik in self._celiskili

    def celiski_denetle(self, havuz, iliski_semasi, tur):
        """Canlı kayıtlar arasında yeni şema çelişkilerini bulur ve kaydeder (kayıt silmeden)."""
        kayitlar = havuz.kayitlar()
        olaylar = []
        for i, a in enumerate(kayitlar):
            for b in kayitlar[i + 1:]:
                for tur_adi in celiski_turleri(a.uclu, b.uclu, iliski_semasi):
                    if (tur_adi, a.kimlik, b.kimlik) in self._celiskiler:
                        continue
                    ortak = sorted(kok_kumesi(havuz, a.kimlik) & kok_kumesi(havuz, b.kimlik))
                    olaylar.append((CELISKI, KAYNAK, {"tur": tur, "tur_adi": tur_adi, "kayitlar": [a.kimlik, b.kimlik],
                                                      "uclular": [list(a.uclu), list(b.uclu)], "ortak_destek": ortak}))
        return self.ekle_toplu(olaylar)
