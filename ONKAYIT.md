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

## ÖK-002a (2026-10-24): Havuz kapasitesi 64 → 128 (K-026)

**Durum:** ONAYLI (kullanıcı, 2026-10-24). ÖK-002'nin yalnız §2'deki havuz değerini değiştirir; ÖK-002'nin metni olduğu gibi kalır.

1. **Değişiklik:** havuz kapasitesi 64 yerine 128 (`config.json` `havuz_kapasitesi`, K-026). Kapı (§6: her kapı bölmesinde ve her tohumda %100, tolerans yok), bölmeler, tohumlar, ölçütler ve DNA kuralları değişmez.
2. **Neden:** Bağımsız danışmanın kendi simülasyonunda (projenin bölüm dosyaları ve gizli tanımları kullanılmadan, kullanıcının iletmesiyle) k=10 zincirlerde havuz 64 yetmedi: doğru %56–71, kaçan %18–36. 128'de doğru %89–92, kaçan ~%0. Kullanıcı 128'e "evet" dedi.
3. **Zaman:** Değişiklik, test bölmeleri gerçek DNA ile koşturulmadan ve DNA eğitim bölmesinde denenmeden önce yapıldı.
4. **Şartnameden sapma:** sistem.md §2 "Kapasite 64" der. Bu sapma kullanıcı kararıdır (K-026); sistem.md değiştirilmedi.
5. **Açıklama (kodlayıcının ihlali):** 2026-10-23'te kodlayıcı, süre kestirmek için uzunluk bölmesinin (tohum 7) ilk 20 bölümünü ve eğitim bölmesinin ilk 20 bölümünü anlamsız, rastgele kurulmuş bir deneme DNA'sıyla koşturdu. Yalnız süre, ortalama tur ve atma sayısı yazdırıldı (atma 0). Doğruluğa ve cevaplara bakılmadı; çıktı silindi. Bu, ÖK-002 durum satırındaki "DNA kilitlenmeden önce test bölmeleri koşturulmaz" kuralına aykırıdır ve burada kayda geçirildi. Sonuç kararlarını etkilemez: havuz kararı danışmanın simülasyonuna dayanır; deneme DNA'sı başka hiçbir yerde kullanılmadı.
6. **Beklenti notu:** Danışmanın simülasyonu 128'de bile k=10'da %89–92 doğru öngörüyor. §6 kapısı %100 ister ve değişmedi.

## ÖK-002b (2026-10-24): Kopya kuralı C (K-028)

**Durum:** ONAYLI (kullanıcı, 2026-10-24). ÖK-002 ve ÖK-002a'nın metni değişmez; çekirdek davranışına aşağıdaki kural eklenir.

1. **Kural ("yeni dayanak"):** Bir adayın dayanağı, ebeveyn kayıtlarının kök kümelerinin (dayandığı olguların) birleşimidir. Aynı üçlünün havuzdaki canlı ve izli (defterde YAZMA izi olan ya da o turda döngünün yazdığı) bir çıkarımının kök kümesi adayın dayanağının alt kümesiyse aday yeni dayanak getirmez ve yazılmaz. Atılan adaylar tur başına sayılarak `ESLESME_ATILDI` (neden: dayanak_yok) olarak deftere yazılır. Epitoplar ve izsiz kayıtlar ispat sayılmaz.
2. **Neden:** Gerçek DNA ile simetrik ve ters kurallar aynı ilişkiyi yeni kökenlerle sonsuza dek yeniden yazdırdı. Döngü 8. tura dayandı, kopyalar doğru cevabı havuzdan attı. Eğitim bölmesinde (tohum 7, ilk 60 bölüm) ölçüldü: bugünkü hâl 33/60, A ("yeni" = yeni üçlü) 55/60, B (aynı üçlü varsa hiç yazma) 60/60, C 60/60. B bağımsız ikinci ispatı da sildiği için müdahale testinin (a) ve (b) kısımlarını anlamsızlaştırıyor; C kök-ayrık ispatları koruyor (V-046).
3. **Zaman ve veri:** Karar test bölmeleri açılmadan verildi. Ölçüm yalnız geliştirme bölmesinde (eğitim, ÖK-002 §3), depodan ayrı kopyalarda yapıldı.
4. **Etki:** V-042 senaryolarından yalnız C'nin aday attığı biri değişti; diğer üçü önceki altın değerlerle aynı. A3/A4 testlerinden ikisinde "aynı olgulardan 10 kopya hücre 10 kayıt yazar" beklentisi "1 kayıt, 9 dayanak_yok" oldu; güven ve destek beklentileri aynı kaldı.
5. Kapı (§6), bölmeler, tohumlar, ölçütler ve DNA değişmez.

