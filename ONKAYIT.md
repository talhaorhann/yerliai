# ÖN KAYIT

Hipotez, metrik, eşik ve bölmeler veriye bakmadan buraya yazılır ve hash'lenir (KODLAMA_PROMPTU §5 İstatistik).

## ÖK-001 (2026-10-23): Altın küme bağımsızlık kısıtı (K-013)

1. **Kaynak:** Altın küme 1. parçanın (50 soru) cevapları LLM ön cevabıdır, kullanıcı gözden geçirip kabul etmiştir. Bağımsız insan cevabı DEĞİLDİR. Kayıt dosyası: `degerlendirme/altin/kullanici_cevaplari_1.json` (sha256 `306ee0a0c54d3d6972695ae8a0c8c14e8dff12e2d6ef084884a9fd345a5c45ff`).
2. **Raporlama:** Altın kümeyle ölçülen her sonuç, 1. parça için "LLM ön cevaplı, kullanıcı onaylı" etiketiyle ayrı satırda raporlanır. 2. parçanın kaynağı ayrıca kaydedilir.
3. **Uyuşma kanıt değildir:**
   - 1. parça cevaplarının 50'si de üreteçle uyuştu.
   - Bu uyuşma gizli tanımların (V-019) doğruluğuna bağımsız kanıt sayılmaz. Tanımlar da bir LLM taslağıdır, ortak yanılgı riski vardır (sistem.md §17: "Çoklu LLM uyuşması doğruluk kanıtı sayılmaz").
4. **Dünya varsayımları:**
   - Cevaplarda iki varsayım kullanıldı: kardeşler aynı anne babanın çocuğudur; çocuğun iki ebeveyni birbirinin eşidir.
   - Bunlar üretecin dünya kurallarıyla (V-017) aynıdır. Etkilenen sorular: 3, 4, 5, 9, 10, 13, 17, 24, 27, 37, 39, 41, 46, 47.
   - Bu sorulardaki başarı, yalnız bu dünya varsayımları altında anlamlıdır.
5. **Kalibrasyon sınırı:**
   - sistem.md §15/§17 ve KODLAMA_PROMPTU §5'e göre LLM etiketi kalibrasyona (τ, T, θ seçimi) giremez.
   - Bu yüzden 1. parça, kullanıcı ayrıca karar vermedikçe yalnız değerlendirme ve otomatik durdurma ölçümünde, yukarıdaki etiketle kullanılır. Kalibrasyonda kullanılmaz.

## ÖK-002 (2026-10-23): H1 ön kaydı (K-023)

**Durum:** ONAYLI (kullanıcı, 2026-10-23), hash'li ve kilitli (`kilit/kilitler.json`). DNA kilitlenmeden önce test bölmeleri koşturulmaz, bölümlerine bakılmaz.

**Dayanak:** sistem.md §13 ("H1: çekirdek + elle doğru DNA ile %100 birim testi + ön kayıt"), §5, §9, §10; K-016, K-017, K-018, K-021; ÖK-001; KODLAMA_PROMPTU §4 (ölçütü gevşetme), §5 (İstatistik).

### 1. Hipotez

Elle yazılmış doğru DNA verilince LLM'siz çekirdek, sentetik soy ağacı sorularını kâhine bakmadan doğru cevaplar. Zincir bozuksa "bilmiyorum" der.

Bu deney kuralı **bulmayı** değil, verilen kuralla **doğru yürütmeyi** sınar. Öğrenme (evrim, gradyan, bellek) kapalıdır; o H2 ve sonrası.

### 2. Sabit ayarlar (deney boyunca değişmez)

- `config.json` olduğu gibi: havuz 64, tur sınırı 8, hücre başına 8 yazma, bütçe 1024, impasse çarpanı 0,5, d = 256, vektör tohumu 2026.
- θ = 0,5 ve hücre güvenilirliği 1 (K-016). τ ile durma kapalı (K-017).
- Hızlı yol (`HizliKodKitabi`, V-042). Referans yolla bit düzeyinde aynılığı testle gösterildi.
- `config.json` ve DNA dosyasının hash'leri ön kayda yazılır, her koşuda doğrulanır.

### 3. DNA

- Yazan ve onaylayan: gizli tanımları görmemiş bağımsız bir danışman yazar, kullanıcı onaylar (K-024). Danışmana yalnız onaylı ilişki listesi verilir (`DANISMAN_ICIN_ILISKI_LISTESI.md`).
- DNA geliştirmesi yalnız **eğitim bölmesinde** (k = 2–3) yapılır; DNA burada düzeltilebilir. Altın küme ve test bölmeleri DNA geliştirmede kullanılmaz.
- Eğitim bölmesinde %100'e ulaşılamazsa test bölmelerine geçilmez. Nedenler (aşağıdaki hata sınıfları) kullanıcıya raporlanır.
- Test bölmeleri bir kez, kilitli DNA ile koşar. Sonradan DNA değişirse yeni ön kayıt (ÖK-003) gerekir; eski sonuç silinmez.

