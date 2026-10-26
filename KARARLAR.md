# KARARLAR

Kullanıcının onayladığı kararlar. Onaylı varsayımlar `VARSAYIMLAR.md`'den buraya taşınır.
Biçim: kimlik, tarih, karar, gerekçe, etkisi.

## K-001 (2026-10-23): "Bu turda prototip kod yazılmayacak" satırı geçersiz
- **Karar:** `sistem.md` "Fikir sahibinin kuralları" altındaki "BU TURDA PROTOTİP KOD YAZILMAYACAK" satırı eski kâğıt üstü tasarım turuna aittir, artık geçerli değildir. Kodlama `KODLAMA_PROMPTU.md` bölüm 4'teki aşama sırasıyla (A0'dan başlayarak) yapılır.
- **Onaylayan:** kullanıcı.
- **Etkisi:** tüm aşamalar. `sistem.md` değiştirilmedi.

## K-002 (2026-10-23): Eski ara dosya atıfları yok sayılır
- **Karar:** `sistem.md` Ek A–D içindeki `cozumler.md`, `bulgular.md` ve `/tmp/...` klasör atıfları eski ara dosyalardır. Gerekli değildir, yok sayılır.
- **Onaylayan:** kullanıcı.

## K-003 (2026-10-23): Çelişkide sistem.md Kısım 1 kazanır
- **Karar:** Ek'ler ile Kısım 1 (§1–19) çelişirse Kısım 1 kazanır (`sistem.md` başlığındaki kuralın kullanıcı tarafından teyidi).
- **Onaylayan:** kullanıcı.

## K-004 (2026-10-23): Çekirdek kayıtlarında saat yerine adım numarası (V-006'dan)
- **Karar:** Çekirdek kayıtlarında gerçek saat (duvar saati) kullanılmaz. Zaman bilgisi mantıksal saattir: sıra/adım/tur numarası. Gerçek saat yalnız çekirdek dışı kayıtlarda (besleme, tercüman) durabilir ve hash, karşılaştırma ve bağımsızlık testi dışında tutulur.
- **Gerekçe:** aynı girdi ve tohum çekirdekte bit düzeyinde aynı çıktıyı vermeli (KODLAMA_PROMPTU §5, sistem.md §16).
- **Onaylayan:** kullanıcı.
- **Etkisi:** `cekirdek/altyapi/olay_gunlugu.py` (zaman alanı yok, sıra numarası var; değişiklik gerekmedi). A1'den itibaren tüm çekirdek veri kayıtları.

## K-005 (2026-10-23): A1'e bağımsız inceleme beklenmeden geçildi
- **Karar:** Kullanıcı, A0 bağımsız incelemesini beklemeden A1'e başlanmasını istedi. İnceleme istemi (`inceleme/A0_istemi.md`) hazır durur ve sonra koşturulabilir.
- **Onaylayan:** kullanıcı.
- **Etkisi:** KODLAMA_PROMPTU §4 "Bağımsız inceleme" adımı A0 için ertelendi.

## K-006 (2026-10-23): İlişki şeması sürüm 1 onaylandı (V-013'ten)
- **Karar:** `sema/iliskiler_v1.json` (21 ilişki, okuma "(A, r, B) = B, A'nın r'sidir") kullanıcı tarafından onaylandı ve `kilit/sema_onayi.json` ile hash kilidine alındı. Dosyadaki "TASLAK" notu, onaylanan baytları değiştirmemek için olduğu gibi bırakıldı.
- **Onaylayan:** kullanıcı. Hata çıkarsa yeni sürüm (`iliskiler_v2.json`) ve yeni onayla düzeltilir.

## K-007 (2026-10-23): Üreteç tasarımı onaylandı (V-015'ten)
- **Karar:** V-015'teki öneri: üreteç `degerlendirme/` altında, soyut ağaç (tamsayı kişi, iki tip, yukarı/aşağı/eş bağı), ilişkilerin yapısal tanımları gizli veri dosyasında, olgular yalnız doğrudan bağlar, ağacın geri kalanı dikkat dağıtıcı, A1'de isim yok, cevaplar ayrı dosyada.
- **Onaylayan:** kullanıcı.

## K-008 (2026-10-23): Kelime çantası kuralı onaylandı (V-016'dan)
- **Karar:** dedektörün çözdüğü örnekler ayrı "Treg kümesine" ayrılır (sistem.md §10). Kalan ana kümede kelime çantası sınıflayıcısının doğruluğu şans + %5'i geçerse üretim durur (KODLAMA_PROMPTU §6). Şans = en sık cevabın oranı. Dedektör: yapıya bakmayan, yalnız ilişki adı sayıları ve kişi kimlikleri kullanan Naive Bayes; ayrı bölmede eğitilir, başka bölmede ölçülür.
- **Onaylayan:** kullanıcı.

