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

## K-014 (2026-10-23): A2 vektör temsili onaylandı (V-024'ten)
- **Karar:** d = 256, öğeler ±1 tamsayı. Bağlama tamsayıyla tam dairesel evrişimdir. Kayıt vektörü v = 16·R[r] + P_s⊛E[s] + P_o⊛E[o]. Kosinüs benzerliği tamsayı nokta çarpımından hesaplanır. Vektörler (tohum, tür, ad) hash'inden üretilir.
- **Onaylayan:** kullanıcı.

## K-015 (2026-10-23): PyTorch hızlı yolu A5 öncesine ertelendi
- **Karar:** Ağ izni şimdilik yok (V-025). A2 yalnız saf Python tamsayı referans yoluyla kapanır. PyTorch hızlı yolu ve referansla bit-eşitlik testi A5 (H1) öncesine bırakılır. Bu sırada hız iddiası yazılmaz.
- **Onaylayan:** kullanıcı.

## K-016 (2026-10-23): Eşleşme, afinite ve güven (V-028'den)
- **Karar:**
  - İlişki geni sert süzgeçtir.
  - Afinite = kırp(kosinüs(alıcı, kayıt) · √3, 0, 1). Elle yazılan hücrede alıcı = 16·R[gen].
  - Halka afinite > θ ise eşleşir. Elle yazılan hücrelerde θ = 0,5.
  - Güven = min(afiniteler, ebeveyn güvenleri) × hücre güvenilirliği. Elle yazılan hücrede güvenilirlik 1.
  - Hücre başına tur başına en iyi 8 eşleşme yazılır. Tur bütçesi 1024.
- **Onaylayan:** kullanıcı.

## K-017 (2026-10-23): Durma ve impasse (V-029'dan)
- **Karar:**
  - Kalibrasyon kümesi oluşana kadar τ ile durma kapalı. Döngü yeni kayıt kalmayınca ya da 8 turda durur.
  - Impasse'te (yanıt yok, yeni kayıt yok) bütün θ'lar bir kez yarıya iner. İkinci impasse'te durur.
- **Onaylayan:** kullanıcı.

## K-018 (2026-10-23): Plazma hücresi (V-030'dan)
- **Karar:**
  - Kök kümesi kesişen ispatlar aynı bileşendedir. Bileşen içi MAX, bileşenler arası noisy-OR, sızıntı 0.
  - Cevap, en yüksek birleşik güvenli ilişkidir. İspat yoksa ya da en yüksekte eşitlik varsa "bilmiyorum".
  - Farklı ilişkilere giden ispatlar "çelişki" diye işaretlenir.
  - Gerekçe, köken DAG'ından verilir.
- **Onaylayan:** kullanıcı.

## K-019 (2026-10-23): Havuzdan atma; yayın sahnesi ertelendi (V-031'den)
- **Karar:**
  - Havuz dolunca çıkarım katmanından en düşük güvenli kayıt atılır. Eşitlikte en yaşlı, sonra en küçük kimlik.
  - Yayın sahnesi H3/H4'e kalır. A3'te eşleşme bütün havuzda yarı-naif yapılır.
- **Onaylayan:** kullanıcı.

## K-020 (2026-10-23): Çelişkinin tanımı ve etkisi (V-036'dan)
- **Karar:**
  - Çelişki türleri (onaylı şemaya göre):
    - **dışlayıcı:** aynı çiftte aynı dışlayıcı gruptan iki ilişki;
    - **işlevsel:** aynı özne, aynı işlevsel ilişki, iki farklı nesne;
    - **ters:** r(A,B) ile q(B,A), q ∉ ters(r).
  - Denetim her tur sonunda canlı kayıtlarda yapılır, epitoplar dahil. Hiçbir kayıt silinmez. `CELISKI` olayı iki kaydı ve ortak destek kümesini (kök kümelerinin kesişimi) kalıcı kaydeder.
  - Cevap K-018'deki gibi verilir. Çelişki cevabın köken alt grafına dokunursa müdahale puanının c bileşeni 0 olur.
- **Onaylayan:** kullanıcı.

## K-021 (2026-10-23): Müdahale testi ve puanı (V-037'den) + kullanıcının ek şartı
- **Karar:**
  - **(a)** Kök epitop silme (yalnız etkilenen köken alt grafı). a = güveni düşüren silmelerin oranı.
  - **(b)** İlgisiz epitopu tür uyumlu yedekle değiştirip yeniden koşma. b = cevabın değişmediği oran.
  - **(c)** Ters tutarlılığı ve çelişkisizlik. c ∈ {0, 1}.
  - **Puan** = a × b × c. Cevap yoksa puan yok. Geçişlilik sınanmaz (şemada bilgi yok).
- **Ek şart (kullanıcı):** (b) için ilgisiz epitop yoksa soru "sınanamadı" olur. Başarı sayılmaz: b ve puan boş kalır. H1 raporunda ayrı bir sayı olarak gösterilir (ör. "100 soruda 18 sınanamadı").
- **Onaylayan:** kullanıcı.

## K-022 (2026-10-23): PyTorch CPU sürümü kurulumu
- **Karar:** torch 2.14.1+cpu (`download.pytorch.org/whl/cpu`) ve CPU bağımlılıkları hash'leriyle sabitlenir (`gereksinimler.txt`). GPU (CUDA) sürümü gerekirse ayrıca konuşulur. Hızlı yol referansla bit düzeyinde aynı olmalıdır (K-015).
- **Onaylayan:** kullanıcı (ağ izni verildi).

## K-023 (2026-10-23): H1 ön kaydı (ÖK-002)
- **Karar:** `ONKAYIT.md` ÖK-002 metni H1'in ön kaydıdır ve kilitlenir. Kapı: kapıya giren her bölmede (uzunluk, yön ters, önsel-ters, zincir-bozuk) ve her tohumda (7–11) doğruluk %100, tolerans yok. DNA yalnız eğitim bölmesinde geliştirilir, test bölmeleri kilitli DNA ile bir kez koşar. Yeniden adlandırma bölmesi H2'ye kalır. Müdahale puanı raporlanır, kapıya girmez; "sınanamadı" ayrı sayılır (K-021).
- **Onaylayan:** kullanıcı.

## K-024 (2026-10-23): H1 DNA'sını bağımsız danışman yazar
- **Karar:** Akrabalık DNA'sını gizli tanımları (`degerlendirme/veri/tanimlar_v1.json`) görmemiş bağımsız bir danışman yazar. Danışmana yalnız onaylı ilişki listesi (adlar, cinsiyet, ters ilişki bilgisi, okuma yönü, dünya varsayımları, DNA biçimi) tek dosya olarak verilir: `DANISMAN_ICIN_ILISKI_LISTESI.md`. Kuralları kullanıcı getirir ve onaylar. Kayıt: kaynak=LLM (bağımsız danışman), onaylayan=kullanıcı.
- **Onaylayan:** kullanıcı.

## K-025 (2026-10-23): DNA'da isteğe bağlı "farklı kişi" şartı
- **Karar:** DNA biçimine (sürüm 2) isteğe bağlı bir şart eklenir: bir hücrede belirtilen değişken çiftleri farklı varlıklara bağlanmalıdır. Şartı olmayan hücreler önceki gibi çalışır (değişkenler aynı varlığa bağlanabilir). Gerekçe: şart yokken çekirdek r1(1,2), r2(2,1) olgularından r3(1,1) yazdı (denendi).
- **Onaylayan:** kullanıcı.
