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


## ÖK-003 eki

Bu ek ÖK-003 §5'teki sırayla doldurulur. Kapı koşusu için gereken özetlerin hepsi bu başlığın altında yazılı olmalı: config, son DNA, yeni manifestler ve tohum kaydı. Biri eksikse kapı koşmaz (`degerlendirme/h1.py` `on_kayit_denetle`).

### 1. Tohum değişimi (K-030)

- **2026-10-24:** Tohum 15'in üretimi önsel-ters bölmesinde kısa yol kapısında (K-008) durdu: "kelime çantası dedektörü 0,250 > şans 0,180 + 0,05".
  - Çıkarılabilirlik denetimi (K-029) bu bölmede aday atmıyor; denetim kapalıyken de aynı sonuç çıkıyor (V-050).
  - Çekirdek tohum 15'te hiç koşmadı.
- **Kural (K-030, kullanıcı onayı 2026-10-24):** yerine kullanılmamış ilk tohum geçer; eşik gevşetilmez; en çok 3 değişim.
- **Uygulama:** Tohum 15 yerine 17 geçti; kullanılan değişim hakkı 1/3. Kullanılan tohumlar: 12, 13, 14, 17, 16.

### 2. Yeni bölümler (§5.2)

- **Üretim:** `.venv/bin/python -m degerlendirme.h1 uret uretilen/h1_v2`, kod commit `de8ca8d`.
  - Üreteç ve çıkarılabilirlik denetimi `00022e0`'dakiyle aynı.
  - Tohum 12–14'ün manifestleri, tohum değişimi kodundan önceki üretimle bayt bayt aynı çıktı.
- **Çıkarılamadığı için atılan aday:** yalnız yön ters bölmesinde; öteki bölmelerde 0. Tohum 12: 2388, 13: 2283, 14: 2180, 17: 2243, 16: 2243.
- **Özetler (sha256):**
  - `tohumlar.json`: `d6c0cd971c11b9c18c79a5bcf0131205b60a6f230a562b92821b97ba27d2d4c5`
  - `tohum_12/ozet.json`: `96937c495cdb8a4215b98a84a399c2b9ff8c5d8ddec47c932b760684509d5855`
  - `tohum_13/ozet.json`: `d01792de370d294eadf960c356ac5ef31c58c693b349b17d67d6a4922c9331c0`
  - `tohum_14/ozet.json`: `eb6a1b41aadba4d16f2ff5dfcb9f2a32ec6302187f89162966d35a34b6e41669`
  - `tohum_16/ozet.json`: `d57357e830f244d3eacf8740fedad8d8295cfdde0eead1a247ea7206737ee19b`
  - `tohum_17/ozet.json`: `94d2026230dc9dfc6279b5842eff30dcb1ffdc0af1578d35e1a6cc5209474616`

### 3. İlk koşunun 14 uzunluk hatası: nedenin düzeltilmesi (2026-10-24)

- §1'de bu 14 hata için "büyük olasılıkla DNA eksiği" yazıyor. Bu yanlıştı.
  - Danışman 14'ünü de kendi motoruyla sınırsız kapanışta çözdü.
  - Kodlayıcının izlemesine göre 14'ünün de nedeni, hücre başına tur başına yazma sınırı (8). Sınır C kuralından önce kesiyor (V-051, `raporlar/H1_hucre_siniri_izleme.md`).
  - İlk koşunun teşhis aracı bu sınırı gevşetmediği için onlara "sınırdan bağımsız" demişti (V-047).
- §1'in metni değiştirilmedi.
- Çekirdekte bir değişiklik yapılacaksa kullanıcının kararını bekler; karar bu eke tarihiyle yazılır.

### 4. Çekirdek değişikliği: kopya kuralı C hücre sınırından önce (K-031, 2026-10-24)

- **Değişiklik:** Bir turda bir hücrenin eşleşmeleri önce C ile süzülür: yeni dayanak getirmeyen aday, hücre sınırından yer almaz. Sonra hücre başına en iyi 8 aday, sonra tur bütçesi uygulanır. Sınır böylece sistem.md §3'teki gibi yazmaları sayar.
  - Hücre sınırı (8), bütçe, θ, güvenilirlik ve DNA değişmez.
  - §3.5'teki "diğer bütün ayarlar aynen kalır" cümlesinin tek istisnası budur.
- **Neden:** §1'deki 14 uzunluk hatasının 14'ünde, sınırın içindeki yerleri C'nin atacağı kopyalar dolduruyordu (bu ekin 3. bölümü).
- **Onay:** kullanıcı, 2026-10-24 (K-031).
- **Kod:** commit `ce2607b`. Test önce yazıldı (`testler/test_a5_sinir_c.py`, kırmızı → yeşil).
  - Hızlı yol ile referans yol yine bit-eşit.
  - Yalnız dayanaksız adayı olan senaryonun değiştiği testle gösterildi.
  - Mutasyon 4/4 yakalandı.
- **Eski eğitim (§3.3, olağan sınırlarla, tur 8, havuz 128):** 2000/2000 doğru (her tohumda 400/400), yanlış 0, bilmiyorum 0; müdahale 2000 puanlı, 0 sınanamadı (`raporlar/H1_v2_eski_egitim_RAPOR.md`).

### 5. Son DNA (§5.3)

- Danışman 14 hatayı kendi motoruyla sınırsız kapanışta çözdü ve DNA'da eksik kural olmadığını bildirdi. DNA değişmedi; ilk koşudaki dosyanın aynısı.
- `dna` (`veri/dna/akrabalik_dna_v2_final.json`, 170 kural): `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e`

### 6. Tur ve havuz sınırları (§3.4)

