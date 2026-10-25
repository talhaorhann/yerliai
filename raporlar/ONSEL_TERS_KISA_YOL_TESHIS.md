# Önsel-ters bölmesinde kısa yol kapısı duruşları: teşhis (2026-10-25)

**Yalnız analiz** (K-040). Üreteç ve kapı değiştirilmedi; çekirdek koşmadı. Bölmeler yalnız üreteçle bellekte yeniden kuruldu; kapıya giren küme, kapının kendi ölçüm işleviyle (`kisa_yol.kapi_olc`) yeniden ölçüldü. Değerler manifestlerdekiyle aynı çıktı. Betik geçici, depoda değil. H2 tasarımına girdidir.

## Kapı nasıl ölçer

- **Kapı:** K-008, V-018. Kelime çantası dedektörü yapıya bakmayan bir Naive Bayes'tir: yalnız olgulardaki ilişki adlarını ve kişi kimliklerini sayar.
- Dedektör, kapıya giren kümenin ilk yarısında eğitilir, ikinci yarısında sınanır.
- **Şans:** ikinci yarıda en sık cevabın oranı. Kural: doğruluk, şans + 0,05'i aşarsa üretim durur.
- **Önsel-ters bölmesi (K-010, V-022):** önce doğal dağılımdan 400 bölüm üretilir; cevap oranları Laplace düzeltmesiyle kestirilir (p). Ana küme, kabul olasılığı (p_en_az / p)² olan reddetme örneklemesiyle seçilir. Sonuç dağılımı q ∝ 1/p: doğal örnekte ne kadar az görülen cevap, o kadar sık sorulur.

## İki duruş

| Tohum | Dedektör | Şans | Eşik (şans + 0,05) | Aşım | Ana kümede en sık 3 cevap (sayı/400; doğal örnekte görülme) |
|---|---|---|---|---|---|
| 15 (ÖK-003) | 0,250 | 0,180 | 0,230 | 0,020 | damat 69 (2), dayı 66 (3), hala 44 (4) |
| 21 (ÖK-004) | 0,445 | 0,370 | 0,420 | 0,025 | gelin 156 (0), kuzen 146 (0), damat 34 (1) |

**Aşım hangi soru türlerinden geliyor:**

- **Tohum 21:**
  - Dedektör sınama yarısında 89 soruyu bildi: 53'ü çoğunluk cevabı "gelin" (74 sorunun), 36'sı "kuzen".
  - "Her zaman gelin de" diyen bir tahminci 0,37 alırdı. Aşım, gelin ile kuzenin kelimelerle ayrılabilmesinden geliyor.
- **Tohum 15:**
  - Dedektör 50 soruyu bildi: 17'si çoğunluk cevabı "damat" (36 sorunun).
  - Kalan 33'ün 16'sı dayı, 8'i hala, 4'ü kuzen, 3'ü anneanne, 1'i kayınvalide, 1'i babaanne.

**Ayırt eden şey ilişki adları:** Kişi kimlikleri atılıp yalnız ilişki adları bırakılınca dedektör daha da iyi çıkıyor: tohum 15'te 0,325, tohum 21'de 0,485. Dedektörün öğrendiği, cevabı tanımlayan zincirin kelimeleri:

| Cevap | Olgulardaki en belirgin ilişki adları |
|---|---|
| gelin | oğul, eş |
| damat | kız, eş |
| hala | kız kardeş, baba |
| dayı | erkek kardeş, anne |
| kuzen | kardeş ve ebeveyn adları (eş yok) |

## Ters ağırlık tasarımı sızıntı yapıyor mu

**Cevabı doğrudan sızdırmıyor, ama var olan bir kelime ipucunu iki yoldan büyütüyor.**

1. **Yığılma:**
   - p, 400 doğal bölümden kestiriliyor ve nadir cevaplarda çok gürültülü: 0, 1 ya da 2 kez görülen cevaplar en büyük ağırlığı alıyor.
   - Ana küme tohuma göre 2–3 nadir hısımlık ya da yan akrabalık cevabına yığılıyor; en sık cevabın payı tohumdan tohuma %15 ile %64 arasında değişiyor.
   - Bu cevapların zincirleri birbirinden belirgin kelime çiftleriyle ayrılıyor.
2. **Treg süzgeci çalışmıyor (V-050, gözlem 1):**
   - Kelime çantasının çözdüğü soruları ayıran dedektör, doğal dağılımdan eğitiliyor. Orada bu cevaplar neredeyse hiç yok, dedektör onları tahmin etmiyor.
   - Önsel-ters bölmesinde Treg'e tohum başına yalnız 2–11 bölüm ayrılıyor.

**Ne zaman duruyor:**
- En sık iki cevap neredeyse eşit büyüklükteyse ve kelimeleri farklıysa durur: tohum 15'te damat 69 ile dayı 66, tohum 21'de gelin 156 ile kuzen 146.
- "Şans" yalnız en sık cevabı sayar. Dedektör ise iki büyük sınıfı kelimelerle ayırıp şansın üstüne çıkar.
- Tek sınıf baskınsa durmaz; şansın kendisi yüksektir. Ör. tohum 14: kuzen 257/400, şans 0,63, dedektör 0,61.
- İki büyük sınıfın kelimeleri benzerse de durmaz. Ör. tohum 16: damat 100 ile gelin 93; ikisinin zincirinde de "eş" var, fark +0,025.

**12 tohumda doğruluk − şans** (12–17: ÖK-003, 18–23: ÖK-004):

| Tohum | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fark | +0,030 | +0,045 | −0,020 | **+0,070** | +0,025 | −0,010 | −0,005 | +0,015 | +0,020 | **+0,075** | −0,015 | −0,010 |

- 12 tohumun 2'si duruyor (yaklaşık 6'da 1); 13'teki +0,045 sınıra yakın.
- Bu, bilinen bir üreteç özelliği. Tohum değişim hakkını tüketiyor.

## H2 tasarımı için girdi (öneri; karar değil)

1. Ters ağırlık 400 bölümlük gürültülü bir kestirime dayanıyor. Daha yumuşak bir ağırlık ya da cevap türü başına eşit kota düşünülebilir. Ör. q ∝ p^(−α), α < 1. Bu bir kâhin ve önsel kararıdır, kullanıcıya gelir.
2. Treg dedektörü ana kümeyle aynı dağılımdan eğitilmeli. V-050'de denendi: Treg büyüdü ama sızıntı azalmadı. Bu yüzden 1. madde olmadan yetmez.
3. Kapının "şans" tanımı yalnız en sık cevaba bakıyor. İki baskın sınıflı dağılımlarda kelime çantası şansı kolay aşıyor. Kapının tanımı değişmez (K-008); ama H2'nin ön kaydında bu bölmenin beklenen durma oranı (yaklaşık 6'da 1) önceden yazılabilir.
4. Bu duruşlar çekirdeğin bir zaafı değil, sorulan soruların dağılımının özelliği. ÖK-004 kapısında önsel-ters 2000/2000 geçti.
