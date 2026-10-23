# VARSAYIMLAR

`KODLAMA_PROMPTU.md` bölüm 3'e göre tutulur. Şartnamenin sessiz kaldığı her nokta burada numaralı kayıttır.
Durum: ONAYSIZ / ONAYLI (onaylı olan `KARARLAR.md`'ye taşınır).
"Felsefi" = felsefeyi ya da çekirdek davranışını etkiler mi (evet ise kod yazılmaz, soru sorulur).

---

## V-001: Ayar dosyasının biçimi
- **Bölüm:** KODLAMA_PROMPTU §5 (Config). Biçim belirtilmemiş.
- **Seçenekler:** (a) JSON (Python ile hazır gelir), (b) YAML/TOML (ek paket ya da sürüm şartı).
- **Öneri ve uygulanan:** (a) JSON, `config.json`. Yapı: `surum`, `degerler`, `bayraklar`. Her girdi tam olarak `deger` + `kaynak` alanı taşır.
- **Dosyalar:** `config.json`, `cekirdek/altyapi/ayar.py`.
- **Geri alma:** dosya biçimini değiştirip `ayar.py` okuyucusunu güncellemek.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-002: Kaynak etiketi biçimi
- **Bölüm:** KODLAMA_PROMPTU §3, §5. "§N ya da V-nnn" deniyor, ancak altyapı kodunun bir kısmı `sistem.md`'den değil, prompt'un çalışma kurallarından geliyor.
- **Seçenekler:** (a) yalnız `sistem.md §N` ve `V-nnn`, (b) ek olarak `KODLAMA_PROMPTU §N` ve `K-nnn` (karar) kabul etmek.
- **Öneri ve uygulanan:** (b). Kabul edilen etiketler: `sistem.md §N`, `KODLAMA_PROMPTU §N`, `V-nnn`, `K-nnn`.
- **Dosyalar:** `cekirdek/altyapi/ayar.py`, `testler/test_a0_yasak_kaliplar.py`, `testler/test_a0_yapi.py`.
- **Geri alma:** düzenli ifadeyi daraltmak.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-003: Python sürümü ve test aracı
- **Bölüm:** KODLAMA_PROMPTU §5 (yalnız standart kütüphane), §8 (kurulum). Sürüm belirtilmemiş.
- **Seçenekler:** (a) Python ≥3.10 + `unittest` (standart kütüphane), (b) `pytest` (ek paket, onay gerekir).
- **Öneri ve uygulanan:** (a). 3.10 alt sınırı, standart kütüphane listesini veren `sys.stdlib_module_names` için gerekiyor. Geliştirme ortamı: Python 3.13.
- **Dosyalar:** `kur.sh`, `kur.bat`, `araclar/kostur.py`.
- **Geri alma:** `kur.*` içindeki sürüm denetimini değiştirmek.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-004: Sihirli sayı taramasının istisnaları
- **Bölüm:** KODLAMA_PROMPTU §3, §6 ("koddaki her sayısal sabit §N ya da V-nnn'e bağlı olmalı").
- **Seçenekler:** (a) istisnasız her sayı, (b) yalnız 0 ve 1 (sayaç başlangıcı, indeks gibi) etiketsiz serbest.
- **Öneri ve uygulanan:** (b). Tarama `cekirdek/ tercuman/ degerlendirme/ karsilastirma/ araclar/` klasörlerini kapsar. `testler/` hariçtir çünkü test dosyaları hash kilidindedir ve test boyutları (7, 11, 13) bilerek seçilir. Etiket aynı satırda `# sistem.md §N`, `# KODLAMA_PROMPTU §N`, `# V-nnn` ya da `# K-nnn` biçiminde olmalı.
- **Dosyalar:** `testler/test_a0_yasak_kaliplar.py`.
- **Geri alma:** istisna kümesini boşaltmak.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-005: Çekirdekte izinli paketler
- **Bölüm:** KODLAMA_PROMPTU §5 ("standart kütüphane + şartnamenin gerektirdiği PyTorch/NumPy") ve §10 (izinli liste bilinen boşluk).
- **Seçenekler:** (a) şimdilik boş liste: çekirdek yalnız standart kütüphane kullanır, (b) şimdiden numpy/torch eklemek.
- **Öneri ve uygulanan:** (a), en dar seçenek. A0 ve A1 için yeterli. Ayrıca çekirdekte şu standart kütüphane modülleri yasak: ağ (`socket, ssl, http, urllib, ftplib, smtplib, poplib, imaplib, xmlrpc, asyncio, webbrowser`), dış süreç ve paralellik (`subprocess, multiprocessing`), yerel kod (`ctypes`). Dinamik import (`__import__`, `importlib.import_module`) da yasak. Gerekçe: prompt §2.3 "ağ kodunu import edemez" ve §5 "paralellik sırası sabit". numpy/torch sorusu A2'den önce sorulacak.
- **Dosyalar:** `config.json` (`izinli_ek_paketler`, `yasak_cekirdek_modulleri`), `testler/test_a0_yasak_kaliplar.py`.
- **Geri alma:** listeyi değiştirmek (onay ister).
- **Felsefi:** EVET (izin ve yalıtım). Şu anki değer en kısıtlayıcı olandır, bu yüzden hiçbir davranışı serbest bırakmıyor. **Durum:** ONAYSIZ. Kullanıcı (2026-10-23): A2'ye kadar bu kısıtlı hâliyle kalsın, A2 öncesi yeniden sorulacak.

## V-006: Zaman damgası ile determinizm çelişkisi
- **Bölüm:** KODLAMA_PROMPTU §5. "Her kayda ... zaman damgası" deniyor, ama aynı bölüm "saat yok" ve "aynı girdi ve tohum aynı çıktı" da diyor. Bağımsızlık testi (sistem.md §16) bit düzeyinde eşitlik istiyor.
- **Seçenekler:** (a) zaman damgası yok, yalnız sıra numarası, (b) duvar saati, ama karşılaştırma ve hash dışında tutulur, (c) mantıksal saat (tur/adım numarası).
- **Öneri:** (c) çekirdek kayıtlarında, (b) yalnız çekirdek dışı (besleme, tercüman) kayıtlarında.
- **Uygulanan (A0):** (a). Olay günlüğünde zaman alanı yok, en dar ve geri alınabilir seçenek.
- **Dosyalar:** `cekirdek/altyapi/olay_gunlugu.py`.
- **Geri alma:** kayda alan eklemek. Bu, şema sürümünü artırır.
- **Felsefi:** EVET (determinizm, bağımsızlık testi). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-004.

## V-007: Hash algoritması ve kanonik JSON
- **Bölüm:** KODLAMA_PROMPTU §5 (hash, hash zinciri). Algoritma belirtilmemiş.
- **Seçenekler:** SHA-256 / BLAKE2 / SHA-3.
- **Öneri ve uygulanan:** SHA-256. Kanonik JSON: anahtarlar sıralı, boşluksuz ayırıcı, UTF-8, `ensure_ascii=False`, NaN/Inf reddedilir.
- **Dosyalar:** `config.json` (`hash_algoritmasi`), `cekirdek/altyapi/kanonik.py`.
- **Geri alma:** config değeri. Ancak eski günlükler eski algoritmayla doğrulanır.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-008: Hash kilidinin kapsamı
- **Bölüm:** KODLAMA_PROMPTU §5 (Kilitli kümeler), §6.
- **Seçenekler:** kilit dosyasının yeri ve kapsamı.
- **Öneri ve uygulanan:** `kilit/kilitler.json`. Kapsam: `testler/` altındaki tüm dosyalar ve `config.json` (eşikler config'te). Güncelleme `python3 araclar/kilitle.py` ile yapılır. Kilitli dosyaya dokunan her değişiklik commit mesajında belirtilir ve kullanıcı onayı ister.
- **Dosyalar:** `araclar/kilitle.py`, `kilit/kilitler.json`, `testler/test_a0_kilit.py`.
- **Geri alma:** kilit dosyasını önceki commit'ten geri almak.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-009: Altyapı kodunun yeri
- **Bölüm:** KODLAMA_PROMPTU §2.3 (bağımlılık yönü yalnız `tercuman → cekirdek`).
- **Seçenekler:** (a) ayrı `ortak/` paketi (çekirdeğe yeni bir bağımlılık yönü açar), (b) `cekirdek/altyapi/` altında, yalnız standart kütüphaneyle.
- **Öneri ve uygulanan:** (b). Diğer paketler altyapıyı `cekirdek` üzerinden kullanır, böylece kuraldaki yön korunur.
- **Dosyalar:** `cekirdek/altyapi/`.
- **Geri alma:** modülleri taşımak.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-010: Atomik kayıt ve uzun koşu durumu
- **Bölüm:** KODLAMA_PROMPTU §5 (Uzun koşular).
- **Seçenekler:** yazma yöntemi ve rastgele üreteç durumunun saklanması.
- **Öneri ve uygulanan:** önce aynı klasörde geçici dosyaya yazılır, `fsync` yapılır, sonra `os.replace` ile yeniden adlandırılır. Üreteç olarak açıkça geçirilen `random.Random` kullanılır ve durumu `getstate()` ile JSON'a yazılır. PyTorch üreteci A2'de eklenecek. Windows klasör `fsync` desteklemediği için orada yalnız dosya `fsync` yapılır.
- **Dosyalar:** `cekirdek/altyapi/atomik.py`.
- **Geri alma:** modülü değiştirmek.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

---

# A1 varsayımları

## V-011: JSON Schema doğrulayıcısı (standart kütüphaneyle alt küme)
- **Bölüm:** KODLAMA_PROMPTU §5 (Şema ve veri: sürümlü JSON Schema, `additionalProperties:false`). V-005 nedeniyle `jsonschema` paketi kullanılamıyor.
- **Seçenekler:** (a) `jsonschema` paketi (onay gerekir), (b) standart kütüphaneyle küçük bir alt küme yazmak.
- **Öneri ve uygulanan:** (b). Desteklenen anahtarlar: `$schema, $id, title, description, type, properties, required, additionalProperties, enum, const, pattern, minLength, maxLength, minimum, maximum, items, minItems, maxItems, uniqueItems`. Bilinmeyen anahtar içeren şema reddedilir, sessizce atlanmaz. Her `object` şemasında `additionalProperties:false` zorunludur. `true/false` sayı sayılmaz.
- **Dosyalar:** `cekirdek/altyapi/sema_dogrulayici.py`.
- **Geri alma:** onaylı bir pakete geçmek.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-012: Üçlü kaydının alanları (sürüm 1)
- **Bölüm:** sistem.md §1 (sembolik üçlü), §2 (kayıt alanları); KODLAMA_PROMPTU §5 (şema sürümü, kaynak, hash, zaman, güven); K-004 (zaman = adım). Ek A P1 (tamsayı varlık kimliği) bağlamdır.
- **Uygulanan:** alanlar `sema_surumu, ozne, iliski, nesne, kaynak, guven, adim, ozet`. Varlıklar 0 ya da daha büyük tamsayı. `guven` [0,1] aralığında olmalı, dışındaki değer düzeltilmez, reddedilir. Kutup/kip/zaman (olumsuzluk, soru vb.) alanları Türkçe aşamasında şema sürümü artırılarak eklenecek, değerleri o gün sorulacak.
- **Dosyalar:** `sema/uclu_kaydi_v1.schema.json`, `cekirdek/bilgi_tabani.py`.
- **Geri alma:** şema sürümünü artırmak.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-013: İlişki şeması dosyasının biçimi, okuma yönü ve onay kilidi
- **Bölüm:** sistem.md §14 (LLM taslak ~20–30 ilişki, kullanıcı bir kez onaylar; ters/simetrik/dışlayıcı işaretleri), KODLAMA_PROMPTU §2.6, §6. Ek A: ters/simetrik tablo, dışlayıcı çiftler, işlevsellik.
- **Uygulanan:**
  - Biçim: `sema/iliski_semasi_v1.schema.json`. Her ilişki şu alanları taşır: `ad`, `ters` (aday listesi, çünkü örneğin "baba"nın tersi karşı tarafın cinsiyetine göre "oğul" ya da "kız"dır), `simetrik`, `islevsel` (bir kişinin en fazla bir tane olabilir). Ayrıca `dislayici_gruplar` listesi.
  - Şema dosyasında ilişkinin TANIMI (ör. "babanın annesi") yer almaz, çünkü tanımlar gizli kuraldır (kâhin) ve çekirdek bu dosyayı okur.
  - Okuma yönü: `(A, r, B)` = "B, A'nın r'sidir". Örnek: `(A, baba, B)` = B, A'nın babasıdır. Bu, sistem.md §3 örneğiyle (baba ∧ baba → dede) tutarlıdır.
  - Onay: `kilit/sema_onayi.json` dosyası, şema dosyasının hash'ini ve bir K-kararını taşır. Hash tutmazsa ya da onay yoksa şema yüklenmez ve hat durur.
  - Taslak `sema/iliskiler_v1.json` dosyasıdır (21 ilişki, LLM taslağı). Kullanıcı onayına kadar hiçbir kod tarafından kullanılmaz.
- **Dosyalar:** `cekirdek/iliski_semasi.py`, `sema/`, `araclar/sema_onayla.py`.
- **Geri alma:** onay kaydını silmek ya da şema sürümünü artırmak.
- **Felsefi:** EVET (şema onayı). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-006.

## V-014: Bilgi tabanının kabul/ret davranışı
- **Bölüm:** KODLAMA_PROMPTU §2.3 (LLM çıktısı karantinada), §5 (uymayan kayıt reddedilir, nedeni deftere yazılır, kaynaksız kayıt girmez).
- **Uygulanan:**
  - Şemaya uymayan, ilişkisi onaylı şemada olmayan ya da hash'i tutmayan kayıt reddedilir ve `KAYIT_REDDEDILDI` olayı yazılır.
  - `kaynak=LLM` olan kayıt ana tabana girmez, karantinaya alınır ve `KARANTINAYA_ALINDI` olayı yazılır.
  - Yalnızca birebir aynı kayıt (aynı hash) "yineleme" diye reddedilir. Farklı kaynaktan ya da farklı adımda gelen aynı üçlü ayrı kayıttır. Bunların bağımsız destek sayılıp sayılmayacağı A4'te (defter, kök-ayrık destek) çözülecek, bilgi tabanı güven birleştirmez.
- **Dosyalar:** `cekirdek/bilgi_tabani.py`.
- **Geri alma:** modül.
- **Felsefi:** kısmen (güven/çift sayım A4'e bırakıldı, burada birleştirme yok). **Durum:** ONAYSIZ.

## V-015: Sentetik soy ağacı üretecinin tasarımı
- **Bölüm:** sistem.md §11 ("gizli kurallar; yalnız son cevabı bilir" + parafraz), §10 (bölmeler; eğitim k=2–3, test k=4–10), §9 (ilgisiz bilgi), Ek A P7 (kural alt kümesi, ilişki adı permütasyonu, ad havuzu). Ağacın nasıl üretileceği, olguların ve sorguların ne olacağı ve cevabın kimde duracağı şartnamede yok.
- **Öneri:**
  1. Üreteç `degerlendirme/` altında durur, çünkü gizli kuralları bilen tek yer kâhindir. Kodda akrabalık sözcüğü yoktur. Ağaç soyut yapıdır: kişi (tamsayı), iki "tip" (0/1), yukarı/aşağı/yan bağ.
  2. Her ilişkinin yapısal tanımı (ör. "yukarı(tip 1), yukarı(tip 0)") gizli bir veri dosyasındadır (`degerlendirme/veri/`). Çekirdek bu dosyayı göremez. Cevap, iki kişi arasındaki gerçek ağaç yolunun hangi tanıma uyduğudur. Hiçbir tanıma uymuyorsa örnek üretilmez.
  3. Bölüme verilen olgular yalnızca doğrudan bağlardır (anne, baba, oğul, kız, eş, erkek/kız kardeş). Sorgu k halkalı bir yolun iki ucudur. Ağacın geri kalanı dikkat dağıtıcı olgu olarak verilir.
  4. A1'de isim ve metin yok, yalnızca tamsayı kimlik var. Parafraz ve ad havuzu Türkçe aşamasına kalır.
  5. Cevaplar ayrı dosyada durur. Eğitimin cevabı (uygunluk için "doğruluk") okuyup okuyamayacağı A3'te ayrıca sorulacak.
- **Uygulanan (şimdilik):** yalnızca `NotImplementedError` iskeleti.
- **Dosyalar:** `degerlendirme/uretec.py`.
- **Felsefi:** EVET (kâhin, veri olarak dil). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-007.

## V-016: Kelime çantası kısa yol kuralı
- **Bölüm:** sistem.md §10 ("kelime çantası kısa yol dedektörünün çözdüğü örnekler Treg'e, verisi test bölmelerinden ayrı") ve KODLAMA_PROMPTU §6 ("şansı +%5'ten fazla geçerse üretim durur"). İkisi farklı şey söylüyor. "Şans"ın tanımı yok.
- **Öneri:**
  - İkisini birleştirmek: dedektörün çözdüğü örnekler ayrı bir "Treg kümesine" ayrılır (§10). Kalan ana kümede dedektörün doğruluğu şans + %5'i geçerse üretim durur (prompt §6).
  - Şans = en sık cevabın oranı.
  - Dedektör = yalnızca olgulardaki ilişki adlarının sayısını (ve kişi kimliklerini) kullanan, yapıya bakmayan, standart kütüphaneyle yazılmış Naive Bayes sınıflayıcısı. Ayrı bir bölmede eğitilir, başka bir bölmede ölçülür.
- **Felsefi:** EVET (veri, kısa yol). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-008.

## V-017: Bölüm biçimi, zincir ve dikkat dağıtıcı kuralları, üreteç parametreleri
- **Bölüm:** sistem.md §10, §11; K-007. Sayılar ve ayrıntılar şartnamede yok.
- **Uygulanan:**
  - **Ağaç:** kök çift. `uretec_nesil_sayisi` (4) nesil. Her çiftin çocuk sayısı `uretec_cocuk_en_az`–`uretec_cocuk_en_cok` (2–4) arasında rastgele. Son nesil dışındaki her çocuk ağaç dışından gelen karşı tipte biriyle evlenir. Akraba evliliği ve üvey kardeş yok. Ağaç her bölümde yeniden kurulur.
  - **Zincir:** olgu ilişkileriyle (doğrudan bağlar) kişi tekrarlamayan k adımlı rastgele yürüyüş. Sorgu (ilk, son). Cevap, iki uç arasındaki gerçek ilişkidir. Gerçek ilişki 21 ilişkiden biri değilse aday atılır. Olgular yürüyüş yönünde yazılır.
  - **k tanımı:** olgu grafiğinde sorgu uçları arasındaki en kısa yol tam k olmalıdır. Bu, üreteçte denetlenir.
  - **Dikkat dağıtıcılar:** ağacın başka doğrudan bağlarından `dikkat_dagitici_olgu_sayisi` (4) olgu. Zincire kısa yol açan seçim yeniden çekilir.
  - **Kişi kimlikleri:** her bölümde rastgele karıştırılır. Olguların sırası karıştırılır.
  - **Bölüm dosyasında** bölme adı, k ve cevap YOK. Bunlar ayrı cevap kaydındadır.
  - **Deneme sınırı:** `uretec_deneme_siniri`. Aşılırsa üretim durur, sessizce küçültülmez.
  - **Tohum:** `uretec_tohum`.
  - **Bölmeler:** eğitim (k=2–3), uzunluk testi (k=4–10), zincir-bozuk, yön ters, ilişki yeniden adlandırma. Zincir-bozuk bölümde bir zincir olgusu silinir, yerine bir dikkat dağıtıcı eklenir (olgu sayısı aynı kalsın diye) ve cevap "yok"tur. Yeniden adlandırma bölmesinde ilişki adları `yeniden_ad_uzunlugu` harfli anlamsız adlarla tutarlı biçimde değiştirilir ve bölmeye yeniden adlandırılmış şema eşlik eder.
- **Dosyalar:** `degerlendirme/dunya.py`, `degerlendirme/uretec.py`, `config.json`, `sema/bolum_v1.schema.json`, `sema/cevap_v1.schema.json`.
- **Geri alma:** config değerleri ve modül.
- **Felsefi:** hayır (K-007 içinde ayrıntı). **Durum:** ONAYSIZ.

## V-018: Kelime çantası dedektörünün ayrıntıları
- **Bölüm:** K-008. Sayılar yok.
- **Uygulanan:**
  - **Özellikler:** olgulardaki ilişki adı sayıları ile olgu ve sorgudaki kişi kimlikleri. Yapıya bakılmaz.
  - **Model:** çok terimli Naive Bayes, Laplace düzeltmesi `dedektor_laplace` (1). Eşitlikte sözlük sırasıyla karar verilir.
  - **Akış:**
    1. Her bölme için önce `dedektor_egitim_sayisi` bölüm yalnız dedektörü eğitmek için üretilir. Bu bölümler ne ana kümeye ne Treg kümesine girer.
    2. Sonraki adaylardan dedektörün doğru bildikleri Treg kümesine, diğerleri ana kümeye gider.
    3. Ana küme dolunca, ana kümenin ilk yarısında sıfırdan eğitilen yeni bir dedektör ikinci yarıda ölçülür. Doğruluk > şans + `kisa_yol_sans_payi` ise üretim durur.
  - **Zincir-bozuk:** bu bölmede Treg ayrımı yapılmaz. Kapı, bozuk bölümler ile bunların bozulmamış eşlerinin karışımında ölçülür, çünkü tek başına bütün cevaplar "yok"tur.
- **Dosyalar:** `degerlendirme/kisa_yol.py`.
- **Felsefi:** hayır (K-008 içinde ayrıntı). **Durum:** ONAYSIZ.

## V-019: Gizli yapısal tanımların içeriği
- **Bölüm:** K-007. İlişkilerin yapısal tanımları kâhin verisidir. Şartnamede yok, akrabalık bilgisinden yazıldı (LLM taslağı).
- **Uygulanan:** `degerlendirme/veri/tanimlar_v1.json`. Testler her üretilen ağaçta şunları denetler:
  - aynı iki kişi arasında en fazla bir ilişki olması,
  - ilişkinin tersinin onaylı şemadaki ters adaylarından biri olması,
  - işlevsel ilişkilerin tekliği.
  Böylece tanımlar ile onaylı şema birbirini sınar.
- **Geri alma:** yeni sürüm (`tanimlar_v2.json`).
- **Felsefi:** EVET (kâhin doğruluğu). **Durum:** ONAYSIZ, kullanıcının okumasına sunulacak.

## V-020: "Önsel-ters" bölmesinin tanımı
- **Bölüm:** sistem.md §10 "önsel-ters". Ne demek olduğu tanımlı değil.
- **Seçenekler:** (a) test cevap dağılımı eğitimdekinin tersi (eğitimde nadir olan cevaplar testte sık), (b) gerçek hayatta alışılmadık ama tutarlı aileler (ör. çok kuşaklı aynı yaş), (c) başka.
- **Öneri:** (a).
- **Uygulanan:** `NotImplementedError`.
- **Felsefi:** EVET (değerlendirme bölmesi). **Durum:** ONAYSIZ, sorulacak.

## V-021: Kilitli kümelerle kesişim denetimi
- **Bölüm:** KODLAMA_PROMPTU §5 (Kilitli kümeler: hash her koşuda doğrulanır, kesişirse hat durur).
- **Uygulanan:**
  - `kilit/kilitli_kumeler.json` kaydı küme dosyalarının hash'ini tutar.
  - Üretilen her bölümün özeti kilitli kümelerdeki özetlerle karşılaştırılır, kesişirse üretim durur.
  - Kesişim birebir aynı bölüm (aynı hash) üzerinden aranır. Kimlikleri farklı ama yapıca aynı (izomorf) bölümler yakalanmaz. Bu sınırlıdır ve raporlanır.
  - Altın/kalibrasyon kümesinin kendisi henüz YOK. Boyutu ve oluşturulma yolu kullanıcıya sorulacak (bilinen boşluk, KODLAMA_PROMPTU §10).
- **Dosyalar:** `degerlendirme/kilitli_kumeler.py`.
- **Felsefi:** hayır (mekanizma), küme içeriği EVET. **Durum:** ONAYSIZ.

## V-011 eki: tip listesi
- JSON Schema `type` alanı liste de olabilir (ör. `["string", "null"]`). Cevap kaydındaki "yok" cevabı için eklendi.
