# H2 tasarımı (nihai öneri; yalnız belge, kod yok)

**Durum:** NİHAİ TASARIM, 2026-10-26. **Kapı 0 onaylandı (K-041):** altı soruya evet; sembolik ön eleme + HRR çekirdeği son hakem; A6 bağımsız incelemesi Kapı 2'den önce. B0 başladı.

**Kaynaklar:**
- `H2_ORTAK_TASARIM_v1.md` (v1): kullanıcı iletti, depoda değil.
- `H2_TASARIM_TASLAGI.md`: kodlayıcının ilk taslağı.
- Mevcut kod ve DNA v8 (`veri/dna/akrabalik_dna_v8.json`, 244 kural).
- Ön kayıt taslağı: `ONKAYIT_H2_TASLAK.md` (ÖK-005 taslağı). **Bütün eşiklerin tek kaynağı oradaki tablodur (§4).**

**sistem.md bağı:**
- §13: H2 = klonal seçilim kuralı sıfırdan buluyor mu.
- §7–§9: öğrenme, kredi, müdahale.
- §10: ezber önleme.
- §16: bağımsızlık kanıtı.

**Yazım kuralı:** v1'e sadık. Her sapma "S-n" ile işaretli ve §11'de gerekçeli. Sessiz değişiklik yok.

