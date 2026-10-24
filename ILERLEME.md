# İLERLEME

## A0: klasör iskeleti, config, rapor/kayıt altyapısı (dal `asama-0`)

**Durum:** testler yeşil, etiket `asama-0` (yalnız yerel; uzak depoya etiket gönderimi 403 ile reddedildi, kullanıcı: bir şey yapma). Bağımsız inceleme bekliyor (`inceleme/A0_istemi.md`); inceleme bitmeden A1'e başlanmaz.

**Çalışan (testle gösterilmiş):**
- Klasörler: `cekirdek/` (+ `altyapi/`), `tercuman/`, `degerlendirme/`, `karsilastirma/`, `veri/`, `sema/`, `kilit/`, `araclar/`, `testler/`.
- `config.json` + `cekirdek/altyapi/ayar.py`: her değer kaynaklı, en fazla 5 bayrak, riskli bayraklar kapalı, bozuk ayar reddedilir.
- `cekirdek/altyapi/olay_gunlugu.py`: sadece-ekleme, sıra numaralı, hash zincirli. Değiştirme, silme, yarım satır yakalanır. `YEDEK_KULLANILDI` sayacı var.
- `cekirdek/altyapi/atomik.py`: atomik kayıt. Öldürülüp devam ettirilen koşu kesintisiz koşuyla aynı sonucu verir.
- Yasak kalıp taramaları: çekirdek importları, kâhin yalıtımı, sihirli sayı, modül başlığı, izlenebilirlik, test atlatma, hash kilidi.
- Mutasyon sınaması: 15 kasıtlı hatanın 15'i yakalandı (`python3 araclar/mutasyon_a0.py`).

**Komutlar:**
- Tüm testler: `python3 araclar/kostur.py` (ya da `./kur.sh`)
- Mutasyon sınaması: `python3 araclar/mutasyon_a0.py`
- Test/eşik dosyası değişirse (onaydan sonra): `python3 araclar/kilitle.py`

**Eksik / sonraki aşamalara bırakılan:**
- "Kodda ilişki sözcüğü geçmez" taraması: sözlük verisi A1'de gelince yazılacak.
- "LLM paketi kurulu olmadan testler geçer" ve bağımsızlık testi: LLM yok, A7'de anlamlı. Şimdilik çekirdek yalnız standart kütüphane kullanıyor.
- Ağ kapalı temiz ortamda kurulum denemesi ve `kur.bat` (Windows): DOĞRULANMADI.
- Aşama öncesi/sonrası test sayısı karşılaştırması: A0 sıfırdan başladı (önce 0, şimdi 57 test).

## A1: bilgi tabanı + sentetik soy ağacı üreteci (dal `asama-1`, etiket `asama-1`)

**Durum:** KAPANDI. Kelime çantası kapısı altı bölmenin hepsinde geçti. Altın küme soruları hazır ve kilitli; kullanıcının cevapları bekleniyor (A1 kapısı değil, K-011).

**Çalışan (testle gösterilmiş):**
- Şema doğrulayıcı, onay kilitli ilişki şeması (K-006), bilgi tabanı (ret/karantina/günlük).
- `degerlendirme/dunya.py`: soyut soy ağacı ve onaylı gizli tanımlar (K-009, hash kilitli). Her ağaçta tanımların şemayla tutarlılığı sınanır.
- `degerlendirme/uretec.py`: bölmeler eğitim, uzunluk, zincir-bozuk, yön ters, yeniden adlandırma ve önsel-ters (K-010). Önsel-ters'te cevap dağılımının ters döndüğü Spearman testiyle gösterildi.
  - Cevaplar `kahin/` klasöründe.
  - Kimlikler ve olgu sırası karıştırılıyor.
  - En kısa yol tam k.
