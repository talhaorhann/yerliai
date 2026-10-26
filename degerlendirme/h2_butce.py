"""sistem.md §13; K-041 (ÖK-005 taslağı §4 madde 2 ve 3), V-063: aşama 5 sorgu bütçesi defteri.

Sorgu birimi (aday, taze dünya) çiftidir; hüküm tek aday kimliği içindir (grup sorgusu yok). Tur sayısı ve turda aday
sayısı sınırlıdır; bir turda kullanılan taze dünya sonraki turlarda kullanılamaz (yanar). Defter sadece-eklemeli ve hash
zincirlidir (`OlayGunlugu`); kaldığı yerden devam eder, kurcalanmış dosya açılmaz.
"""
from cekirdek.altyapi.olay_gunlugu import OlayGunlugu

TUR_ACILDI, SORGU = "TUR_ACILDI", "SORGU"  # V-063: olay türleri


class ButceHatasi(RuntimeError):
    pass


class SorguDefteri(OlayGunlugu):
    def __init__(self, yol, h2_ayar, tur_basina_aday, algoritma="sha256", sema_surumu="1"):  # V-007, V-063
        self.tur_basina = tur_basina_aday
        self.tur_siniri = h2_ayar.deger("sorgu_tur_siniri")
        self.kaynak = h2_ayar.deger("sorgu_defteri_kaynagi")
        self.tur, self._adaylar, self._dunya_turu, self._ciftler = 0, {}, {}, set()
        super().__init__(yol, algoritma, sema_surumu, {self.kaynak})

    def _eklendi(self, kayit):
        v = kayit["veri"]
        if kayit["tur"] == TUR_ACILDI:
            self.tur = v["tur"]
            self._adaylar[self.tur] = set()
        elif kayit["tur"] == SORGU:
            self._adaylar[v["tur"]].add(v["aday"])
            self._dunya_turu.setdefault(v["dunya"], v["tur"])
            self._ciftler.add((v["tur"], v["aday"], v["dunya"]))

    def tur_ac(self):
        if self.tur >= self.tur_siniri:
            raise ButceHatasi("tur sınırı doldu")
        return self.ekle(TUR_ACILDI, self.kaynak, {"tur": self.tur + 1})

    def turdaki_adaylar(self):
        return set(self._adaylar.get(self.tur, ()))

    def sorgu(self, aday, dunya):
        if not isinstance(aday, str) or not isinstance(dunya, str):
            raise ButceHatasi("sorgu tek aday kimliği ve tek dünya içindir (grup sorgusu yok)")
        if self.tur == 0:
            raise ButceHatasi("tur açılmadan sorgu yok")
        if aday not in self._adaylar[self.tur] and len(self._adaylar[self.tur]) >= self.tur_basina:
            raise ButceHatasi("turda aday sınırı doldu")
        if self._dunya_turu.get(dunya, self.tur) != self.tur:
            raise ButceHatasi("taze dünya önceki bir turda kullanıldı (yandı)")
        if (self.tur, aday, dunya) in self._ciftler:
            raise ButceHatasi("aynı (aday, dünya) çifti bu turda zaten soruldu")
        return self.ekle(SORGU, self.kaynak, {"tur": self.tur, "aday": aday, "dunya": dunya})


def tur_basina_aday(talep, p_yildiz, h2_ayar):
    """ÖK-005 taslağı §4 madde 3: talep (C) ≤ 200 × 12 ise 200, değilse 400; P* ölçüldüyse en çok ⌊P*/(2 × 12)⌋."""
    dar, genis = h2_ayar.deger("sorgu_tur_basina_aday"), h2_ayar.deger("sorgu_tur_basina_aday_genis")
    tur = h2_ayar.deger("sorgu_tur_siniri")
    secim = dar if talep <= dar * tur else genis
    if p_yildiz is not None:
        secim = min(secim, p_yildiz // (h2_ayar.deger("sorgu_basinc_boleni") * tur))
    return secim
