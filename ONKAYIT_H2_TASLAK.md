# ÖK-005 TASLAĞI: H2 ön kaydı (mühürsüz)

**Durum:** TASLAK, 2026-10-26. Mühürlü değildir. **Kapı 0 onaylandı (K-041, 2026-10-26):** altı soruya evet; sayaç + çekirdek hakem hattı; A6 bağımsız incelemesi Kapı 2'den önce.

- **Kapı 0:** kullanıcı bu taslağı ve `H2_TASARIM.md`'yi okuyup onaylar. Sonra B0 başlar.
- **Kapı 1:** B0 sonunda nihai ÖK-005 `ONKAYIT.md`'ye "## ÖK-005" başlığıyla yazılır ve kilitlenir. Yalnız hash'ler ve B0'da ölçülen süre eklenir; buradaki sayılar değişmez.

**Kurallar:**
- Bütün eşikler veriye bakılmadan yazıldı.
- "D" = bu ÖK'de donar. "K" = B1'de yalnız aşağıdaki kurala göre kalibre edilir, ÖK-005 ekine yazılır, sonra donar.
- Sonuçtan sonra değişen eşik, sonuca "keşif" damgası vurdurur.
- LLM (kodlayıcı dahil) şema, kalibrasyon, tohum etiketi ya da altın küme seçmez. §2'deki şemalar yalnız **öneridir**; kullanıcı onaylar.

## 1. Soru ve iddia sınırı

- **Soru (sistem.md §13, v1 §1):** sistem 244 kuralı (DNA v8), kimse söylemeden, tipli şablon ailesi içinde bulup güvenle kabul edebilir mi?
- **İddia:** etiketsiz, kâhinsiz, kendini sınayan ve denetlenebilir bir kabul geçidi. "Genel zekâ" sözü kullanılmaz.

## 2. Dünya aileleri ve şemaları (kullanıcı onayına açık)

### 2.1 Akrabalık, mevcut terim sistemi (B2 kapsam aileleri)

**Ortak noktalar:**
- Şema: `sema/iliskiler_v1.json` (21 ilişki, tek dışlayıcı grup).
- Tanımlar: mevcut tanım dosyası.
- Temel (gözlem yürüyüşü) ilişkileri: anne, baba, oğul, kız, eş, erkek_kardeş, kız_kardeş.
- **Etiket önerisi:** "mevcut (Türkçe)". "Eskimo tipi" tam uymaz: amca/dayı/hala/teyze ayrımı Sudan tipine, tek "kuzen" terimi Eskimo tipine yakındır.

| Etiket | Üretici | Parametreler | Kişi sayısı (kâğıt) |
|---|---|---|---|
| **A1** akrabalık-mevcut | `Dunya.uret` (bugünkü) | 4 nesil; çift başına 2–4 çocuk; son nesil dışında her çocuk dışarıdan biriyle evlenir (oran 1,0) | en az 22, beklenen 53, en çok 106 |
| **A2** akrabalık-kaydırılmış | Aynı üretici + yeni "evlilik oranı" parametresi (A1'de 1,0, davranış değişmez) | 5 nesil; 1–4 çocuk; son nesil dışındaki her çocuk 0,8 olasılıkla evlenir | beklenen ≈53,5; tek çocuklu, evlenmemiş ve çocuksuz dallar var |
| **A3** akrabalık-ikinci-üretici | Ayrı modül; `degerlendirme/dunya.py`'den hiçbir şey almaz; ≤300 satır | 3 kurucu çift (üç ayrı soy); 4 nesil; kurucuların 2–4, sonrakilerin 0–4 çocuğu; son nesil dışındaki çocuk 0,8 olasılıkla evlenir | kâğıt tahmini 40–60 (B0'da ölçülür, eşik değildir) |

**A3'ün evlilik kuralları:**
- Eş önce öteki soylardan, aynı nesilden, evlenmemiş, karşı cinsten biri olur; yoksa dışarıdan biri.
- Aynı soydan evlilik yok. Yeniden evlilik ve boşanma yok.
- Bir evlilik bir çifte iki akrabalık terimi verecekse o eş adayı atlanır. Tohum değişmez.

**Ortak varsayımlar (ölçülmez; yasak iddia §12):** iki ebeveyn, tek eşlilik, karşı cins evlilik, boşanma yok.

**Gözlem bölümü (V-057 + kapalı dünya):**
- Kişiler seçilir, seçilen kişiler arasındaki bütün ilişkiler yazılır. Yazılmamış çift ilişkisizdir.
- **Rastgele bölüm:** 2–3 adımlık zincir yürüyüşü + 4 dikkat dağıtıcı bağ.
- **Gövde-merkezli bölüm (aşama 5; K-041 ile onaylı):** adayın gövdesinin dünyadaki eşleşmelerinden tohumla biri seçilir. Kişileri, bunlardan başlayan 2–3 adımlık yürüyüş ve 4 dikkat dağıtıcı bağ eklenir. Maskelenen olgu çekirdeğe verilmez.

### 2.2 Türetilmiş dünyalar (aile değildir; veto ve null)