**Nasıl hesaplandı:**
- Kâğıt üstü sayılar için depoda olmayan küçük sayma betikleri çalıştı. Saydıkları: DNA v8'in yalnız biçimi, şablon ailesinin aday sayısı, şemanın ad değişimleri.
- Çekirdek, üreteç ve deney koşmadı. `uretec_cevaplari.jsonl` ve `degerlendirme/altin/` açılmadı.
- Aday sayısı ikinci bir yoldan, depodaki `kanonik_bicim` ile doğrulandı: K5/7 için iki yolda da 693.833 (OI'li 1.322.209).

## 1. Amaç (v1 §1, aynen)

H1'de sistem, elle yazılmış 244 kuralı (DNA v8) kullanarak akrabalık sorularını 0 yanlışla cevapladı. H2'nin sorusu: **sistem bu kuralları, kimse söylemeden, kendisi bulup güvenle kabul edebilir mi?** — hem de bulduğu kuralın "sahte kısayol" (örn. kelime/ad sıklığı hilesi) olmadığından emin olarak.
H2'nin iddiası "yeni bir kural öğrenme yöntemi" DEĞİL (AMIE/ILP/Popper benzerleri var). İddia: **etiketsiz, kâhinsiz, kendini sınayan ve denetlenebilir bir kabul geçidi.**
"Genel zekâ" sözü H2'de KULLANILMAZ. Söz: "alan-bağımsız, denetlenebilir kural keşfi". Genel zekâya giden kapılar (yüklem icadı, bileşim, aktarım, merak) arayüz olarak açık bırakılır ve ölçülür; iddia edilmez.

## 2. Sözlük

v1 §2 sözlüğü geçerlidir. Altı tanımın kodlanabilir biçimi ÖK-005 taslağı §13'tedir; aynı metin burada da kullanılır.

**Bu belgenin eklediği terimler:**

- **Sembolik değerlendirici:** kuralları olgular üzerinde tam sayılarla, hatasız sayan araç. M0, aşama 1–4, null ve boş dünya bununla çalışır. Çekirdek (HRR) değildir.
- **Çekirdek geçidi:** A6 bellek geçidi (K-035, K-037). Aşama 5'te, sembolik süzgeçten geçen adaylar için çalışır.
- **Tipli şablon ailesi T:**
  - en çok 3 halka, en çok 4 değişken, bağlı gövde;
  - iki ucu aynı değişken olan halka yok;
  - "hepsi farklı kişi" (OI) bayrağı;
  - gövde ve baş sözlüğü: şemanın 21 ilişkisi.
  - Kademeleri K1–K5 (§6.1).
- **A1, A2, A3:** B2'nin üç akrabalık dünya ailesi (§5).
- **Ters-dayanaklı aday:** gövdesinde, baş çiftini (X ile Y'yi) doğrudan bağlayan halka olan aday. DNA v8'de 81 tane.
- **Şemadan okunabilir kural:** tek halkalı, gövdesi başın şemadaki tersi ya da simetriği olan kural. DNA v8'de 9 tane.
- **Kapalı dünya:** gözlem bölümü, seçilen kişiler arasındaki bütün doğru olguları içerir (V-057). Yazılmamış bir çift ilişkisizdir.
- **Bölüm-düzeyi Wilson:** küme = gözlem bölümü. Kanıtlı bölüm = adayın en az bir tanığı olan bölüm. Başarılı bölüm = içinde yanlış olmayan bölüm.
- **Kapanış geri bulma:** maskelenmiş türetilmiş olgulardan, kabul kümesinin yeniden türettiklerinin oranı. Elle yazılmış kural kümesi gerektirmez.

## 3. Karşılaştırma: v1 ↔ taslak ↔ kod ve DNA v8

### 3.1 Zaten yapılmış

1. **Kanonik biçim:** `cekirdek/bellek_gecidi.py` `kanonik_bicim`. Değişken adı ve halka sırasından bağımsızdır, `farkli` çiftleri dahil. Kanonik kimlik bunun özetidir.
2. **Bellek deposu (V-056, K-036):** sadece-ekleme, hash zincirli, geri alma olaylı. Susturma için altyapıdır; silme yoktur.
3. **Maskeli geçit (K-035, K-037):**
   - Aday kendi kanıtını onaylayamaz.
   - Müdahale puanı b·c'dir.
   - En kötü ortam esas alınır (grup-DRO).
   - Doğruluk çekirdek dışında hesaplanır (`gozlem_puani`).
4. **Gözlem bölümleri (V-057):** seçilen kişiler arasındaki bütün ilişkiler. Ortam ayrımı var (olağan / kaydırılmış zincir uzunluğu).
5. **Anlatıcı (LLM) karardan sonra çağrılır;** karar vermez. Bağımsızlık testi var.
6. **İstatistik:** Clopper–Pearson ve bootstrap (`degerlendirme/istatistik.py`).
7. **Ön kayıt ve kilitler:**
   - Ön kayıt hash denetimi (`on_kayit_denetle`).
   - Dosya kilitleri (`araclar/kilitle.py`).
   - Kilitli küme kesişim denetimi (`kilitli_kumeler.py`).
   - Onaylı tohum değişimi kaydı (K-039).
8. **Kod mutasyon sınaması:** `araclar/mutasyon_*.py`. Bu, v1'in "geçidin mutant skoru"ndan farklıdır: orada mutant bir kuraldır.
9. **H2 kapısı idari olarak açık (K-040).**

### 3.2 Koda uymayan (B0–B3'te yapılacak ya da v1 varsayımı kodla uyuşmuyor)

1. M0, aday üretici ve sembolik değerlendirici yok. DNA elle yazılmıştı.
2. Tek dünya üreticisi var (`Dunya.uret`). İkinci bağımsız üretici, Z12, Hawaii, Iroquois ve Omaha dünyaları yok.
3. **Üreteçte "evlilik yaşı" yok.** Yaş kavramı yoktur.
   - Kaydırılabilen parametreler: nesil sayısı, çocuk aralığı.
   - Evlilik oranı için yeni bir parametre gerekir. Bugün son nesil dışındaki herkes dışarıdan biriyle evlenir. (S-8)
4. **Hüküm ayrıntılı dönüyor:** bugünkü geçit (`HatSonucu`) ölçüm ve neden döndürüyor.
   - v1'e göre önericiye yalnız KABUL, RET ya da BİLMİYORUM döner.
   - Ayrıntılar yalnız denetçi kanalına yazılır.
5. Kümeli Wilson, Westfall–Young, derece-koruyan yeniden bağlama ve Thresholdout yok.
6. Çekirdek kod özeti (dondurma sözleşmesi) yok. Yalnız config, test ve veri kilidi var.
7. **"Tipli" şablonun kestiği bir şey yok.** Şemada argüman türü yoktur.
   - Akrabalıkta tek tür vardır (kişi), Z12'de de tek tür (eleman). Tip budaması 0 aday keser.
   - Tip yalnız ileride çok türlü alanlar için bir arayüzdür.
8. **Bu ortamda GPU yok:** 4 CPU çekirdeği ve 15 GB bellek var.
   - Bulut kabında arka plan işi en çok 2 saat sürer. Uzun koşular kaldığı yerden devam edebilmelidir. (S-13)
9. **"Mevcut akrabalık = Eskimo tipi" etiketi tam doğru değil:**
   - amca/dayı/hala/teyze ayrımı Sudan tipine yakın;
   - tek "kuzen" terimi Eskimo tipine yakın.
   - Etiket önerisi: "mevcut (Türkçe)". (S-15)

### 3.3 İmkânsız ya da çelişkili (ve çözüm)

1. **M0 uzayı (v1 "~30–124 bin"):**
   - **Eski sayım hatalıydı:** taslaktaki 124.068 baş yönünü iki kez saydı. Doğrusu 7 temel ilişki, zincir, ≤3 halka (K4/7) için 62.027.
   - **Bu uzay DNA v8'in yalnız 118/244 kuralının biçimini içerir** (%48). B2b'nin %90 eşiği bu uzayla tanım gereği tutmaz.
   - En geniş temel-sözlüklü uzay (K5/7) bile 202/244'tür (%83).
   - 244/244 biçim kapsamı yalnız K5/21'de vardır (≤3 halka, bağlı gövde, sarkan değişken serbest, 21 ilişki): 18.652.809 kural, OI ile 35.544.873. (S-1)
2. **"Şablon ailesi DNA'yı görmeden üretilir" koşulu kodlayıcı için sağlanamaz.**
   - Kodlayıcı DNA'yı görmüştür.
   - ≤3 halka sınırı, DNA biçiminin kendi sınırıdır (`dna_v2` en çok 3 halka).
   - Telafi: aile, v1'in sınırı ile şemanın bütün sözlüğünden mekanik olarak tanımlandı (en genel seçim). Sızıntı tablosuna yazıldı. Sıfır-şablon kolu ve şablon bütçesi eğrisi ölçer.
3. **Yol-kesme maskesi aynen uygulanamaz.**
   - v1 aşama 3, maskelenen olgunun ters ve simetrik kenarlarını da maskeler.
   - DNA v8'in 81 kuralının gövdesinde baş çiftini doğrudan bağlayan halka vardır, ve bu halka hep başın tersidir: 9 tek halkalı, 72 çok halkalı (ör. "Y, X'in kızı ve X bir erkeğin kardeşi ise X, Y'nin babası").
   - Ters maskelenince bu kurallar hiç kanıt bulamaz; B2b'nin tavanı 163/244 = %66,8 olur.
   - Çözüm: maske, gövdesi baş çiftine dokunmayan adaylara uygulanır. Bu, eş üzerinden geri dönen kısa devreleri kapatır. Ters-dayanaklı adaylar maskesiz sınanır ve ayrı raporlanır. (S-4)
4. **Mühürlü final havuzu "tek atış" ile "12 tur sorgu" bağdaşmaz.**
   - Aşama 5 sorguları final havuzuna giderse havuz tek atış olmaz.
   - Çözüm: aşama 5, önkayıtlı tohum akışından gelen yenilenebilir taze dünyalarla çalışır; her taze dünya bir turda yanar. 24'lük final yalnız B2b ölçümünde bir kez açılır. (S-3)
5. **Çekirdekle (HRR) yapılamayanlar:**
   - Westfall–Young, B = 10.000: tur başına 200 aday × 10.000 × ~22 s.
   - 100 boş koşu.
   - B3 kesişim eğrisi: 505 koşu.
   - Çözüm: bunlar sembolik değerlendiriciyle yapılır. Çekirdek yalnız aşama 5'te, sembolik süzgeçten geçenlere çalışır. Çekirdek ile sembolik sayaç aynı adayda ayrışırsa hüküm BİLMİYORUM'dur (uyum şartı). (S-2, S-19)
6. **"Kapsam ≥2 aile" ile Hawaii, Iroquois ve Omaha birlikte olmaz.**
   - DNA v8 kuralları yalnız mevcut terim sisteminde doğrudur. Hawaii'de "kuzen" yoktur. Iroquois'de babanın erkek kardeşi de "baba"dır; "baba tek kişi" şema kuralı bozulur.
   - Bu dünyalar B2'nin kapsam ailesi olamaz. Her biri kendi şeması ve kendi kapanış ölçüsüyle bir B3 aktarım dünyasıdır.
   - B2 kapsam aileleri, mevcut terim sisteminin üç ailesidir: A1, A2, A3. (S-6)
7. **"Etkin n ≈ aile sayısı" kural başına uygulanamaz.**
   - Bu kural, kural başına kümeli Wilson'a uygulanırsa (3 aile) alt sınır en çok 3/(3 + 1,96²) = %44 olur. %85'e hiçbir kural ulaşamaz.
   - Çözüm, kullanıma göre küme:

     | Kullanım | Küme |
     |---|---|
     | Kural başına kabul | gözlem bölümü |
     | B2 kapısı | sonuç ilişkisi (21 küme) |
     | Aile | yalnız kapsam ve veto |

     (S-5)
8. **Kural başına kabul eşiği v1 tablosunda yok.**
   - Tabloda yalnız toplu B2 kapısı ve yanlış kabul var.
   - Eklendi: doğruluk 1,0 (gürültüsüz dünya) VE bölüm-düzeyi Wilson alt sınırı ≥ τ (K, başlangıç 0,85). (S-10)
9. **Aşırı genel kurallar bugünkü geçitte cezasız kalabilir.**
   - K-035'te "yanlış", görünür bir olguyla şema çelişkisidir. Aradaki ilişki şemada olmayan bir çift için yapılan tahmin hiç sayılmaz.
   - Örnek: kuzenin kuzenini "kuzen" sayan bir kural, ilişkisiz (ör. ikinci derece) çiftlerde cezasız kalır.
   - Çözüm: kapalı dünya (bölüm bütün ilişkileri içerir, V-057). Yazılmamış çift için tahmin = yanlış.
   - Bu, V-057'nin (kodlayıcı kararı) kapsamındadır; V-059'a yazıldı. (S-9)
10. **Ters-çift "bijeksiyonu" bire-bir değil.**
    - Şemada ters listesi bire-çoktur (baba → oğul, kız). "r↔ters(r)" eşlemesi bijeksiyon değildir.
    - Kodlanabilir karşılığı şema otomorfizmidir: 1536 tane, temel ilişkiler temele gider. (S-7)
11. **Z12 dünyaları birbirinin yeniden adlandırmasıdır.**
    - Z12 tek bir yapıdır, "16/24/8 bağımsız dünya" Z12'de bağımsız değildir.
    - Z aileleri n'ye ve üreticiye göre ayrılır: Z12-a, Z12-b (ikinci üretici), Z24. (S-16)
12. **Şemadan okunabilir kurallar boş dünyada da doğrudur.**
    - Bu 9 kural yalnız tersi ya da simetriği okur. Boş dünya şemayı koruduğu için orada da doğru çıkarlar ve sayaç her koşuda alarm verirdi.
    - Bu kurallar ayrı sınıftır ve boş-dünya sayacına girmez. B2'de ikinci payda 235'tir. (S-14)
13. **"Gizli" mutant türlerini geçidi yazan kodlayıcı yazarsa gizli olmaz.**
    - Çözüm: gizli aileleri danışman ya da kullanıcı yazar; kodlayıcı açmaz (altın küme gibi). (S-18)
14. **Rastgele gözlem bölümüyle nadir kurallara kanıt yetmez.**
    - A6'da, ortam başına 8 rastgele bölümde 244 kuralın 46'sının gövdesi hiç eşleşmedi; 84'ünde bir ortamda kanıt 3'ün altındaydı.
    - τ = 0,85 kural başına en az 22 kanıtlı bölüm ister. 48 rastgele bölümde nadir kurallar buna ulaşamaz.
    - Öneri: gövde-merkezli bölüm. Geçit, dünyadan adayın gövdesinin rastgele bir eşleşmesinin çevresini ister; maskeli cevap yine gizlidir. Kullanıcı sorusu 2.

## 4. Mimari

### 4.1 Aday üretimi

- **Şablon ailesi (üretimde):** K5/21, 35.544.873 aday (OI bayraklı).
  - Tanımı ÖK-005 §6'da. B0'da dosyaya yazılır ve hash'lenir.
  - Kodlayıcının DNA bilgisi sızıntı tablosundadır. Kademeler K1–K5 eğri içindir.
- **M0:** sembolik değerlendiriciyle bütün uzayı sayar. Geliştirme havuzunda her aday için şunlar hesaplanır:
  - tanık sayısı (aynı üçlü bir kez);
  - kapalı dünya güveni;
  - işlevsel başlarda PCA paydası.
- **M0 süzgeci:** geliştirme havuzunda yanlış 0 VE tanık ≥ 3.
- **M0 sırası:** tanık sayısı azalan, halka sayısı artan, kanonik kimlik artan. Kesin ve tekrarlanabilir.
- **Kollar (B3; eşit süreç-saniyesi):**
  - M0;
  - M0 + sıralı budama;
  - rastgele örnekleme;
  - rastgele mutasyon;
  - mutasyon + klonal (+ çaprazlama);
  - sıfır-şablon: ≤4 halka, ≤5 değişken, bağlılık şartı yok, OI yok, rastgele örnekleme.
- **Mutasyon işleçleri:** bir ilişki adını değiştir, halka ekle ya da sil, değişken bağla ya da ayır, yön çevir, OI aç ya da kapat.
- **Klonal seçilim (sistem.md §7):** uygunluk = geliştirme havuzundaki tanık × güven. Klonlanır; mutasyon oranı uygunlukla ters orantılıdır.
- **Mutasyonun yeri:** yalnız kesişim eğrisinde (054; 20 eşleşmiş tohum × 5 bütçe) M0'ı yenerse kalır. Yenemezse "gereksiz" yazılır; bu da başarıdır.

### 4.2 Kabul protokolü (ucuzdan pahalıya; hepsi geçmeden kabul yok)

Aşama 1–4 geliştirme havuzunda sembolik değerlendiriciyle çalışır. Aşama 5 taze dünyalarda önce sembolik, sonra çekirdekle çalışır. Önericiye yalnız üç değerli hüküm döner.

1. **Yol bağımsızlığı (kongrüans):** aynı çifte iki yoldan iki farklı terim çıkamaz.
   - Adayın tahmini (A,r,B) ile görünür (A,r',B), r ≠ r' aynı dışlayıcı grupta → ihlal.
   - Eşik: 0 ihlal.
2. **Kök silme + ratio/obiter:** her halka için, halka çıkarılmış kural aynı havuzda ölçülür (bağlı kalıyorsa ve X ile Y'yi içeriyorsa).
   - Halka çıkarılınca hâlâ 0 ihlal ve en az aynı tanık varsa → o halka obiterdir.
   - Aday şüphelidir ve aşama 5'e gitmez; yerine indirgenmiş kural sıraya girer.
   - Kalan halkalar ratio'dur. Örnek: cinsiyet tanığı halka ratio'dur, çıkarılınca kural yanlışlanır.
3. **Karşı-örnek + yol-kesme + işlevsellik:**
   - İşlevsel ilişkide ikinci değer → ihlal.
   - Ters tutarsızlık → ihlal.
   - Kapalı dünyada yazılmamış çift → yanlış.
   - Gövdesi baş çiftine dokunmayan adayda maskelenen olgunun tersleri de maskelenir (S-4).
   - Eşik: 0 ihlal; maskeyle de tanık ≥ 3.
4. **Veto dünyaları.** Reddedebilir, kabul ettiremez. Tek ailenin vetosu RET değil BİLMİYORUM yapar; RET için en az iki aile gerekir.
   - **Ad-permütasyon ikizi:** ters-çift koruyan bijeksiyon π, mühürlü tohumla seçilir. Koşul: hüküm(π(k), π(d)) = hüküm(k, d). Değilse BİLMİYORUM; bu, çekirdeğin ada bağlı artefaktını yakalar.
   - **Derece-koruyan yeniden bağlanmış ikiz:** yalnız baş ilişkisi yeniden bağlanır, tersleri yeniden yazılmaz. Adayın orada da ≥3 tanığı ve 0 yanlışı varsa dereceden gelen kısayoldur → BİLMİYORUM.
   - **Karşı-model dünyalar:** A3, yani ikinci üretici. A2 de veto ailesi sayılır. Herhangi bir ailede yanlış > 0 → o aile veto eder.
5. **Taze-dünya doğrulama (mühürlü akış):** aday başına bir turda 6 taze dünya (A1, A2, A3'ten ikişer), her dünyada 8 gözlem bölümü.
   - Sembolik ön adım:
     - yanlış = 0;
     - bölüm-düzeyi Wilson alt sınırı ≥ τ;
     - Westfall–Young düzeltilmiş p ≤ %1/12 (tur başına);
     - kapsam ≥ 2 aile (her birinde ≥3 tanık).
   - Çekirdek adımı: maskeli bellek geçidi (K-035), müdahale b·c ≥ eşik (K-037), çekirdek ile sembolik sayımın uyumu.
   - Thresholdout yalnız Wilson istatistiğine uygulanır; yanlış = 0 vetosu gürültüsüzdür.

**Kapsam tabanı:**
- Her kabul edilen kural ≥2 ailede destek gösterir. Kapsamı geçit hesaplar; adayın kapsam alanı olamaz.
- "Bilmiyorum" üst sınırı %10'dur (final havuzunda kapanış ölçüsü). H1'in "0 yanlış"ı kapsamla birlikte raporlanır.

**Sürekli denetimler:**
- boş-dünya sayacı (şemadan okunabilir sınıf hariç);
- Goodhart makası (kontrol havuzu, kapanış ölçüsü);
- kırmızı takım + geçidin mutant skoru.

**Yedeklilik:**
- Kanonik kimlik + tanık kümesi + tabu testi.
- Geliştirme havuzunda, tanıklarının hepsi kabul edilmiş kurallarca zaten türetilen aday "uyutulur" ve sorgu bütçesi harcamaz.
- Kabulden sonra çıkarılınca hiçbir hüküm değişmeyen kural da uyutulur.
- Uyutulan kural geri bulma sayımında "fazlalık-doğru" sınıfında görünür.

**Kabul sonrası:**
- Susturma ve karantina var; silme yok.
- Geri çağırma yalnız taze kanıtla olur ve sorgu bütçesinden düşer.
- K-037 koşulu: H2'de bozuk bir kural kabul edilirse müdahale formülü kararı yeniden açılır.

### 4.3 Sızıntı muhasebesi

- **Üç havuz (B2, akrabalık):**
  - geliştirme 16 (A1 6, A2 5, A3 5): kalibrasyon serbest;
  - mühürlü final 24 (8/8/8): tek atış;
  - kontrol 8 (3/3/2): hiç sorgulanmaz, yalnız makas.
- **Sorgu birimi:** (aday, taze dünya). Turda ≤200 aday, ≤12 tur.
  - Önkayıtlı tek anahtar: geliştirme havuzunda ölçülen talep 2400'ü aşarsa turda 400 (S-17).
  - Grup sorgusu yasak.
- **Arama basıncı:** üretimdeki basınç, sahte kabulün başladığı basıncın (P\*, B1'de ölçülür) yarısını aşmaz.
- **Thresholdout:** T = 0,04, σ = 0,01, Laplace gürültüsü (K).
  - B2b'de M0 sabit sırayla önerdiği için uyarlamalılık yoktur. Thresholdout asıl B3'ün uyarlamalı kollarında iş görür (S-20).
- **Taze dünyalar:** tohum türetme kuralı önkayıtta mühürlüdür. Her taze dünya defterde ve sızıntı tablosunda kayıtlıdır. Kodlayıcı taze dünya içeriğini açmaz.
- **Ret raporu ve zor-durum arşivi** arama döngüsüne girmez.

### 4.4 Aktarım (H2 içinde)

- **Çekirdek dondurma sözleşmesi:**
  - Çekirdek kod özeti B0 sonunda mühürlenir.
  - Hiperparametreler H1 değerleridir: tur 8, havuz 128, bütçe 1024, hücre yazma 8.
  - Alan başına değişenler: yalnız üçlü dosyası, ilişki şeması ve şablon kademesi.
- **Dünyalar:**
  - akrabalık-mevcut: A1–A3 ve ad-permütasyon ikizleri;
  - Z12/mod-n: Z12-a, Z12-b, Z24 (B3);
  - Hawaii, Iroquois, Omaha: B3, isteğe bağlı, tanımları kullanıcı ya da danışman onaylar; kullanıcı sorusu 5.
- **Ölçü:** B3 dünyalarında ölçü, kapanış geri bulmadır. Elle yazılmış kural kümesi gerekmez; LLM kural ya da şema seçmez.
- **Şablon bütçesi eğrisi (088):**
  - 5 kademe: K5, K4, K3, K2, K1.
  - "Düz" = 3 kademe geri çekilince (K5 → K2) kayıp ≤5 puan, TOST ±5 puan ile, 3 dünya ailesinde (akrabalık, akrabalık-permüte, Z12).
  - K3 ile K4 iç içe değildir; sıralama boyuta göredir.
- **Dürüst notlar:**
  - Z12 aynı tipli üçlü şablonu kullandığı için zayıf aktarım kanıtıdır (v1).
  - K2'nin DNA biçim kapsamı 128/244'tür. Akrabalıkta eğrinin düz çıkması beklenmez; çıkmazsa "şablon ön bilgisi önemli" diye yazılır.

### 4.5 Menteşeler (H3'e açık kapılar; H2'de yalnız ucuz arayüz)

- **Tek aday şeması:** her aday şu alanlarla tutulur: baş, gövde, kaynak (kol ve tohum), tanık kümesi özeti, sürüm. İleride yüklem = başı yeni ad olan aday.
- **Terfi deneyi (B3, isteğe bağlı):**
  - Kabul edilmiş bir kuralın gövdesi tanık kümesiyle yeni bir türetilmiş ilişki olarak sözlüğe girer. M0 aynı kodla ikinci tur çalışır.
  - Ölçü: 4–5 halkalı zincir eşdeğeri gövdelerin kapanış geri bulmaya katkısı. Terfi açık ve kapalı karşılaştırılır.
  - Eşik yok, yalnız ölçüm.
- **Neden grafı:** her kabulün gerekçe zinciri defterde pasif tutulur.
- **MK-lite:** çıkmaz günlüğü, ret raporu, zor-durum arşivi. Hepsi pasiftir (kullanıcı kararı 5).
- **H3'e kalanlar:** tam yüklem icadı, merak sıralaması, ses/kafiye (kullanıcı kararı 4), çevirmen, uyku/konsolidasyon, A7, zevk katmanı.

## 5. Dünyalar ve aileler (özet; tam liste, şemalar ve parametreler ÖK-005 §2)

| Etiket | Ne | Rol |
|---|---|---|
| A1 akrabalık-mevcut | Bugünkü üretici: 4 nesil, 2–4 çocuk, son nesil dışında herkes dışarıdan evlenir; ortalama 53 kişi (22–106) | B2 kapsam ailesi |
| A2 akrabalık-kaydırılmış | Aynı üretici: 5 nesil, 1–4 çocuk, evlilik oranı 0,8 (yeni parametre); ortalama ≈53,5 kişi | B2 kapsam ve veto ailesi |
| A3 akrabalık-ikinci-üretici | Ayrı kod (≤300 satır): 3 ayrı soy, soylar arası evlilik, çocuk 0–4, evlilik 0,8 | B2 kapsam ve karşı-model ailesi |
| π-ikiz, yeniden bağlı ikiz | Türetilmiş dünyalar | Veto (aile değil) |
| Boş dünya | Her ters sınıfı bağımsız, şemayı koruyarak yeniden bağlanmış | Boş-dünya sayacı |
| Z12-a, Z12-b, Z24 | Saat aritmetiği (10 ilişki) | B3 aktarım |
| H, I, O | Hawaii, Iroquois, Omaha terim sistemleri (aynı soy ağacı, başka adlandırma) | B3, isteğe bağlı |

## 6. Kâğıt üstü hesaplar

### 6.1 Aday uzayı (kanonik kimlik sayısı)

**Sayım kuralları:**
- Baş: şemanın 21 ilişkisinden biri, X'ten Y'ye. Başın yönü değişken adlandırmasına katılır; iki kez sayılmaz.
- Tek halkalı gövde başla aynıysa atıldı.
- OI bayrağı yalnız bitişik olmayan bir değişken çifti olan gövdelerde ayrı aday sayılır.

| Kademe | 7 temel ilişkili gövde: gövde / kural / OI'li | 21 ilişkili gövde: gövde / kural / OI'li | DNA v8 biçim kapsamı (7 / 21) |
|---|---|---|---|
| K1 tek halka | 14 / 287 / 287 | 42 / 861 / 861 | 1 / 9 |
| K2 ≤2 halka zincir | 210 / 4.403 / 8.519 | 1.806 / 37.905 / 74.949 | 86 / 128 |
| K3 ≤2 halka genel | 693 / 14.259 / 26.411 | 6.195 / 127.449 / 236.817 | 122 / 164 |
| K4 ≤3 halka zincir | 2.954 / 62.027 / 123.767 | 75.894 / 1.593.753 / 3.186.645 | 118 / 160 |
| **K5 ≤3 halka genel (T)** | 33.593 / 693.833 / 1.322.209 | **903.203 / 18.652.809 / 35.544.873** | 202 / **244** |

**Denetim:**
- Zincir satırları kapalı biçimle tutar: K4/7 gövde = 14 + 14² + 14³ = 2954; kural = 2954·21 − 7.
- K5/7, depodaki `kanonik_bicim` ile ikinci kez sayıldı; aynı çıktı.

**DNA v8 biçimi:**
- halka sayısı: 1 halka 9, 2 halka 155, 3 halka 80;
- değişken: en çok 4;
- gövdesi yalnız 7 temel ilişkili: 202 (42'sinde türetilmiş ilişki var);
- zincir 160, bir sarkan değişkenli 84 (ör. cinsiyet tanığı);
- `farkli` şartlı 28: 24'ü baş çiftinde, 4'ü başka çiftte. T'de OI bayrağıyla karşılanır; anlamca birebir aynı olmayabilir, sınıflamada "daha genel" ya da "kapanış-eşdeğer"e düşebilir.

**Sonuç:** üretimde K5/21 kullanılır. Gerekçe "DNA'yı kapsasın" değil, v1'in "genel Horn ≤3" tanımıdır. Kapsam sayısı yalnız yapılabilirlik denetimidir.

### 6.2 M0 süresi ve belleği

**Dünya büyüklüğü (üreteç kodundan):** A1'de en az 22, beklenen 53, en çok 106 kişi.

**Bir dünyada iş:**
- G ≈ 1,7 milyon gövde değerlendirmesi: 903.203 gövde, OI'li varyantlarla.
- Gövde matrislerinin ara çarpımları: U ≈ 7,6·10⁴ (42² + 42³).
- Destek sayımı: gövde matrisi × 21 baş matrisi.

**İşlem (FLOP):**
- Destek ≈ G·21·N²·2 ≈ 2,0·10¹¹.
- Çarpımlar ≈ U·2N³ ≈ 2,3·10¹⁰.
- Toplam: ortalama dünyada ≈ 2,2·10¹¹. 16 geliştirme dünyasında boy dağılımıyla ≈ (4–10)·10¹².

**Süre (4 çekirdek, float32 matris çarpımı, etkin 10–50 GFLOP/s):**
- 1,5–17 dakika.
- OI için içerme-dışlama ×1,5–2.
- Alt uç, Python ve parçalama ek yükü için yukarı çekildi.
- **M0 tek koşu ≈ 5–35 dakika; üç bit-aynı koşu ≈ 15–105 dakika.**

**Bellek:**
- Dünya tensörü ≤ 1 MB.
- Gövde blokları 20–50 bin gövdelik parçalarla ≤ 2,5 GB.
- Sonuç tablosu ≈ 200 MB.
- **Tepe ≤ 3 GB** (makinede 15 GB).

**Bit-aynılık:** 2²⁴'ün altındaki tam sayı toplamları float32'de kesindir, sıraya bağlı değildir. Çekirdek sayısı da sabitlenir.

**Çekirdekle karşılaştırma:**
- Aynı uzayı çekirdek geçidinden geçirmek ≈ 35,5·10⁶ aday × 16 bölüm × 2,8 s ≈ 1,6·10⁹ süreç-saniyesi ≈ 50 CPU-yılı. Bu imkânsızdır.
- Bu yüzden M0 sembolik sayar.
- Taban: 7 temel ilişkili zincir uzayı (K4/7) saniyeler sürer, K5/7 bir dakikanın altındadır.

### 6.3 Sorgu aritmetiği (B1, B2)

**Ölçülmüş çekirdek geçidi maliyeti:**
- A6 gösterimi: 356 kural × 16 bölüm, 88 dk × 3 süreç → 44,5 s/kural → 2,8 s/(kural, bölüm), bellek boşken.
- Bellek doluyken her maske iki koşu → ≈5,6 s.

**Hesap:**
- (aday, dünya) çifti, 8 bölüm: 22–45 süreç-saniyesi.
- Bir tur: 200 aday × 6 dünya = 1200 çift → 7,3–15 süreç-saati → 4 süreçle **1,8–3,8 saat**.
- 12 tur, en kötü durum (2400 adayın hepsi çekirdeğe): **22–45 saat**.
- Beklenen durum: çekirdek yalnız sembolik süzgeçten geçenlere çalışır; kaba tahmin 300–1000 aday → **3–19 saat**.

**Sembolik yük:**
- Westfall–Young (tur başına 200 aday × 48 bölüm × 10.000 yeniden bağlama ≈ 10⁸ küçük değerlendirme): ≈ 16–80 süreç-dakikası/tur. Tutar.

**B1 tutuyor mu: evet.**
- 320 mutant = 2 tur (≈11,7 süreç-saati, ≈3 saat).
- P\* ölçümü ayrı tohum akışında: 4800 boş aday, sembolik süzgeçte elenir.
- Kalibrasyon geliştirme havuzundadır ve bütçeden düşmez.

**B2b: sınırda, kâğıt üstünde kesin değil.**
- **Talep C:** geliştirme havuzunda M0 süzgecini ve aşama 1–4'ü geçen, uyutulmamış aday sayısı.
- **Alt sınır:** 244 hedefin bir kısmı kendi aralarında yedektir.
- **Kaba üst tahmin:** her baş ilişkisi için 50–150 en küçük doğru gövde → 1000–3000. Bunlara DNA'da olmayan doğru kurallar da dahil ("farklı-doğru").
- **Gerekli isabet:** 2400 yerde 220 hedef için aşama 5'e girenlerin en az %9'u hedef (ya da kapanış-eşdeğeri) olmalı.

**Öneri (S-17):**
1. Geliştirme havuzunda yedeklilik aşama 5'ten önce uygulansın (bütçe harcamadan uyutma).
2. Önkayıtlı tek anahtar; B1 sonunda, DNA'ya bakılmadan ölçülen C'ye göre:

   | C | Turda aday |
   |---|---|
   | C ≤ 2400 | 200 |
   | 2400 < C ≤ 4800 | 400 |
   | C > 4800 | 400; fazlası "bütçede sınanmadı" diye raporlanır |

   12 tur değişmez.
3. Üst sınır: tur başına aday ≤ ⌊P\*/2/12⌋. P\* daha küçükse o geçerlidir ve raporlanır.
4. **Kanıt gücü:** rastgele bölümle nadir kurallar τ'nun istediği 22 kanıtlı bölüme ulaşamaz (§3.3 madde 14).
   - Gövde-merkezli bölüm onaylanırsa her bölüm ≥1 kanıt taşır.
   - Onaylanmazsa dünya başına bölüm 8 → 32 olur (maliyet ×4, B2b ≈ 4 gün) ve nadir kurallar yine "bilmiyorum" kalabilir.

### 6.4 İstatistik eşiklerinin aritmetiği

**Kural başına Wilson (hepsi doğru, n kanıtlı bölüm):** alt sınır = n/(n + 1,96²).

| n | 3 | 6 | 16 | 22 | 35 | 48 |
|---|---|---|---|---|---|---|
| Alt sınır | 0,44 | 0,61 | 0,81 | 0,85 | 0,90 | 0,93 |

τ = 0,85 → en az 22 bölüm; τ = 0,80 → 16; τ = 0,90 → 35.

**B2 kapısı:**
- 220/244 = %90,2 için kümesiz Wilson alt sınırı 0,858'dir.
- Kümeli hâlde %85 için etkin n ≥ 184 gerekir (tasarım etkisi ≤1,33). Küme etkisi büyükse nokta tahmini %90'ın üstünde olmalıdır.

**Yanlış kabul (Clopper–Pearson tek yanlı %95 üst ≤ %2):**

| Bozuk kabul sayısı | Gereken en az kabul |
|---|---|
| 0 | 149 |
| 1 | 236 |
| 2 | 313 |

B2b'de 220–244 kabul beklendiğine göre bu, fiilen "en çok 1 bozuk" demektir.

**Kırmızı takım:**
- 320/320 yakalanırsa tek yanlı %95 alt sınır %99,07 (300/300 için %99,01).
- ≥%98 için en az 149 mutant gerekir; 320 yeter.

### 6.5 Toplam süre (CPU; GPU yok)

| Basamak | İş | Süre (süreç-saati) |
|---|---|---|
| B0 | M0 × 3 | ≈2–7 |
| B1 | Kırmızı takım | ≈12 |
| B1 | 100 boş koşu | ≈30–230 |
| B1 | Kalibrasyon | ≈20 |
| B2 | B2a + B2b | ≈20–200 |
| B3 | 505 sembolik koşu | ≈250 |
| B3 | Z12 ve aktarım | ≈30 |

- **Toplam ≈ 360–750 süreç-saati.** 4 çekirdekte ≈ 4–8 gün duvar saati.
- v1'in "≈150 GPU-saati" bu ortama uymaz (S-13).
- **Takvim darboğazı** v1'deki gibi mühendislik ve onaydır.

## 7. Basamaklar ve kapılar

- **Kapı 0 (yeni, S-12): GEÇTİ (K-041).** A6 bağımsız inceleme şartı Kapı 2'ye taşındı.
- **B0:**
  - şablon dosyası ve hash;
  - sembolik değerlendirici ve M0 (önce test);
  - A2 parametresi (evlilik oranı), A3 ikinci üretici;
  - havuzlar ve tohum türetme;
  - sorgu bütçesi defteri, boş-dünya sayacı, çekirdek hash.
  - Bitiş: M0 3 kez bit-bit aynı.
- **Kapı 1:** ÖK-005 nihai mühür. Hash'ler eklenir, sayılar değişmez.
- **B1:**
  - kabul protokolü aşama 1–5;
  - kırmızı takım: 4 görünür aile + 4 gizli aile (danışman);
  - K kalibrasyonu (yalnız görünür aileler + boş adaylar; DNA kullanılmaz);
  - P\* ve C ölçümü.
  - Bitiş: 0/320 kaçak, boş dünya geçti.
  - Sahte kabul > 0 → en çok 2 onarım turu; hâlâ varsa dur, kullanıcı.
- **B2:**
  - B2a: 20 silinmiş kural, yalnız duman testi, kapı değil.
  - B2b: 244'ün tamamı silinmiş, sıfır tohum, final havuzunda tek atış.
  - → **Kapı 2:** sonuç ve ara bölge. Ön şart: A6 bağımsız inceleme sonucu (K-041).
- **B3:**
  - kesişim eğrisi (054), sıfır-şablon, şablon bütçesi eğrisi (088), makas;
  - Z12; (isteğe bağlı) Hawaii, Iroquois, Omaha; (isteğe bağlı) terfi deneyi.
  - Bitiş: L\* bulundu ya da "mutasyon gereksiz" yazıldı.
- **Kapanış:** toplu ablasyon tablosu. Önkayıtlı katkı eşiğinin altında kalan bileşen silinir. Mekanizma tavanı 16 (§10).
- **Kapı 3:** H3 açılsın mı.

## 8. Yasak iddialar / önkayıt kuralları (v1 §7, aynen)

Yasak: "kendi buldu" (şablon/tohum ön bilgisi sıfırlanmadan); "genel zekâ" (üç ölçü yoksa); "kısayol yok" (yalnız "kırmızı takım X% yakaladı"); "mutasyon M0'dan iyi" (kesişim eğrisi yoksa); "geçit güvenilir" (taze dünya + mutant skoru yoksa); tek-üretici dünyadan genelleme; aynı-model gözden geçirici onayı "bağımsız doğrulama" sayılmaz (insan veya <300 satırlık, eğitim kodu paylaşmayan denetçi).
Önkayıt: eşikler/dünya aileleri/şemalar veriye bakmadan; tohum/şablon/ad listesi hash'i; LLM altın küme, kalibrasyon, şema seçmez; negatif sonuçlar aynı biçimde raporlanır; oracle (gizli kural/etiket) eğitime asla girmez.

**Bu tasarıma özgü ek not (yasak listesini değiştirmez):**
- B2b sonucu yalnız şu kalıpla yazılır (K-041): "Sayaç + çekirdek hakem hattı, K5/21 şablon ailesi içinde, X/244 kuralı geri buldu". "Çekirdeğin tek başına keşfi" yazılmaz.
- A3'ü aynı kodlayıcı yazdığı için "bağımsız üretici" iddiası "ayrı kod, aynı yazar" diye sınırlanır.

## 9. Kanıt düzeyi (v1 §8 + bu belgenin hesapları)

- **Kanıtlanmış (H2'ye ait):** yok.
- **Hesapla bilinen (kâğıt üstü):**
  - aday uzayı büyüklükleri ve DNA biçim kapsamı (§6.1);
  - dar uzayla ve aynen uygulanan yol-kesmeyle B2b'nin tavanı;
  - istatistik eşiklerinin gerektirdiği en az sayılar (§6.4).
- **Literatür:** M0 küçük uzayda çalışır; yeniden kullanılan test kümesi aşınır (Thresholdout).
- **Makul:** 4.2 aşamaları bilinen kısayol türlerini yakalar. M0'ın süre tahmini (±3 kat).
- **Spekülasyon:**
  - mutasyonun M0'ı yenmesi;
  - eğrinin düz çıkması;
  - terfi ve menteşelerin değeri;
  - genel zekâya elverişlilik;
  - gizli kısayol türlerine karşı koruma;
  - B2b talebinin (C) 2400'e sığması.

## 10. Mekanizma sayımı (tavan 16, artış yasak)

| Grup | Parçalar | Sayı |
|---|---|---|
| Üretim | M0 (sembolik değerlendirici dahil), budama (obiter indirgeme + sıralı budama) | 2 |
| Geçit | Aşama 1–5 (gövde-merkezli bölüm ve uyum şartı aşama 5'in parçası) | 5 |
| Sürekli denetim | Boş-dünya sayacı, makas, kırmızı takım | 3 |
| Diğer | Yedeklilik, susturma, dondurma sözleşmesi, tek aday şeması, MK-lite, ölçümler | 6 |
| **Toplam** | | **16** |

## 11. v1'den sapmalar (gerekçeli)

| No | Sapma | Gerekçe |
|---|---|---|
| S-1 | M0 uzayı ~30–124 bin → K5/21 (35,5 milyon, OI'li) | Eski sayım çift; dar uzay DNA biçiminin %48'i, %90 kapısı imkânsız (§6.1) |
| S-2 | M0, aşama 1–4, null ve boş koşu sembolik; çekirdek yalnız aşama 5'te, sembolik süzgeçten sonra | Çekirdekle 50 CPU-yılı (§6.2) |
| S-3 | Aşama 5 = yenilenebilir taze dünya akışı; final 24 yalnız B2b'de bir kez | "Tek atış" ile "12 tur" çelişir |
| S-4 | Yol-kesme yalnız gövdesi baş çiftine dokunmayan adaylara; ters-dayanaklılar ayrı raporlanır | Aynen uygulansa 81 DNA kuralı sınanamaz, tavan %66,8 |
| S-5 | Küme: kural başına = bölüm, B2 kapısı = sonuç ilişkisi, aile = kapsam ve veto | Aile kümesiyle kural başına alt sınır en çok %44 |
| S-6 | B2 kapsam aileleri A1/A2/A3; Hawaii/Iroquois/Omaha B3 aktarımı | DNA kuralları o terim sistemlerinde doğru değil |
| S-7 | Ters-çift bijeksiyonu = şema otomorfizmi (1536) | Ters listesi bire-çok |
| S-8 | Evlilik yaşı → evlilik oranı (+ nesil, çocuk aralığı) | Üreteçte yaş yok |
| S-9 | Kapalı dünya: yazılmamış çift tahmini = yanlış | Aşırı genel kurallar cezasız kalıyordu (V-057 kapsamı, V-059) |
| S-10 | Kural başına eşik eklendi: doğruluk 1,0 + bölüm-düzeyi Wilson ≥ τ | v1 tablosunda yoktu |
| S-11 | Westfall–Young tur başına α = %1/12 | 12 turda toplam FWER %1 |
| S-12 | Kapı 0 eklendi; ÖK-005 nihai mühür B0 sonunda (Kapı 1) | Kullanıcı: "onay gelmeden B0'a geçme" |
| S-13 | GPU → CPU; ≈360–750 süreç-saati | Ortamda GPU yok |
| S-14 | Şemadan okunabilir 9 kural ayrı sınıf; boş-dünya sayacı dışında; ikinci B2 paydası 235 | Şemayı koruyan boş dünyada doğrudur |
| S-15 | "Eskimo tipi" → "mevcut (Türkçe)" | Amca/dayı ayrımı Sudan tipine yakın |
| S-16 | Z aileleri n ve üreticiyle ayrılır (Z12-a, Z12-b, Z24) | Z12 dünyaları birbirinin yeniden adlandırması |
| S-17 | Turda aday için önkayıtlı tek anahtar (200 ya da 400) + P\*/2 tavanı | B2b talebi kâğıtta sınırda |
| S-18 | Gizli mutantları danışman ya da kullanıcı yazar | Geçit yazarı bilirse gizli olmaz |
| S-19 | B3 eğrisi ve L\* sembolik; "eşit GPU-saniyesi" → eşit süreç-saniyesi | 505 koşu çekirdekle imkânsız |
| S-20 | Thresholdout yalnız Wilson istatistiğine; yanlış = 0 vetosu gürültüsüz | Gürültü doğru kuralı rastgele düşürürdü |

## 12. Kullanıcıya sorular

Sade metin ÖK-005 taslağı §14'tedir. **Kullanıcı altısına da evet dedi (K-041).** Altı soru:
1. Başka kurallarla aynı sonuç "bulundu" sayılsın mı?
2. Gövde-merkezli bölüm?
3. A1/A2/A3?
4. Gizli sahte kurallar?
5. Hawaii, Iroquois, Omaha?
6. Z12 ilişki listesi?
