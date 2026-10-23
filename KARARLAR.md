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

## K-009 (2026-10-23): Gizli yapısal tanımlar sürüm 1 onaylandı (V-019'dan)
- **Karar:** `degerlendirme/veri/tanimlar_v1.json` (okunur hâli `TANIMLAR_OKUNUR.md`) onaylandı ve hash kilidine alındı (`kilit/kilitler.json`). Hata çıkarsa yeni sürümle düzeltilir.
- **Onaylayan:** kullanıcı.

## K-010 (2026-10-23): "Önsel-ters" bölmesinin tanımı (V-020'den)
- **Karar:** önsel-ters bölmesinde cevap dağılımı eğitimdekinin tersidir: eğitimde nadir olan cevaplar burada sık, sık olanlar nadir olur.
- **Onaylayan:** kullanıcı.

## K-011 (2026-10-23): Altın küme yolu (V-021'den)
- **Karar:** Üreteçten ayrı tohumla 100 soru hazırlanır, iki parça (50 + 50). Kullanıcı üretecin cevabını görmeden cevaplar. Biçim: her soruda A/B/C/D seçeneği. Altın kümede "beklenen" cevap kullanıcının cevabıdır, kodun çıktısı beklenen diye kaydedilmez. Kullanıcı ile üretecin uyuşmadığı sorular ayrıca incelenir.
- **Onaylayan:** kullanıcı.

## K-012 (2026-10-23): PyTorch ve NumPy çekirdekte izinli (V-005'ten)
- **Karar:** Çekirdek PyTorch ve NumPy kullanabilir. Sürümler sabittir: torch==2.14.1, numpy==2.5.3. Lisanslar `LISANSLAR.md`'de, resmî dosyalardan doğrulanmıştır.
- **Ek karar:** Çekirdek önce CPU/tamsayı yolunda deterministik yazılır. GPU ayrı aşamada, ayrı doğrulamayla açılır (KODLAMA_PROMPTU §10 bilinen boşluğun cevabı).
- **Onaylayan:** kullanıcı.

## K-013 (2026-10-23): Altın küme 1. parça cevaplarının kaynağı
- **Karar:**
  - 1. parça cevapları bir LLM'in ön cevabıdır. Kullanıcı gözden geçirip kabul etmiştir.
  - Kayıt: `kaynak=LLM, onaylayan=kullanıcı, bagimsiz_insan_cevabi=false` (`degerlendirme/altin/kullanici_cevaplari_1.json`, sha256 306ee0a0c54d3d6972695ae8a0c8c14e8dff12e2d6ef084884a9fd345a5c45ff).
  - Bağımsızlık kısıtı `ONKAYIT.md`'ye eklendi.
- **Onaylayan:** kullanıcı.