## K-009 (2026-10-23): Gizli yapısal tanımlar sürüm 1 onaylandı (V-019'dan)
- **Karar:** `degerlendirme/veri/tanimlar_v1.json` (okunur hâli `TANIMLAR_OKUNUR.md`) onaylandı ve hash kilidine alındı (`kilit/kilitler.json`). Hata çıkarsa yeni sürümle düzeltilir.
- **Onaylayan:** kullanıcı.

## K-010 (2026-10-23): "Önsel-ters" bölmesinin tanımı (V-020'den)
- **Karar:** önsel-ters bölmesinde cevap dağılımı eğitimdekinin tersidir: eğitimde nadir olan cevaplar burada sık, sık olanlar nadir olur.
- **Onaylayan:** kullanıcı.

## K-011 (2026-10-23): Altın küme yolu (V-021'den)
- **Karar:** Üreteçten ayrı tohumla 100 soru hazırlanır, iki parça (50 + 50). Kullanıcı üretecin cevabını görmeden cevaplar. Biçim: her soruda A/B/C/D seçeneği. Altın kümede "beklenen" cevap kullanıcının cevabıdır, kodun çıktısı beklenen diye kaydedilmez. Kullanıcı ile üretecin uyuşmadığı sorular ayrıca incelenir.
- **Onaylayan:** kullanıcı.

## K-012 (2026-10-23): PyTorch ve NumPy çekirdekte izinli (V-005'ten)
- **Karar:** Çekirdek PyTorch ve NumPy kullanabilir. Sürümler sabittir: torch==2.14.1, numpy==2.5.3. Lisanslar `LISANSLAR.md`'de, resmî dosyalardan doğrulanmıştır.
- **Ek karar:** Çekirdek önce CPU/tamsayı yolunda deterministik yazılır. GPU ayrı aşamada, ayrı doğrulamayla açılır (KODLAMA_PROMPTU §10 bilinen boşluğun cevabı).
- **Onaylayan:** kullanıcı.

## K-013 (2026-10-23): Altın küme 1. parça cevaplarının kaynağı
- **Karar:**
  - 1. parça cevapları bir LLM'in ön cevabıdır. Kullanıcı gözden geçirip kabul etmiştir.
  - Kayıt: `kaynak=LLM, onaylayan=kullanıcı, bagimsiz_insan_cevabi=false` (`degerlendirme/altin/kullanici_cevaplari_1.json`, sha256 306ee0a0c54d3d6972695ae8a0c8c14e8dff12e2d6ef084884a9fd345a5c45ff).
  - Bağımsızlık kısıtı `ONKAYIT.md`'ye eklendi.
- **Onaylayan:** kullanıcı.

## K-014 (2026-10-23): A2 vektör temsili onaylandı (V-024'ten)
- **Karar:** d = 256, öğeler ±1 tamsayı. Bağlama tamsayıyla tam dairesel evrişimdir. Kayıt vektörü v = 16·R[r] + P_s⊛E[s] + P_o⊛E[o]. Kosinüs benzerliği tamsayı nokta çarpımından hesaplanır. Vektörler (tohum, tür, ad) hash'inden üretilir.
- **Onaylayan:** kullanıcı.

## K-015 (2026-10-23): PyTorch hızlı yolu A5 öncesine ertelendi
- **Karar:** Ağ izni şimdilik yok (V-025). A2 yalnız saf Python tamsayı referans yoluyla kapanır. PyTorch hızlı yolu ve referansla bit-eşitlik testi A5 (H1) öncesine bırakılır. Bu sırada hız iddiası yazılmaz.
- **Onaylayan:** kullanıcı.

## K-016 (2026-10-23): Eşleşme, afinite ve güven (V-028'den)
- **Karar:**
  - İlişki geni sert süzgeçtir.
  - Afinite = kırp(kosinüs(alıcı, kayıt) · √3, 0, 1). Elle yazılan hücrede alıcı = 16·R[gen].
  - Halka afinite > θ ise eşleşir. Elle yazılan hücrelerde θ = 0,5.
  - Güven = min(afiniteler, ebeveyn güvenleri) × hücre güvenilirliği. Elle yazılan hücrede güvenilirlik 1.
  - Hücre başına tur başına en iyi 8 eşleşme yazılır. Tur bütçesi 1024.
- **Onaylayan:** kullanıcı.

