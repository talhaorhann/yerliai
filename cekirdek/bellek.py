"""sistem.md §8 (bellek hücresi), §15 (bellek salt okunur, sürüm kilitli), EK A P7 (geri alınabilir statü); V-056.

Bellek, sadece-ekleme ve hash zincirli bir olay günlüğüdür (OlayGunlugu alt sınıfı). İki olay vardır:
`BELLEK_KABUL` (hücre verisi + geçit kanıtı) ve `BELLEK_GERI_ALMA` (kimlik + neden). Kabul edilmiş kayıt hiçbir zaman
değiştirilmez ya da silinmez; geri alma yeni bir olaydır. Sürüm = son olayın özeti. Aktif hücreler olaylardan kurulur;
dosyadan yeniden açılınca aynı sonuç çıkar, kurcalanmış dosya açılmaz.
Mutasyondan koruma ve düşük eşikle hızlı tetiklenme (§8) H2/H3 ile gelir.
"""
import copy

from cekirdek.altyapi.olay_gunlugu import ILK_ONCEKI_OZET, OlayGunlugu
from cekirdek.dna import dna_kur

BELLEK_KABUL, BELLEK_GERI_ALMA = "BELLEK_KABUL", "BELLEK_GERI_ALMA"  # V-056
KAYNAK = "çekirdek"  # KODLAMA_PROMPTU §5
DNA_SURUMU = "2"  # V-043: bellekteki hücreler DNA sürüm 2 biçimindedir


class BellekHatasi(ValueError):
    pass


class Bellek(OlayGunlugu):
    def __init__(self, yol, algoritma, sema_surumu, izinli_kaynaklar):
        self._aktif = {}
        super().__init__(yol, algoritma, sema_surumu, izinli_kaynaklar)

    def _eklendi(self, kayit):
        veri = kayit["veri"]
        if kayit["tur"] == BELLEK_KABUL:
            self._aktif[veri["hucre"]["kimlik"]] = veri["hucre"]
        elif kayit["tur"] == BELLEK_GERI_ALMA:
            self._aktif.pop(veri["kimlik"], None)

    @property
    def surum(self):
        return self._kayitlar[-1]["ozet"] if self._kayitlar else ILK_ONCEKI_OZET

    def kabul_et(self, hucre_verisi, kanit):
        if hucre_verisi["kimlik"] in self._aktif:
            raise BellekHatasi(f"{hucre_verisi['kimlik']} zaten bellekte")
        return self.ekle(BELLEK_KABUL, KAYNAK, {"hucre": hucre_verisi, "kanit": kanit})

    def geri_al(self, kimlik, neden):
        if kimlik not in self._aktif:
            raise BellekHatasi(f"{kimlik} bellekte aktif değil")
        return self.ekle(BELLEK_GERI_ALMA, KAYNAK, {"kimlik": kimlik, "neden": neden})

    def aktif_veriler(self):
        """Kabul sırasıyla aktif hücre verileri (kopya: bellek dışarıdan değiştirilemez)."""
        return [copy.deepcopy(self._aktif[k]) for k in self._aktif]

    def hucreler(self, bicim_yolu, iliski_semasi):
        veriler = self.aktif_veriler()
        return dna_kur({"sema_surumu": DNA_SURUMU, "hucreler": veriler}, bicim_yolu, iliski_semasi) if veriler else ()
