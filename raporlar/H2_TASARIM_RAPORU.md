# H2 tasarımı: kısa rapor (2026-10-26)

## Ne yaptım

- Ortak tasarım v1'i, kendi eski taslağımla, bugünkü kodla ve 244 kurallık DNA v8 ile karşılaştırdım. İki belge yazdım:
  - `H2_TASARIM.md`: nihai tasarım önerisi.
  - `ONKAYIT_H2_TASLAK.md`: H2 ön kaydının taslağı, mühürsüz.
- v1'in "genel zekâ sözü yasak" ve "yasak iddialar" bölümleri aynen geçti.
- Kod yazmadım, deney koşmadım; çekirdek ve üreteç çalışmadı. Yalnız sayım için depoda olmayan küçük sayma betikleri kullandım. Kural sayısını ikinci bir yoldan doğruladım.
- **Kâğıt üstü sonuçlar:**
  - **Aday kural sayısı:** v1'in öngördüğü dar arama alanı (≈62 bin kural; eski "124 bin" sayım hatasıydı) DNA kurallarının yalnız yarısının biçimini içeriyor. Bu alanla H2'nin %90 geçme şartı tutamaz. Gereken alan 35,5 milyon aday; 244 kuralın hepsinin biçimi içinde.
  - **Kaba kuvvet sayımı:** bu bilgisayarda 5–35 dakika, en çok 3 GB bellek. Aynı işi çekirdekle yapmak yaklaşık 50 yıl sürerdi; bu yüzden sayımı ayrı, kesin bir sayaç yapar.
  - **"Turda 200 aday, 12 tur":** B1'de rahat tutuyor. B2'de sınırda; önceden yazılmış tek bir kuralla 400'e çıkabilmesini öneriyorum. Asıl sınama 3–45 saat sürer.
  - **H2'nin tamamı:** 4–8 gün işlem süresi. Bu bilgisayarda ekran kartı yok.

## v1'den başlıca sapmalar (hepsi gerekçeli, `H2_TASARIM.md` §11, 20 madde)

1. Arama alanı genişletildi (yukarıda).
2. **"Cevabın tersini de gizle" kuralı daraltıldı.** v1'deki gibi uygulansa 244 kuralın 81'i hiç sınanamaz ve en iyi sonuç %67 olurdu.
3. **Güven hesabında "aile sayısı kadar örnek" kuralı tek tek kurallara uygulanamaz.** Üç ailede en yüksek güven %44 çıkar. Kural başına örnek birimi, tek tek aile parçaları oldu.
4. **Hawaii, Iroquois ve Omaha dünyaları H2'nin geçme şartından çıkarıldı.** O sistemlerde bizim kurallarımız doğru değil. Yalnız son basamakta ölçüm olarak kalıyorlar.
5. **Kesin hesaplar ayrı sayaçta:** şans sınaması, boş dünya ve karşılaştırma eğrisi çekirdekle yapılamayacak kadar pahalı.
6. **İki kişi arasında hiç akrabalık yazılmamışsa,** kuralın onlar için akrabalık uydurması "yanlış" sayılacak. Bugünkü geçit bunu kaçırıyordu.
7. **Tasarım onayı için yeni bir kapı (Kapı 0) eklendi;** son mühür, ilk basamağın sonunda vurulur.

## Size sorular (evet/hayır; önerim parantezde)

1. Sistem bir kuralı tam yazılan biçimde değil de başka kurallarla aynı sonuçları çıkararak bulursa, bu "bulundu" sayılsın mı? Aynı biçimde bulunanlar ayrıca sayılacak. (Evet)
2. Sistem bir kuralı sınarken, rastgele bir aile parçası yerine o kuralın "eğer" kısmının gerçekten geçtiği bir aile parçasını isteyebilsin mi? Cevap yine gizli kalır. (Evet; hayır olursa nadir kurallar "bilmiyorum" kalır, sınama dört kat uzar.)
3. Bir kuralın kabulü için şu üç aile türünün en az ikisinde doğru çıkması şart olsun mu? (Evet)
   - bugünkü aileler;
   - daha derin, içinde çocuksuz ya da evlenmemiş kişiler olan aileler;
   - başka bir programla kurulmuş, iki soyun evlendiği aileler.
4. Sistemi kandırmak için tasarlanmış sahte kuralların yarısını danışman (ya da siz) yazsın, ben hiç görmeyeyim mi? (Evet)
5. Kuzenlere ve amcalara başka adlar veren üç akrabalık sistemi yalnız son basamakta ölçüm olarak kullanılsın mı? Tanımlarını siz ya da danışman onaylarsınız. (Evet)
6. Saat aritmetiği dünyası için önerdiğim on ilişkilik listeyi (bir sonraki, karşısı, aynı kalan, …) onaylıyor musunuz? (Evet)

## B0'a başlamak için eksik olan

1. İki belgenin ve bu altı sorunun onayı (Kapı 0). Danışman sapmaları görmeli.
2. A6 bağımsız inceleme sonucu (sizin önceki şartınız). Hâlâ gelmedi.

**B0'ı engellemeyen, ama sonra gerekenler:**
- B1'den önce: danışmanın gizli sahte kuralları.
- Son basamaktan önce: üç akrabalık sisteminin tanım onayı.
