"""sistem.md §2: iki katmanlı havuz (0: epitoplar, 1: çıkarımlar), ilişki dizini, (üçlü, köken) tekilleştirmesi.

Kayıt: vektör (kod kitabının yoluyla, V-042), üçlü, katman, köken (zincir kimliği + ebeveyn kayıt kimlikleri),
güven, yaş. Yaş = geçen tur sayısı (K-004: saat yok). Dolunca yalnız çıkarım katmanından en düşük güvenli kayıt atılır (eşitlikte en yaşlı,
sonra en küçük kimlik; K-019). Atılan kayıt eşleşmeye katılmaz ama kökeni mezar taşında kalır (V-033).
"""
import math
from dataclasses import dataclass

EPITOP, CIKARIM = 0, 1  # sistem.md §2


class HavuzHatasi(RuntimeError):
    pass


class HavuzDoluHatasi(HavuzHatasi):
    """Havuz dolu ve atılabilecek çıkarım yok: yeni çıkarım yazılamaz (çağıran YEDEK_KULLANILDI yazar)."""


@dataclass(frozen=True)
class Kayit:
    kimlik: int
    vektor: tuple
    uclu: tuple
    katman: int
    zincir: object
    ebeveynler: tuple
    guven: float
    yazildigi_tur: int


class Havuz:
    def __init__(self, kapasite, kod_kitabi):
        self.kapasite = kapasite
        self.kod_kitabi = kod_kitabi
        self.tur = 0
        self._kayitlar = {}
        self._sonraki = 0
        self._dizin = {}
        self._kokenler = set()
        self._mezar = {}
        self._son_atilanlar = []

    def _guven_denetle(self, guven):
        if not isinstance(guven, (int, float)) or not math.isfinite(guven) or not 0 <= guven <= 1:
            raise HavuzHatasi(f"güven [0,1] aralığında sonlu sayı olmalı: {guven!r}")

    def _yaz(self, uclu, katman, zincir, ebeveynler, guven):
        k = Kayit(self._sonraki, self.kod_kitabi.kayit_vektoru(*uclu), tuple(uclu), katman, zincir,
                  tuple(ebeveynler), guven, self.tur)
        self._kayitlar[k.kimlik] = k
        self._dizin.setdefault(k.uclu[1], []).append(k.kimlik)
        self._sonraki += 1
        return k

    def epitop_ekle(self, ozne, iliski, nesne, guven):
        self._guven_denetle(guven)
        if len(self._kayitlar) >= self.kapasite:
            raise HavuzHatasi("epitoplar havuz kapasitesini aşıyor: bölüm reddedildi (V-031)")
        return self._yaz((ozne, iliski, nesne), EPITOP, None, (), guven)

    def cikarim_ekle(self, uclu, zincir, ebeveynler, guven):
        """Yeni çıkarım kaydı. Aynı (üçlü, köken) zaten yazılmışsa None döner (§3 karma tablo)."""
        self._guven_denetle(guven)
        if not ebeveynler or any(e not in self._kayitlar and e not in self._mezar for e in ebeveynler):
            raise HavuzHatasi(f"çıkarımın ebeveynleri havuzda olmalı: {ebeveynler}")
        anahtar = (tuple(uclu), zincir, tuple(ebeveynler))
        if anahtar in self._kokenler:
            return None
        if len(self._kayitlar) >= self.kapasite:
            self._at()
        self._kokenler.add(anahtar)
        return self._yaz(uclu, CIKARIM, zincir, ebeveynler, guven)

    def _at(self):
        adaylar = [k for k in self._kayitlar.values() if k.katman == CIKARIM]
        if not adaylar:
            raise HavuzDoluHatasi("havuz dolu ve atılabilecek çıkarım yok")
        atilan = min(adaylar, key=lambda k: (k.guven, k.yazildigi_tur, k.kimlik))
        del self._kayitlar[atilan.kimlik]
        self._dizin[atilan.uclu[1]].remove(atilan.kimlik)
        self._mezar[atilan.kimlik] = atilan
        self._son_atilanlar.append(atilan)

    def atilanlari_al(self):
        """Son çağrıdan beri atılan kayıtlar (günlüğe yazılmak üzere)."""
        atilanlar, self._son_atilanlar = self._son_atilanlar, []
        return atilanlar

    def tur_ilerlet(self):
        self.tur += 1

    def yas(self, kimlik):
        return self.tur - self._kayitlar[kimlik].yazildigi_tur

    def kayit(self, kimlik):
        """Canlı kayıt ya da mezar taşı (köken ve gerekçe için)."""
        return self._kayitlar[kimlik] if kimlik in self._kayitlar else self._mezar[kimlik]

    def kayitlar(self):
        return [self._kayitlar[k] for k in sorted(self._kayitlar)]

    def iliski_dizini(self, iliski):
        return tuple(self._dizin.get(iliski, ()))
