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

## A4: destek/çelişki defteri + müdahale testi (dal `asama-4`)

**Durum:** YARIM. Defter altyapısı yazıldı (V-035). Çelişkinin tanımı ve etkisi (V-036) ile müdahale testi ve puanı (V-037) kullanıcı onayında.

**Çalışan (testle gösterilmiş):**
- `cekirdek/defter.py`: hash zincirli olay günlüğünün alt sınıfı. Dizini olaylardan kurulur, dosyadan yeniden açılınca yeniden oluşur. `yazildi_mi`, `canli_ispatlar`, kök-ayrık `destek` var.
- Döngü her ateşlemeyi, yazmayı (kök kümesiyle) ve atmayı deftere yazıyor. Bir turun olayları tek seferde, sırası korunarak yazılıyor.
- İz kuralı: plazma yalnız defterde YAZMA izi olan çıkarımı ispat sayıyor. Defteri atlayarak havuza yazılan kayıt cevaba giremiyor.
- Olay günlüğü: dosyasız (bellekte) çalışabiliyor. Toplu yazım tek tek yazımla aynı baytları üretiyor. Toplu yazımda tek geçersiz olay varsa hiçbiri yazılmıyor.

**Kilitli dosya değişikliği:** `testler/test_a3_cekirdek.py`'de yalnız `cevapla` çağrılarına koşunun defteri eklendi (iz kuralı). Beklentiler aynı.