## K-017 (2026-10-23): Durma ve impasse (V-029'dan)
- **Karar:**
  - Kalibrasyon kümesi oluşana kadar τ ile durma kapalı. Döngü yeni kayıt kalmayınca ya da 8 turda durur.
  - Impasse'te (yanıt yok, yeni kayıt yok) bütün θ'lar bir kez yarıya iner. İkinci impasse'te durur.
- **Onaylayan:** kullanıcı.

## K-018 (2026-10-23): Plazma hücresi (V-030'dan)
- **Karar:**
  - Kök kümesi kesişen ispatlar aynı bileşendedir. Bileşen içi MAX, bileşenler arası noisy-OR, sızıntı 0.
  - Cevap, en yüksek birleşik güvenli ilişkidir. İspat yoksa ya da en yüksekte eşitlik varsa "bilmiyorum".
  - Farklı ilişkilere giden ispatlar "çelişki" diye işaretlenir.
  - Gerekçe, köken DAG'ından verilir.
- **Onaylayan:** kullanıcı.

## K-019 (2026-10-23): Havuzdan atma; yayın sahnesi ertelendi (V-031'den)
- **Karar:**
  - Havuz dolunca çıkarım katmanından en düşük güvenli kayıt atılır. Eşitlikte en yaşlı, sonra en küçük kimlik.
  - Yayın sahnesi H3/H4'e kalır. A3'te eşleşme bütün havuzda yarı-naif yapılır.
- **Onaylayan:** kullanıcı.

## K-020 (2026-10-23): Çelişkinin tanımı ve etkisi (V-036'dan)
- **Karar:**
  - Çelişki türleri (onaylı şemaya göre):
    - **dışlayıcı:** aynı çiftte aynı dışlayıcı gruptan iki ilişki;
    - **işlevsel:** aynı özne, aynı işlevsel ilişki, iki farklı nesne;
    - **ters:** r(A,B) ile q(B,A), q ∉ ters(r).
  - Denetim her tur sonunda canlı kayıtlarda yapılır, epitoplar dahil. Hiçbir kayıt silinmez. `CELISKI` olayı iki kaydı ve ortak destek kümesini (kök kümelerinin kesişimi) kalıcı kaydeder.
  - Cevap K-018'deki gibi verilir. Çelişki cevabın köken alt grafına dokunursa müdahale puanının c bileşeni 0 olur.
- **Onaylayan:** kullanıcı.

## K-021 (2026-10-23): Müdahale testi ve puanı (V-037'den) + kullanıcının ek şartı
- **Karar:**
  - **(a)** Kök epitop silme (yalnız etkilenen köken alt grafı). a = güveni düşüren silmelerin oranı.
  - **(b)** İlgisiz epitopu tür uyumlu yedekle değiştirip yeniden koşma. b = cevabın değişmediği oran.
  - **(c)** Ters tutarlılığı ve çelişkisizlik. c ∈ {0, 1}.
  - **Puan** = a × b × c. Cevap yoksa puan yok. Geçişlilik sınanmaz (şemada bilgi yok).
- **Ek şart (kullanıcı):** (b) için ilgisiz epitop yoksa soru "sınanamadı" olur. Başarı sayılmaz: b ve puan boş kalır. H1 raporunda ayrı bir sayı olarak gösterilir (ör. "100 soruda 18 sınanamadı").
- **Onaylayan:** kullanıcı.

## K-022 (2026-10-23): PyTorch CPU sürümü kurulumu
- **Karar:** torch 2.14.1+cpu (`download.pytorch.org/whl/cpu`) ve CPU bağımlılıkları hash'leriyle sabitlenir (`gereksinimler.txt`). GPU (CUDA) sürümü gerekirse ayrıca konuşulur. Hızlı yol referansla bit düzeyinde aynı olmalıdır (K-015).
- **Onaylayan:** kullanıcı (ağ izni verildi).

## K-023 (2026-10-23): H1 ön kaydı (ÖK-002)
- **Karar:** `ONKAYIT.md` ÖK-002 metni H1'in ön kaydıdır ve kilitlenir. Kapı: kapıya giren her bölmede (uzunluk, yön ters, önsel-ters, zincir-bozuk) ve her tohumda (7–11) doğruluk %100, tolerans yok. DNA yalnız eğitim bölmesinde geliştirilir, test bölmeleri kilitli DNA ile bir kez koşar. Yeniden adlandırma bölmesi H2'ye kalır. Müdahale puanı raporlanır, kapıya girmez; "sınanamadı" ayrı sayılır (K-021).
- **Onaylayan:** kullanıcı.