### 4. Bölmeler ve veri

- **Kapıya girenler:** uzunluk (k = 4–10), yön ters, önsel-ters, zincir-bozuk.
- **Ayrı satır, kapıya girmez:** eğitim (k = 2–3; geliştirme bölmesi).
- **Kapsam dışı:** ilişki yeniden adlandırma. Gerekçe: elle yazılan DNA ilişki adlarını içerir, yeni adlarla eşleşemez. Bu bölme kuralın sıfırdan bulunmasını sınar, H2'ye kalır.
- **Tohum:** §10 "≥5 tohum". Üreteç tohumu 7 (A1) ve 4 ek tohum (8, 9, 10, 11). Bölme başına, tohum başına 400 bölüm (`ana_kume_sayisi`). Bölümler koşudan önce üretilir; dosya hash'leri ön kayda eklenir; kilitli kümelerle kesişim denetlenir.
- **Altın küme (100 soru):** ayrı satır. 1. parça "LLM ön cevaplı, kullanıcı onaylı" etiketiyle (ÖK-001); 2. parça kendi kaynağıyla.

### 5. Ölçütler

- **M1 Doğruluk:** bölme ve tohum başına doğru / toplam. Doğru = çekirdeğin cevabı üretecin cevabıyla aynı ilişki. Zincir-bozukta doğru = "bilmiyorum". Zincirli bölmede "bilmiyorum" (eşitlik dahil, K-018) yanlış sayılır.
- **M2:** zincirli bölmelerde "bilmiyorum" oranı; zincir-bozukta yanlış cevap oranı.
- **M3 Müdahale (K-021):** bölme başına toplam / puanlı / sınanamadı / cevapsız / ortalama puan, bootstrap %95 aralığıyla. "Sınanamadı" başarı sayılmaz, ayrı sayıyla gösterilir (ör. "400 soruda 18 sınanamadı").
- **M4:** duvar saati, tur sayısı, durma nedeni dağılımı, havuzdan atma ve `YEDEK_KULLANILDI` sayıları.
- Hiç hata yoksa bile "%100" tek başına sunulmaz: N ile birlikte, hata oranı için %95 üst sınır (Clopper–Pearson) verilir.

### 6. Kapı (geçti / geçmedi)

- **H1 GEÇTİ:** kapıya giren her bölmede ve her tohumda M1 = %100. Tolerans yoktur.
- Müdahale puanı için şartnamede H1 eşiği yok: yalnız raporlanır, kapıya girmez (r > 0,8 hedefi CLUTRR kalibrasyon kümesinindir, §9).
- Her hata, defterdeki gerekçesiyle tek tek listelenir ve sınıflanır:
  1. temsil sınırı: ara akrabalığın şemada adı yok, 8 tur yetmedi ya da havuz doldu;
  2. cevap olgulardan türetilemiyor (ör. cinsiyet ipucu yok);
  3. DNA hatası;
  4. çekirdek hatası.
- Sınıflama kâhin tarafında (`degerlendirme/`) yapılır. Çekirdek cevap kaydını görmez.
- Kapı geçilmezse ayarlar değiştirilmez, DNA test verisine bakılarak düzeltilmez. Rapor kullanıcıya gelir, karar kullanıcınındır.

### 7. Yalıtım ve bağımsızlık

- Çekirdek yalnız olguları ve sorguyu görür. Cevaplar yalnız `degerlendirme/` içinde okunur.
- Gizli tanımlar (`degerlendirme/veri/tanimlar_v1.json`) DNA yazımında kullanılmaz.
- Gizli tanımları bu kodlayıcı oturum yazdı (V-019). Bu yüzden DNA'yı bu oturum değil, bağımsız danışman yazar (K-024).

### 8. Bilinen riskler (koşudan önce yazıldı)

- **Aynı kişiye iki değişken bağlanabiliyor.** Denendi: r1(1,2) ve r2(2,1) olgularından r1(X,Y) ∧ r2(Y,Z) → r3(X,Z) hücresi r3(1,1) yazdı. Ters kurallar varken "babasının oğlu" kuralı kişiyi kendi kardeşi yapabilir. Önlem: DNA'ya isteğe bağlı "farklı kişi" şartı eklendi (K-025).
- Uzun zincirde (k = 10) ara kişinin akrabalığının şemada adı yoksa ya da 8 tur yetmezse cevap çıkmayabilir.
- Yön-ters sorularda cevap cinsiyete bağlıysa (oğul / kız) ve olgularda cinsiyet ipucu yoksa cevap türetilemeyebilir.

### 9. Koşu öncesi ek

`config.json`, DNA dosyası ve H1 bölüm dosyalarının hash'leri, DNA kilitlenince ve test bölmeleri koşmadan önce "ÖK-002 eki" olarak buraya eklenir. Ekleme kullanıcıya bildirilir. Bu bölümün dışındaki metin değişmez.