- **π-ikiz:** ters-çift koruyan bijeksiyonla adları değiştirilmiş dünya (§13.4).
  - Mevcut şemada bu bijeksiyonlardan 1536 tane vardır: 2⁶ × 4! (temel ilişkiler temele gider).
  - Takaslar: anne↔baba, oğul↔kız, erkek_kardeş↔kız_kardeş, babaanne↔anneanne, kayınpeder↔kayınvalide, gelin↔damat, ve {amca, dayı, hala, teyze} içinde her sıra.
- **Yeniden bağlı ikiz:** adayın yalnız baş ilişkisi derece koruyarak yeniden bağlanır, tersleri yeniden yazılmaz (§13.6).
- **Boş dünya:** her ters sınıfının bir temsilcisi (sözlük sırasında ilki) bağımsız yeniden bağlanır, tersleri ondan yeniden yazılır. Şema korunur, ilişkiler arası yapı bozulur.

### 2.3 Z12/mod-n (B3 aktarım; ikinci alan, kullanıcı kararı 4)

**Okunuş ve dünya:**
- Okunuş (A, r, B) = "B, A'nın r'sidir".
- Elemanlar 0…n−1; çekirdek yalnız rastgele kimlik görür.
- Tür tektir (eleman).

**Aileler:**

| Etiket | Ne |
|---|---|
| **Z12-a** | Doğrudan modüler aritmetik, n = 12 |
| **Z12-b** | İkinci üretici: eleman = (a mod 3, b mod 4) çifti, ilişkiler bileşenlerden hesaplanır (Çin kalan teoremi); ayrı kod |
| **Z24** | Parametre-kaydırılmış, n = 24 |

| Ad (taslak) | Tanım | Ters | Simetrik | İşlevsel n=12 | İşlevsel n=24 |
|---|---|---|---|---|---|
| ardıl | B ≡ A+1 | öncül | hayır | evet | evet |
| öncül | B ≡ A−1 | ardıl | hayır | evet | evet |
| iki_ileri | B ≡ A+2 | iki_geri | hayır | evet | evet |
| iki_geri | B ≡ A−2 | iki_ileri | hayır | evet | evet |
| üç_ileri | B ≡ A+3 | üç_geri | hayır | evet | evet |
| üç_geri | B ≡ A−3 | üç_ileri | hayır | evet | evet |
| altı_öte | B ≡ A+6 ya da B ≡ A−6 | altı_öte | evet | evet | **hayır** |
| karşıt | A+B ≡ 0, A ≠ B | karşıt | evet | evet | evet |
| kalan3_eş | A ≡ B (mod 3), A ≠ B | kalan3_eş | evet | hayır | hayır |
| kalan4_eş | A ≡ B (mod 4), A ≠ B | kalan4_eş | evet | hayır | hayır |

**Şema ve bölüm ayrıntıları:**
- **Dışlayıcı grup:** {ardıl, öncül, iki_ileri, iki_geri, üç_ileri, üç_geri, altı_öte}. Bir çift hem öteleme hem kalan ilişkisinde olabilir.
- **Temel ilişkiler:** ardıl, öncül, karşıt.
- **Bölüm:** 2–3 adım + 2 dikkat dağıtıcı bağ, seçilen elemanlar arasındaki bütün ilişkiler. Havuz sınırı 128 olduğu için akrabalıktan kısadır.
- **Dürüst not:** aynı n'deki bütün dünyalar birbirinin yeniden adlandırmasıdır.

### 2.4 Hawaii, Iroquois, Omaha (B3, isteğe bağlı; kullanıcı sorusu 5)

**Kurulum:**
- A1 soy ağacı üzerinde başka adlandırma kullanılır. Kaynak: Murdock (1949), altı terim tipi.
- Şemalar tanımlardan türetilir.
- **Tanımlar kodlayıcının önerisidir. Kullanıcı ya da danışman onaylamadan kullanılmaz.**

| Etiket | Mevcuttan farkı (kime ne denir) | İşlevsel |
|---|---|---|
| **H** Hawaii (kuşak) | Ebeveynin kardeşleri anne/baba; bütün birinci kuzenler erkek_kardeş/kız_kardeş; kardeş çocukları oğul/kız; büyükanne taraf ayırmaz (yeni ad: büyükanne). Amca, dayı, hala, teyze, kuzen, yeğen, babaanne, anneanne yok. | yalnız eş |
| **I** Iroquois (çatallı birleştiren) | Babanın erkek kardeşi baba, annenin kız kardeşi anne; dayı, hala kalır; amca, teyze yok. Paralel kuzen erkek_kardeş/kız_kardeş, çapraz kuzen kuzen. | yalnız eş |
| **O** Omaha (baba soylu kaydırma) | Iroquois gibi; ek olarak dayının oğlu dayı, dayının kızı anne, halanın çocukları yeğen. | yalnız eş |

**Ölçü:** kapanış geri bulma. Elle yazılmış hedef kural kümesi gerekmez.

## 3. Havuzlar

