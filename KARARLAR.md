# KARARLAR

Kullanıcının onayladığı kararlar. Onaylı varsayımlar `VARSAYIMLAR.md`'den buraya taşınır.
Biçim: kimlik, tarih, karar, gerekçe, etkisi.

## K-001 (2026-10-23): "Bu turda prototip kod yazılmayacak" satırı geçersiz
- **Karar:** `sistem.md` "Fikir sahibinin kuralları" altındaki "BU TURDA PROTOTİP KOD YAZILMAYACAK" satırı eski kâğıt üstü tasarım turuna aittir, artık geçerli değildir. Kodlama `KODLAMA_PROMPTU.md` bölüm 4'teki aşama sırasıyla (A0'dan başlayarak) yapılır.
- **Onaylayan:** kullanıcı.
- **Etkisi:** tüm aşamalar. `sistem.md` değiştirilmedi.

## K-002 (2026-10-23): Eski ara dosya atıfları yok sayılır
- **Karar:** `sistem.md` Ek A–D içindeki `cozumler.md`, `bulgular.md` ve `/tmp/...` klasör atıfları eski ara dosyalardır. Gerekli değildir, yok sayılır.
- **Onaylayan:** kullanıcı.

## K-003 (2026-10-23): Çelişkide sistem.md Kısım 1 kazanır
- **Karar:** Ek'ler ile Kısım 1 (§1–19) çelişirse Kısım 1 kazanır (`sistem.md` başlığındaki kuralın kullanıcı tarafından teyidi).
- **Onaylayan:** kullanıcı.

## K-004 (2026-10-23): Çekirdek kayıtlarında saat yerine adım numarası (V-006'dan)
- **Karar:** Çekirdek kayıtlarında gerçek saat (duvar saati) kullanılmaz. Zaman bilgisi mantıksal saattir: sıra/adım/tur numarası. Gerçek saat yalnız çekirdek dışı kayıtlarda (besleme, tercüman) durabilir ve hash, karşılaştırma ve bağımsızlık testi dışında tutulur.
- **Gerekçe:** aynı girdi ve tohum çekirdekte bit düzeyinde aynı çıktıyı vermeli (KODLAMA_PROMPTU §5, sistem.md §16).
- **Onaylayan:** kullanıcı.
- **Etkisi:** `cekirdek/altyapi/olay_gunlugu.py` (zaman alanı yok, sıra numarası var; değişiklik gerekmedi). A1'den itibaren tüm çekirdek veri kayıtları.

## K-005 (2026-10-23): A1'e bağımsız inceleme beklenmeden geçildi
- **Karar:** Kullanıcı, A0 bağımsız incelemesini beklemeden A1'e başlanmasını istedi. İnceleme istemi (`inceleme/A0_istemi.md`) hazır durur ve sonra koşturulabilir.
- **Onaylayan:** kullanıcı.
- **Etkisi:** KODLAMA_PROMPTU §4 "Bağımsız inceleme" adımı A0 için ertelendi.
