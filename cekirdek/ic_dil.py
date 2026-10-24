"""sistem.md §17 (kapalı iç form), §15, §18; V-055: iç dil, sürüm 1.

Çekirdek yalnız bu kapalı, tipli, sürümlü forma bakar: üçlü + kutup + kip + zaman + kaynak + güven. Biçim
`sema/ic_dil_v1.schema.json`; ilişki onaylı şemada olmalı. Özet, kaydın `ozet` dışındaki alanlarının kanonik JSON'ından
alınır: kayıt sonradan değiştirilirse özet tutmaz ve kayıt reddedilir.
Havuza şimdilik yalnız olumlu + kesin + zamansız kayıt girer. Olumsuz kutup, olası kip ve zamanın çekirdekteki anlamı
kullanıcı kararıdır (NotImplementedError). LLM kaynaklı kayıt karantinasız havuza giremez (§15, §18; karantina A7'de).
"""
from cekirdek.altyapi.kanonik import kanonik_json, ozet
from cekirdek.altyapi.sema_dogrulayici import sema_yukle

SURUM = "ic1"  # V-055
OLUMLU, OLUMSUZ = "olumlu", "olumsuz"  # V-055: kutup
KESIN, OLASI = "kesin", "olasi"  # V-055: kip
LLM_KAYNAGI = "LLM"  # sistem.md §15: insan onayı ve karantina olmadan öğrenmeye girmez


class IcDilHatasi(ValueError):
    pass


class KarantinaHatasi(IcDilHatasi):
    """LLM kaynaklı kayıt karantinadan geçmeden çekirdeğe giremez (§15, §18)."""


def _ozet(kayit, algoritma):
    return ozet(kanonik_json({a: d for a, d in kayit.items() if a != "ozet"}), algoritma)


def ic_kayit(ozne, iliski, nesne, *, kaynak, guven, algoritma, kutup=OLUMLU, kip=KESIN, zaman=None):
    kayit = {"sema_surumu": SURUM, "ozne": ozne, "iliski": iliski, "nesne": nesne, "kutup": kutup, "kip": kip,
             "zaman": zaman, "kaynak": kaynak, "guven": guven}
    kayit["ozet"] = _ozet(kayit, algoritma)
    return kayit


def ic_kayit_dogrula(kayit, iliski_semasi, bicim_yolu, algoritma):
    hatalar = sema_yukle(bicim_yolu).hatalar(kayit)
    if hatalar:
        raise IcDilHatasi("iç dil biçimine uymuyor: " + "; ".join(hatalar))
    if kayit["iliski"] not in iliski_semasi:
        raise IcDilHatasi(f"ilişki onaylı şemada yok: {kayit['iliski']}")
    if kayit["ozet"] != _ozet(kayit, algoritma):
        raise IcDilHatasi("özet tutmuyor: kayıt değiştirilmiş")
    return kayit


def havuza_al(havuz, kayit, iliski_semasi, bicim_yolu, algoritma):
    """Doğrulanmış iç dil kaydını havuza epitop olarak ekler."""
    ic_kayit_dogrula(kayit, iliski_semasi, bicim_yolu, algoritma)
    if kayit["kaynak"] == LLM_KAYNAGI:
        raise KarantinaHatasi("LLM kaynaklı kayıt karantinadan geçmeden havuza giremez")
    if kayit["kutup"] != OLUMLU or kayit["kip"] != KESIN or kayit["zaman"] is not None:
        raise NotImplementedError("olumsuz kutup, olası kip ve zamanın çekirdekteki anlamı kullanıcı kararıdır (V-055)")
    return havuz.epitop_ekle(kayit["ozne"], kayit["iliski"], kayit["nesne"], guven=kayit["guven"])
