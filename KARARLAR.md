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

## K-006 (2026-10-23): İlişki şeması sürüm 1 onaylandı (V-013'ten)
- **Karar:** `sema/iliskiler_v1.json` (21 ilişki, okuma "(A, r, B) = B, A'nın r'sidir") kullanıcı tarafından onaylandı ve `kilit/sema_onayi.json` ile hash kilidine alındı. Dosyadaki "TASLAK" notu, onaylanan baytları değiştirmemek için olduğu gibi bırakıldı.
- **Onaylayan:** kullanıcı. Hata çıkarsa yeni sürüm (`iliskiler_v2.json`) ve yeni onayla düzeltilir.

## K-007 (2026-10-23): Üreteç tasarımı onaylandı (V-015'ten)
- **Karar:** V-015'teki öneri: üreteç `degerlendirme/` altında, soyut ağaç (tamsayı kişi, iki tip, yukarı/aşağı/eş bağı), ilişkilerin yapısal tanımları gizli veri dosyasında, olgular yalnız doğrudan bağlar, ağacın geri kalanı dikkat dağıtıcı, A1'de isim yok, cevaplar ayrı dosyada.
- **Onaylayan:** kullanıcı.

## K-008 (2026-10-23): Kelime çantası kuralı onaylandı (V-016'dan)
- **Karar:** dedektörün çözdüğü örnekler ayrı "Treg kümesine" ayrılır (sistem.md §10). Kalan ana kümede kelime çantası sınıflayıcısının doğruluğu şans + %5'i geçerse üretim durur (KODLAMA_PROMPTU §6). Şans = en sık cevabın oranı. Dedektör: yapıya bakmayan, yalnız ilişki adı sayıları ve kişi kimlikleri kullanan Naive Bayes; ayrı bölmede eğitilir, başka bölmede ölçülür.
- **Onaylayan:** kullanıcı.
