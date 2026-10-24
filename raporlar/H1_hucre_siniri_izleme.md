# İlk koşunun 14 uzunluk hatası: çekirdek izlemesi (2026-10-24)

Yalnız teşhis. Veri: ilk koşunun uzunluk bölmesi (tohum 7–11). Bu veri ÖK-003'e göre artık geliştirme verisidir. Çekirdek kodu değişmedi. Karşılaştırma ölçümleri çekirdeğin geçici bir kopyasında yapıldı.

## 1. DNA aynı mı?

Kullanılan dosya `veri/dna/akrabalik_dna_v2_final.json` ile danışmanın gönderdiği dosya bayt bayt aynı. İkisinin de sha256 özeti `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e`.

- Kural sayısı 170, kural kimlikleri aynı ve aynı sırada.
- Hiçbir kuralın içeriğinde fark yok.
- İlk H1 koşusu da bu özeti kullandı (ÖK-002 eki).

## 2. En küçük örnek: tohum 9, bölüm `cedede6ce548`

Olgular:

- baba(19,35)
- oğul(35,21)
- anne(21,33)
- baba(33,27)
- dört dikkat dağıtıcı olgu

Soru: 19 → 27.

Danışmanın beklediği sıra çekirdeğin ilk iki turunda aynen gerçekleşti:

| Tur | Kayıt | Kural | Çekirdekte |
|---|---|---|---|
| 1 | erkek_kardeş(19,21) | baba_ogul_erkek_kardes | 1. turda yazıldı |
| 2 | anne(19,33) | erkek_kardes_anne_anne | 2. turda yazıldı |
| 3 | dede(19,27) | anne_baba_dede | **yazılmadı** |

Danışmanın kapanışında olup çekirdekte olmayan **ilk ve tek kayıt dede(19,27)**. Cevabın kendisi bu kayıt.

**Neden: hücre başına tur başına yazma sınırı (8; sistem.md §3, `hucre_tur_yazma_siniri`).** 3. turda `anne_baba_dede` hücresi 11 eşleşme buldu. Eşleşmeler afinite × güven puanına göre sıralanır ve ilk 8'i alınır:

| Sıra | Üçlü | Güven | Akıbet |
|---|---|---|---|
| 1–8 | dede(21,27) (zaten havuzda olan üçlünün başka ebeveynlerle kopyaları) | 0,96–0,98 | sınırın içinde; sonra C kuralı "yeni dayanak yok" deyip attı |
| 9–11 | **dede(19,27)** | 0,88 | **hücre sınırıyla atıldı** |

Sonuç olarak hücre o turda hiçbir şey yazmadı. Sekiz yeri, C'nin zaten atacağı kopyalar doldurdu.

Sonra olanlar:

- **4. tur:** Yarı-naif eşleşme yalnız bir önceki turda yazılan kayıtlara bakar. dede(19,27)'nin ebeveynleri yeni olmadığı için bu eşleşme yeniden denenmez. Yeni kayıt çıkmaz ve birinci impasse olur: eşik düşer, bütün havuz yeniden denenir.
- **5. tur:** Aynı hücre bu kez 12 eşleşme buldu. dede(19,27) 10.–12. sırada, yine sınır dışında kaldı. İkinci impasse oldu, döngü durdu, cevap "bilmiyorum" çıktı.

Öteki olası nedenler:

- **Eşik değil:** iki halkanın afinitesi 1,0 / 1,0, θ = 0,5.
- **Bütçe değil:** turda en çok 178 eşleşme vardı (bütçe 1024); bütçe atması hiç olmadı.
- **Farklı kişi şartı değil:** sınırsız kapanış bu şartla kuruldu ve kaydı içeriyor.
- **C değil:** dede(19,27) hiç C'ye ulaşmadı.
- **Eşleşme değil:** eşleşme bulundu ve ateşleme günlükte var.

## 3. 14 hatanın hepsi

Kapanış, DNA'yla sınırsız sembolik kapanıştır: afinite yok, sınır yok, farklı kişi şartı var. Her satırda ilk eksik kayıt cevap kaydının kendisi ve kapanışın 3. turunda. Çekirdek onu 3. turda buldu ama hücre sınırıyla attı.

