# H2 B1 raporu: DUR (boş-dünya tetiği)

**Tarih:** 2026-10-31. **Dal:** `asama-6`. **Önkayıt:** ÖK-005 ve ekleri §1–§3.

## Kısaca
B1 önkayıttaki başarı aralığının **dışında** kaldı. Kırmızı takım temiz (kaçak 0) ve K seçildi. Ama yapısı bozulmuş "boş" dünyalarda geçit kural kabul etti; önkayıta göre bu bir tetiktir. Talimatınız gereği durdum: **B2a ve B2b yapılmadı**, final ve kontrol havuzları ve DNA v8 açılmadı.

## Sonuçlar (sayılar)
| Ne | Sonuç | Eşik | Durum |
|---|---|---|---|
| Kırmızı takım | 339 sahte (160 görünür + 179 gizli), kaçak 0; alt sınır 0,9912 | ≥ 0,98, kaçak 0 | geçti |
| K değerleri | τ 0,85, müdahale 0,9, T 0,04, σ 0,01 (başlangıç kaldı) | kalibrasyon kuralı | seçildi |
| Talep C | 22 → turda 200 aday | — | — |
| P\* | > 4800 (sansürlü) | — | — |
| Boş dünya | koşu 1: 190 kabul, koşu 2: 187 kabul (okunur sınıf dışında) | 2 koşuda kabul → tetik | **tetiklendi** |

## Neden durdu (sade dille)
- "Boş dünya", gerçek dünyanın bağları karıştırılmış hâlidir; akrabalık yapısı bozulur. Ama karıştırma, her bağın tersini (ör. dede ↔ torun) ve kişinin cinsiyetini korur.
- Geçidin boş dünyada kabul ettiği 377 kuralın hepsi şu türden: "Y, X'in torunu ve Y erkek (ör. birinin babası) → Y, X'in dedesi". Yani başı, gövdedeki tersinden ve bir cinsiyet tanığından okuyor.
- Bu kurallar gerçek dünyada da doğrudur, ama aile yapısını değil "ters + cinsiyet" bilgisini kullanır.
- Önkayıttaki "şemadan okunabilir" istisnası yalnız tek halkalı ters kuralları kapsıyor; bu 2–3 halkalılar istisnaya girmiyor. Bu yüzden tetik doldu.

## İkinci bulgu (B2'yi etkileyecek)
- Çekirdek her turda bir kural için en çok 8 sonuç yazar (mühürlü H1 değeri). Çok eşleşen kurallarda (ör. kuzen) maskelenen olguyu bazen türetemez, sembolik sayımla uyuşmaz; önkayıt gereği bu kurallar BİLMİYORUM olur.
- Kalibrasyondaki ilk 200 adayın çekirdeğe ulaşan 6'sı bu yüzden düştü. Bu nedenle K başlangıçta kaldı.
- Tanı (yalnız geliştirme havuzu): her baş ilişkisi için birer temsilci kuralın 22'sinden 21'i tam uyumlu.

## Bu aşamada bulduğum ve düzelttiğim hatalar (hiçbir hüküm etkilenmeden, test önce; ÖK-005 ek §2a–§2e)
1. Sembolik tanık sayımı iki adımlıydı, önkayıt §13.2 tek adım diyor. Düzeltildi ve kalibrasyon yeniden yapıldı.
2. Boş akışta ölçülecek aday olmayınca bir anahtar hatası çıkıyordu.
3. Tetik sayımına obiterle sıraya giren okunur kurallar karışabiliyordu.
4. Yeniden başlatmada "görülen aday" kümesi yanlıştı; B2'nin kaldığı yerden sürmesini bozardı.

## Karar gereken (önkayıtta yazmıyor; sizin kararınız)
Önkayıt §9 madde 3 "en çok 2 onarım turu" diyor, ama onarımın ne olacağını söylemiyor. Seçenekler:
- **(a)** Sonucu olduğu gibi kabul edin: H2 bu önkayıtla B1'de durdu (negatif sonuç, aynı biçimde raporlanır).
- **(b)** Onarım: "şemadan okunabilir" sınıfını "başı gövdedeki tersinden okuyan bütün kurallar" olarak genişletmek. Boş dünyada kabul edilenlerin hepsi bu sınıfta. B2'de bu kurallar yine kabul edilebilir ve ayrı sayılır.
- **(c)** Onarım: boş dünya dönüşümünde cinsiyeti de karıştırmak. Böylece "ters + cinsiyet" kuralları boş dünyada yanlışlanır.
- (b) ve (c) önkayıt değişikliğidir: ek olarak yazılır ve B1 baştan koşar (boş koşular ~100 × 40 dk).
- İsterseniz yazma sınırı bulgusu için de ayrıca karar verebilirsiniz; önerim, mühürlü değeri değiştirmeden sonucu raporlamak.

## Sınır
Gizli sahte kural ailelerinin yazarı danışmandır; danışman kodlayıcıyla aynı model ailesindendir. Bu yüzden gizli aileler tam bağımsız bir sınama sayılmaz.

Ham dosyalar: `raporlar/h2_b1/`. Yapı: sayaç + çekirdek hakem hattı.
