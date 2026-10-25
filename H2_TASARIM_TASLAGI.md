# H2 tasarım taslağı (yalnız belge; kod yok)

**Durum:** TASLAK (2026-10-25). Danışmanın maddelerinden (K-039) kodlayıcı yazdı. Hiçbir karar içermez. H2 başlamadan önceki tasarım tartışmasının (FIKIRLER.md madde 1) girdisidir. H2 kapısı kapalıdır (K-032 §4): H1 son denemesi (ÖK-004) sonuçlanmadan H2 kodu yazılmaz.

**H2'nin sorusu (sistem.md §13):** Klonal seçilim, doğru kuralları sıfırdan bulabiliyor mu?

**Terimler:**
- **Kural (hücre, DNA):** "eğer bu ilişkiler zinciri varsa şu ilişki de vardır" diyen bir satır. Ör. "X'in babası Y, Y'nin babası Z ise Z, X'in dedesidir".
- **Halka:** kuralın "eğer" kısmındaki tek bir ilişki adımı.
- **Önerici:** aday kuralları üreten parça (mutasyon, klonal seçilim).
- **Geçit:** adayları kabul ya da reddeden parça (A6'daki bellek geçidi).

## a) M0: kaba kuvvet temel çizgisi

- **Amaç:** klonal seçilimin bir işe yarayıp yaramadığını görmek için önce en basit yöntem: bütün küçük kuralları tek tek saymak.
- **Kural uzayı:**
  - Gövde: 7 temel ilişki (anne, baba, oğul, kız, eş, erkek kardeş, kız kardeş) ve her birinin ters yönde okunuşu, yani 14 sembol. Halka sayısı en çok 3, zincir biçimli.
  - Gövde sayısı: 14 + 14² + 14³ = 2954. Baş (sonuç): şemadaki 21 ilişki × 2 yön = 42.
  - Toplam aday: 2954 × 42 = 124.068. Bu, bugünkü çekirdekle kaba kuvvetle sayılabilir.
  - Zincir dışı biçimler (ortak değişkenli ağaçlar, `farkli` koşulu) ayrı bir genişletme olarak sayılır ve raporda ayrı satırda durur.
- **Güven (AMIE tarzı):**
  - Standart güven = kuralın doğru tahmin sayısı / gövdenin eşleştiği sayı.
  - PCA güveni yalnız işlevsel ilişkilerde kullanılır. İşlevsel ilişki: kişi başına tek değer alan ilişki; şemada 7 tane (anne, baba, eş, babaanne, anneanne, kayınpeder, kayınvalide). PCA, "kişinin o ilişkiden hiç gözlemi yoksa bilinmiyor say" demektir.
  - Çok değerli ilişkilerde (oğul, kardeş, …) standart güven kullanılır.
- **Ablasyon:** mutasyon ve klonal seçilim M0'ın üstüne eklenir; her parça çıkarılarak (ablasyon) katkısı ölçülür. Katkısı sıfırsa raporda açıkça yazılır.

## b) Başlangıç basamakları

1. **Onarım:** DNA v8'den kurallar silinir; sistem silinenleri yeniden bulabiliyor mu?
2. **5–10 tohum kural:** az sayıda doğru kuralla başlanır.
3. **Sıfır tohum:** hiç kural yok. Ama verili bir Horn şablon ailesi vardır: en çok 3 halka, zincir biçimi. Horn şablonu: "şunlar varsa bu vardır" biçimindeki kural kalıbı.

**Sızıntı tablosu:** sıfır tohumda bile sisteme verilen ön bilgiler. Her biri "sıfırdan" iddiasını sınırlar.

| Ön bilgi | Ne söyler | Kâhin mi? | Azaltma / ablasyon |
|---|---|---|---|
| İlişki şeması: adlar, ters listesi, işlevsellik, dışlayıcı grup (tek grup, 21 ilişki) | Hangi ilişkilerin çelişeceği, hangisinin tek değerli olduğu | Hayır, ama alan bilgisi | Ters ve işlevsellik bilgisi olmadan bir kol |
| Temel ilişki listesi (7) | Gövdede hangi sembollerin kullanılacağı | Hayır | Bütün 21 ilişkiyle gövde kolu |
| Şablon ailesi: ≤ 3 halka, zincir biçimi | Kuralların şekli | Hayır, ama güçlü önsel | 4 halka ve zincir dışı biçim kolu |
| Gözlem bölümü tasarımı (V-057): seçilen kişiler arasındaki bütün ilişkiler | Türetilmiş ilişkilerin gözlenebildiği | Üreteç gerçek ağacı bilir; gözlemler doğrudur | Gözlem seyrekliği ekseni (f) |
| Dünya varsayımları (iki ebeveyn, tek evlilik, karşı cins; V-053) | Üretecin dünyası | Üreteç tarafı | Farklı dünya aileleri (f) |
| İlişki adları | Anlamlı Türkçe adlar | Hayır, ama dil ipucu | Ad permütasyonu (f) |
| Geçit eşikleri ve müdahale testi | Kabulün ölçütü | Hayır | Sahte kural havuzuyla kestirilir (c) |

## c) Kabul ölçütü

- **Doğruluk:** her ortam için Wilson alt sınırı. En kötü ortam esas alınır (EK A P7, grup-DRO).
  - Wilson alt sınırı: az kanıtta "yüzde 100" gibi görünen oranı kanıt sayısına göre aşağı çeken güven aralığının alt ucu. Bugünkü geçitteki "doğruluk 1,0 ve en az 3 kanıt" (K-036, geçici) bunun yerine geçebilir.
- **Müdahale testi:** K-037 (b·c).
- **Eşik:** etiketleri karıştırılmış sahte kural havuzundan kestirilir. Sonuç ilişkileri rastgele değiştirilmiş kurallar geçitten geçirilir; sahte kural kabul oranı hedef değerin altında kalacak şekilde eşik seçilir.
- **Çoklu test düzeltmesi:** aday sayısına göre (ör. Holm). 124.068 aday sınanınca şansla geçen olur; düzeltme bunu sınırlar.
- Eşik değişikliği kullanıcı kararıdır ve yeni bir ön kayıtla gelir (i).

## d) Geçit verisinin üçe ayrılması

1. **Yönlendirme verisi:** önericinin uygunluk sinyali için.
2. **Geçit verisi:** kabul kararı için. Önericiye yalnız "geçti / kaldı" döner, sayı dönmez. Böylece önerici geçide göre ayar çekemez.
3. **Son doğrulama verisi:** hiç dokunulmaz. Yalnız sonunda bir kez kullanılır.

Kabulden sonra kural, taze tohumlu yeni bir dünyada yeniden doğrulanır.

## e) Kırmızı takım ve gerileme

- Bilerek sahte kısayol kuralları tohumlanır. Örnek: yalnız bir ortamda tutan bir ilişki çakışması; A6 testindeki zindle∘zindle → vonk kuralının akrabalık karşılığı. Hedef: sahte kuralların kabul oranı 0.
- Her kabul sürümlenir (bellek deposu: hash zinciri, V-056).
- Her kabulden sonra gerileme paketi koşar: H1 kapı bölmeleri ve altın küme.
- Çelişki artarsa kabul otomatik geri alınır (`gozden_gecir`, geri alma olayı).

## f) Ortamlar

- Akrabalığın yanına **en az 4 farklı dünya ailesi**. Öneri:
  1. kurum hiyerarşisi (yönetici, çalışma arkadaşı);
  2. coğrafi içerme (il, ilçe, mahalle, komşuluk);
  3. zaman sırası (önce, sonra, aynı gün);
  4. parça-bütün ve tedarik zinciri.
- **Eksenler:**
  - ilişki adı permütasyonu;
  - topoloji: zincir uzunluğu, dallanma, döngü;
  - gözlem seyrekliği.
- **"Destekleyici gürültü" tuzakları:** yanlış bir kuralı destekler gibi duran gürültü.
- **Gürültü merdiveni:** olgu silme %0–50, yanlış olgu %0–10.
- **Genelleme:** Hawaii, Iroquois ve Omaha/Crow tipi sentetik akrabalık dünyaları. Bunlar kuzenleri ve kardeşleri farklı adlandıran gerçek akrabalık terim sistemleridir:
  - Hawaii: bütün kuzenler kardeş sayılır.
  - Iroquois: paralel kuzen kardeş sayılır, çapraz kuzen ayrıdır.
  - Omaha/Crow: nesiller bir soy çizgisinde kayar.
  - Başarı, bu dünyalardaki soy ağacı sorgularının doğruluğuyla ölçülür.

## g) Değerlendirme bölmeleri

H2'den önce dondurulur (hash kilidi):

- **Kural derinliği:** 1–2 halkalı kurallarla eğit, 3 halkalıda sına.
- **Görülmemiş ilişki çifti bileşimi:** eğitimde hiç birlikte görülmemiş ilişki çiftleri.
- **Kısayol ortamı:** bir kısayolun eğitimde tutup testte tutmadığı ortam.

## h) Başarı raporu

**Altı sınıf** (bulunan her kural DNA v8'le karşılaştırılır):

1. **Özdeş:** yapıca aynı (değişken adı ve halka sırası dışında; `kanonik_bicim`).
2. **Daha genel:** bir DNA kuralını kapsar ve doğrudur.
3. **Fazlalık-doğru:** doğru ama ötekilerden türetilebilir.
4. **Kapanış-eşdeğer:** başka kurallar ama rastgele dünyalarda aynı sonuçları üretir.
5. **Farklı-doğru:** doğru, DNA'da yok, fazlalık da değil.
6. **Bozuk:** yanlış.

**Fazlalık denetimi:**

- Kanonik biçim.
- Theta-subsumption. Bir kural, değişkenleri eşlenince ötekinin gövdesinin parçası oluyorsa onu kapsar.
- Rastgele dünyalarda kapanış karşılaştırması.
- Önce güvenilirlik ve müdahale sınanır; kapsama (subsumption) tercihi ondan sonra gelir.

**İstatistik:**

- En az 20 bağımsız tohum.
- Geliştirme ve kilitli test tohumları ayrı.
- %95 bootstrap aralığı.

## i) Ön kayıt

- Eşikler, bütçe ve durdurma kuralları sonuç görülmeden kilitlenir. Kilit: yeni bir ÖK, git etiketiyle.
- Başarısızlık şöyle raporlanır: "bu bütçede, bu uzunlukta, bu dünyada bulunamadı". "Bulunamaz" denmez.

## j) LLM ve yan kollar

- H2'de LLM önerici **yok**.
- Şunlar ana yol değil, ayrı ablasyon kollarıdır:
  - müfredat (1 → 2 → 3 halka);
  - MAP-Elites arşivi: farklı türde iyi adayları ayrı ayrı saklayan arşiv;
  - HRR süzgeci: çekirdeğin vektör eşleşmesiyle ön eleme;
  - SAFRAN tarzı kanıt birleştirme: aynı kanıta dayanan kuralları tek sayan birleştirme.

## k) Yenilik iddiası

- "İlk kural öğrenen sistem" denmez. Bu alanda var olanlar:
  - tümevarımsal mantık programlama (ILP: FOIL, Progol, Metagol, Popper);
  - bilgi grafiği kural madenciliği (AMIE, AnyBURL);
  - nöral kural öğrenme (NeuralLP, DRUM, RNNLogic).
- **Konum:** etiketsiz, kâhinsiz, kendini sınayan ve denetlenebilir bir bellek geçidi.
- Ablasyonla gösterilmeden "yeni" denmez.

## l) Kafiye (yalnız taslak; koşulmaz)

FIKIRLER.md madde 2: H2'den sonra ilk alan aktarımı adayı. Aşağıdakiler yalnız elle yazılmış taslaktır.

**Ünlüler (Türkçe'nin 8 ünlüsü):**

| Ünlü | Kalın / ince | Düz / yuvarlak | Geniş / dar |
|---|---|---|---|
| a | kalın | düz | geniş |
| ı | kalın | düz | dar |
| o | kalın | yuvarlak | geniş |
| u | kalın | yuvarlak | dar |
| e | ince | düz | geniş |
| i | ince | düz | dar |
| ö | ince | yuvarlak | geniş |
| ü | ince | yuvarlak | dar |

**Ünsüzler (kaba sınıflama):**

| Özellik | Ünsüzler |
|---|---|
| Sert (ötümsüz) | ç, f, h, k, p, s, ş, t |
| Yumuşak (ötümlü) | b, c, d, g, ğ, j, l, m, n, r, v, y, z |
| Sert–yumuşak eşleri | p–b, ç–c, t–d, k–g/ğ, f–v, s–z, ş–j |
| Akıcı | l, m, n, r, y |

**Veri biçimi taslağı:**
- Kelime kaydı: `{"kelime": "...", "heceler": ["..."], "son_unlu": "a", "son_unsuzler": ["r"]}`.
- Gözlem olarak üçlüler (çekirdeğin biçimi): (kelime_1, son_unlusu_ayni, kelime_2), (kelime_1, son_hecesi_ayni, kelime_2), (kelime_1, kafiyeli, kelime_2).
- Öğrenilecek kural örneği: "son_hecesi_ayni(X,Y) → kafiyeli(X,Y)".
- Bu ilişki adları yalnız örnektir; şema ve tanımlar kullanıcı onayıyla gelir.

## m) Noisy-OR yedek kural testi (taslak; testler/ altına eklenmedi)

- **Soru:** Aynı bilgiyi taşıyan "yedek" kurallar ya da gözlemler, plazma hücresinde güveni şişiriyor mu?
- **Bugünkü durum (K-018):** plazma, aynı sonuca giden ispatları kök kümelerine göre gruplar. Kök kümesi kesişenler aynı bileşendir; bileşen içinde en büyük güven alınır, bileşenler arasında noisy-OR. Yani aynı olgulara dayanan iki kural güveni şişirmemeli.
- **Açık risk:** mantıksal olarak aynı bilgiyi taşıyan iki ayrı olgu. Ör. "Y, X'in babası" ve "X, Y'nin oğlu" ikisi de gözlenmişse kök kümeleri ayrık olur ve noisy-OR iki bağımsız kanıt gibi birleştirir.
  - Olgu güveni 1,0 olduğunda bu görünmez (güven zaten 1'de doyar). Güven 1'in altındaysa görünür: 0,6 ile 0,6 → 0,84.

**Taslak test** (eşikler değiştirilmez; yalnız ölçer):

```python
class NoisyOrYedekTesti(t3.Ortam):
    def test_ayni_koklu_yedek_kural_guveni_sisirmez(self):
        # iki eşdeğer kural, aynı olgulardan aynı sonucu türetir -> tek bileşen -> güven tek kuralınkiyle aynı
        tek = self.cevap(self.kos(OLGULAR_06, K1, sorgu=S), S).guven
        cift = self.cevap(self.kos(OLGULAR_06, K1, K1_ESDEGER, sorgu=S), S).guven
        self.assertEqual(cift, tek)

    def test_ters_olgu_bagimsiz_kanit_sayiliyor_mu(self):
        # aynı bilgiyi taşıyan ters olgu eklenince güven artıyor mu? (beklenen bugün: artar; ölçülüp raporlanır)
        tek = self.cevap(self.kos(OLGULAR_06, K1, K_TERS, sorgu=S), S).guven
        ters_eklenmis = self.cevap(self.kos(OLGULAR_06 + TERS_OLGU_06, K1, K_TERS, sorgu=S), S).guven
        self.olc("ters_olgu_sisirmesi", tek, ters_eklenmis)

    def test_yedek_kural_sayisiyla_guven(self):
        # k = 1..5 yedek kural, her biri ayrık ama ilişkili olgulardan -> güvenin k ile değişimi tabloya yazılır
        ...
```

- **Önerilecek ölçüt (karar değil):** mantıksal olarak aynı bilgiyi taşıyan olgular (şemadaki ters listesiyle eşleşen çiftler) tek kanıt sayılmalı. Bu, plazmanın bileşen tanımında bir değişiklik olur; K-018'e dokunduğu için kullanıcı kararıdır.

## Tartışmada kullanıcı kararı gerektirecek noktalar (şimdi sorulmuyor)

1. Kabul ölçütünün K-036'daki geçici eşiklerden Wilson alt sınırına ve sahte havuzdan kestirilen eşiğe geçmesi (kalibrasyon).
2. Sızıntı tablosundaki hangi ön bilginin H2'de verili kalacağı (kâhin ve veri olarak dil).
3. Ters olguların tek kanıt sayılması (m; güven, K-018).
