# H1 ön kaydı: TASLAK (kullanıcı onayı bekliyor)

**Durum:** TASLAK. Onaylanınca `ONKAYIT.md`'ye ÖK-002 olarak taşınır, hash'lenir ve kilitlenir. Bu onaydan ve DNA kilitlenmeden önce test bölmeleri koşturulmaz, bölümlerine bakılmaz.

**Dayanak:** sistem.md §13 ("H1: çekirdek + elle doğru DNA ile %100 birim testi + ön kayıt"), §5, §9, §10; K-016, K-017, K-018, K-021; ÖK-001; KODLAMA_PROMPTU §4 (ölçütü gevşetme), §5 (İstatistik).

## 1. Hipotez

Elle yazılmış doğru DNA verilince LLM'siz çekirdek, sentetik soy ağacı sorularını kâhine bakmadan doğru cevaplar. Zincir bozuksa "bilmiyorum" der.

Bu deney kuralı **bulmayı** değil, verilen kuralla **doğru yürütmeyi** sınar. Öğrenme (evrim, gradyan, bellek) kapalıdır; o H2 ve sonrası.

## 2. Sabit ayarlar (deney boyunca değişmez)

- `config.json` olduğu gibi: havuz 64, tur sınırı 8, hücre başına 8 yazma, bütçe 1024, impasse çarpanı 0,5, d = 256, vektör tohumu 2026.
- θ = 0,5 ve hücre güvenilirliği 1 (K-016). τ ile durma kapalı (K-017).
- Hızlı yol (`HizliKodKitabi`, V-042). Referans yolla bit düzeyinde aynılığı testle gösterildi.
- `config.json` ve DNA dosyasının hash'leri ön kayda yazılır, her koşuda doğrulanır.

## 3. DNA

- Yazan ve onaylayan: onay listesinin 2. maddesine göre.
- DNA geliştirmesi yalnız **eğitim bölmesinde** (k = 2–3) yapılır; DNA burada düzeltilebilir. Altın küme ve test bölmeleri DNA geliştirmede kullanılmaz.
- Eğitim bölmesinde %100'e ulaşılamazsa test bölmelerine geçilmez. Nedenler (aşağıdaki hata sınıfları) kullanıcıya raporlanır.
- Test bölmeleri bir kez, kilitli DNA ile koşar. Sonradan DNA değişirse yeni ön kayıt (ÖK-003) gerekir; eski sonuç silinmez.

## 4. Bölmeler ve veri

- **Kapıya girenler:** uzunluk (k = 4–10), yön ters, önsel-ters, zincir-bozuk.
- **Ayrı satır, kapıya girmez:** eğitim (k = 2–3; geliştirme bölmesi).
- **Kapsam dışı:** ilişki yeniden adlandırma. Gerekçe: elle yazılan DNA ilişki adlarını içerir, yeni adlarla eşleşemez. Bu bölme kuralın sıfırdan bulunmasını sınar, H2'ye kalır.
- **Tohum:** §10 "≥5 tohum". Üreteç tohumu 7 (A1) ve 4 ek tohum (8, 9, 10, 11). Bölme başına, tohum başına 400 bölüm (`ana_kume_sayisi`). Bölümler koşudan önce üretilir; dosya hash'leri ön kayda eklenir; kilitli kümelerle kesişim denetlenir.
- **Altın küme (100 soru):** ayrı satır. 1. parça "LLM ön cevaplı, kullanıcı onaylı" etiketiyle (ÖK-001); 2. parça kendi kaynağıyla.

## 5. Ölçütler

- **M1 Doğruluk:** bölme ve tohum başına doğru / toplam. Doğru = çekirdeğin cevabı üretecin cevabıyla aynı ilişki. Zincir-bozukta doğru = "bilmiyorum". Zincirli bölmede "bilmiyorum" (eşitlik dahil, K-018) yanlış sayılır.
- **M2:** zincirli bölmelerde "bilmiyorum" oranı; zincir-bozukta yanlış cevap oranı.
- **M3 Müdahale (K-021):** bölme başına toplam / puanlı / sınanamadı / cevapsız / ortalama puan, bootstrap %95 aralığıyla. "Sınanamadı" başarı sayılmaz, ayrı sayıyla gösterilir (ör. "400 soruda 18 sınanamadı").
- **M4:** duvar saati, tur sayısı, durma nedeni dağılımı, havuzdan atma ve `YEDEK_KULLANILDI` sayıları.
- Hiç hata yoksa bile "%100" tek başına sunulmaz: N ile birlikte, hata oranı için %95 üst sınır (Clopper–Pearson) verilir.

## 6. Kapı (geçti / geçmedi)

- **H1 GEÇTİ:** kapıya giren her bölmede ve her tohumda M1 = %100. Tolerans yoktur.
- Müdahale puanı için şartnamede H1 eşiği yok: yalnız raporlanır, kapıya girmez (r > 0,8 hedefi CLUTRR kalibrasyon kümesinindir, §9).
- Her hata, defterdeki gerekçesiyle tek tek listelenir ve sınıflanır:
  1. temsil sınırı: ara akrabalığın şemada adı yok, 8 tur yetmedi ya da havuz doldu;
  2. cevap olgulardan türetilemiyor (ör. cinsiyet ipucu yok);
  3. DNA hatası;
  4. çekirdek hatası.
- Sınıflama kâhin tarafında (`degerlendirme/`) yapılır. Çekirdek cevap kaydını görmez.
- Kapı geçilmezse ayarlar değiştirilmez, DNA test verisine bakılarak düzeltilmez. Rapor kullanıcıya gelir, karar kullanıcınındır.

## 7. Yalıtım ve bağımsızlık

- Çekirdek yalnız olguları ve sorguyu görür. Cevaplar yalnız `degerlendirme/` içinde okunur.
- Gizli tanımlar (`degerlendirme/veri/tanimlar_v1.json`) DNA yazımında kullanılmaz.
- Gizli tanımları bu kodlayıcı oturum yazdı (V-019). Bu yüzden bu oturumun yazacağı DNA tanımlardan bağımsız sayılmaz (onay listesi madde 2).

## 8. Bilinen riskler (koşudan önce yazıldı)

- **Aynı kişiye iki değişken bağlanabiliyor.** Denendi: r1(1,2) ve r2(2,1) olgularından r1(X,Y) ∧ r2(Y,Z) → r3(X,Z) hücresi r3(1,1) yazdı. Ters kurallar varken "babasının oğlu" kuralı kişiyi kendi kardeşi yapabilir (onay listesi madde 3).
- Uzun zincirde (k = 10) ara kişinin akrabalığının şemada adı yoksa ya da 8 tur yetmezse cevap çıkmayabilir.
- Yön-ters sorularda cevap cinsiyete bağlıysa (oğul / kız) ve olgularda cinsiyet ipucu yoksa cevap türetilemeyebilir.