- **Ölçüm (2026-10-24):** son DNA ve K-031'li çekirdekle, geliştirme verisinin dört eski test bölmesinde (uzunluk, yön ters, önsel-ters, zincir-bozuk; tohum 7–11; 8000 bölüm).
  - Yalnız çekirdek + plazma koşuldu; müdahale testi doğruluğu etkilemez.
  - Komut: `.venv/bin/python -m degerlendirme.h1_sinir uretilen/h1 veri/dna/akrabalik_dna_v2_final.json uretilen/h1_sinir_1`.
  - Kural §3.4'teki gibi harfiyen uygulandı.
- **Seçilen:** tur 8, havuz 256. Config: `h1_tur_siniri` = 8, `h1_havuz_kapasitesi` = 256.
  - Bu değerler yalnız kapı, altın küme ve yeni tohumların eğitim satırında kullanılır (`degerlendirme/h1.py` `kosu_parametreleri`).
  - Genel ayarlar (`tur_siniri` 8, `havuz_kapasitesi` 128) değişmedi.
  - Tur sistem.md §5'teki 8 ile aynı. Havuz sistem.md §2'deki 64'ten sapar; bu K-029'a dayanır (genel ayar K-026 ile 128).
- **Ölçüm tablosu (doğru sayısı / 8000):**

  | Tur | Havuz | Doğru |
  |---|---|---|
  | 8 | 128 | 6567 |
  | 8 | 256 | 6573 |
  | 8 | 1024 | 6573 |
  | 32 | 1024 | 6573 |

  - Kural: önce havuz 1024'te, tur 32'deki (6573) ile eşit olan en küçük tur: 8. Sonra tur 8'de, havuz 1024'teki (6573) ile eşit olan en küçük havuz: 256. Tablodakiler dışındaki adaylar kural gereği ölçülmedi.
  - Tur 8, havuz 256'da bölme dökümü: uzunluk 2000/2000, önsel-ters 2000/2000, zincir-bozuk 2000/2000, yön ters 573/2000. Yön ters açığı, §1'deki ölçüme göre eski verideki çıkarılamayan sorulardan gelir; yeni tohumlarda üreteç bu soruları ayıklar (§3.1).

### 7. Kapı koşusu öncesi özetler (§5.5)

- `config.json`: `ce14605aca9e3498bb6d9df7afee1c97748c5eb70e9c074ed9211de4a1cba7e1`
- `dna`: `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e`
- Yeni manifestler ve `tohumlar.json`: 2. bölümdeki özetler.
- Kod: commit `157c1fb`.
- Kapı bölmeleri bu ekten sonra, tohum 12, 13, 14, 17, 16 ile bir kez koşar; sonra altın küme. Kapı geçmezse ayarlar ve DNA bu sonuca bakılarak değiştirilmez (§6).

### 8. Sonuç ve kullanıcı kararı (2026-10-24, kapı koşusundan sonra yazıldı)

- **Kayıt (kullanıcının metni):** "H1 iki kez kapıyı geçmedi. İkinci koşuda uzunluk, önsel-ters, zincir-bozuk bölmeleri 5 tohumda 2000/2000, yön ters 1881/2000 (ilk koşuda 573/2000). Yanlış ilişki iki koşuda da 0. 119 hatanın hepsi 'bilmiyorum'; 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanmasından. H1 resmen KANITLANMAMIŞTIR; çekirdek lehine güçlü kanıt vardır."
- **Karar (K-032):** Sonuç olduğu gibi kabul edildi; H1 "geçti" diye işaretlenmez. Kullanıcı kararıyla A6'ya geçildi.
- ÖK-004 iptal edilmedi, ertelendi. Yeniden deneme şu sırayla olur: önce V-053 kapanır (çıkarılabilirlik tanımı kullanıcı onayına gelir), sonra H1 taze tohumlarla tek sefer koşar. Bu yeniden denemede tohum değişim hakkı 2'dir (3'ten 1'i ÖK-003'te kullanıldı).
- V-053 kapanmadan ve H1 taze tohumlarla yeniden koşulmadan H2 başlatılamaz; bu kural kodda bir kapıyla zorunludur.
- Ayrıntı: `raporlar/H1_v2_SONUC.md`.

### 9. Güncellenmiş kayıt ve kararlar (2026-10-24, kullanıcı; 8. bölümün yerine geçmez, onu tamamlar)

- **Kayıt (kullanıcının metni):** "H1 iki kez kapıyı geçmedi. İkinci koşuda uzunluk, önsel-ters ve zincir-bozuk bölmeleri 5 tohumda 2000/2000, yön ters 1881/2000 (ilk koşuda 573/2000). Yanlış ilişki iki koşuda da 0. 119 yön ters hatasının hepsi 'bilmiyorum'; 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanmasından, 6'sı DNA'da silinmiş 6 kuraldan. H1 resmen KANITLANMAMIŞTIR; çekirdek lehine güçlü kanıt vardır."
- 6 hatanın nedeni danışmanın incelemesiyle düzeltildi: DNA'dan silinmiş 6 kural (`kiz_ogul_baba` dahil). Danışman bunları yeni sürümde geri koydu (gelen dosya v8, 244 kural; 170 eski kural aynen içinde; `raporlar/DNA_v8_karsilastirma.md`). Bu dosya henüz kilitli değil. 8. bölümdeki "DNA kapsam açığı" yorumu bununla kesinleşti.
- H1 "geçti" diye işaretlenmez. Tohum değişim hakkı: 3'ten 1'i kullanıldı, 2 kaldı.
- **Sıra (K-033):** A6 tamamlanır. DNA "son sürüm" gelince V-053 tanımı üretece bağlanır, ÖK-004 yazılır ve kilitlenir. H1 taze tohumlarla tek sefer koşar. Bu, bu tür kapı koşusunun son denemesidir: geçmezse durulur, kapsamlı karar kullanıcıya gelir. Eşik gevşetilmez.


