"""sistem.md §13, KODLAMA_PROMPTU §5 (Determinizm); K-041 (ÖK-005 taslağı §5): H2 tohum türetme. Tohum etiketten gelir,
seçilmez ve değiştirilmez: tohum = sha256(önek + etiket) özetinin ilk hanelerinin onaltılık değeri."""
import hashlib

AYIRICI = "|"  # K-041: etiket parçalarının ayırıcısı


def etiket(*parcalar):
    metinler = [str(p) for p in parcalar]
    if any(AYIRICI in m for m in metinler):
        raise ValueError("etiket parçasında ayırıcı olamaz")
    return AYIRICI.join(metinler)


def tohum(h2_ayar, *parcalar):
    metin = h2_ayar.deger("tohum_oneki") + etiket(*parcalar)
    return int(hashlib.sha256(metin.encode("utf-8")).hexdigest()[:h2_ayar.deger("tohum_hex_uzunlugu")], 16)  # K-041
