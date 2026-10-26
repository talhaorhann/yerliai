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
- Yeni testler: B1–B3 için 14 test modülü. Tüm takım: (mutasyon sonrası yazılacak).
- Mutasyon sınaması: (sonuç yazılacak).

## Sınır (raporlara yazılır)
Gizli sahte kural ailelerinin yazarı danışmandır; danışman kodlayıcıyla aynı model ailesindendir. Bu yüzden gizli aileler tam bağımsız bir sınama sayılmaz.

## Sıradaki adım
Adım 2: gizli dosyanın adını içeriğine dokunmadan değiştirmek ve yalnız biçim denetimini çalıştırmak (beklenen: 4 aile, 180 kural, en küçük aile 45, sha256 c8adb685…).