| Havuz | Dünya | Aile dağılımı | Kullanım | D/K |
|---|---|---|---|---|
| B2 geliştirme | 16 | A1 6, A2 5, A3 5 | M0, aşama 1–4, K kalibrasyonu (serbest) | D |
| B2 mühürlü final | 24 | 8 / 8 / 8 | Yalnız B2b ölçümü, tek atış | D |
| B2 kontrol | 8 | 3 / 3 / 2 | Hiç sorgulanmaz; yalnız Goodhart makası | D |
| Taze akış | yenilenebilir | Aday başına tur içinde A1, A2, A3'ten 2'şer | Aşama 5; her taze dünya tek turda yanar | D |
| B3 akrabalık | 16 / 24 / 8 | B2 ile aynı dağılım, ayrı tohum | Kesişim eğrisi, şablon eğrisi, ablasyon | D |
| B3 Z (aile başına) | 4 / 8 / 2 | Z12-a, Z12-b, Z24 | Aktarım | D |
| B3 H, I, O (aile başına) | 4 / 8 / 2 | Onaylanırsa | Aktarım | D |

- **Bağımsızlık birimi:** kural başına kabulde gözlem bölümü; B2 kapısında sonuç ilişkisi; kapsamda dünya ailesi (tasarım §3.3 madde 7).
- **Ayrıklık:** havuzlar ayrıktır. Bölüm özetleri H1 kilitli kümeleriyle kesişmez (`kesisim_denetle`). Kesişim ya da yinelenen dünya özeti → dur (§9).

## 4. Eşik tablosu (eksiksiz)