## K-024 (2026-10-23): H1 DNA'sını bağımsız danışman yazar
- **Karar:** Akrabalık DNA'sını gizli tanımları (`degerlendirme/veri/tanimlar_v1.json`) görmemiş bağımsız bir danışman yazar. Danışmana yalnız onaylı ilişki listesi (adlar, cinsiyet, ters ilişki bilgisi, okuma yönü, dünya varsayımları, DNA biçimi) tek dosya olarak verilir: `DANISMAN_ICIN_ILISKI_LISTESI.md`. Kuralları kullanıcı getirir ve onaylar. Kayıt: kaynak=LLM (bağımsız danışman), onaylayan=kullanıcı.
- **Onaylayan:** kullanıcı.

## K-025 (2026-10-23): DNA'da isteğe bağlı "farklı kişi" şartı
- **Karar:** DNA biçimine (sürüm 2) isteğe bağlı bir şart eklenir: bir hücrede belirtilen değişken çiftleri farklı varlıklara bağlanmalıdır. Şartı olmayan hücreler önceki gibi çalışır (değişkenler aynı varlığa bağlanabilir). Gerekçe: şart yokken çekirdek r1(1,2), r2(2,1) olgularından r3(1,1) yazdı (denendi).
- **Onaylayan:** kullanıcı.

## K-026 (2026-10-24): Havuz kapasitesi 64 → 128 (ÖK-002a)
- **Karar:** `havuz_kapasitesi` 128. sistem.md §2 "Kapasite 64" der; bu, kullanıcının bilerek verdiği bir sapma kararıdır, sistem.md değiştirilmez. ÖK-002 §2'deki "havuz 64" ÖK-002a ile 128 olur; ön kaydın geri kalanı (kapı %100, tolerans yok, bölmeler, tohumlar) aynen geçerlidir.
- **Gerekçe (kullanıcının ilettiği):** bağımsız danışmanın kendi simülasyonunda k=10 zincirlerde havuz 64 yetmedi (doğru %56–71, kaçan %18–36); 128'de doğru %89–92, kaçan ~%0.
- **Zamanlama:** test bölmeleri gerçek DNA ile hiç koşturulmadan ve DNA eğitim bölmesinde denenmeden önce.
- **Onaylayan:** kullanıcı.

## K-027 (2026-10-24): H1 DNA'sı onaylandı (9 grup)
- **Karar:** `veri/dna/akrabalik_dna_v2_final.json` (170 kural, sha256 `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e`) H1 DNA'sıdır. Kullanıcı 9 grubun (`veri/dna/AKRABALIK_DNA_GRUPLARI.md`) tümüne tek "evet" verdi. Kaynak: bağımsız danışman (LLM, K-024); beş bağımsız gözetmen "yanlış türetme yok" dedi; onaylayan: kullanıcı.
- **Kural:** Eğitim bölmesinde hata çıkarsa düzeltmeyi danışman yapar, kodlayıcı yapmaz. DNA, eğitimde %100'e ulaşınca ÖK-002 ekiyle kilitlenir; test bölmeleri ondan sonra açılır.
- **Onaylayan:** kullanıcı.

## K-028 (2026-10-24): Kopya kuralı C (V-046'dan)
- **Karar:** Aynı üçlünün yeni kökenli kaydı yalnız **yeni dayanak** getiriyorsa yazılır. Adayın dayanağı = ebeveynlerinin kök kümelerinin (dayandığı olguların) birleşimi. Aynı üçlünün havuzdaki canlı, izli (defterde YAZMA izi olan ya da bu turda döngünün yazdığı) bir çıkarımının kök kümesi bu dayanağın alt kümesiyse aday yeni dayanak getirmez, yazılmaz; tur başına sayısı `ESLESME_ATILDI` (dayanak_yok) olarak kaydedilir. Epitoplar ve izsiz kayıtlar ispat sayılmaz.
- **Gerekçe:** Eğitim bölmesi ölçümü (tohum 7, ilk 60 bölüm; test bölmeleri açılmadı): bugünkü hâl 33/60, A 55/60, B 60/60, C 60/60. B bağımsız ikinci ispatı da sildiği için müdahale testinin (a) ve (b) kısımlarını anlamsızlaştırıyor; C kök-ayrık ispatları koruyor.
- **Onaylayan:** kullanıcı.