## ÖK-004 (2026-10-25): H1 son deneme ön kaydı (K-033, K-034, K-038)

**Durum:** Kullanıcı kararlarıyla (K-033, K-034, K-037, K-038) yazıldı ve kilitlendi. Yeni bölümler üretilmeden ve koşudan önce yazıldı. Koşu öncesi özetler "ÖK-004 eki"ne yazılır; ek dışındaki metin değişmez. **Bu, bu tür kapı koşusunun son denemesidir (K-033).**

### 1. Önceki iki koşu (silinmez)

- **Birinci koşu (ÖK-002, 2026-10-24):** kod `91591f3`, DNA `624b073c…` (170 kural), tohum 7–11.
  - **KAPI GEÇMEDİ:** önsel-ters 2000/2000, zincir-bozuk 2000/2000, uzunluk 1980/2000, yön ters 573/2000. Yanlış ilişki 0; bütün hatalar "bilmiyorum".
  - Nedenler: yön ters hatalarının neredeyse hepsi cevabı olgulardan çıkarılamayan sorular (üreteç bu şartı koymuyordu). Uzunluktaki 20 hatanın 14'ü hücre sınırının kopya kuralı C'den önce kesmesi (K-031 ile düzeltildi), 6'sı tur ve havuz sınırı (ÖK-003 eki §6 ile seçildi).
  - Kayıtlar: ÖK-003 §1, ÖK-003 eki §3, `raporlar/H1_SONUC.md`, `raporlar/H1_kapi_ozet.json` (`f65b2611…`).
- **İkinci koşu (ÖK-003, 2026-10-24):** kod `157c1fb`, aynı DNA, tohum 12, 13, 14, 17, 16 (15 yerine 17, K-030).
  - **KAPI GEÇMEDİ:** uzunluk, önsel-ters ve zincir-bozuk 2000/2000; yön ters 1881/2000. Yanlış ilişki 0; 119 hatanın hepsi "bilmiyorum".
  - Nedenler: 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanması (V-053); 6'sı DNA'dan silinmiş 6 kural (danışman).
  - Kayıtlar: ÖK-003 eki §8–§9, `raporlar/H1_v2_SONUC.md`, `raporlar/H1_v2_kapi_ozet.json` (`6e723c63…`), `raporlar/V053_inceleme.md`.
- **Kullanıcının kaydı (K-033):** "H1 iki kez kapıyı geçmedi. İkinci koşuda uzunluk, önsel-ters ve zincir-bozuk bölmeleri 5 tohumda 2000/2000, yön ters 1881/2000 (ilk koşuda 573/2000). Yanlış ilişki iki koşuda da 0. 119 yön ters hatasının hepsi 'bilmiyorum'; 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanmasından, 6'sı DNA'da silinmiş 6 kuraldan. H1 resmen KANITLANMAMIŞTIR; çekirdek lehine güçlü kanıt vardır."

### 2. Hipotez

ÖK-002 §1 ile aynı: elle yazılmış doğru DNA verilince LLM'siz çekirdek soruları kâhine bakmadan doğru cevaplar, zincir bozuksa "bilmiyorum" der.

### 3. Değişiklikler (yalnız bunlar)

1. **Üretecin çıkarılabilirlik tanımı V-053 (K-034).** Dünya verilmez. Olgular ve üç dünya varsayımı kullanılır:
   - her kişinin ya hiç ebeveyni yoktur ya da birbiriyle evli iki ebeveyni vardır;
   - en çok bir evlilik;
   - evli çiftler karşı cinsten.
   Bunların zorunlu kıldığı yapıda, cinsiyetlerin olgulara uyan bütün atamalarında sorgu çiftinin ilişkisi gerçek cevapla aynı değilse aday atılır. Çekirdek bu seçimde hiç çalışmaz. Zincir-bozuk bölümler denetime girmez. Atılan aday sayısı bölme başına raporlanır.
   - Kod: `degerlendirme/dunya.py` `olgudan_cikarilabilir_mi`, `degerlendirme/uretec.py` `cikarilabilirlik_tanimi`. Config: `h1_cikarilabilirlik_tanimi` = "olgu". Commit `1d0b7d3`.
2. **DNA v8, son sürüm (K-038):** `veri/dna/akrabalik_dna_v8.json`, 244 kural.
   - 170 eski kural aynen içinde; 74 yeni kural. Yenilerin 6'sı ikinci koşudaki 6 hatanın nedeni olan silinmiş kurallar (`raporlar/DNA_v8_karsilastirma.md`).
   - Danışman ölçümü: 16.000 rastgele kümede yanlış türetme 0; çıkarılabilir sorulardan kaçan %0,02.
   - DNA bu ön kayıttan sonra değişmez; sorun çıkarsa danışmana bildirilir.
3. **Tohumlar:** 18, 19, 20, 21, 22. Tohum 7–17 kullanıldı; H2 kapısı onları taze saymaz.
   - Kısa yol kapısında (K-008) duran tohumun yerine kullanılmamış ilk tohum geçer (K-030). Eşik gevşetilmez. En çok 2 değişim (config `h1_tohum_degisim_siniri` = 2). Her değişim bu ekin tarihli satırına yazılır.
4. **Sınırlar ve çekirdek:** ÖK-003 eki §6 aynen (tur 8, havuz 256). Eşleşme bütçesi 1024, hücre başına tur başına 8 yazma, kopya kuralı C hücre sınırından önce (K-031), θ = 0,5, güvenilirlik 1 aynen.
5. Başka değişiklik yok. A6 kodu (bellek geçidi K-035/K-037, iç dil, bellek deposu) H1 koşusuna girmez.

### 4. Bölmeler, ölçütler, kapı

