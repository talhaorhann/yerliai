"""KODLAMA_PROMPTU §5 (Tensör şekilleri): tek SEKILLER tablosu (eksen anlamları) ve şekil denetimi.

Referans yol iç içe listelerle/demetlerle çalışır; hızlı yol (K-015) aynı eksen adlarını kullanacak.
Denetim `assert` ile değil açık hatayla yapılır (python -O ile kapanmasın diye).
"""

SEKILLER = {
    "boyut": "vektör boyutu d (K-014)",
    "kayit": "üçlü kaydı sırası (bilgi tabanı / havuz satırları)",
    "aday": "karşılaştırılan aday sırası (benzerlik matrisinin sütunları, kod kitabı girdileri)",
}


class SekilHatasi(ValueError):
    pass


def sekil(x):
    """İç içe liste/demetin şekli. Düzensiz (girintili) yapı reddedilir. Boş liste (0,) döner."""
    if not isinstance(x, (list, tuple)):
        return ()
    if not x:
        return (0,)
    alt = [sekil(o) for o in x]
    if any(s != alt[0] for s in alt):
        raise SekilHatasi("düzensiz şekil")
    return (len(x),) + alt[0]


def sekil_dogrula(x, eksenler, **boyutlar):
    """x'in eksen sayısı ve verilen eksen boyları doğru mu? Boş (ilk ekseni 0) yapıda sonraki eksenler bilinemez."""
    for eksen in tuple(eksenler) + tuple(boyutlar):
        if eksen not in SEKILLER:
            raise SekilHatasi(f"SEKILLER tablosunda olmayan eksen: {eksen}")
    s = sekil(x)
    if s == (0,):
        if boyutlar.get(eksenler[0], 0) != 0:
            raise SekilHatasi(f"{eksenler[0]} ekseni boş")
        return x
    if len(s) != len(eksenler):
        raise SekilHatasi(f"beklenen eksenler {eksenler}, şekil {s}")
    for eksen, uzunluk in zip(eksenler, s):
        if eksen in boyutlar and boyutlar[eksen] != uzunluk:
            raise SekilHatasi(f"{eksen} ekseni {boyutlar[eksen]} olmalı, {uzunluk} geldi")
    return x