## K-029 (2026-10-24): H1 yeniden deneme (ÖK-003)
- **Karar:** İlk H1 koşusu (ÖK-002) kapıyı geçmedi; sonuç ve raporları silinmez. Yeniden deneme ÖK-003 ile yapılır. Kullanıcının üç şartı:
  1. Üreteçte "cevap olgulardan çıkarılabilir" denetimi çekirdekten bağımsızdır: olguların izin verdiği bütün cinsiyet atamalarında aynı cevap çıkmalı. Soru, çekirdeğin cevap verip vermediğine bakılarak seçilmez.
  2. ÖK-003 ilk koşunun sonucunu, nedenlerini ve tarihini açıkça içerir.
  3. Tur ve havuz sınırları eski test bölmelerinde (artık geliştirme verisi) belirlenir, yeni koşudan önce kilitlenir. sistem.md §5 (8 tur) ve §2 (64) değerlerinden sapma bu karara dayanır.
- **Ek:** Danışman, ilk koşunun 14 sınırdan bağımsız uzunluk hatasını (olgular, soru, cevap) görür (`raporlar/H1_ilk_kosu_uzunluk_14_hata.md`). Eski bölümler artık geliştirme verisidir.
- **Onaylayan:** kullanıcı.

## K-030 (2026-10-24): Kısa yol kapısında duran tohumun değişimi (V-050'den)
- **Karar:** H1 yeniden denemesinde bir tohumun üretimi kısa yol kapısında (K-008) durursa, yerine kullanılmamış ilk tohum geçer: ön kayıt ve geliştirme tohumlarının en büyüğünden sonraki ilk sayı; o da durursa bir sonraki.
  - Eşik (şans + 0,05) gevşetilmez.
  - En çok 3 değişim (`h1_tohum_degisim_siniri`); aşılırsa üretim durur, karar kullanıcıya gelir.
  - Kapı dışındaki durmalar değişim sebebi değildir.
  - Her değişim tarih ve nedeniyle ÖK-003 ekine yazılır. Kullanılan tohumlar üretim klasöründe `tohumlar.json`'a yazılır; kapı koşusu tohumları buradan alır ve bu dosyanın özeti ön kayıt ekinde aranır.
- **Ek:** V-050 (önsel-ters bölmesinde kelime çantası sızıntısı) üreteç açığı olarak incelenir.
- **Onaylayan:** kullanıcı.

## K-031 (2026-10-24): Kopya kuralı C hücre sınırından önce (V-051'den)
- **Karar:** Her turda bir hücrenin eşleşmeleri önce C ile süzülür (turun başındaki havuz ve defterle): yeni dayanak getirmeyen aday sınırdan yer almaz. Sonra hücre başına en iyi `hucre_tur_yazma_siniri` (8) aday, sonra tur bütçesi uygulanır. Yazma sırasında C, bu turda yazılanlarla birlikte bir kez daha denetlenir. "Dayanak yok" sayısı turda tek olay olarak kaydedilir. Böylece sınır, sistem.md §3'teki gibi yazmaları sayar. Başka ayar değişmez.
- **Gerekçe:** İlk koşunun 14 uzunluk hatasının 14'ünde, sınırın içindeki yerleri C'nin atacağı kopyalar dolduruyordu; cevap üçlüsü sınır dışında kalıp bir daha denenmiyordu (`raporlar/H1_hucre_siniri_izleme.md`). Geliştirme verisinde geçici kopyayla ölçüldü: eğitim 2000/2000, uzunluk 1980 → 1994, öteki bölmeler aynı.
- **Ön kayıt:** ÖK-003 §3.5 "diğer bütün ayarlar aynen kalır" dediği için ÖK-003 ekinde ayrıca yazıldı.
- **Onaylayan:** kullanıcı.

## K-032 (2026-10-24): H1 yeniden deneme sonucu kabul; A6'ya geçiş; ÖK-004 ertelendi; H2 kapısı
- **Kayıt:** "H1 iki kez kapıyı geçmedi. İkinci koşuda uzunluk, önsel-ters, zincir-bozuk bölmeleri 5 tohumda 2000/2000, yön ters 1881/2000 (ilk koşuda 573/2000). Yanlış ilişki iki koşuda da 0. 119 hatanın hepsi 'bilmiyorum'; 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanmasından. H1 resmen KANITLANMAMIŞTIR; çekirdek lehine güçlü kanıt vardır."
- **Karar:**
  1. ÖK-003 sonucu olduğu gibi kabul edildi; H1 "geçti" diye işaretlenmez.
  2. Kullanıcı kararıyla A6'ya (bellek geçidi + iç dil) geçilir. Bu, KODLAMA_PROMPTU'daki "bir aşama kapısı geçmeden sonrakini başlatma" kuralına kullanıcının koyduğu istisnadır.
  3. ÖK-004 ertelendi, iptal edilmedi. H2'ye geçmeden önce V-053 kapanır. Yeni tanım: olgular + dünya varsayımlarının zorunlu kıldığı yapı verilir; cinsiyetlerin bütün olası atamalarında aynı cevap çıkıyorsa soru çıkarılabilirdir; olgularda olmayan ve varsayımlardan da çıkmayan bilgi kullanılmaz. Tanım çekirdekten bağımsız kaba kuvvetle ve üç kümede (113, 6, 27) sınanır, kullanıcı onayına gelir. Sonra H1 taze tohumlarla tek sefer yeniden koşar; tohum değişim hakkı 2.
  4. **H2 kapısı:** V-053 kapanmadan ve H1 taze tohumlarla yeniden koşulmadan H2 çalıştırma komutu "V-053 açık" diye reddeder. Bu kuralı kapatan ya da gevşeten kod yazılmaz.
  5. Altın küme 2. parça cevapları H1 yeniden koşusundan önce gelir. Aşama sonu bağımsız inceleme A6 sonunda yapılır.