| No | Madde | Değer | D/K |
|---|---|---|---|
| 1 | Havuzlar | 16 / 24 / 8 (dağılım §3) | D |
| 2 | Sorgu birimi | (aday, taze dünya); ≤200 aday/tur; ≤12 tur; grup sorgusu yok | D |
| 3 | Tur anahtarı | C ≤ 2400 → 200/tur; C > 2400 → 400/tur (fazlası "bütçede sınanmadı"); her durumda tur başına ≤ ⌊P\*/24⌋. C ve P\* B1'de ölçülür. | D (kural) |
| 4 | Aşama 5 dünya ve bölüm | Aday başına tur içinde 6 taze dünya (ailede 2) × dünyada 8 gövde-merkezli bölüm (K-041) | D |
| 5 | M0 süzgeci | Geliştirme havuzunda yanlış 0 VE tanık ≥3 (kapalı dünya) | D |
| 6 | Aşama 1–3 | 0 kongrüans, 0 işlevsel, 0 ters ihlali; obiter halka 0; yol-kesmeli tanık ≥3 | D |
| 7 | Aşama 4 veto | π-ikizinde hüküm aynı; yeniden bağlı ikizde (≥3 tanık VE 0 yanlış) → BİLMİYORUM; bir ailede yanlış > 0 → o aile veto; RET için ≥2 aile vetosu | D |
| 8 | Kural başına doğruluk | Taze dünyalarda yanlış 0 (gürültüsüz) | D |
| 9 | Kural başına Wilson | Bölüm-düzeyi Wilson alt sınırı (z = 1,96) ≥ τ; başlangıç τ = 0,85 (≥22 kanıtlı bölüm) | K: {0,80; 0,85; 0,90} |
| 10 | Müdahale (K-037, b·c) | ≥ 0,9 | K: {0,8; 0,9; 1,0} |
| 11 | Uyum şartı | Çekirdek ile sembolik sayım aynı adayda farklı doğru ya da yanlış sayısı verirse BİLMİYORUM | D |
| 12 | Thresholdout | T = 0,04, σ = 0,01; yalnız Wilson istatistiğine. Ayrıntı aşağıda. | K: T {0,02; 0,04; 0,06} × σ {0,005; 0,01; 0,02} |
| 13 | Null | Derece-koruyan yeniden bağlama (baş ilişkisi, dünya düzeyinde); Westfall–Young maks-T, istatistik bölüm-düzeyi Wilson; B = 10.000; toplam FWER %1, tur başına α = %1/12 | D |
| 14 | Kapsam tabanı | ≥2 aile, her birinde ≥3 tanık ve 0 yanlış; adayın kapsam alanı yasak | D |
| 15 | "Bilmiyorum" üst sınırı | Final kapanış ölçüsünde: bilmiyorum(kabul kümesi) − bilmiyorum(DNA v8) ≤ 10 puan (§8) | D |
| 16 | B2 kapı | Geri bulma nokta ≥ %90 (≥220/244) VE kümeli Wilson alt sınırı ≥ %85 (küme = sonuç ilişkisi, 21) | D |
| 17 | Yanlış kabul | Kabul kümesinde bozuk oranı, Clopper–Pearson tek yanlı %95 üst sınır ≤ %2 | D |
| 18 | B2 ara bölge | Nokta %50–90, ya da nokta ≥%90 ama 15–17'den biri tutmadı → dur + ham rapor + kullanıcı. Nokta < %50 → dur. | D |
| 19 | Kırmızı takım | 320 mutant = 8 aile × 40 (4 görünür + 4 gizli); kaçak 0; tek yanlı %95 alt sınır ≥ %98 (320/320 → %99,07) | D |
| 20 | Boş dünya | 100 boş koşu; ≥2 koşuda herhangi kabul (şemadan okunabilir sınıf hariç) → arama donar | K: maliyet kuralı (aşağıda) |
| 21 | Makas | Kontrol ve sorgulanan tarafta ≥2000'er maskeli olgu; tetik: fark (sorgulanan − kontrol) için %95 kümeli bootstrap alt sınırı (küme = dünya, 10.000 yeniden örnek) > 3 puan → arama donar | K: örnek sayısı (aşağıda) |
| 22 | Tohum ve kollar | M0: 3 koşu bit-aynı. Stokastik kollar: 20 eşleşmiş tohum × 5 bütçe. L\*: eşleşmiş fark için %95 kümeli bootstrap güven aralığı > 0, en az 2 bütçede. | D |
| 23 | Bütçe kademeleri | M0'ın K5/21 tam koşu süresinin %1, %3, %10, %30, %100'ü (süreç-saniyesi; B0'da ölçülür, eke yazılır) | D (kural) |
| 24 | Eğri düz | K5 − K2 kapanış geri bulma farkı için TOST ±5 puan (%90 güven aralığı, kümeli bootstrap); 3 aile: akrabalık, akrabalık-π, Z12 | D |
| 25 | Ablasyon | Bileşen çıkarılınca kırmızı takım kaçağı artmıyor VE B3-akrabalık geri bulma değişimi < 2 puan → bileşen silinir | D |
| 26 | Mekanizma tavanı | 16 | D |
| 27 | Çekirdek | Hiperparametreler H1 değerleri: tur 8, havuz 128, bütçe 1024, hücre yazma 8. Çekirdek kod özeti B0 sonunda mühürlenir. | D |

**Thresholdout ayrıntısı (madde 12):**
- |T_gel − T_taze| > T + η₁ ise kullanılan değer T_taze + η₂'dir; değilse T_gel.
- η₁ ~ Laplace(0, 2σ), η₂ ~ Laplace(0, σ).
- "Yanlış 0" vetosu gürültüsüzdür.

**Görünür kırmızı takım aileleri (madde 19; kodlayıcı yazar, DNA kullanılmaz):**

| Aile | Ne | Nasıl üretilir |
|---|---|---|
| G1 bozuk sonuç | Doğru görünen gövde, yanlış sonuç | M0 süzgecini geçen adaylardan tohumla seçilir; baş ilişkisi aynı dışlayıcı gruptan tohumla seçilen başka bir ilişkiyle değiştirilir |
| G2 aşırı genel | Gerekli bir halkası (ör. cinsiyet tanığı) silinmiş kural | M0 süzgecini geçen, ≥2 halkalı adaylardan bir halka silinir; kalan kural bağlı olmalı ve geliştirme havuzunda yanlış > 0 vermeli |
| G3 kapsam artefaktı | Yalnız bir ailede tutan kural | Geliştirme havuzunda A1'de 0 yanlış ve ≥3 tanıklı, A2 ya da A3'te yanlışlı T adayları |
| G4 gizli ters | Baş çiftine sözdizimsel olarak dokunmayan, ama simetrik-işlevsel bir ilişkinin iki adımlık geri dönüşüyle (ör. eşin eşi = kendisi) başın tersini okuyan kural | t(Z,X) ∧ s(Z,W) ∧ s(W,Y) → r(X,Y); t ∈ ters(r), ters(t) birden çok, s simetrik ve işlevsel; OI kapalı. Yarı yarıya yanlıştır ve yol-kesme maskesini sınar. |

- Her aile 40 mutanttır. Bir aile 40'tan az üretebiliyorsa hepsi alınır, eksik G1'den doldurulur; sayı raporlanır.
- G1–G3 B1'de M0 çıktısından, G4 şemadan üretilir.
- **Gizli aileler (G5–G8):** danışman yazar ve bu dört türden farklı türlerden olur; biçim `sema/aday_v1.schema.json` + `sema/kirmizi_dosyasi_v1.schema.json`.

**K kalibrasyon kuralı (madde 9, 10, 12):**
- **Ortam:** B1'de, yalnız geliştirme havuzu ve B1 taze akışında.
- **Girdiler:** yalnız görünür kırmızı takım aileleri ve boş adaylar. DNA v8 ve gizli aileler girmez.
- **Seçim:** sahte kabulü 0 olan değerler içinden, geliştirme havuzunda M0 sırasının ilk 200 adayına en çok KABUL veren seçilir. Eşitlikte başlangıç değeri kalır.
- **Kayıt:** sonuç ÖK-005 ekine yazılır, kullanıcıya bildirilir, sonra donar.

**Diğer K kuralları:**
- **Madde 20:** B1'de tek boş koşu ölçülür. 100 koşu 120 duvar saatini aşacaksa 50 koşu yapılır, tetik ≥1 olur.
- **Madde 21:** B1'de 2000 örnekte güven aralığının yarı genişliği 2 puanı aşarsa örnek sayısı 4000 olur. Tetik 3 puan değişmez.

**Kümeli Wilson (madde 16):**
- p̂ = geri bulunan / 244.
- ρ̂ = ICC'nin ANOVA (Fleiss) kestiricisi; negatifse 0.
- Tasarım etkisi = 1 + (m₀ − 1)ρ̂, m₀ = (n − Σmᵢ²/n)/(k − 1), k = 21.
- n_etkin = 244 / tasarım etkisi; sonra Wilson(p̂, n_etkin).

**Westfall–Young çekilişi (madde 13):**
- b'inci çekilişte her ilişki her taze dünyada bağımsız yeniden bağlanır.
- Aday j için gövde eşleşmeleri özgün dünyadan, baş doğruluğu baş ilişkisi yeniden bağlanmış dünyadan alınır.
- p_j = (1 + #{b : maxᵢ Tᵢᵇ ≥ T_j}) / (B + 1).

## 5. Tohumlar

**Türetme kuralı (değiştirilemez; tohum değişimi yoktur):**
- tohum(e) = int(sha256(("ÖK-005|" + e) UTF-8).hexdigest()[:8], 16).
- Üretilemeyen dünya ya da kesişim → dur ve bildir (§9).

| Ne | Etiket e | Sayı |
|---|---|---|
| Havuz dünyası | `havuz|<gelistirme/final/kontrol>|<aile>|<i>` | §3 |
| B3 havuzları | `havuzB3|<alan>|<havuz>|<aile>|<i>` | §3 |
| Taze dünya | `taze|<B1/B2a/B2b/B3>|<tur>|<aile>|<j>` | turda aday başına 6 |
| Gözlem bölümü | `bolum|<dünya etiketi>|<aday kimliği>|<m>` | dünyada 8 (ya da 32) |
| π seçimi | `ikiz|<dünya etiketi>|<aday kimliği>` | aday başına 1 |
| Veto yeniden bağlama | `bag|<dünya etiketi>|<aday kimliği>` | aday başına 1 |
| Null çekilişi | `null|<basamak>|<tur>|<b>|<dünya etiketi>|<ilişki>` | B = 10.000 |
| Boş dünya | `bos|<k>|<havuz dünyası etiketi>` | 100 (ya da 50) |
| Kırmızı takım (görünür) | `kirmizi|<aile>|<i>` | 4 × 40 |
| Stokastik kollar | `kol|<kol>|<s>|<bütçe>` | 20 × 5 × 5 kol |
| Thresholdout gürültüsü | `gurultu|<basamak>|<tur>|<aday kimliği>` | aday başına |
| B2a seçimi | DNA kimliği için sha256("ÖK-005|B2a|" + kimlik); en küçük 20 | 20 |

**Koşu sayıları:**
- M0: 3 (bit-aynı).
- B2a: 1. B2b: 1 (tek atış).
- B3 kesişim eğrisi: M0 için 5 bütçe; her stokastik kol için 20 × 5.

## 6. Tipli şablon ailesi (ön bilgi; dosyası B0'da yazılıp hash'lenir)

**T = K5/21:**
- gövde 1–3 halka;
- değişkenler {X, Y, Z, W} (en çok 4); baş r(X, Y), r ∈ 21 ilişki;
- gövde sözlüğü 21 ilişki;
- gövde bağlı ve X ile Y'yi içerir;
- iki ucu aynı değişken olan halka yok;
- tek halkalı gövde başla aynı olamaz;
- OI bayrağı (bütün değişken çiftleri farklı kişi) yalnız bitişik olmayan bir çifti olan gövdelerde ayrı aday;
- tip: tek tür (kişi), tip budaması yok.

**Boyut:** 903.203 gövde, 18.652.809 kural, OI ile 35.544.873 aday.

**Kademeler (eğri için):**

| Kademe | Tanım | Kural (OI'siz) |
|---|---|---|
| K1 | tek halka | 861 |
| K2 | ≤2 halka zincir | 37.905 |
| K3 | ≤2 halka genel | 127.449 |
| K4 | ≤3 halka zincir | 1.593.753 |
| K5 | T | 18.652.809 |

**Sıfır-şablon kolu:** ≤4 halka, ≤5 değişken, bağlılık şartı yok, OI yok. Önce halka sayısı, sonra halkalar düzgün rastgele seçilir.

**M0 sırası:** tanık azalan, halka sayısı artan, kanonik kimlik artan.

## 7. Kabul protokolü ölçütleri

Tam tanım `H2_TASARIM.md` §4.2'dedir; eşikler §4'tedir.

**Önericiye dönen:** yalnız KABUL, RET ya da BİLMİYORUM. Ham skor, neden ve düşen dünya dönmez; bunlar yalnız denetçi kanalına yazılır.

**Yol-kesme maskesi:** maskelenen (A, r, B) için, gövdesi baş çiftine sözdizimsel olarak dokunmayan adaylarda (B, t, A), t ∈ ters(r) olguları da maskelenir. Ters-dayanaklı adaylarda maskelenmez; ayrı raporlanır.

**Yedeklilik:** geliştirme havuzunda bütün tanıkları kabul kümesince zaten türetilen aday uyutulur, bütçe harcamaz. Kabulden sonra tabu testi yapılır (çıkarılınca hüküm değişmiyorsa uyut).

**Hata tanımı (kapalı dünya, V-059):**
- doğru = tahmin gözlenmiş;
- yanlış = aynı çiftte başka bir ilişki gözlenmiş ya da çift ilişkisiz (yazılmamış).

## 8. B2 ölçümü (yalnız final havuzunda, bir kez)

**Hedef:** DNA v8'in 244 kuralı. Kâhindir: yalnız bu ölçümde ve sınıflamada kullanılır. Arama, kalibrasyon ve K seçimine girmez.

**Kurulum:**
- **B2a:** sha256 seçimiyle 20 kural silinir. Kalan 224 kural bellekte "B2a tohumu" kaynağıyla durur. Duman testidir, kapı değildir.
- **B2b:** bellek boştur. Aday üreteci M0'dır (K5/21). 12 tur.

**Maske:**
- Her final dünyasının tam olgu kümesinde bir olgu f maskelenir.
- Maskeye f ve, değerlendirilen kural ters-dayanaklı değilse, f'nin tersleri girer.

**Her DNA kuralının sınıfı (öncelik sırası):**
1. **Özdeş:** aynı kanonik kimlik, kabul ya da uyutulmuş.
2. **Daha genel:** kabul kümesinde onu θ-kapsayan bir kural var ve finalde yanlışsız.
3. **Kapanış-eşdeğer:** DNA kuralının maskeli olgudan yeniden türettiği her olguyu, kabul kümesi aynı maske altında, en çok 8 turda türetir.
4. **Finalde örneği yok:** gövdesi 24 dünyanın hiçbirinde eşleşmiyor. Paydada kalır, ayrıca listelenir.
5. **Bulunamadı.**

**Geri bulma oranı:**
- **Birincil:** (1 + 2 + 3) / 244 (K-041). Biçimce özdeş ve daha genel olanların oranı, (1 + 2) / 244, ayrıca raporlanır.
- **İkincil paydalar:**
  - 235: şemadan okunabilir 9 kural hariç;
  - örneği olanlar.

**Kabul edilenlerin sınıfı:**
- özdeş, daha genel, fazlalık-doğru (uyutulmuş), farklı-doğru, bozuk.
- **Bozuk:** finalin tam olgu kümesinde, kapsamındaki bir ailede kapalı dünyaya göre en az bir yanlış tahmin. Yanlış kabul oranı (§4 madde 17) budur.

**Bilmiyorum ölçüsü (§4 madde 15):**
- Final dünyalarında her olgu yukarıdaki maskeyle maskelenir; kabul kümesi en çok 8 turda türetmeye çalışır.
- Türetemezse "bilmiyorum", çelişen bir şey türetirse "yanlış".
- Aynı ölçü DNA v8 ile de yapılır ve fark raporlanır.

**Rapor kalıbı (K-041):** "Sayaç + çekirdek hakem hattı, K5/21 şablon ailesi içinde, X/244 kuralı geri buldu". "Çekirdeğin tek başına keşfi" ve "kendi buldu" yazılmaz.

## 9. Durma kuralları

1. **Ön kayıt tutmazsa** koşu başlamaz: ÖK-005, şablon dosyası, çekirdek ya da config hash'i.
2. **B0:** M0'ın 3 koşusu bit-aynı değilse dur. Neden bulunmadan B1 yok.
3. **B1:** kırmızı takımda (görünür + gizli) ≥1 kaçak ya da boş-dünya tetiği → onarım turu (en çok 2). Hâlâ varsa dur ve kullanıcıya bildir; B2'ye geçilmez.
4. **Arama sırasında** boş-dünya sayacı ya da makas tetiklenirse arama donar; rapor kullanıcıya gider.
5. **Sorgu bütçesi biterse** arama durur. Kalan adaylar "bütçede sınanmadı" sayılır ve raporlanır.
6. **B2b sonucu:** §4 madde 16–18'e göre geçti, ara bölge ya da dur. Negatif sonuç aynı biçimde raporlanır.
7. **Üretim hatası:** bir dünya üretilemez, kesişim çıkar ya da dünya özeti yinelenirse dur ve bildir. Tohum değiştirilmez.
8. **Bozuk kabul:** H2'de bozuk bir kural kabul edilirse K-037 (müdahale b·c) yeniden açılır. Kullanıcı kararı.
9. **Eşik değişikliği:** sonuçtan sonra eşik değişirse sonuç "keşif" damgası taşır ve ÖK-005'e göre başarı sayılmaz.

## 10. Kullanıcı kapıları

| Kapı | Ne zaman | Ne onaylanır |
|---|---|---|
| 0 | **Geçti (K-041, 2026-10-26)** | Bu taslak, `H2_TASARIM.md`, §14'teki sorular |
| 1 | B0 sonu | Nihai ÖK-005 (hash'ler eklenmiş, sayılar aynı) |
| B1 sonu | Yalnız bildirim | K değerleri, C, P\*, tur anahtarının konumu. Sahte kabul > 0 ise kullanıcı kararı. |
| 2 | B2b sonu | Sonuç; ara bölgede devam kararı. **Ön şart: A6 bağımsız inceleme sonucu** (K-041) |
| 3 | H2 sonu | H3 açılsın mı |

**Ön şartlar:**
- B1'den önce: gizli kırmızı takım aileleri danışman ya da kullanıcıdan gelmeli.
- B3'ten önce: H, I, O tanımları onaylanmalı (isteğe bağlı).

## 11. Sızıntı tablosu (ön bilgi)

| Ön bilgi | Ne söyler | Kâhin mi? | Kim biliyor | Ölçüm / azaltma |
|---|---|---|---|---|
| **Tipli şablon ailesi T (K5/21)** | Kuralların biçimi: ≤3 halka, ≤4 değişken, bağlı gövde, OI bayrağı, 21 ilişkilik sözlük | Hayır, ama güçlü önsel. ≤3 sınırı DNA biçiminin kendi sınırıdır (`dna_v2`); DNA'nın 244/244'ü biçimce içeride | Kodlayıcı DNA'yı görmüştür; "DNA'yı görmeden" koşulu kodlayıcı için sağlanamaz | Aile en genel seçimle tanımlandı (v1 sınırı + şemanın bütün sözlüğü); sıfır-şablon kolu; şablon bütçesi eğrisi K1–K5 |
| Şablon kademeleri | Kademe boyutları ve DNA biçim kapsamı (§6) | Hayır | Herkes | Yalnız eğri için |
| İlişki şeması (ad, ters, simetrik, işlevsel, dışlayıcı grup) | Çelişkinin tanımı; 9 DNA kuralı doğrudan şemadan okunur | Alan bilgisi | Çekirdek ve geçit | 9 kural ayrı sınıf; ikincil payda 235 |
| Gözlem tasarımı (V-057) + kapalı dünya | Türetilmiş ilişkiler de (ör. dede) doğrudan gözlenir; yazılmamış çift ilişkisizdir | Hayır (bağımsız gözlem), ama güçlü ipucu | Üreteç gerçek ağacı bilir | Yok; H2 bu gözlemle tanımlıdır. Seyrek gözlem H3. |
| Gövde-merkezli bölüm (onaylanırsa) | Geçit, adayın gövdesinin geçtiği yere bakar | Hayır; cevap maskeli | Geçit | B3'te rastgele bölümle karşılaştırılır |
| Dünya aile etiketi | Hangi dünya hangi aileden (ortam etiketi) | Hayır | Geçit | Kapsam hesabı için gerekli |
| Üretici varsayımları (iki ebeveyn, tek eşlilik, karşı cins, boşanma yok; A1: herkes evlenir, eşler dışarıdan) | Dünyanın biçimi | Üreteç tarafı | Herkes | A2, A3 kısmen ölçer; ortak varsayımlar ölçülmez (yasak iddia) |
| A3'ün yazarı | "Bağımsız" üretici | — | Aynı kodlayıcı | "Ayrı kod, aynı yazar" diye raporlanır |
| Türkçe ilişki adları | Anlamlı adlar | Hayır, dil ipucu | Çekirdek adları yalnız anahtar olarak kullanır | π-ikizi (1536 bijeksiyon) |
| Çekirdek hiperparametreleri | DNA v8 ile H1'de seçildi (tur 8, havuz 128, bütçe 1024) | Hayır | Herkes | Dondurma sözleşmesi; ölçülmez, raporda yazılır |
| K eşikleri | Kabul ölçütü | Hayır | Geçit | Yalnız görünür kırmızı takım ve boş adaylarla; DNA girmez |
| Görünür kırmızı takım aileleri | Hangi sahte türlerin sınandığı | Hayır | Geçidin yazarı | Gizli 4 aile (kodlayıcı açmaz) |
| M0 sırası ve süzgeci | Hangi aday önce sınanır | Hayır | ÖK'de önceden | DNA'ya göre ayar yok |
| Taze dünya tohum kuralı | Hangi dünyaların sorulacağı | Hayır | Kodlayıcı tohumu hesaplayabilir | İçeriği yalnız geçit okur; okuma defterde |
| DNA v8 (B2 hedefi) | Doğru kurallar | **Evet** | Kodlayıcı | Yalnız final ölçümünde ve sınıflamada; arama, kalibrasyon ve sıralamaya girmez |
| Hüküm geri bildirimi (3 değer) | Önericiye tur başına bilgi | Hayır | Önerici | Thresholdout; taze dünya her tur yanar; B2b'de M0 sabit sırada |
| B2a'da bellekteki 224 kural | Tohum kurallar | Evet (tohum) | Geçit | B2a kapı değildir |
| Ters-çift bijeksiyonları | Ad simetrileri | Hayır | Şemadan | — |

## 12. Yasak iddialar / önkayıt kuralları (v1 §7, aynen)

Yasak: "kendi buldu" (şablon/tohum ön bilgisi sıfırlanmadan); "genel zekâ" (üç ölçü yoksa); "kısayol yok" (yalnız "kırmızı takım X% yakaladı"); "mutasyon M0'dan iyi" (kesişim eğrisi yoksa); "geçit güvenilir" (taze dünya + mutant skoru yoksa); tek-üretici dünyadan genelleme; aynı-model gözden geçirici onayı "bağımsız doğrulama" sayılmaz (insan veya <300 satırlık, eğitim kodu paylaşmayan denetçi).
Önkayıt: eşikler/dünya aileleri/şemalar veriye bakmadan; tohum/şablon/ad listesi hash'i; LLM altın küme, kalibrasyon, şema seçmez; negatif sonuçlar aynı biçimde raporlanır; oracle (gizli kural/etiket) eğitime asla girmez.

## 13. Kodlanabilir tanımlar (her biri tek cümle)

1. **Kanonik kimlik:** Bir adayın kanonik kimliği, OI bayrağı açıksa gövdedeki bütün değişken çiftleri `farkli` listesine yazıldıktan sonra depodaki `kanonik_bicim` işlevinin (halka sırasının bütün permütasyonlarında değişkenleri ilk görünüş sırasıyla 0, 1, 2, … diye numaralayıp (halkalar, sonuç, sıralı farklı çiftleri) üçlüsünün sözlük sırasında en küçüğünü alan) çıktısının `kanonik_json` biçiminin sha256 özetidir; eşik ve güvenilirlik kimliğe girmez.
2. **Tanık:** Bir adayın bir gözlem bölümündeki tanık kümesi, gövdesinin o bölümün maskelenmiş olgular çıkarılmış olguları üzerindeki eşleşmelerinin X ve Y'ye bağladığı (A, B) çiftlerinden kurulan (bölüm özeti, A, baş ilişkisi, B) dörtlülerinin kümesidir; bir dörtlü kaç ayrı eşleşmeden gelirse gelsin bir kez sayılır ve doğru ile yanlış sayıları bu küme üzerinden hesaplanır.
3. **Kapsam (sistem türetir):** Bir kuralın kapsamı, aşama 5'in sembolik ve çekirdek adımlarında o kuralın en az 3 tanıkla ve 0 yanlışla desteklendiği dünya ailelerinin (§2 etiketleri) kümesidir; kapsamı yalnız geçit hesaplayıp bellek kaydına yazar, aday kaydında kapsam alanı bulunursa aday reddedilir.
4. **Ters-çift koruyan bijeksiyon:** Ters-çift koruyan bijeksiyon, şemadaki ilişki adlarının, her r için {π(t) : t ∈ ters(r)} = ters(π(r)), simetrik(π(r)) = simetrik(r), işlevsel(π(r)) = işlevsel(r) ve temel(π(r)) = temel(r) koşullarını sağlayan bir π permütasyonudur (mevcut şemada 1536 tane); ikiz dünyada her olgu (A, r, B) yerine (A, π(r), B) yazılır, ikiz adayda π kuralın bütün halka ve sonuç adlarına uygulanır ve π mühürlü tohumla bu kümeden düzgün rastgele seçilir.
5. **Parametre-kaydırılmış dünya:** Parametre-kaydırılmış dünya, A1'in üreticisiyle, §2.1'de A2 için mühürlü parametrelerle (5 nesil, çift başına 1–4 çocuk, son nesil dışındaki çocuk için evlilik olasılığı 0,8; A1'de 4 nesil, 2–4 çocuk, 1,0) ve §5'teki kurala göre türetilmiş tohumla üretilen dünyadır.
6. **Derece-koruyan yeniden bağlama:** Bir dünyanın olgu kümesinde yeniden bağlanacak her ilişki r için, mühürlü tohumlu üreteçle r olgularından (A, r, B) ve (C, r, D) seçilip (A, r, D) ve (C, r, B) ile değiştirilir (simetrik r'de kenar yönsüz alınır ve iki yönü birlikte yazılır); kendine bağ, var olan bir olgunun yinelenmesi ya da aynı çiftte aynı dışlayıcı gruptan ikinci ilişki doğuran takas reddedilir, r olgu sayısının 10 katı kadar takas denenir, böylece her kişinin r'deki giriş ve çıkış sayısı değişmez; tersler yalnız boş dünyada r'den yeniden yazılır, veto ikizinde ve null'da yazılmaz.

## 14. Onay listesi ve sorular (Kapı 0)

**Kullanıcı neyi onaylar:**
1. §2 aileleri, etiketleri ve şemaları: A1–A3, türetilmiş dünyalar, Z, (isteğe bağlı) H, I, O.
2. §3 havuzlar.
3. §4 eşik tablosu (D değerleri ve K kuralları).
4. §5 tohum türetme kuralı.
5. §6 şablon ailesi.
6. §8 B2 ölçümü.
7. §9 durma kuralları.
8. §10 kapılar.

**Sorular (evet/hayır; önerim parantezde). Kullanıcı cevabı: altısına da EVET (K-041).**
1. Sistem bir kuralı tam yazılan biçimde değil de başka kurallarla aynı sonuçları çıkararak bulursa, bu "bulundu" sayılsın mı? Aynı biçimde bulunanlar ayrıca sayılacak. **(Evet)**
2. Sistem bir kuralı sınarken, rastgele bir aile parçası yerine, o kuralın "eğer" kısmının gerçekten geçtiği bir aile parçasını isteyebilsin mi? Sorulan şeyin cevabı yine gizli kalır. **(Evet.** Hayır olursa nadir kuralların çoğu "bilmiyorum" kalır ve sınama yaklaşık dört kat uzar.)
3. Bir kuralın kabulü için şu üç aile türünün en az ikisinde doğru çıkması şart olsun mu? **(Evet)**
   - bugünkü aileler;
   - daha derin, içinde tek çocuklu, evlenmemiş ya da çocuksuz kişiler olan aileler;
   - başka bir programla kurulmuş, iki soyun birbiriyle evlendiği aileler.
4. Sistemi kandırmak için tasarlanmış sahte kuralların yarısını danışman (ya da siz) yazsın ve ben onları hiç görmeyeyim mi? **(Evet)**
5. Kuzenlere ve amcalara başka adlar veren üç akrabalık sistemi (Hawaii, Iroquois, Omaha) H2'nin son basamağında yalnız ölçüm olarak kullanılsın mı? Tanımlarını siz ya da danışman onaylarsınız; H2'nin geçme şartına girmez. **(Evet)**
6. Saat aritmetiği dünyası için önerdiğim ilişki listesini (bir sonraki, iki sonraki, karşısı, aynı kalan gibi on ilişki, §2.3) onaylıyor musunuz? **(Evet)**