- ÖK-003 §4 ile aynı. Kapı bölmeleri: uzunluk, yön ters, önsel-ters, zincir-bozuk. Her bölmede ve her tohumda %100; tolerans yok.
- Müdahale raporlanır, kapıya girmez; "sınanamadı" ayrı sayılır (K-021).
- Yeni tohumların eğitim bölmesi ayrı satırda raporlanır, kapıya girmez.
- Altın küme ayrı satır; iki parça kendi kaynak etiketleriyle.
- Ek rapor (kapıya girmez): havuz ve eşleşme bütçesi baskısı. Tur sınırına ulaşan bölüm, havuzdan atılan ve havuz dolu diye yazılamayan kayıt, bütçe ve hücre sınırıyla atılan eşleşme sayıları.

### 5. Sıra

1. V-053 üretece bağlanır (test önce). Yapıldı: commit `1d0b7d3`.
2. Bu ön kayıt yazılır ve kilitlenir. Ekine config ve DNA özetleri yazılır.
3. Altın küme 2. parça kullanıcı cevapları gelir. **Gelmeden kapı koşmaz.**
4. Yeni bölümler üretilir (tohum 18–22). Manifest ve tohum kaydı özetleri ekin 2. bölümüne yazılır.
5. Kapı bölmeleri bir kez koşar. Sonra yeni tohumların eğitim satırı ve altın küme (iki parça).
6. Sonuç "## ÖK-004 sonucu" başlığıyla yazılır. Kapı özeti `raporlar/H1_v3_kapi_ozet.json`'un sha256'sı da içinde olur (H2 kapısı bunu arar).

### 6. Kapı geçmezse

Bu son denemedir. Durulur. Ayarlar, DNA ve eşikler bu sonuca bakılarak değiştirilmez. Kapsamlı karar kullanıcıya gelir (K-033).


## ÖK-004 eki

Bu ek ÖK-004 §5'teki sırayla doldurulur. Kapı koşusu için gereken özetlerin hepsi bu başlığın altında yazılı olmalı: config, DNA, yeni manifestler ve tohum kaydı. Biri eksikse kapı koşmaz (`degerlendirme/h1.py` `on_kayit_denetle`).

### 1. Ön kayıt anındaki özetler (2026-10-25)

- `config.json`: `9c5694fa3b0d97a6fb6c26609709b661cbd31879875d3f87476eeb89c36b9424`
- `dna` (`veri/dna/akrabalik_dna_v8.json`): `4a4af6b83c58e33d9971f9d84ed6c440fbb2341d14ec70dc4710128d74bfaa75`
- Kod: commit `1d0b7d3`.
- Yeni manifestler ve `tohumlar.json`: üretimden sonra 2. bölüme yazılır.

### 2. Tohum değişimi onay şartı ve güncel config özeti (K-039, 2026-10-25)

- **Kural (danışman, kullanıcı iletti):** tohum değişimi ancak danışman ve kullanıcı onayıyla yapılır. Kısa yol kapısında duran tohumda üretim durur ve nedeni bildirilir; onaylanan tohum `h1_onayli_tohum_degisimleri` listesine yazılır. ÖK-004 §3.3'teki K-030 kuralı ve en çok 2 değişim sınırı aynen kalır; bu yalnız onay şartı ekler (sıkılaştırma).
- Kod: `degerlendirme/h1.py` `tohumlari_uret`, `kapi_tohumlari` (test önce).
- Config bu yüzden değişti; ön kayıt anındaki 1. bölüm özetinin yerine bundan sonra bu geçerlidir:
  - `config.json`: `144a532865430d53b8b7e1d959609cc819cf565e294d8ebcf56c716d76a5ed9e`
- Yeni manifest ve tohum kaydı özetleri, üretimden sonra bu ekin 3. bölümüne yazılır (1. bölümdeki "2. bölüm" atfının yerine).

### 3. Üretim: tohum 21 kısa yol kapısında durdu, onay bekleniyor (2026-10-25)

- **Komut:** `.venv/bin/python -m degerlendirme.h1 uret uretilen/h1_v3`, kod commit `3b5a6bc`.
- Tohum 18, 19, 20 üretildi. Çıkarılamadığı için atılan aday yalnız yön ters bölmesinde: 18: 2311, 19: 2340, 20: 2590.
- **Tohum 21 durdu:** önsel-ters bölmesinde kelime çantası dedektörü 0,445 > şans 0,370 + 0,05 (K-008). Öteki beş bölmesi kapıdan geçiyor. ÖK-003'teki tohum 15 duruşuyla aynı desen (V-050).
- Çekirdek hiçbir tohumda koşmadı. Eşik gevşetilmedi.
- Ön kayıtlı tohum 22, yalnız üreteçle sınandı: altı bölmenin hepsi kapıdan geçiyor (yön ters atılan aday 2539).
- **K-039:** yerine tohum geçmesi danışman ve kullanıcı onayı ister. Onaylanırsa yerine kullanılmamış ilk tohum, 23 geçer (değişim hakkı 2'den 1'i). Onay gelmeden üretim tamamlanmaz, kapı koşmaz. Yeni manifest özetleri onaydan sonra bu ekin 4. bölümüne yazılır.

### 4. Tohum 21 → 23 değişimi onaylandı (2026-10-25, kullanıcı ve danışman)

- **Kapı:** kelime çantası kısa yol kapısı (K-008, `degerlendirme/kisa_yol.py` `kapi_denetle`). Eşik: dedektör doğruluğu ≤ şans + 0,05 (V-018). Bölme: **önsel-ters**.
  - Tohum 21: ölçülen 0,445; şans 0,370; eşik 0,420; aşım 0,025.
  - Önceki durum, tohum 15 (ÖK-003 eki §1): yine önsel-ters bölmesi; ölçülen 0,250; şans 0,180; eşik 0,230; aşım 0,020.
  - İkisinde de öteki beş bölme geçti. İkisinde de çıkarılabilirlik denetimi önsel-ters bölmesinde aday atmadı.