## ÖK-002 eki (2026-10-24): DNA kilidi, koşu öncesi özetler (§9)

**Durum:** DNA eğitim bölmesinde 5 tohumun hepsinde 400/400, toplam 2000/2000 doğru (ÖK-002 §3, K-027). DNA ve aşağıdaki dosyalar bu özetlerle kilitlendi. Kapı bölmeleri bu ekten sonra, kilitli DNA ile bir kez koşar. Kod: commit `91591f3` (kopya kuralı C dahil, ÖK-002b).

- `config.json`: `556babab6116dd286492fe955229c40887e679ba734d06c30dfbd6fa2eac22eb`
- DNA `veri/dna/akrabalik_dna_v2_final.json`: `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e`
- `tohum_7/ozet.json`: `d95f6afebd56c4008fe91f11b813c0e5c8c817a34b180f79d9c5e4907547f127`
- `tohum_8/ozet.json`: `6f481451bb2c661e130987e3b2af48fa9acac223d927e516afff5de023bc1f31`
- `tohum_9/ozet.json`: `68647318999d1ef59430ec84928e49bcc76ac38da1cbda7c02e80a4d243f0b29`
- `tohum_10/ozet.json`: `7a331cee31840531547d7b8cf988921c364e66318bb87fcd8baceabdc9981c19`
- `tohum_11/ozet.json`: `b2f57c2be8821982a892ff1abb311bd3c536e2a9eda3a70443c07100cb93c863`

## ÖK-003 (2026-10-24): H1 yeniden deneme ön kaydı (K-029)

**Durum:** ONAYLI (kullanıcı, 2026-10-24). Bu metin yeni bölümler üretilmeden ve yeni koşudan önce yazıldı. Seçilen sınırlar, son DNA ve yeni bölümlerin özetleri koşudan önce "ÖK-003 eki"ne yazılır; ek dışındaki metin değişmez.

### 1. İlk koşunun sonucu (silinmez)

- **Tarih:** 2026-10-24. **Ön kayıt:** ÖK-002 (+ ÖK-002a havuz 128, ÖK-002b kopya kuralı C). **Kod:** `91591f3`. **DNA:** `624b073c…` (170 kural).
- **Sonuç: KAPI GEÇMEDİ.** Önsel-ters 2000/2000, zincir-bozuk 2000/2000, uzunluk 1980/2000, yön ters 573/2000. Eğitim (geliştirme) 2000/2000. Bütün hatalar "bilmiyorum"; yanlış ilişki 0.
- **Nedenler (ölçüldü):**
  - Yön ters: 1427 hatanın 1426'sında cevabı belirleyen kişinin cinsiyetine olgularda (doğrudan ya da eş üzerinden) kanıt yok. Büyük olasılıkla üreteç cevabı olgulardan çıkarılamayan sorular üretti; V-017 bu şartı koymuyordu.
  - Uzunluk: 20 hatanın 3'ü tur sınırı (8), 3'ü havuz (128) yüzünden; 14'ü sınırdan bağımsız (büyük olasılıkla DNA eksiği).
- **Kayıtlar:** `raporlar/H1_SONUC.md`, `raporlar/H1_kapi_RAPOR.md`, `raporlar/H1_kapi_ozet.json`, `raporlar/H1_altin_RAPOR.md`, `raporlar/H1_ilk_kosu_uzunluk_14_hata.md`. Bunlar silinmez ve değiştirilmez.

### 2. Hipotez