- **Onaylayan:** kullanıcı.

## K-033 (2026-10-24): H1 durumunun güncel kaydı ve sıra
- **Kayıt:** "H1 iki kez kapıyı geçmedi. İkinci koşuda uzunluk, önsel-ters ve zincir-bozuk bölmeleri 5 tohumda 2000/2000, yön ters 1881/2000 (ilk koşuda 573/2000). Yanlış ilişki iki koşuda da 0. 119 yön ters hatasının hepsi 'bilmiyorum'; 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanmasından, 6'sı DNA'da silinmiş 6 kuraldan. H1 resmen KANITLANMAMIŞTIR; çekirdek lehine güçlü kanıt vardır."
- **Karar:**
  - H1 "geçti" diye işaretlenmez. Tohum değişim hakkı 2.
  - Sıra: (1) A6 tamamlanır. (2) DNA "son sürüm" gelince V-053 tanımı üretece bağlanır; ÖK-004 yazılır, ilk iki koşunun sonucunu ve nedenlerini içerir; DNA ve config özetleri eklenir, kilitlenir. (3) H1 taze tohumlarla tek sefer koşar; bu, bu tür kapı koşusunun son denemesidir; geçmezse durulur ve kapsamlı karar kullanıcıya gelir; eşik gevşetilmez. (4) H2 kapısı korunur (K-032 §4).
  - DNA: danışmanın 176 kurallı sürümü depoya konur ve önceki 170 kurallı sürümle kimlik kimlik karşılaştırılır. Danışman "son sürüm" demeden kilitlenmez (danışman bağımsız bir çıkarılabilirlik kâhiniyle boşluk taraması yapıyor).
- **Onaylayan:** kullanıcı.
- **Not (2026-10-25, kodlayıcı):** Gelen ek v8 ve 244 kurallı (`veri/dna/akrabalik_dna_v8.json`); 170 eski kural aynen içinde, 74 yeni kural. Karşılaştırma: `raporlar/DNA_v8_karsilastirma.md`. Kilitli değil.

## K-034 (2026-10-24): Çıkarılabilirlik tanımı (V-053'ten)
- **Karar:** V-053'teki tanım onaylandı. Dünya verilmez; olgular ve üç dünya varsayımı kullanılır: her kişinin ya hiç ebeveyni yoktur ya da birbiriyle evli iki ebeveyni vardır; en çok bir evlilik; evli çiftler karşı cinsten. Bunların zorunlu kıldığı yapıda cinsiyetlerin bütün atamalarında cevap aynıysa soru çıkarılabilirdir. Üretece DNA "son sürüm" gelince bağlanır (K-033).
- **Onaylayan:** kullanıcı.