- **Koşullar:** 23, öteki tohumlarla (18, 19, 20, 22) aynı config ve aynı üretim koşullarıyla üretilir; başka ayar yok, eşik değişmez. Bu bir kapı koşusu değil, yalnız üretimdir.
- **Kayıt:** `config.json` `h1_onayli_tohum_degisimleri` = [21 → 23, neden, tarih 2026-10-25, kalan hak 1]. Kalan son hak ancak yeniden onayla kullanılır.
- Config bu yüzden değişti; bundan sonra geçerli özet:
  - `config.json`: `feae40960a4f24f24121bdf74cea782c384593fd2f31f87b0115ebc0ee32890f`
- 23 ya da başka bir tohum yine durursa üretim durur ve bildirilir. Yeni manifest özetleri bu ekin 5. bölümüne yazılır.

### 5. Yeni bölümler ve kapı koşusu öncesi özetler (2026-10-25)

- **Üretim:** `.venv/bin/python -m degerlendirme.h1 uret uretilen/h1_v3`, kod commit `d534dac`. Tohum 21 yine durdu ve onaylı değişimle 23 geçti; 23 bütün bölmelerden geçti. Kullanılan tohumlar: 18, 19, 20, 23, 22. Değişim hakkı: 2'den 1'i kullanıldı, 1 kaldı.
- Tohum 18, 19, 20'nin manifestleri, onaydan önceki ilk üretimle bayt bayt aynı.
- **Çıkarılamadığı için atılan aday:** yalnız yön ters bölmesinde; öteki bölmelerde 0. Tohum 18: 2311, 19: 2340, 20: 2590, 23: 2335, 22: 2539.
- **Özetler (sha256):**
  - `config.json`: `feae40960a4f24f24121bdf74cea782c384593fd2f31f87b0115ebc0ee32890f`
  - `dna`: `4a4af6b83c58e33d9971f9d84ed6c440fbb2341d14ec70dc4710128d74bfaa75`
  - `tohumlar.json`: `215814be7ebd9cfe482285ab47b3ca15d4b07a467d74ece6822fd63aa7c80545`
  - `tohum_18/ozet.json`: `f1e7fe5caa423c7d61cc3c79476cb4ca77ba6931eb41748d2c6e0481cf5d33ea`
  - `tohum_19/ozet.json`: `490ca61c977f66cff40456429106ed3724be3924f89eaa57504d4c70a9c7ab61`
  - `tohum_20/ozet.json`: `0c4fc16d11c1e706dc67c2a9d73dee3abd8ae132394887943ed5b27a42c65fb1`
  - `tohum_22/ozet.json`: `6f6a5ab522f3ed05b56e324050b8a555a4d8b88900f28e67480ef6a7a5652c67`
  - `tohum_23/ozet.json`: `900355ca51975f76ba4dbfa5fa2325c6c5145c0e755ee44fca4d4f85260702b6`
- Kapı bölmeleri bu ekten sonra tohum 18, 19, 20, 23, 22 ile bir kez koşar; sonra yeni tohumların eğitim satırı, altın küme ve baskı ölçümü. Kapı geçmezse ayarlar, DNA ve eşikler bu sonuca bakılarak değiştirilmez (§6).

### 6. Kapı koşusu sonucu (2026-10-25, koşudan sonra yazıldı)

