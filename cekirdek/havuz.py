"""sistem.md §2: iki katmanlı havuz (0: epitoplar, 1: çıkarımlar), ilişki dizini, (üçlü, köken) tekilleştirmesi.

Kayıt: vektör, üçlü, katman, köken (zincir kimliği + ebeveyn kayıt kimlikleri), güven, yaş. Yaş = geçen tur
sayısı (K-004: saat yok). Kapasite dolunca atma kuralı V-031 onayına bağlıdır; o zamana kadar çalışmaz.
"""
import math
from dataclasses import dataclass

from cekirdek.vektor import kayit_vektoru

EPITOP, CIKARIM = 0, 1  # sistem.md §2


class HavuzHatasi(RuntimeError):
    pass


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

    def _guven_denetle(self, guven):
        if not isinstance(guven, (int, float)) or not math.isfinite(guven) or not 0 <= guven <= 1:
            raise HavuzHatasi(f"güven [0,1] aralığında sonlu sayı olmalı: {guven!r}")

    def _yaz(self, uclu, katman, zincir, ebeveynler, guven):
        k = Kayit(self._sonraki, kayit_vektoru(self.kod_kitabi, *uclu), tuple(uclu), katman, zincir,
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
        if not ebeveynler or any(e not in self._kayitlar for e in ebeveynler):
            raise HavuzHatasi(f"çıkarımın ebeveynleri havuzda olmalı: {ebeveynler}")
        anahtar = (tuple(uclu), zincir, tuple(ebeveynler))
        if anahtar in self._kokenler:
            return None
        if len(self._kayitlar) >= self.kapasite:
            self._at()
        self._kokenler.add(anahtar)
        return self._yaz(uclu, CIKARIM, zincir, ebeveynler, guven)

    def _at(self):
        raise NotImplementedError("VARSAYIM V-031 onay bekliyor: havuzdan atma kuralı")

    def tur_ilerlet(self):
        self.tur += 1

    def yas(self, kimlik):
        return self.tur - self._kayitlar[kimlik].yazildigi_tur

    def kayit(self, kimlik):
        return self._kayitlar[kimlik]

    def kayitlar(self):
        return [self._kayitlar[k] for k in sorted(self._kayitlar)]

    def iliski_dizini(self, iliski):
        return tuple(self._dizin.get(iliski, ()))