## K-035 (2026-10-24): Bellek geçidinin kanıt kaynağı (V-054'ten, seçenek A)
- **Karar:**
  - Geçit etiket ve kâhin kullanmaz.
  - Eğitim verisine, kâhin etiketi olarak değil bağımsız gözlem olarak, olgu şeklinde geçen türetilmiş ilişkiler (dede, amca, …) eklenir.
  - Geçit bir kuralı değerlendirirken kuralın tahmin ettiği olgu maskelenir; kural kendi kendini onaylayamaz.
  - Doğruluk hesabı çekirdek dışındadır (`degerlendirme/`, kâhine dokunmadan); çekirdek yalnız ham çıktısını verir ve eşikleri uygular.
  - Bağımsızlık testi (LLM'siz, sahte LLM'li, başka LLM'li) bit düzeyinde aynı sonucu vermelidir (sistem.md §16).
- **Onaylayan:** kullanıcı.

## K-036 (2026-10-24): Bellek eşikleri (geçici), iç dil, bellek deposu (V-054, V-055, V-056'dan)
- **Karar:**
  - Eşikler onaylandı ama GEÇİCİ: doğruluk 1,0; en az 3 kanıt; müdahale 0,9. H2 kalibrasyonunda yeniden bakılacak.
  - İç dil sürüm 1 (V-055) onaylandı.
  - Bellek deposu (V-056: yalnız ekleme, hash zinciri, geri alma) onaylandı.
  - Bozuk 73 kuralın reddedilmeyen 3'ü raporlanır.
- **Onaylayan:** kullanıcı.

## K-037 (2026-10-25): Bellek geçidinde müdahale puanı b·c (V-058'den)
- **Karar:** Bellek geçidinde müdahale puanı yalnız b·c'dir (b: ilgisiz bilgi değişince cevap aynı mı; c: ters ilişki ve çelişki tutarlılığı). (a) bileşeni ölçülmeye ve kanıtta saklanmaya devam eder ama eşiğe girmez. H1'deki müdahale testi (K-021) değişmez.
- **Koşul:** H2'de bozuk bir kural kabul edilirse bu karar yeniden açılır.
- **Gerekçe:** Gözlemli veride aynı cevap çoğu kez birden çok bağımsız yoldan çıkıyor; bir kök silinince öteki yol kaldığı için (a) düşüyor. Gerçek DNA v8 gösteriminde 45 doğru kural yalnız bu yüzden "kısayol" sayıldı; hepsinde iki ortamda doğruluk 1,0 idi. b·c ile 114 doğru kural kabul, bozuklarda sonuç aynı (93 yanlış, 0 kabul) (`raporlar/A6_gosterim_v8.md`).
- **Etkisi:** `cekirdek/bellek_gecidi.py` `maskeli_kos` (geçit puanı b·c; a, b, c ve a·b·c ham çıktıda), `degerlendirme/gozlem_puani.py` (`mudahale` = b·c, `mudahale_a`, `mudahale_abc` kanıtta). `cekirdek/mudahale.py` değişmedi.
- **Onaylayan:** kullanıcı.

## K-038 (2026-10-25): DNA v8 son sürüm ve kilit
- **Karar:** `veri/dna/akrabalik_dna_v8.json` (244 kural) son sürümdür. Kilitlendi (`config.json` `kilitli_veri_dosyalari`).
  - sha256: `4a4af6b83c58e33d9971f9d84ed6c440fbb2341d14ec70dc4710128d74bfaa75`.
  - Danışman ölçümü: 16.000 rastgele kümede yanlış türetme 0; çıkarılabilir sorulardan kaçan %0,02.
- **Kural:** Bundan sonra DNA'ya dokunulmaz. Bir sorun çıkarsa danışmana bildirilir (K-024).
- **Onaylayan:** kullanıcı.

## K-039 (2026-10-25): Danışman güncellemesi (kullanıcı iletti)
- **Kabul:** K-037, V-057 belgelemesi, K-038 (DNA v8 son sürüm), K-034'ün üretece bağlanması, ÖK-004, baskı ölçümü onaylandı. DNA'ya dokunulmaz; sorun yalnız danışmana bildirilir.
- **Tohum değişimi:** ancak danışman ve kullanıcı onayıyla. Kısa yol kapısında duran tohum artık kendiliğinden değişmez; üretim durur ve nedenini bildirir. Onaylanan tohum `config.json` `h1_onayli_tohum_degisimleri` listesine yazılır (K-030'un sınırı ve kuralı aynen; ÖK-004 §3.3'teki hak 2).
- **Altın küme 2. parça:** cevaplar kullanıcıdan gelir (danışman hazırlar, kullanıcı verir). `degerlendirme/altin/kullanici_cevaplari_2.json` depoya konmadan H1 koşmaz, bölüm üretilmez. Gelince: (a) biçim doğrulanır; (b) etiketi "LLM taslağı, kullanıcı onaylı" olan kayıtlar ayrı sayılır ve raporlanır; (c) ÖK-004 sırası izlenir, kapı tek sefer koşar.
- **H1'den sonra:** sonuca bakarak ayar yapılmaz. Kapı geçmezse durulur; sonuç ve neden bölme bazında, hata sınıflarıyla raporlanır, danışmana dönülür. H2 kapısı kapalı kalır. `asama-5-hizli-yol-dogrulanmadi` dalı silinmez.
- **Bağımsız inceleme:** sonuç gelince bulgular `raporlar/` altına kaydedilir; her bulgu için KARŞILANDI / KARŞILANMADI / düzeltme önerisi. Düzeltmeler kendi başına uygulanmaz; önce danışmana gösterilir.
- **H2 tasarım taslağı:** yalnız belge (`H2_TASARIM_TASLAGI.md`), kod yok; `FIKIRLER.md`'ye işlenir.
- **Değişmeyen kurallar:** kâhin eğitime girmez; `uretec_cevaplari.jsonl` ve `degerlendirme/altin/` cevap dosyaları açılmaz; LLM şema, tohum etiketi, kalibrasyon ya da altın küme kararı vermez; eşik sonuca bakarak değişmez; felsefi kararlar kullanıcıya sorulur.
- **Onaylayan:** kullanıcı (danışmanın metnini iletti).

## K-040 (2026-10-25): ÖK-004 sonucu yazıldı, H2 kapısı açıldı; H2 kodu koşullu
- **Karar:** "## ÖK-004 sonucu" başlığı, kapı özetinin sha256'sıyla (`935cea7b…`) ÖK-004'e yazıldı (K-032 §4). H2 kapısı açık (`degerlendirme/h2.py`).
- **Koşul:** H2 koduna başlanmaz. Önce: (a) A6 bağımsız incelemesinin sonucu; (b) H2 tasarım tartışması (danışman ve kullanıcı, literatür taraması ışığında); (c) H2 ön kayıt belgesi (yeni ÖK). Kapının açılması bunları atlamaya izin vermez.
- DNA v8, config ve ÖK-004 kilitli kalır. Kalan tohum değişim hakkı 1; onaysız kullanılmaz.
- Önsel-ters bölmesindeki iki kısa yol duruşu (tohum 15 ve 21) için teşhis notu yazılır; yalnız analiz, üreteç ve kapı değişmez; H2 tasarımına girdi olur.
- **Onaylayan:** kullanıcı ve danışman.

## K-041 (2026-10-26): H2 Kapı 0 onayı; sayaç + çekirdek hakem hattı; B0 başlar
- **Karar:** `H2_TASARIM.md` ve `ONKAYIT_H2_TASLAK.md` (ÖK-005 taslağı) onaylandı. Altı sorunun hepsine **evet**:
  1. **Geri bulma:** başka kurallarla aynı sonuçları çıkaran kural "bulundu" sayılır. Birincil oran özdeş + daha genel + kapanış-eşdeğer; biçimce özdeş olanlar ayrıca raporlanır.
  2. **Gövde-merkezli gözlem bölümü:** dünyada 8 bölüm.
  3. **Kapsam aileleri:** A1, A2, A3; en az ikisinde doğru.
  4. **Gizli sahte kurallar:** danışman yazar, kodlayıcı açmaz.
  5. **Hawaii, Iroquois, Omaha:** B3'te yalnız ölçüm; tanımları kullanıcı ya da danışman onaylar.
  6. **Z12:** on ilişkilik liste onaylı.
- **Ek kararlar:**
  - **(1) Hat yapısı:** sembolik ön eleme + HRR çekirdeği son hakem yapısı onaylı.
    - Raporlarda H2 "çekirdeğin tek başına keşfi" diye değil, **"sayaç + çekirdek hakem hattının keşfi"** diye yazılır.
    - Bu, KODLAMA_PROMPTU §2 (Özgünlük: bilinen yöntemler yalnız `karsilastirma/`) için kullanıcının açık istisnasıdır, şu sınırlarla:
      - sayaç ve M0 ayrı pakettedir (`kesif/`);
      - çekirdek (`cekirdek/`) onları import etmez;
      - `kesif/` kâhine bağlanmaz (`degerlendirme/`'yi import etmez);
      - kabul yalnız çekirdek geçidinden sonra olur.
  - **(2) A6 bağımsız inceleme:** B0'ı ve B1'i engellemez. B2b sonucu kabul edilmeden önce (Kapı 2) yapılmış olmalıdır. K-040 (a) buna göre değişti.
  - **(3) Gizli sahte kurallar:** danışman yazar. Kodlayıcı ona aday kayıt biçimini (JSON şeması), 3 örnek kaydı ve görünür ailelerin listesini verir. Gizli aileler B1'den önce mühürlü dosya olarak gelir; kodlayıcı açmaz, yalnız biçimini kodla doğrular ve özetini kaydeder.
- **Sonuç:** B0 başlar. ÖK-005'in nihai mühürü B0 sonundadır (Kapı 1).
- **Onaylayan:** kullanıcı.