| Tohum | Bölüm | İlk eksik kayıt (= cevap) | Kapanış turu | Hücre | Hücredeki sıra (sınır 8) | Çekirdeğin durması | Kapanışta yeni kayıt çıkan son tur |
|---|---|---|---|---|---|---|---|
| 7 | `a7cd33dc162a` | (4, 'anne', 29) | 3 | baba_es_anne | 11 | impasse, tur 5 | 3 |
| 7 | `f20f1841cf2d` | (20, 'yeğen', 19) | 3 | kiz_kardes_ogul_yegen | 10 | impasse, tur 5 | 3 |
| 8 | `d5fe8563cbda` | (0, 'teyze', 3) | 3 | anne_kiz_kardes_teyze | 12 | impasse, tur 5 | 3 |
| 9 | `afe84f5f0594` | (53, 'torun', 9) | 3 | kiz_ogul_torun | 11 | impasse, tur 6 | 3 |
| 9 | `c850289190dd` | (14, 'teyze', 31) | 3 | anne_kiz_kardes_teyze | 9 | impasse, tur 5 | 3 |
| 9 | `cedede6ce548` | (19, 'dede', 27) | 3 | anne_baba_dede | 9 | impasse, tur 5 | 3 |
| 10 | `45945f1d94ca` | (52, 'dayı', 69) | 3 | anne_erkek_kardes_dayi | 9 | impasse, tur 6 | 3 |
| 10 | `77c806d8805e` | (15, 'anneanne', 34) | 3 | anne_anne_anneanne | 10 | impasse, tur 5 | 3 |
| 10 | `976a827a1eac` | (21, 'teyze', 13) | 3 | anne_kiz_kardes_teyze | 9 | impasse, tur 6 | 3 |
| 10 | `ae47ac162d8a` | (6, 'anneanne', 31) | 3 | anne_anne_anneanne | 9 | impasse, tur 5 | 3 |
| 10 | `c18869a332ce` | (48, 'dayı', 40) | 3 | anne_erkek_kardes_dayi | 10 | impasse, tur 6 | 4 |
| 11 | `5472eb84cf75` | (23, 'teyze', 8) | 3 | anne_kiz_kardes_teyze | 22 | impasse, tur 7 | 4 |
| 11 | `a6401130a140` | (20, 'dede', 56) | 3 | anne_baba_dede | 9 | impasse, tur 5 | 3 |
| 11 | `ed9f8213d471` | (8, 'amca', 34) | 3 | baba_erkek_kardes_amca | 16 | impasse, tur 5 | 3 |

**Teşhis aracının yanılgısı (V-047):** Araç yalnız tur sınırını (×4) ve havuzu (×32) gevşetiyordu. Hücre sınırını ve bütçeyi gevşetmediği için bu hatalara "sınırdan bağımsız" dedi. ÖK-003 §1'deki "büyük olasılıkla DNA eksiği" yorumu bu yüzden yanlıştı; doğru neden hücre sınırı. §1'in metni değiştirilmedi; düzeltme ÖK-003 ekinde.

## 4. Şartnameye göre fark

sistem.md §3: "Hücre başına tur başına ≤8 **yazma**."

Bugünkü kod 8'i yazmalara değil, adaylara uyguluyor. Sınır, C kuralından (K-028) **önce** kesiyor. Bu yüzden C'nin atacağı kopyalar sekiz yazma yerini harcıyor.

- C'den önce de bir benzeri vardı: havuzda zaten bulunan (üçlü, köken) çifti yazılmaz, yine de sınırdan yer harcar. Ama asıl etki C ile geldi.
- Sıralama afinite × güven'e göre. Bu yüzden zincirden gelen, güveni biraz düşük (0,88) yeni üçlü, güveni yüksek kopyaların gerisinde kalıyor.

## 5. Karşılaştırma ölçümü (çekirdek değişmedi, geçici kopya)

Ölçülen seçenek **B:** C süzgeci hücre sınırından önce uygulanır. Böylece sınır yalnız yazılabilecek adayları sayar ("≤8 yazma"). Başka hiçbir şey değişmez: 8, bütçe, tur 8, havuz 128, θ, DNA aynı.

| Bölme (tohum 7–11) | Bugün | B |
|---|---|---|
| eğitim | 2000 | 2000 |
| uzunluk | 1980 | 1994 |
| önsel-ters | 2000 | 2000 |
| zincir-bozuk | 2000 | 2000 |
| yön ters | 573 | 573 |

Uzunlukta B'nin etkisi:

- **14 hatanın 13'ü düzeliyor.** Eskiden tur ya da havuz sınırına takılan 6 hatanın da 4'ü düzeliyor.
- **Yeni 3 hata çıkıyor:** `ef38f3e18a55` (tohum 7), `88ecd56c827e` (tohum 10), `7baa7c2839a6` (tohum 11).
- **Kalan 6 hatanın hepsi 8. turda tur sınırıyla duruyor ve havuz dolu (128):**
  - 5'inde cevap yazılıyor, sonra havuz dolunca atılıyor.
  - Birinde (`59e478a8b73f`) 8 turda cevaba hiç varılamıyor.
  - B'de C'nin yazdığı bağımsız kanıtlar daha çok yer bulduğu için havuz daha çabuk doluyor.
- Bu, ÖK-003 §3.4'te önceden belirlenmiş tur ve havuz seçiminin ölçeceği türden bir hata.

Yön ters değişmiyor (573). Oradaki hatalar çıkarılamayan sorulardan geliyor; K-029'un üreteç denetimi bunları yeni tohumlarda ayıklıyor.

Not: Bu oturumdaki ilk karşılaştırma koşusunda, "sınır 16" ve "sınır 32" seçenekleri ile geçici kopyadaki "bugünkü" ölçüm, yeniden kullanılan süreçlerde B'nin yamasını taşıdı. O sayılar geçersiz sayıldı ve kullanılmadı. Düzeltilmiş betikle "bugünkü" sonuç ilk H1 koşusuyla birebir aynı çıktı (tohum 7: 5, 10: 5, 11: 4 hata). Çekirdek belirlenimlidir.
