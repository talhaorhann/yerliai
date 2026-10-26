# H2 durum raporu: kod yazımı bitti (K-043 adım 1)

**Tarih:** 2026-10-26. **Dal:** `asama-6`.

## Kısaca
H2'nin bütün kodu yazıldı ve sınandı. Kod yalnız geliştirme havuzunda ve küçük, anlamsız adlı yapay dünyalarda denendi. Final ve kontrol havuzları, DNA v8 ve gizli sahte kural dosyası açılmadı.

## Ne yazıldı (sade dille)
- **Kabul geçidi (aşama 1–5):** bir aday kural önce geliştirme dünyalarında sınanır (yanlış yok mu, gereksiz halkası var mı, maskeyle de tutuyor mu, rastgele bağlanmış dünyada da tutuyor mu). Sonra o tura ait taze dünyalarda, kuralın "eğer" kısmının geçtiği gözlem parçalarında sınanır. En sonda HRR çekirdeği aynı sayıları verirse ve müdahale testi geçerse kabul edilir. Yapı: **sayaç + çekirdek hakem hattı**.
- **Tur koşucusu:** adayları sırayla alır, turda en çok 200 adayı sorgular, yinelenen (zaten bilinenden çıkan) adayları uyutur, kesilirse kaldığı yerden sürer.
- **Kırmızı takım:** 4 görünür sahte aile kodla üretilir. Gizli dosyadan yalnız aile başına sayılar çıkar; içerik ve kimlik hiçbir yere yazılmaz.
- **Kalibrasyon, C, P\*, boş dünya:** önkayıttaki kurallar aynen kodlandı.
- **B2 ölçümü:** hedef kuralların sınıfları, yanlış kabul üst sınırı, "bilmiyorum" farkı, kapı kararı, makas, A3 aktarımı.
- **Z12 (B3):** iki ayrı üretici ve aktarım ölçümü yazıldı; B3 sizin onayınız olmadan çalışmaz.
- **Ön kayıt denetimi:** her koşu başında taslak, çekirdek, keşif paketi ve dosya özetleri ÖK-005 ile karşılaştırılır; tutmazsa koşu başlamaz.

## Küçük kararlarım (her biri tek satır; ayrıntı V-065, V-066)
1. Yeniden bağlama kodu önkayıt §13.6'ya uymuyordu (simetrik ilişkiyi yönlü bağlıyordu); düzelttim. Bu koddan önce hiçbir sonuç üretilmemişti. Dosya özeti ek §2'ye yazılacak.
2. Simetrik ve şemadan okunabilen kurallar yeniden bağlı ikizde de doğru kaldığı için BİLMİYORUM olur; önkayıttaki 235 paydası bunu zaten ayrı sayar.
3. Gözlem parçasında 4 dikkat dağıtıcı bağ önkayıtta mühürlü; geliştirme havuzunda en büyük parça 132 olgu çıktı, çekirdek havuzu 128. Sığmayan parça ölçülemez sayılır (BİLMİYORUM) ve sayısı raporlanır. Değeri değiştirmedim.
4. Çekirdek çok yavaştı (bir maskeli koşu 9 sn). Çekirdek koduna dokunmadan, aynı vektörleri veren önbellekli bir kod kitabı verdim: 0,6 sn, sonuç bit-aynı (test).
5. Yeni değerlendirici kodu, mühürlü "keşif paketi özeti" değişmesin diye `kesif/` dışına konuldu.
6. B1'de sorgu bütçesi yok (önkayıt: kalibrasyon bütçeden düşmez); taze dünyalar tur özetlerinde özetleriyle durur.
7. P\* akışında sahte kabul yoksa P\* sansürlüdür ve tavan 200 aday/turdur.
8. Z12 adlarındaki rakamlar şema biçimi yüzünden yazıyla yazıldı (ör. kalan_üç_eş); "altı_öte" n = 24'te tek değerli olmadığı için alan şemasında tek değerli sayılmadı.

## Sınama
- Yeni testler: B1–B3 için 14 test modülü. Tüm takım: 619 test, hepsi geçti.
- Mutasyon sınaması (koda bilerek hata sokup testlerin yakalayıp yakalamadığına bakmak): 55 mutantın 55'i yakalandı. İlk turda 2'si kaçtı: biri testin boş olmasındandı (test düzeltildi), öteki etkisiz bir değişiklikti (anlamlı bir mutantla değiştirildi).

## Sınır (raporlara yazılır)
Gizli sahte kural ailelerinin yazarı danışmandır; danışman kodlayıcıyla aynı model ailesindendir. Bu yüzden gizli aileler tam bağımsız bir sınama sayılmaz.

## Adım 2–3 (gizli dosya)
- Ad, içerik açılmadan `git mv` ile değişti (`kirmizi_gizli_v1.json`).
- Biçim denetimi beklenenle aynı: 4 aile, 180 kural, en küçük aile 45, sha256 c8adb685…565b. Özet `config_h2.json`'a yazıldı, dosya kilitlendi, ÖK-005 eki §2 eklendi; ön kayıt denetimi tutuyor.
- Geliştirme dünyalarında (A1, A2, A3) yalnız sayılar:

  | Gizli aile (sıra) | Kural | Yanlış veren | Hiç tetiklenmeyen |
  |---|---|---|---|
  | 1 | 45 | 45 | 0 |
  | 2 | 45 | 45 | 0 |
  | 3 | 45 | 45 | 0 |
  | 4 | 45 | 44 | 0 |

  Hiçbir aile 40'ın altına düşmedi; kırmızı takımda etkin gizli kural 179 (4. ailedeki bir kural geliştirme dünyalarında yanlış vermiyor; ayrı raporlanacak, sahte sayılmayacak).

## Sıradaki adım
Adım 4: B1'in otomatik koşusu (C, görünür kırmızı takım, boş adaylar, K kalibrasyonu, gizli kırmızı takım, P\*, boş dünya koşuları). Uzun sürecek (boş koşular baskın); her evre diske yazılır.
