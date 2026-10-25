"""sistem.md §8, §15, §16, §18, EK A P7; K-035, K-036, V-054, V-056: bellek hattı (geçit + bellek deposu + anlatıcı yeri).

- `degerlendir`: adayın bellekteki bir kuralla yapıca eşdeğerliği (çekirdek) ve ortam ölçümleri (`gozlem_puani`,
  çekirdek dışı) toplanır; kararı çekirdeğin `karar_ver`'i verir (yalnız eşikler).
- `bellege_al`: adaylar sırayla, o anki aktif bellekle değerlendirilir; kabul edilen belleğe yazılır (kanıt = ölçümler).
- `gozden_gecir`: her aktif bellek hücresi ötekilerle yeniden sınanır; yanlış, kısayol ya da çelişkili çıkan geri alınır
  (silinmez, olay yazılır; EK A P7 geri alınabilir statü).
- Anlatıcı (LLM'in yeri, sistem.md §15): bütün kararlar verilip belleğe yazıldıktan SONRA her kararın kopyasıyla
  çağrılır. Döndürdüğü metin yalnız geri verilir ve "doğrulanmadı" işaretlidir; metin olmayan çıktı alınmaz. Karara,
  belleğe ya da deftere girmez. Bağımsızlık testi (sistem.md §16): anlatıcısız, sahte ve başka anlatıcıyla kararlar ve
  bellek baytları aynıdır.
Kâhin yoktur: üreteç, dünya ve altın küme içe aktarılmaz.
"""
import dataclasses
from dataclasses import dataclass

from cekirdek.bellek import DNA_SURUMU
from cekirdek.bellek_gecidi import CELISKILI, KABUL, KISAYOL, RET, YANLIS, esdeger_mi, karar_ver
from cekirdek.dna import dna_kur
from degerlendirme import gozlem_puani

DOGRULANMADI = "dogrulanmadi"  # sistem.md §15: çekirdekten gelmeyen cümle
GERI_ALMA_NEDENLERI = (YANLIS, KISAYOL, CELISKILI)  # EK A P7: gözden geçirmede geri aldıran ret nedenleri


@dataclass(frozen=True)
class HatSonucu:
    kararlar: list
    anlatimlar: list


def degerlendir(aday, bellek, ortamlar, iliski_semasi, kk, prm, gunluk_ayari, esikler):
    """`ortamlar`: {ad: [bölüm]}; bölümde yalnız gözlemler kullanılır (sorgu ve cevap okunmaz)."""
    if not ortamlar:
        raise ValueError("bellek geçidi en az bir ortam ister")
    bellek = tuple(bellek)
    if esdeger_mi(aday, bellek):
        return karar_ver(True, {}, esikler)
    olcum = {ad: gozlem_puani.ortam_olcumu(aday, bellek, ortamlar[ad], iliski_semasi, kk, prm, gunluk_ayari)
             for ad in sorted(ortamlar)}
    return karar_ver(False, olcum, esikler)


def _anlat(anlatici, kimlik, karar):
    metin = anlatici({"kimlik": kimlik, **dataclasses.asdict(karar)})  # asdict derin kopya verir
    return {"kimlik": kimlik, "metin": metin if isinstance(metin, str) else None, "durum": DOGRULANMADI}


def bellege_al(depo, aday_verileri, ortamlar, bicim_yolu, iliski_semasi, kk, prm, gunluk_ayari, esikler,
               anlatici=None):
    """`aday_verileri`: DNA sürüm 2 hücre verileri, sırayla. `depo`: `cekirdek.bellek.Bellek`."""
    kararlar = []
    for veri in aday_verileri:
        aday = dna_kur({"sema_surumu": DNA_SURUMU, "hucreler": [veri]}, bicim_yolu, iliski_semasi)[0]
        k = degerlendir(aday, depo.hucreler(bicim_yolu, iliski_semasi), ortamlar, iliski_semasi, kk, prm,
                        gunluk_ayari, esikler)
        if k.karar == KABUL:
            depo.kabul_et(veri, k.olcumler)
        kararlar.append((veri["kimlik"], k))
    anlatimlar = [] if anlatici is None else [_anlat(anlatici, kimlik, k) for kimlik, k in kararlar]
    return HatSonucu(kararlar, anlatimlar)


def gozden_gecir(depo, bicim_yolu, ortamlar, iliski_semasi, kk, prm, gunluk_ayari, esikler):
    """Geri alınan kimlikler döner."""
    geri = []
    for h in depo.hucreler(bicim_yolu, iliski_semasi):
        oteki = [x for x in depo.hucreler(bicim_yolu, iliski_semasi) if x.kimlik != h.kimlik]
        k = degerlendir(h, oteki, ortamlar, iliski_semasi, kk, prm, gunluk_ayari, esikler)
        if k.karar == RET and k.neden in GERI_ALMA_NEDENLERI:
            depo.geri_al(h.kimlik, k.neden)
            geri.append(h.kimlik)
    return geri