ÖK-002 §1 ile aynı: elle yazılmış doğru DNA verilince LLM'siz çekirdek soruları kâhine bakmadan doğru cevaplar, zincir bozuksa "bilmiyorum" der.

### 3. Değişiklikler

1. **Üreteç: "cevap olgulardan çıkarılabilir" şartı, çekirdekten bağımsız.** Her aday için ağaç yapısı (ebeveyn ve eş bağları) sabit tutulur. Olguların izin verdiği bütün cinsiyet atamaları denenir: her olgu doğru kalmalı ve eşler karşı cinsten olmalı. Bu atamaların hepsinde sorgu çiftinin ilişkisi gerçek cevapla aynı değilse aday atılır. Çekirdek bu seçimde hiç çalıştırılmaz; soru, çekirdeğin cevap verip vermediğine bakılarak seçilmez. Zincir-bozuk bölümler (beklenen cevap "bilmiyorum") bu denetime girmez. Atılan aday sayısı bölme başına raporlanır. Varsayım: farklı kişi numaraları farklı kişilerdir; yapı sabittir, yalnız cinsiyet değişir.
2. **Tohumlar:** kapı koşusu yeni tohumlarla, 12, 13, 14, 15, 16. İlk koşunun tohumları (7–11) geliştirme verisi olur.
3. **Geliştirme verisi:** ilk koşunun bütün bölümleri (eğitim ve dört test bölmesi, tohum 7–11). DNA'yı danışman bunlara bakarak düzeltebilir; kodlayıcı düzeltmez (K-024). Son DNA kullanıcı onayından sonra eski eğitim bölmesinde %100 olmalı (ÖK-002 §3 gibi). Eski test bölmelerinde %100 şartı yok; onlar DNA düzeltmesi ve sınır seçimi içindir. Yeni tohumların eğitim bölmesi ayrı satırda raporlanır, kapıya girmez, DNA geliştirmede kullanılmaz.
4. **Tur ve havuz sınırları:** son DNA ile, geliştirme verisinin dört eski test bölmesinde (8000 bölüm), önceden belirlenen şu kuralla seçilir:
   - Adaylar: tur {8, 12, 16, 24, 32}, havuz {128, 256, 512, 1024}.
   - Önce havuz 1024'te, doğru sayısı tur 32'dekine eşit olan en küçük tur seçilir. Sonra o turla, doğru sayısı havuz 1024'tekine eşit olan en küçük havuz seçilir.
   - Seçilen değerler ve ölçüm tablosu ÖK-003 ekine yazılır ve yeni koşudan önce kilitlenir. sistem.md §5 (8 tur) ve §2 (64) değerlerinden sapma kullanıcı kararıdır (K-029).
5. Kopya kuralı C (ÖK-002b), θ = 0,5, güvenilirlik 1 ve diğer bütün ayarlar aynen kalır.

### 4. Bölmeler, ölçütler, kapı

ÖK-002 §4–§6 ile aynı. Kapı: kapıya giren her bölmede (uzunluk, yön ters, önsel-ters, zincir-bozuk) ve her yeni tohumda %100, tolerans yok. Yeniden adlandırma H2'ye kalır. Müdahale raporlanır, kapıya girmez; "sınanamadı" ayrı sayılır. Altın küme ayrı satır.

### 5. Sıra

1. Üreteç denetimi testle eklenir.
2. Yeni bölümler (tohum 12–16) üretilir; manifest özetleri ÖK-003 ekine yazılır.
3. Danışman DNA'yı (gerekirse) düzeltir; kullanıcı onaylar; eski eğitim bölmesinde %100.
4. Sınırlar §3.4'teki kuralla seçilir.
5. ÖK-003 eki: config, son DNA, yeni manifestler, seçilen sınırlar ve ölçüm tablosu.
6. Kapı bölmeleri yeni tohumlarla bir kez koşar; sonra altın küme.

### 6. Kapı geçmezse

Ayarlar ve DNA bu sonuca bakılarak değiştirilmez. Rapor kullanıcıya gider, karar kullanıcınındır.