- **Komut:** `.venv/bin/python -m degerlendirme.h1 kapi uretilen/h1_v3 veri/dna/akrabalik_dna_v8.json uretilen/h1_v3_kapi_1`, bir kez, kod commit `60e38f3`. Ön kayıt denetimi (`on_kayit_denetle`) geçti.
- **KAPI GEÇTİ:** uzunluk, yön ters, önsel-ters ve zincir-bozuk bölmelerinin her birinde, tohum 18, 19, 20, 23, 22'nin her birinde 400/400. Toplam 8000/8000; yanlış ilişki 0, "bilmiyorum" 0.
- Müdahale (kapıya girmez): 5996 puanlı, 4 sınanamadı (ayrı sayıldı, K-021), zincir-bozukta 2000 cevapsız.
- Kapı özeti: `raporlar/H1_v3_kapi_ozet.json`, sha256 `935cea7b47dcccb319e86bf68f02b3be7312cf9b924334ce9a449cc446cf11cf`.
- Kapıya girmeyen satırlar: yeni tohumların eğitim bölmesi 2000/2000; altın küme parça 1 ve parça 2 kullanıcı cevabıyla 50/50 ve 50/50 aynı (parça 2'nin 50 cevabı LLM taslağı, kullanıcı onaylı; bağımsız insan cevabı değil); baskı ölçümünde tur, havuz ve bütçe sınırına ulaşan bölüm 0.
- Ayarlar, DNA ve eşikler bu sonuca bakılarak değiştirilmedi. Ayrıntı: `raporlar/H1_v3_SONUC.md`.
- **H2 kapısı:** "## ÖK-004 sonucu" başlığı (K-032 §4'e göre H2 kapısını açar) yazılmadı; kullanıcı kararı bekliyor.


## ÖK-004 sonucu

**Yazıldı:** 2026-10-25, kullanıcı ve danışman onayıyla (K-040). Bu başlık K-032 §4'e göre H2 kapısını açar. H2 koduna başlamak için ayrıca şunlar gerekir (K-040): A6 bağımsız incelemesinin sonucu, H2 tasarım tartışması (danışman ve kullanıcı, literatür taraması ışığında) ve H2 ön kayıt belgesi (yeni ÖK).

- **Sonuç: KAPI GEÇTİ.** Uzunluk, yön ters, önsel-ters ve zincir-bozuk; tohum 18, 19, 20, 23, 22; her bölme-tohumda 400/400, toplam 8000/8000. Yanlış ilişki 0, "bilmiyorum" 0. Ayrıntı: ÖK-004 eki §6, `raporlar/H1_v3_SONUC.md`.
- **Kapı özeti:** `raporlar/H1_v3_kapi_ozet.json`, sha256 `935cea7b47dcccb319e86bf68f02b3be7312cf9b924334ce9a449cc446cf11cf`.
- **Önceki iki koşu (silinmez):** ÖK-002 (tohum 7–11) ve ÖK-003 (tohum 12, 13, 14, 17, 16) kapıyı geçmedi; K-033'teki kayıt geçerlidir.

## ÖK-005 (H2): mühür (Kapı 1)

**Tarih:** 2026-10-26.
**Dayanak:**
- K-041: Kapı 0 onayı; altı soruya evet; sayaç + çekirdek hakem hattı; A6 bağımsız incelemesi Kapı 2'den önce.
- K-042: Kapı 1 onayı.

**Metin:** `ONKAYIT_H2_TASLAK.md`, sha256 `38833917d2b75a3bac89e7520edff8f79ce07c86b2da26bb1785b2ee84d397ea`.
- Kapı 0'da onaylanan taslaktır.
- B0'da yapılan üç yazım düzeltmesi içindedir; hiçbiri bir sayıyı değiştirmedi:
  - V-060: gövde başın kendisini içeremez;
  - V-062: A3'te çift terimde üretim durur;
  - V-063: boş dünyada ileri taraf.
- Dosya kilitlidir (`config_h2.json` `h2_kilitli_veri_dosyalari`).
- Bundan sonraki her değişiklik yalnız aşağıya "ÖK-005 eki" olarak yazılır. Sonuçtan sonra değişen eşik sonuca "keşif" damgası vurdurur.

**Tasarım:** `H2_TASARIM.md`, sha256 `a409858e54b2a0434d0b84a77e15ca4d7ac7063beeea23e179705e180aafb1db`.

### ÖK-005 eki §1: B0 sonuçları ve mühür anındaki özetler (2026-10-26)

1. **M0 (geliştirme havuzu, 16 dünya, K5/21):**
   - aday uzayı 35.544.873 (kâğıt üstü hesapla aynı);
   - süzgeçten geçen 203.124.
   - Üç koşu bit-aynı:
     - `m0_adaylar.jsonl` `1b4388dbfb05cf5bfa55bc6e30a1671a38fcf8b595279bbe8d75227667c5ba0b`;
     - `m0_ozet.json` `9baf3703586c019ca57339387e9e5e22ef48a63f655dc4da7b2d4c1ec4c35fd1` (`raporlar/h2_b0/m0_ozet.json`).
   - Süreler: 885, 901 ve 907 s; ortanca 901 s; 4 iş parçacıklı tek süreç.
   - Koşular `config_h2.json` `7a67eb949240f6f821374d32af49d95d2108d4ca6ceab4a572d8011aa30e0e53` ile yapıldı. Mühürdeki özetle farkı yalnız `h2_kilitli_veri_dosyalari` alanıdır.
2. **Bütçe kademeleri (ÖK-005 §4 madde 23):** 9, 27, 90, 270, 901 s. Birim: 4 iş parçacıklı tek sürecin duvar saniyesi.
3. **Havuzlar:**
   - geliştirme 16, final 24, kontrol 8; 48 dünya özeti tekil;
   - liste `raporlar/h2_b0/havuz_ozetleri.json`, sha256 `f4e81f2a12eb2365c4c3b6b9ab201ef6bebfa873a68babcca28a35e5c76a9be1`.
   - Final ve kontrol dünyaları yalnız özetlendi; içerikleri açılmadı.
4. **Çekirdek dondurma sözleşmesi:**
   - çekirdek özeti (`araclar/cekirdek_ozeti.py`): `db87374f5835af1d37aae951ae9b5f931fe5c6c483da38fb96eedf9595d4aafa`;
   - keşif paketi özeti: `bd28557183f70c7ec290d98f4ffc23588fce08de2247c1ff0d97304f561032b1`.
   - Hiperparametreler H1 değerleridir.
5. **Dosya özetleri:**

   | Dosya | sha256 |
   |---|---|
   | `config_h2.json` | `c48869ca88b4c2026b3c380035ab0dce7e1a05ad01b19c77d66f5350f47ecb59` |
   | `sema/aday_v1.schema.json` | `c20ff73649ee42504fd4ce6e1d84dbee84608063793a8f2691a92ca6a779ef51` |
   | `sema/kirmizi_dosyasi_v1.schema.json` | `b98151939e96b23db7e732673dddded1a521e9f930ad292d443aaef9e9bff83b` |
   | `veri/h2/kirmizi_ornek_v1.json` | `2f993c84541e9bd28443627a34a24a03eaa4fbdd9983bc0ed038f5d62705e095` |
   | `degerlendirme/h2_dunya.py` | `3847838b0484650e17b9846900315bac4a2c9ddd2352feb734f497f32996bb81` |
   | `degerlendirme/ikinci_uretec.py` | `c8dc8147b0c6d2652201aec016c2ad2d57ac14871c292c48bd91b3ad2d9db958` |
   | `degerlendirme/h2_butce.py` | `7fcba03a8809f6e46850963eda8dc1226483d53ee869d15aef229e9e23b32feb` |
   | `degerlendirme/h2_bagla.py` | `ddbf39ce741897b7b65022b0df7c9b0403a30c7b34d6d64d090e1cef2e5b744f` |
   | `degerlendirme/h2_m0.py` | `ea4144173c7a443c782aa1467a5ee33617f674f548108990a80b5f00ba9bc05d` |
   | `degerlendirme/dunya.py` | `e2af2801191c2814676634f26e9d78c75234336a93ef7f1fc013b05f5a242b03` |

6. **Mutasyon sınaması:** 48 mutant, 48 yakalandı. İlk turda 3'ü kaçtı (M0 sırası, M0'da OI sayımı, havuz tohumunun ailesi); üçü için test eklendi, kod değişmedi.
7. **Henüz gelmeyenler:**
   - Gizli kırmızı takım dosyası: B1'den önce danışmandan gelir; özeti §2 olarak eklenir.
   - K değerleri: B1 kalibrasyonundan sonra §3 olarak eklenir.
   - A6 bağımsız inceleme: Kapı 2'nin ön şartı.

### ÖK-005 eki §2: gizli kırmızı takım dosyası ve B1 öncesi kod (2026-10-26, K-043)

1. **Gizli sahte kural dosyası (danışman yazdı; K-041, K-043):**
   - Yol: `degerlendirme/kirmizi_gizli/kirmizi_gizli_v1.json` (adı içerik açılmadan `git mv` ile değişti; eski ad "kirmizi gizli v1.json").
   - Biçim denetimi (`python3 -m kesif.aday ... kirmizi_gizli`): 4 aile, 180 kural, en küçük aile 45.
   - sha256 `c8adb6855a4b20c853f32d7e12f254712f49cf4ee97fb9464108b3614c8d565b`; beklenenle aynı.
   - İçerik açılmadı, okunmadı, yazdırılmadı. Özet `config_h2.json` `kirmizi_gizli_dosyasi` alanına yazıldı; dosya `h2_kilitli_veri_dosyalari` ile kilitli.
   - **Sınır:** gizli ailelerin yazarı danışmandır; danışman kodlayıcıyla aynı model ailesindendir.
2. **B1 öncesi kod ve ayar (ek §1 tablosundaki özetlerin yerine geçenler ve yeni dosyalar):**
   - `degerlendirme/h2_bagla.py` değişti: veto/null kipinde simetrik ilişki yönsüz bağlanır; ÖK §13.6'ya uyum düzeltmesidir (V-065 madde 10). Bu koddan önce hiçbir sonuç üretilmemişti.
   - `config_h2.json` değişti: geçit sabitleri (ÖK §4, §2.1, §8), K başlangıcı ve ızgarası, B1/B2 sayıları, Z12 alanı, gizli dosya özeti. Eşik değerlerinin hiçbiri ÖK'tekinden farklı değil.
   - Kodlayıcının küçük kararları: V-065, V-066.
   - Çekirdek özeti ve keşif paketi özeti ek §1'dekiyle aynıdır (çekirdek kodu ve `kesif/` değişmedi).

   | Dosya | sha256 |
   |---|---|
   | `config_h2.json` | `82a66030e75003d0a907dd862fee03d0c1fe522393b7385c8d09e091ceae67cc` |
   | `degerlendirme/h2_bagla.py` | `2cdf1008c090cbb083bbec74d93ffcef784628c1537dc862b0c65812dd5a1c31` |
   | `degerlendirme/kural.py` | `082d450b91839e25fbf1b8e72ca527a67318e185d24b74e0cb9c99613d1f6805` |
   | `degerlendirme/h2_bolum.py` | `143322561e887b60f1553cedf5d91cf6182fa161540bc59a391c9d6e4bd6d7c7` |
   | `degerlendirme/h2_gecit.py` | `869cd87a2d0866da727b9c859c0af0715344512c686575045661fd98df17fe2a` |
   | `degerlendirme/h2_ikiz.py` | `5dd13a83a3441ae08e0b60dd4b0e68e740f97122e9d467912e235ee17a88f3b6` |
   | `degerlendirme/h2_tur.py` | `53be994a9b7eb51da07625385baf5af2fca0a2b8104258ba795a74db8122ae8f` |
   | `degerlendirme/h2_kirmizi.py` | `f93f644027a6c843719e043e9a23e3e4b76e1b7d68dea7aa295b8c39bc6cfcf6` |
   | `degerlendirme/h2_kalibrasyon.py` | `793dfed61a5de454ec4ee241714f7aee2e90e200e3e83ab8f778fb3af9c3069d` |
   | `degerlendirme/h2_b1.py` | `393ab1d97fb37751ce9a9de3ff51e3518ddaad35a479970b7a2ef33bee3799fa` |
   | `degerlendirme/h2_b2.py` | `2f79d9e0cd8d968cef6a5afdac0d4a0c8ae9f2f56c46e6650c892d3950fbcd41` |
   | `degerlendirme/h2_olcum.py` | `bc2a92e1e1da758bf80690c6ed5faabbdbe80ceef7369b6569f6823314e47506` |
   | `degerlendirme/h2_onkayit.py` | `aa9834a7d7c3c76e954235969f7e36fd0a83e9449b02b3fc75b2b16cb67c3807` |
   | `degerlendirme/h2_aktarim.py` | `19b7ea01e1baea2fb33af7c2eb4227768a4e2faeaab181bf38a89bd9c8d4af23` |
   | `degerlendirme/z12.py` | `9f054a7494fe5dcec0114035310ea278134c25027a8dbef0d54701c74f4b51d9` |
   | `degerlendirme/z12_ikinci.py` | `0ff66b6611c704f0f39442f8584742257e3c405e3ce9fa8605f5745cfb1307cb` |
   | `degerlendirme/h2_rapor.py` | `d4eafe0eb088888cf97be63e2a652661f310309410aaab93b35f8d162805f585` |
   | `degerlendirme/istatistik.py` | `7279e6d5450abdf05bf1d951eeec45e920e6913357dc2852d649fd547b25ffef` |
   | `sema/z12_iliskiler_v1.json` | `487886a20da4cb77b5cf0d42ef55200b57fbd00480abebade21093dd50a5595a` |
   | `veri/h2/z12_tanimlar_v1.json` | `a862689d727181214fc60f2f821da9876e51cbc0421eb35263c4585ab70a6e5a` |
   | `kilit/z12_sema_onayi.json` | `0f5f393d4e1fed12e695631a55834d0660f56409a11afa43af9ea1d9f84d230f` |


### ÖK-005 eki §2a: B1 koşucusunda akış kısaltması (2026-10-30, V-065 madde 15)

- Boş aday (P*) akışında yalnız sahte adaylar geçitte ölçülür; sahte olmayanların hükmü ne K seçimine ne P*'a girer. Sonuç aynıdır, süre kısalır. Değişiklik B1'in kalibrasyon turları başlamadan önce yapıldı; hiçbir hüküm henüz verilmemişti.
- B1'de akışın ilk 4800 adayının hiçbiri gerçek geliştirme havuzunda yanlış vermedi (sahte sayısı 0).

   | Dosya | sha256 |
   |---|---|
   | `degerlendirme/h2_b1.py` | `39ee2f09da54c82425c043e30e2b8b5baa294e4b137cd5297079b5a544acf30f` |


### ÖK-005 eki §2b: boş ölçüm grubu düzeltmesi (2026-10-31)

- Akışta hiç sahte aday olmayınca kalibrasyon ölçümleri "bos" grubunu oluşturmuyordu (hata, K seçiminden önce durdu). Gruplar baştan kurulur; test önce. Hiçbir hüküm etkilenmedi.

   | Dosya | sha256 |
   |---|---|
   | `degerlendirme/h2_b1.py` | `5a48d48d2f3eb2035b123b2bd686117529f291c1faa83432d7cf5d87d6a12dc4` |


### ÖK-005 eki §2c: sembolik tanık sayımı §13.2 ile uyumlu hâle getirildi (2026-10-31, V-065 madde 2)

- **Hata:** aşama 5'in sembolik "doğru" sayımı, maskelenen olguyu kuralın kendi türettiği ters olgu üzerinden ikinci adımda da sayıyordu. §13.2'deki tanık tanımı tek adımlıktır (gövdenin maskeli olgular çıkarılmış olgular üzerindeki eşleşmesi). Hata, çekirdekle sembolik sayımın uyumunu bozuyordu.
- **Nasıl görüldü:** B1 kalibrasyonunda M0'ın ilk 200 adayından çekirdek adımına ulaşan 6 adayın 6'sı "uyum" şartında düştü; 81 ızgara noktasının hepsinde KABUL 0'dı, K başlangıç değerinde kalmıştı.
- **Düzeltme:** sembolik doğru tek adımdır (test önce). Kapanış yalnız küme ölçülerinde (B2 sınıfları, bilmiyorum, makas) kalır.
- **Yeniden ölçüm:** kalibrasyona bağlı bütün ara sonuçlar silindi; aşama 1–4 önbelleği (tanımdan etkilenmez) korundu. Aynı B1 taze dünyaları (aynı tohumlar) ve aynı aday akışlarıyla yeniden hesaplanır; eşik, aile ve kural değişmedi.
- **Kalan ve önkayıta göre olağan durum:** çekirdek her turda hücre başına en çok 8 yazar (mühürlü H1 değeri) ve ilk turda sığmayan eşleşmeleri sonraki turlarda yeniden denemez; çok eşleşmeli kurallarda maskeli olgu türetilemeyebilir. Bu adaylar §4 madde 11 gereği BİLMİYORUM olur; sayısı raporlanır.

   | Dosya | sha256 |
   |---|---|
   | `degerlendirme/h2_gecit.py` | `3517546c74616ed635dd3207b9d10e72df9ab6ad303a9922877303b24e151b6e` |


### ÖK-005 eki §2d: boş-dünya tetiğinde şemadan okunabilir sınıf (2026-10-31)

- Eksiklik: boş koşuda sıra şemadan okunabilir adaylardan süzülüyordu, ama obiterin indirgenmiş kuralı sıraya sonradan girebildiği için okunabilir bir kabul tetik sayımına karışabiliyordu. Kabuller artık ayrıca denetlenir (§4 madde 20); okunur kabul sayısı ayrı yazılır. Test önce.
- Boş koşu 1'in sonucu değişmez: 197 kabulün 190'ı okunur sınıf dışındadır. Koşu 1 önbellekten yeniden sayılır; süresi ilk ölçümdür (2283 sn).

   | Dosya | sha256 |
   |---|---|
   | `degerlendirme/h2_b1.py` | `2bcc0cbd5878ba993fd27612419201be7f596ad66f8a86fb1fe2812a78af2e81` |


### ÖK-005 eki §2e: kaldığı yerden devamda "görülen aday" kümesi (2026-10-31)

- Hata: yeniden başlatılan koşuda önbellekteki bütün adaylar "bu aramada görülmüş" sayılıyordu; obiterin indirgenmiş kuralları ikinci koşuda sıraya girmiyor, tur farklı adaylarla doluyordu. Sorgu defteri bunu "turda aday sınırı doldu" diye durdurdu (boş koşu 1'in önbellekten yeniden sayımında). Görülen küme artık koşucunun kendi durumudur. Test önce. Hiçbir hüküm değişmedi; B2 henüz başlamadı.

   | Dosya | sha256 |
   |---|---|
   | `degerlendirme/h2_tur.py` | `afb47255da21fdee241c40028b26a6c330528d634af60dba29b2d916367b6647` |

