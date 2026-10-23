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