- `degerlendirme/kisa_yol.py`: dedektör, Treg ayrımı ve kapı. Dedektör ham veride kısa yolu yakalıyor.
- `degerlendirme/altin.py`: 2 × 50 altın soru (40 zincirli + 10 zincir-bozuk), A/B/C/D seçenekli.
  - Kayıtlı ve kilitli (`kilit/kilitli_kumeler.json`). Eğitim üretimi bu kümeyle kesişirse durur.
  - Kullanıcı cevabı ayrıştırıcısı ve karşılaştırıcısı hazır.
- Tam üretim: `python3 -m degerlendirme.uretec <klasör>` (~27 sn), deterministik.

**Kapı sonuçları (config boyutu):**

| Bölme | Dedektör doğruluğu | Şans | Sınır |
|---|---|---|---|
| eğitim | 0,135 | 0,140 | 0,190 |
| uzunluk | 0,105 | 0,150 | 0,200 |
| zincir-bozuk (karışım) | 0,453 | 0,500 | 0,550 |
| yön ters | 0,085 | 0,125 | 0,175 |
| yeniden adlandırma | 0,105 | 0,160 | 0,210 |
| önsel-ters | 0,295 | 0,295 | 0,345 |

**Kilitli dosya değişiklikleri (bildirim):**
- `config.json`'a üreteç (K-007/K-008), altın küme (K-011) ve kilitli veri listesi (K-009) için yalnız yeni anahtarlar eklendi.
- `testler/test_a1_uretec_iskelet.py` artık önsel-ters testi.
- `testler/test_a1_uretec.py`'den eski "önsel-ters yazılmadı" testi çıkarıldı. Yerine üç önsel-ters testi geldi. Toplam test sayısı arttı: 134 → 147.

**Mutasyon:** A0 15/15, A1 30/30 yakalandı (`python3 araclar/mutasyon_a0.py`, `python3 araclar/mutasyon_a1.py`).

**Altın küme 1. parça (2026-10-23):** cevaplar kaydedildi (kaynak=LLM, onaylayan=kullanıcı, K-013). Üreteçle 50/50 uyuştu. Bağımsızlık kısıtı ÖK-001'de.

