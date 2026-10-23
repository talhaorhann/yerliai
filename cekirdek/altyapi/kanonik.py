"""KODLAMA_PROMPTU §5 (Determinizm, Şema ve veri): kanonik JSON ve hash (V-007)."""
import hashlib
import json


class KanonikHata(ValueError):
    pass


def kanonik_json(nesne):
    """Anahtar sıralı, boşluksuz, UTF-8 JSON baytları. NaN/Inf ve JSON dışı tipler reddedilir."""
    try:
        metin = json.dumps(nesne, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as hata:
        raise KanonikHata(f"kanonik JSON'a çevrilemez: {hata}") from hata
    return metin.encode("utf-8")


def ozet(baytlar, algoritma):
    return hashlib.new(algoritma, baytlar).hexdigest()