**Eksik:**
- Altın küme 2. parça cevapları (A5'e kadar).
- Kalibrasyon kümesi: ~500 örnek, CLUTRR aşamasında (sistem.md §9).
- Kesişim yalnız birebir aynı bölümü yakalar.
- İsim/parafraz Türkçe aşamasında.

## A2: vektörler (HRR/VSA) (dal `asama-2`, etiket `asama-2`)

**Durum:** KAPANDI, yalnız saf Python tamsayı referans yoluyla (K-015). PyTorch hızlı yolu ve bit-eşitlik testi A5 öncesine ertelendi, çünkü ağ izni yok (V-025).

**Çalışan (testle gösterilmiş):**
- `cekirdek/vektor.py` (K-014):
  - d=256, ±1 tamsayı vektörler, SHAKE-256'dan durumsuz üretim. Farklı `PYTHONHASHSEED` ile ayrı süreçte aynı vektör çıkıyor.
  - Tamsayıyla tam dairesel evrişim. Elle hesaplanmış örnekler, değişme, birleşme ve dağılma özellikleri tutuyor.
  - Kayıt vektörü v = 16·R + P_s⊛E[s] + P_o⊛E[o]. Bileşen ölçek oranı [0,5; 2] içinde.
  - Kosinüs benzerliği tek son bölmeyle hesaplanıyor. cos(a,a) = 1.0 tam.
  - Çözme: 60 kayıtta özne, nesne ve ilişki %100 geri bulunuyor (100 varlık, 21 anlamsız ilişki).
  - Yarı-diklik: 100 vektörde bütün çiftlerde |cos| < 5/√d.
  - Rol bağı asimetrik. İlgisiz kayıt değişince diğer satırlar sabit kalıyor.
- `cekirdek/sekiller.py`: SEKILLER tablosu (boyut, kayit, aday) ve şekil denetimi (7/11/13 boyları, boş ve tek öğe).

**Ölçüm (hız iddiası değil):** referans yolda 64 kayıt vektörü 0,52 sn (8,1 ms/kayıt), 64×64 kosinüs matrisi 0,23 sn. Hızlı yol olmadan A3'teki 300–500 hücrelik popülasyon yavaş olacak. Bu, PyTorch erişiminin A3–A5 arasında gerekeceği anlamına geliyor.

**Mutasyon:** A2'de 11/11 yakalandı (`python3 araclar/mutasyon_a2.py`). A0/A1 kodu ve testleri bu aşamada değişmedi, o mutasyonlar yeniden koşturulmadı.

**Eksik:**
- PyTorch hızlı yol (toplu int64) ve referansla bit-eşitlik testi (K-015).
- GPU yolu (K-012: ayrı aşama).
- Reseptör vektörleri ve gradyan (sistem.md §3, §7): A3 ve sonrası.

## A3: LLM'siz çekirdek (dal `asama-3`, etiket `asama-3`)

**Durum:** KAPANDI (saf Python referans yolu). Kapsam V-027'ye göre: sitokin ve Treg H4'te, öğrenme H2'de, kredi H3'te, defter ve müdahale A4'te, yayın sahnesi H3/H4'te (K-019).

**Çalışan (testle gösterilmiş):**
- `cekirdek/dna.py`: 1–3 halkalı DNA veri dosyası.
- `cekirdek/havuz.py`:
  - İki katman, ilişki dizini, (üçlü, köken) tekilleştirmesi.
  - En düşük güvenli çıkarım atılır (K-019) ve mezar taşı kalır (V-033).
  - Atılacak çıkarım yoksa `YEDEK_KULLANILDI` yazılır.
- `cekirdek/eslesme.py`:
  - Sembolik yarı-naif bağlama.
  - Afinite = kırp(cos·√3). θ süzgeci.
  - Güven = min(afiniteler, ebeveyn güvenleri) × güvenilirlik (K-016). Bağımsız yeniden hesapla birebir aynı.
- `cekirdek/dongu.py`:
  - Eşzamanlı turlar. Hücre başına en iyi 8 eşleşme, tur bütçesi 1024; atılanlar günlükte.
  - Durma: yeni kayıt yok, tur sınırı 8, impasse. Impasse'te θ bir kez yarıya iner ve tüm havuz yeniden denenir (K-017).
  - Her yazma, atma ve durma günlükte.
- `cekirdek/plazma.py` (K-018):
  - Kök kümesi bileşenleri, bileşen içi MAX, bileşenler arası noisy-OR. Bağımsız iki ispatta elle hesapla eşit.
  - Aynı kaynaktan 10 kopya ispat güveni değiştirmiyor.
  - "Bilmiyorum" ve çelişki işareti.
  - Gerekçe ağacı epitoplara iniyor.
- Belirlenim: iki koşu, havuz ve günlük baytları aynı.
- İlişki adları tutarlı değişince cevap da aynı eşlemeyle değişiyor ("blorp" testi).
- Zincirden bir olgu silinince cevap düşüyor. İlgisiz olgu değişince cevap ve güven sabit kalıyor.

**Mutasyon:** A3 25/25 yakalandı (`python3 araclar/mutasyon_a3.py`).

**Ölçüm (hız iddiası değil):** 9 olgulu geçişli kapanış (1 hücre) referans yolda 0,53 sn, 8 tur, 51 yazma.

**Eksik:**
- PyTorch hızlı yol ve bit-eşitlik testi (K-015, A5 öncesi).
- Yayın sahnesi, sitokin, Treg, öğrenme, kredi (yol haritasındaki aşamalarında).
- Akrabalık için elle doğru DNA ve H1 deneyi A5'te.
- τ ile durma kalibrasyon kümesi oluşunca açılacak.

## A4: destek/çelişki defteri + müdahale testi (dal `asama-4`, etiket `asama-4`)

**Durum:** KAPANDI (saf Python referans yolu).

**Çalışan (testle gösterilmiş):**
- `cekirdek/defter.py` (V-035, K-020):
  - Hash zincirli, sadece ekleme. Her ateşleme, yazma (kök kümesiyle) ve atma kayıtlı.
  - Dizin olaylardan kurulur, dosyadan yeniden açılınca yeniden oluşur. Kök-ayrık destek var.
  - Çelişkiler: dışlayıcı, işlevsel, ters (tersi tanımsız ilişki denetlenmez).
  - Hiçbir kayıt silinmez. Her çelişki bir kez `CELISKI` olayıyla iki kayda bağlanır ve ortak destek kümesi kalıcı yazılır. Epitoplar dahil her turda denetlenir.
- İz kuralı: plazma yalnız defterde YAZMA izi olan çıkarımı ispat sayar. `calistir` defter ve onaylı şema olmadan çalışmaz.
- `cekirdek/mudahale.py` (K-021):
  - (a) Kök silme, yalnız etkilenen köken alt grafında (`BudanmisHavuz`).
  - (b) İlgisiz epitopu tür uyumlu yedekle değiştirip yeniden koşma.
  - (c) Ters tutarlılığı ve çelişkisizlik.
  - Puan = a·b·c. İlgisiz epitop yoksa "sınanamadı": b ve puan boş, başarı sayılmaz.
  - `mudahale_ozeti` sınanamadı ve cevapsız soruları ayrı sayar (H1 raporu için).
  - Karşı-olgusal koşular bellekteki defterle yapılır; ana deftere yalnız `MUDAHALE` özeti yazılır.
- Olay günlüğü: bellekte çalışma, toplu yazım (tek fsync, aynı baytlar, tek hata hepsini durdurur).

**Kilitli test değişiklikleri (bildirim):**
- `testler/test_a3_cekirdek.py`: `cevapla` çağrılarına defter, `calistir` çağrısına `iliski_semasi` eklendi. Beklentiler aynı.
- `testler/test_a4_defter.py`: `calistir` çağrılarına `iliski_semasi` eklendi.

**Mutasyon:**
- A4: 22/22 yakalandı.
- A3 yeniden koşturuldu: 25/25 yakalandı. "Tur sınırı yok" mutasyonu çekirdeği sonsuz döngüye soktuğu için zaman aşımıyla yakalandı (V-039).
- İlk A4 koşusunda iki mutasyon kaçmıştı:
  - Ortak destekte kesişim yerine birleşim: test eksikti, kök kümeleri farklı bir durum eklendi.
  - c'den yalnız ters tutarlılığını çıkaran mutasyon: eşdeğer mutanttı (onaylı tanımda ters tutarsızlık her zaman ters çelişkisi olarak da deftere düşer). Mutasyon, raporlanan `ters_tutarli` alanını bozacak biçimde değiştirildi.
  - Bu sırada ters tutarlılığındaki "tersi tanımsız ilişki" kuralı, çelişki kuralıyla aynı hâle getirildi (V-038).

**Eksik:**
- Geri çekme olayı (henüz geri çeken işlem yok; A7).
- Hücre susturma ve uygunluk (§8, H3).
- Geçişlilik denetimi (şemada bilgi yok).
- Müdahale puanının CLUTRR kalibrasyon kümesinde doğrulukla ilişkisi (r > 0,8 hedefi; CLUTRR aşaması).

## A5: H1 deneyi (dal `asama-5`, sürüyor)

**Durum:** Hızlı yol kuruldu ve döngüye bağlandı. H1 ön kaydı (ÖK-002) onaylandı ve kilitlendi. DNA dışındaki H1 hazırlıkları bitti. Danışmanın DNA'sı bekleniyor; H1 deneyinin kendisi başlamadı.

**Çalışan (testle gösterilmiş):**
- torch 2.14.1+cpu ve bağımlılıkları `gereksinimler.txt`'de hash'le sabit (K-022). Lisans `LISANSLAR.md`'de, kaynakla karşılaştırılarak doğrulandı.
- `cekirdek/vektor_hizli.py` (V-040): toplu evrişim (int64 dairesel matris), kayıt matrisi, kosinüs ve afinite matrisleri. Referans yolla `float.hex` düzeyinde aynı (`testler/test_a5_hizli_yol.py`, 14 test).
- Bulgu: `torch.sqrt` (float64, CPU) bu derlemede doğru yuvarlanmıyor (√36912709632'de 1 ulp). Kök `math.sqrt` ile alınıyor.
- Taşma denetimi çarpımlardan önce yapılıyor (2^53 sınırı, int64 sarması dahil).
- Kurulum: `sh kur.sh` → Python 3.13 denetimi, `.venv`, hash denetimli kurulum, testler (V-041). Boş kopyada doğrulandı. `kur.bat` DOĞRULANMADI.
- Ölçüm (`araclar/hiz_olc.py`, hız iddiası değil): 64 kayıt matrisi referans 0,622 sn / hızlı 0,020 sn; 64×64 kosinüs 0,200 / 0,002 sn; bit-eşit.

**Mutasyon:** ilk koşuda 12 mutasyondan 10'u yakalandı, 2'si kaçtı (benzerlikte int64 denetimi, eksen sayısı denetimi): testi yoktu, eklendi. Son koşu: 12/12 yakalandı, taban 244/244.

**2. adım, döngüye bağlama (V-042, testle gösterilmiş):**
- Kod kitabı vektör hesabının giriş noktası (`kayit_vektoru`, `benzerlik_matrisi`). `KodKitabi` referans, `HizliKodKitabi` hızlı yol. Havuz, döngü ve müdahale verilen kod kitabının yolunu kullanır.
- Afiniteler tur başında bir kez tablo olarak hesaplanır (`afinite_tablosu`).
- `testler/test_a5_dongu_hizli.py` (10 test), senaryolar `testler/yardimci_senaryo.py`'de (atma, bütçe, hücre sınırı, impasse, çelişki, müdahale):
  - defterin her olayı iki yolda kanonik JSON ile aynı;
  - referans yolun izi, bağlamadan önceki koddan (797eeaa) alınan altın değerlerle aynı;
  - hızlı koşuda saf Python evrişim ve kosinüs hiç çağrılmıyor (eşitlik tek başına hızlı yolun kullanıldığını göstermez).
- Ölçüm (`araclar/hiz_olc.py`): 4 senaryo, 38 çıkarım: referans 0,999 sn, hızlı 0,216 sn; defter ve vektörler aynı. Profil: referans yolda sürenin büyük kısmı kayıt vektörünün saf Python evrişimiydi.
- Mutasyon: 19/19 yakalandı (12 vektör + 7 bağlama), taban 254/254. Eşdeğer mutant: döngünün tabloyu eşleşmeye vermemesi (sonuç aynı, yalnız hız); listede yok.
- Bulgu: büyük vektör listelerinde `assertEqual`'ın fark çıktısı (difflib) dakikalar sürüyor; bir mutant yakalandığı hâlde 600 sn sınırına takıldı. Test ilk farkı raporlayacak biçimde düzeltildi.

**3. adım, H1 hazırlıkları (DNA hariç):**
- ÖK-002 onaylandı ve kilitlendi (K-023). DNA'yı bağımsız danışman yazacak (K-024). DNA'ya isteğe bağlı "farklı kişi" şartı eklenecek (K-025).
- DNA sürüm 2 (V-043): `sema/dna_v2.schema.json`, hücrede isteğe bağlı `farkli` ve `okunus`. `testler/test_a5_dna_v2.py` önce kırmızı (8 hata), sonra yeşil. Sürüm 1 ve şartsız hücreler aynen çalışıyor (V-042 altın değerleri değişmedi).
- Danışman dosyası `DANISMAN_ICIN_ILISKI_LISTESI.md`: onaylı şemadan üretildi, gizli tanım içermiyor. `testler/test_a5_danisman.py` tablonun şemayla aynı olduğunu ve gizli tanım metninin geçmediğini denetliyor (sızıntı eklenince yakaladığı denendi).
- H1 koşturucusu `degerlendirme/h1.py` ve `degerlendirme/istatistik.py` (V-044):
  - çekirdek cevabı görmeden koşar, sonra kâhinle karşılaştırılır;
  - kapı bölmeleri ve altın küme, config, DNA ve tohum manifestlerinin özetleri ÖK-002 ekinde yoksa koşmaz;
  - bölüm dosyaları manifestle denetlenir; ara kayıt atomik, kaldığı yerden sürer;
  - Clopper–Pearson üst sınırı, bootstrap aralığı, "sınanamadı" ayrı sayım (K-021);
  - altın küme her parça kendi kaynak etiketiyle (ÖK-001).
  - Testler: `test_a5_h1.py` (14), `test_a5_istatistik.py` (7), önce kırmızı.
- H1 bölümleri üretildi: 5 tohum (7–11), `uretilen/h1/` (git dışında, 36 MB, 2 dk 12 sn). Kısa yol kapısı 5 tohumun hepsinde geçti. Manifest özetleri (sha256):
  - tohum 7 `d95f6afebd56c4008fe91f11b813c0e5c8c817a34b180f79d9c5e4907547f127`
  - tohum 8 `6f481451bb2c661e130987e3b2af48fa9acac223d927e516afff5de023bc1f31`
  - tohum 9 `68647318999d1ef59430ec84928e49bcc76ac38da1cbda7c02e80a4d243f0b29`
  - tohum 10 `7a331cee31840531547d7b8cf988921c364e66318bb87fcd8baceabdc9981c19`
  - tohum 11 `b2f57c2be8821982a892ff1abb311bd3c536e2a9eda3a70443c07100cb93c863`
- Bulgu: tohum 8'de önsel-ters bölmesi 20000 adayda doldurulamadı (356/400). Aday sınırı 100000'e çıkarıldı (V-045). Sınır yalnız durdurucu; tohum 7 manifesti önce ve sonra aynı.
- Config (kilitli) değişti: H1 değerleri (tohumlar, bölmeler, güven düzeyi, bootstrap, ara kayıt) ve aday sınırı.
- Mutasyon: 37/37 yakalandı (vektör 12, bağlama 7, farklı kişi 4, koşturucu ve istatistik 14), taban 287/287.

**4. adım, DNA geldi (2026-10-24):**
- `veri/dna/akrabalik_dna_v2_final.json`: 170 kural (8 tek, 150 iki, 12 üç halkalı; 26'sında farklı kişi şartı), DNA v2 ve onaylı şemayla geçerli. 9 grupluk özet `veri/dna/AKRABALIK_DNA_GRUPLARI.md`; kullanıcının tek evet/hayır onayı bekleniyor.
- Havuz 128 (ÖK-002a, K-026).
- Bulgu: aynı ilişkinin yeni kökenle yeniden yazılması döngüyü 8 tura sürüklüyor, kopyalar doğru cevabı havuzdan atıyor. Eğitimde ilk 60 bölümde bugünkü hâl 33/60. Seçenekler ölçüldü (V-046); karar kullanıcıda.
- Hızlandırma: dairesel matrisler bir kez kuruluyor (V-042 eki); ölçülen en pahalı adım buydu.

**Eksik:**
- V-046 kararı (felsefi), DNA'nın 9 grupluk onayı, sonra eğitim bölmesinde geliştirme.
- ÖK-002 eki: config, DNA ve tohum manifest özetleri (DNA kilitlenince).
- Kapı koşusu ve altın küme koşusu. Gerçek DNA ile süre ölçümü (deneme DNA'sıyla ölçülen 0,02 sn/bölüm gerçeği yansıtmaz).
- Altın küme 2. parça cevapları (kullanıcıda).
- Otomatik ayrılamayan hata sınıfları (ad yok / türetilemez / DNA / çekirdek) için inceleme aracı.
- GPU (CUDA) sürümü: gerekirse konuşulacak (K-022).
