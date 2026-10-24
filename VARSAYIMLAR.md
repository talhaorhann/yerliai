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
- **Felsefi:** EVET (izin ve yalıtım). Şu anki değer en kısıtlayıcı olandır, bu yüzden hiçbir davranışı serbest bırakmıyor. **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-012 (numpy ve torch izinli; ağ ve dış süreç yasağı aynen sürer).

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
- **Felsefi:** EVET (kâhin doğruluğu). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-009.

## V-020: "Önsel-ters" bölmesinin tanımı
- **Bölüm:** sistem.md §10 "önsel-ters". Ne demek olduğu tanımlı değil.
- **Seçenekler:** (a) test cevap dağılımı eğitimdekinin tersi (eğitimde nadir olan cevaplar testte sık), (b) gerçek hayatta alışılmadık ama tutarlı aileler (ör. çok kuşaklı aynı yaş), (c) başka.
- **Öneri:** (a).
- **Uygulanan:** `NotImplementedError`.
- **Felsefi:** EVET (değerlendirme bölmesi). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-010.

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

## V-022: Önsel-ters bölmesinin uygulanışı (K-010)
- **Bölüm:** K-010. Nasıl "ters" yapılacağı tanımlı değil.
- **Uygulanan:**
  - Bölümler eğitim gibi üretilir (k=2–3).
  - Dedektör eğitim kümesi aynı zamanda doğal cevap dağılımı p(r) tahminidir. Laplace (+1) ile düzeltilir, böylece hiç görülmemiş cevap da tanımlı olur.
  - Hedef dağılım q(r) ∝ 1/p(r). Bir aday p_en_az²/p(r)² olasılıkla kabul edilir. Bu reddetme örneklemesi sonuçta q dağılımını verir.
  - Sonra K-008'deki Treg ayrımı ve kapı aynen uygulanır.
- **Dosyalar:** `degerlendirme/uretec.py`.
- **Felsefi:** hayır (K-010 içinde ayrıntı). **Durum:** ONAYSIZ.

## V-023: Altın küme sorularının biçimi (K-011)
- **Bölüm:** K-011, KODLAMA_PROMPTU §5 (altın küme elle izlenmiş küçük örnekler).
- **Uygulanan:**
  - Ayrı tohum `altin_tohum`. Parça başına `altin_normal_sayisi` (40) zincirli ve `altin_bozuk_sayisi` (10) zincir-bozuk soru.
  - Elle izlemeyi kolaylaştırmak için k=2–3 ve `altin_dikkat_dagitici` (2) dikkat dağıtıcı kullanılır. Eğitimde bu sayı 4'tür.
  - Kişiler soru içinde 1'den başlayarak numaralanır.
  - Olgular "Kişi 1 → ilişki → Kişi 3" biçimindedir (okuma: Kişi 3, Kişi 1'in ilişkisidir). Türkçe çekim yok, çekim Türkçe aşamasına kaldı.
  - Seçenekler: A, B, C ilişki adı, D "Bilgi yetmez". Zincirli soruda doğru cevap A–C arasında, öteki ikisi şemadan rastgele. Zincir-bozuk soruda A–C rastgele, doğru cevap D.
  - Kullanıcı emin değilse "?" yazabilir.
  - Soru bölümleri `degerlendirme/altin/altin_bolumler.jsonl` dosyasına yazılır ve hemen kilitli kümeye kaydedilir (`kilit/kilitli_kumeler.json`). Böylece eğitim üretimi altın kümeyle kesişirse durur.
  - Üretecin cevapları ayrı dosyadadır (`degerlendirme/altin/uretec_cevaplari.jsonl`). Kullanıcı bu dosyayı açmamalıdır.
- **Felsefi:** kısmen (altın küme). **Durum:** ONAYSIZ.

## V-008 eki (2026-10-23): onaylı veri dosyaları da kilitli
- `config.json` içindeki `kilitli_veri_dosyalari` listesi de hash kilidindedir. Listede şunlar var: onaylı gizli tanımlar (K-009), `ONKAYIT.md` ve altın küme 1. parça cevapları (K-013). `araclar/kilitle.py` bu dosyaların yalnız hash'ini alır, içeriğini kullanmaz.

---

# A2 varsayımları

## V-024: HRR/VSA vektör temsili (tamsayı, CPU)
- **Bölüm:** sistem.md §1 (vektör ~128–384 boyut), §3 (kosinüs afinitesi, vektörleştirilmiş maskeli matmul), KODLAMA_PROMPTU §4 (A2 = HRR/VSA), K-012 (önce CPU/tamsayı, deterministik). Ek A O1 (bağlam): v = R[ilişki] + P_s⊛E[özne] + P_o⊛E[nesne], d~256. Ek A P1 (bağlam): vektör öğrenilmez, üçlüden yeniden kurulur.
- **Boşluk:** d'nin kesin değeri, öğe türü, ⊛'ın tamsayıyla nasıl hesaplanacağı, vektörlerin nasıl üretileceği, bileşen ölçekleri.
- **Öneri:**
  1. d = 256.
  2. Her öğe −1 ya da +1 tamsayı.
  3. ⊛ = dairesel evrişim. Tamsayıyla tam hesaplanır, FFT ve yuvarlama yok, bu yüzden her makinede bit düzeyinde aynıdır.
  4. v = 16·R[r] + P_s⊛E[s] + P_o⊛E[o]. ±1 vektörlerin evrişimi √d = 16 kat büyür; 16 çarpanı üç bileşenin büyüklüğünü eşitler.
  5. E[varlık], R[ilişki], P_s, P_o: (tohum, tür, ad) üçlüsünün hash'iyle açıkça kurulan üreteçten. Küresel rastgelelik yok, ekleme sırası sonucu değiştirmez.
  6. Benzerlik: kosinüs = tamsayı nokta çarpımı / √(normların çarpımı). Tek bölme, float64, CPU.
  7. Referans: saf Python döngüleri. Hızlı yol: torch int64 toplu hesap. Aynı girdide bit-eşitlik testi. GPU yok.
- **Önerilen kabul testleri:**
  - Belirlenim.
  - Referans = hızlı yol (bit-eşit).
  - SEKILLER tablosu ve şekil denetimi (eksen boyları 7, 11, 13; boş ve tek öğe).
  - Bileşen büyüklüklerinin eşitliği.
  - Çözme: v'den P_s'nin tersiyle özne geri bulunmalı (küçük kod kitabında en yakın komşu).
  - Yarı-diklik: rastgele çiftlerde |kosinüs| < 5/√d (d=256 için 0,3125).
  - Halka/olgu değişince vektör değişmeli, ilgisiz olgu değişince değişmemeli.
- **Felsefi:** EVET (eşleşme). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-014.

## V-025: torch'un kurulum yolu
- **Bölüm:** K-012, KODLAMA_PROMPTU §5 (lisansı belirsiz olanı kullanma), §8 (kurulum).
- **Durum:** Bu bulut ortamının ağ politikası `download.pytorch.org`'u engelliyor (403). PyPI'daki Linux torch tekerleği lisansı doğrulanmamış NVIDIA paketlerini zorunlu bağımlılık olarak çekiyor.
- **Öneri:** Kullanıcı ortam ayarlarında `download.pytorch.org`'a izin verir, CPU tekerleği hash'iyle sabitlenir. O zamana kadar A2 referans yolu (saf Python) torch'suz yazılabilir, hızlı yol bekler.
- **Felsefi:** hayır (lisans kuralı gereği). **Durum:** Kullanıcı (2026-10-23): ağ izni şimdilik yok, hızlı yol A5 öncesine (K-015).

## V-026: A2 kabul eşikleri ve vektör tohumu
- **Bölüm:** K-014 (V-024 test listesi). Çözme ve ölçek testleri için şartnamede sayı yok.
- **Uygulanan:**
  - **Vektör üretimi:** `vektor_tohum` (config). Bitler SHAKE-256("tohum|tür|ad") çıktısından alınır, 1 biti +1, 0 biti −1 olur. Python'un `hash()` işlevi kullanılmaz (süreçten sürece değişir).
  - **Yarı-diklik (K-014'te onaylı):** 100 rastgele varlık vektörünün bütün çiftlerinde |kosinüs| < 5/√d. Bu, 5 standart sapmaya karşılık gelir.
  - **Denge:** her vektörde |Σöğe| < 5√d (5 standart sapma).
  - **Ölçek:** ||P⊛E||² / ||16·R||² oranı [0,5; 2] aralığında (aynı büyüklük mertebesi). Ölçülen değer 0,93.
  - **Çözme:** sabit tohumla 60 kayıt, 100 varlık ve 21 anlamsız ilişki adı üzerinde özne, nesne ve ilişki %100 geri bulunur. Önden ölçümde doğru ile en yakın yanlış aday arasındaki en küçük fark 2,2 kattı, %100 sınırının arkasında bu pay var.
- **Dosyalar:** `config.json`, `testler/test_a2_vektor.py`.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

---

# A3 varsayımları

## V-027: A3 kapsamı
- **Bölüm:** KODLAMA_PROMPTU §4 (A3 = LLM'siz çekirdek), sistem.md §13 (H1: çekirdek + elle doğru DNA; H2: klonal seçilim; H3: müdahale, bellek; H4: sitokin, Treg, ablasyonlar).
- **Uygulanan:**
  - A3'te: havuz (§2), hücre/DNA (§3), sembolik eşleşme + afinite + yazma (§3), döngü ve durma (§5'in durma kısmı), plazma hücresi (§6).
  - A3'te yok: sitokin (§4) ve Treg (§5'in baskılama kısmı) H4'te. Öğrenme (§7) H2'de. Kredi (§8) H3'te. Defter ve müdahale testi (§9) A4'te.
  - A3'te "taklit" sitokin/Treg kodu yazılmaz.
  - A3 testleri anlamsız ilişki adlı ("blorp") elle yazılmış DNA ile yapılır. Akrabalık için elle doğru DNA H1'e (A5) aittir.
- **Felsefi:** hayır (yol haritasından). **Durum:** ONAYSIZ.

## V-028: Afinite, eşik ve güven formülü (eşleşme, güven)
- **Bölüm:** sistem.md §3: "sembolik bağlama maskesi × kosinüs afinitesi > θ", "ilişki dizini", "hücre başına tur başına ≤8 yazma", "tur başına eşleşme bütçesi", "güven = min-t-norm(afiniteler) × hücre güvenilirliği". KODLAMA_PROMPTU §5: zincir içinde min-t-norm, güven [0,1]'e kırpılır.
- **Boşluk:** afinitenin neyle neyin kosinüsü olduğu ve ölçeği; θ başlangıcı; ebeveyn kayıtların güveninin hesaba girip girmediği; hücre güvenilirliğinin başlangıcı; bütçe sayısı; 8'den fazla eşleşmede hangilerinin yazılacağı.
- **Öneri:**
  1. İlişki geni sert süzgeçtir. Halka yalnız aynı ilişkili kayıtlara bakar (ilişki dizini).
  2. Afinite = kırp(kosinüs(alıcı, kayıt vektörü) · √3, 0, 1). Kayıt vektörü üç eşit büyüklükte bileşenden oluştuğu için (K-014) tam uyumda kosinüs ≈ 1/√3 olur; √3 çarpanı bunu ≈1'e getirir. Elle yazılan hücrede alıcı = 16·R[ilişki geni]. Öğrenme H2'de.
  3. Halka ancak afinite > θ ise eşleşir. Elle yazılan hücrelerde başlangıç θ = 0,5. Ölçülen doğru-eşleşme afinitesi ≈1 ± 0,1, yani bol pay var. θ ileride kalibrasyon kümesinde seçilecek.
  4. Güven = min(halka afiniteleri, eşleşen kayıtların güvenleri) × hücre güvenilirliği. Ebeveyn güveni de min'e girer; böylece zincir hiçbir halkasından daha güvenilir olamaz. Elle yazılan hücrenin güvenilirliği = 1.
  5. Hücre bir turda 8'den fazla eşleşirse en yüksek afinite×güvenli 8'i yazılır. Eşitlikte kayıt kimliği sırası belirler.
  6. Tur başına eşleşme bütçesi 1024. Aşılırsa en düşük afinite×güvenliler atılır (§3) ve atılan sayısı günlüğe yazılır.
- **Felsefi:** EVET. **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-016.

## V-029: Durma ve impasse
- **Bölüm:** sistem.md §5: durma (a) yeni kayıt yok, (b) yanıt güveni > τ (τ = güven dağılımının yüzdeliği), (c) 8 tur; impasse'te bir kez eşik düşürülür. KODLAMA_PROMPTU §5: τ yalnız kilitli kalibrasyon kümesinde seçilir.
- **Boşluk:** kalibrasyon kümesi yokken τ'nun değeri; eşiğin ne kadar düşürüleceği.
- **Öneri:**
  1. Kalibrasyon kümesi oluşana kadar (b) kapalıdır. Döngü (a) ya da (c) ile durur. τ'yu kafadan uydurmuyorum.
  2. Impasse: sorgu için yanıt yok ve yeni kayıt da yoksa, bütün hücrelerin θ'sı bir kez yarıya iner, döngü sürer. İkinci impasse'te durur.
  3. Tur sınırı 8 (§5), config'te.
- **Felsefi:** EVET (durma). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-017.

## V-030: Plazma hücresi: ispat birleştirme ve cevap
- **Bölüm:** sistem.md §6 (aynı sonuca giden ispatlar noisy-OR, gerekçe zinciri), KODLAMA_PROMPTU §5 (noisy-OR yalnız ortak atası olmayan ispatlar arasında, log1p/expm1) ve §10 (sızıntı terimi ve bağımsızlık tanımı bilinen boşluk). Ek A P5 (bağlam): kök kümelerine göre bileşen, bileşen içi MAX, bileşenler arası noisy-OR.
- **Öneri:**
  1. Sorgu (A, B) için çıkarım katmanında öznesi A, nesnesi B olan kayıtlar ispattır.
  2. İki ispatın kök kümesi (katman 0'daki ata epitopları) kesişiyorsa aynı bileşendedir (geçişli). Bileşen içi MAX, bileşenler arası noisy-OR: 1 − Π(1 − g). Sızıntı terimi 0.
  3. Cevap, birleşik güveni en yüksek ilişkidir. İspat yoksa ya da en yüksek güvende iki farklı ilişki eşitse cevap "bilmiyorum" olur.
  4. Farklı ilişkilere giden ispatlar varsa sonuçta "çelişki var" diye işaretlenir. Çözümü A4'teki defterin işidir.
  5. Gerekçe, köken DAG'ından epitoplara kadar ağaç olarak verilir. Güven olasılık diye sunulmaz.
- **Felsefi:** EVET (güven, "bilmiyorum"). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-018.

## V-031: Havuzdan atma kuralı ve yayın sahnesi
- **Bölüm:** sistem.md §2: "dolunca YALNIZ çıkarım katmanından en düşük güven × yaş kaydı atılır", "her turda en yüksek skorlu ~4 öğe yayın sahnesine çıkar".
- **Boşluk:**
  - "güven × yaş" harfiyen okunursa yeni yazılan kayıt (yaş 0) hemen atılır.
  - Yayın sahnesinin skoru tanımsız. Eşleşmeyi nasıl etkilediği de belirtilmemiş.
- **Öneri:**
  1. Atma kuralı: çıkarım katmanında en düşük güvenli kayıt atılır. Eşitlikte en yaşlı, sonra en küçük kimlik. Yeni bir çarpan (γ) uydurulmaz.
  2. Katman 0 tek başına kapasiteyi aşarsa bölüm reddedilir. Atılacak çıkarım kalmamışsa yeni çıkarım yazılmaz ve günlüğe "havuz dolu" diye kaydedilir.
  3. Yayın sahnesi A3'te yoktur. Skoru sitokin, kredi ve sorgu uzaklığına (H3/H4) bağlı; onlarla birlikte gelir. Eşleşme bütün havuzda yarı-naif yapılır.
- **Felsefi:** EVET (bellek). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-019.

## V-032: DNA dosya biçimi ve tur düzeni
- **Bölüm:** sistem.md §3 (1–3 halka, değişkenli zincir, her halka ilişki geni + alıcı + θ), KODLAMA_PROMPTU §2.4 (dil veridir), §5 (şemalı veri).
- **Uygulanan:**
  - DNA bir JSON veri dosyasıdır (`sema/dna_v1.schema.json`). Her hücrede şunlar var: `kimlik`, 1–3 halka, `sonuc`, `guvenilirlik`.
  - Her halka ve sonuç bir ilişki geni ve iki değişken adı taşır. Halkanın ayrıca θ'sı vardır. Alıcı vektörü dosyada tutulmaz; elle yazılan hücrede ilişki geninden kurulur (V-028).
  - Sonuç değişkenleri gövdede geçmelidir. Genler onaylı şemada olmalıdır.
  - Tur eşzamanlıdır: bütün hücreler turun başındaki havuza bakar, yazmalar tur sonunda kayıt sırasıyla yapılır.
  - Yarı-naif kural: en az bir halka önceki turda yazılmış kayda bağlanır. İlk turda bütün epitoplar "yeni" sayılır.
  - Aynı (üçlü, köken) iki kez yazılmaz (karma tablo, §3).
- **Felsefi:** hayır (§3'ün doğrudan uygulaması). **Durum:** ONAYSIZ.

## V-033: Atılan kaydın mezar taşı
- **Bölüm:** K-019 (atma), K-018 (gerekçe köken DAG'ından). Ek A P6'da "mezar taşı" geçiyor (bağlam).
- **Uygulanan:**
  - Havuzdan atılan kayıt eşleşmeye katılmaz ve kapasiteye sayılmaz.
  - Kimliği, üçlüsü ve kökeni "mezar taşı" olarak saklanır. Böylece ondan türemiş kayıtların gerekçe ağacı ve kök kümesi kopmaz.
  - Atma günlüğe `ATMA` olayı olarak yazılır.
- **Felsefi:** hayır (kökeni korur, eşleşmeyi değiştirmez). **Durum:** ONAYSIZ.

## V-034: Sınırı aşan eşleşmeler ve günlük olayları
- **Bölüm:** K-016 (hücre başına 8, bütçe 1024), KODLAMA_PROMPTU §5 (hata yutma yok, durdurma, üst sınırlar).
- **Uygulanan:**
  - Hücre başına 8 sınırına giremeyen ve bütçeyi aşan eşleşmeler atılır. Sonraki turlara taşınmaz; §3'teki "atılır" ifadesiyle tutarlı.
  - Atılan sayısı günlüğe `ESLESME_ATILDI` olarak yazılır.
  - Atılacak çıkarım kalmadığı için yazılamayan kayıt `YEDEK_KULLANILDI` (neden: havuz dolu) olarak yazılır.
  - Her yazma `YAZMA`, her durma `DURMA` (neden ve tur) olayıdır. Zaman bilgisi tur numarasıdır (K-004).
  - Bütçe ve impasse çarpanı config'tedir: `eslesme_butcesi` (K-016), `impasse_esik_carpani` (K-017).
- **Felsefi:** hayır (onaylı kuralın uygulanışı). **Durum:** ONAYSIZ.

---

# A4 varsayımları

## V-035: A4 kapsamı ve defter altyapısı
- **Bölüm:** KODLAMA_PROMPTU §4 (A4 = defter + müdahale testi), §2.1 (destek/çelişki defteri ve müdahale testi ayrı modül), §5 (Defter, Müdahale testi); sistem.md §9, §18 (kök-ayrık destek ve çelişki).
- **Uygulanan:**
  - **Defter sınıfı:** `cekirdek/defter.py`. Hash zincirli olay günlüğünün (A0) alt sınıfıdır ve çekirdeğin günlüğü odur. Dizini olaylardan kurulur, dosyadan yeniden açılınca yeniden oluşur.
  - **Kaydedilen olaylar:** her ateşleme (θ'yı geçen her eşleşme, `ATESLEME`), yazma (`YAZMA`, kök kümesiyle), atma (`ATMA`), durma ve impasse.
  - **Toplu yazım:** bir turun olayları sırası korunarak tek seferde yazılır (`ekle_toplu`, tek fsync, zincir aynı).
  - **İz kuralı:** "Defterde izi olmayan sonuç yanıta giremez." Plazma yalnız defterde `YAZMA` izi olan çıkarımları ispat sayar. Bu yüzden `cevapla` artık defter ister. A3 testleri buna göre güncellendi; kilitli dosya değişikliği raporda bildirilir.
  - **Destek:** bir üçlünün canlı ispatlarında kök kümeleri ayrık bileşen sayısı (K-018 ile aynı bileşen tanımı).
  - **Bellekte günlük:** karşı-olgusal (müdahale) koşuları ana defteri kirletmesin diye dosyasız, bellekte günlüğe yazılır. Ana deftere yalnız sonuç özeti (`MUDAHALE`) gider.
  - **Kapsam dışı:** geri çekme olayı. Henüz geri çekme yapan bir işlem yok; KB'den olgu geri çekme besleme aşamasında (A7) gelecek. Hücre susturma ve uygunluk (§8) H3'te.
- **Felsefi:** hayır (prompt §5'in doğrudan uygulaması). **Durum:** ONAYSIZ.

## V-036: Çelişkinin tanımı ve etkisi
- **Bölüm:** KODLAMA_PROMPTU §5 ("çelişki bulunca iki kaydı da silme, çelişki düğümüne bağla, ortak destek kümesini kalıcı kaydet"), sistem.md §9 (c) ve §18, K-006 (şemadaki ters/simetrik/dışlayıcı/işlevsel işaretleri), K-018 (plazma çelişkiyi işaretler).
- **Boşluk:** çelişkinin tam tanımı; "ortak destek kümesi"nin anlamı; çelişkinin cevaba ve puana etkisi.
- **Öneri:**
  1. Onaylı şemaya göre üç tür çelişki var:
     - **dışlayıcı:** aynı (A,B) çiftinde aynı dışlayıcı gruptan iki farklı ilişki;
     - **işlevsel:** işlevsel bir ilişkide aynı A için iki farklı B;
     - **ters:** r(A,B) ve q(B,A) var ama q, r'nin ters adaylarından değil.
     Denetim her tur sonunda canlı kayıtlar arasında yapılır; epitoplar da dahildir.
  2. Hiçbir kayıt silinmez. Her çelişki bir kez `CELISKI` olayıyla kaydedilir: tür, iki kaydın kimliği ve ortak destek kümesi. Ortak destek kümesi, iki kaydın kök kümelerinin kesişimidir, yani iki tarafın da dayandığı epitoplar; şüpheli olgular bunlardır.
  3. Cevap K-018'deki gibi verilir, değişmez. Çelişki cevabın köken alt grafındaki bir kayda dokunuyorsa müdahale puanının tutarlılık (c) bileşeni 0 olur.
- **Felsefi:** EVET (güven, tutarlılık). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-020 (V-037'deki "b = 1, sınanamadı" önerisi kullanıcı şartıyla değişti: b ve puan boş, ayrı sayılır).

## V-037: Müdahale testi ve müdahale puanı
- **Bölüm:** sistem.md §9 (silme / tür uyumlu yedekle değiştirme, yalnız etkilenen köken alt grafı, ölçümler a/b/c), §8 (uygunluk = doğruluk × (ε + müdahale puanı); uygunluk H3'te), KODLAMA_PROMPTU §5 (yalnız çekirdeğin kendi zincirleri), §6 (ispat sadakati).
- **Boşluk:** hangi epitoplara müdahale edileceği, "tür uyumlu yedek"in ne olduğu, a/b/c'nin sayıya nasıl çevrileceği ve nasıl birleşeceği, geçişliliğin nasıl sınanacağı.
- **Öneri:**
  - **(a) Silme:** cevabın ispatlarındaki her kök epitop tek tek silinir. Kök kümesinde o epitop olan kayıtlar düşer, diğerleri kalır; bu "yalnız etkilenen köken alt grafı"dır. Cevabın güveni plazmayla yeniden hesaplanır. a = güveni gerçekten düşüren silmelerin oranı.
  - **(b) İlgisiz değişiklik:** sorgu yolundaki varlıklarla (cevabın köken ağacındaki epitopların varlıkları) kenar paylaşmayan her epitop, aynı ilişkili ama bölümde hiç olmayan yeni varlıklarla değiştirilir (tür uyumlu yedek). Ardından çekirdek bu olgularla yeniden çalışır. b = cevabın (ilişki ve güven) hiç değişmediği değişikliklerin oranı. İlgisiz epitop yoksa b = 1 olur ve "sınanamadı" diye işaretlenir.
  - **(c) Tutarlılık:**
    - Ters sorgu (B,A) cevaplanıyorsa cevabı ilk cevabın ters adaylarından biri olmalı.
    - Cevabın köken alt grafına çelişki (V-036) dokunmamalı.
    - İkisi de sağlanırsa c = 1, yoksa 0.
    - Geçişlilik sınanmaz: şemada geçişlilik bilgisi yok, uydurmuyorum.
  - **Müdahale puanı:** a × b × c, [0,1] aralığında. Cevap "bilmiyorum" ise puan yoktur.
  - **Kurallar:** Etiket, kâhin, kalibrasyon ve LLM bu hesaba girmez. Karşı-olgusal koşular ana havuzu ve defteri değiştirmez.
- **Felsefi:** EVET (kredi/uygunluk girdisi). **Durum:** ONAYLI (2026-10-23) → `KARARLAR.md` K-021 (V-037'deki "b = 1, sınanamadı" önerisi kullanıcı şartıyla değişti: b ve puan boş, ayrı sayılır).

## V-038: Çelişki ve müdahalenin uygulama ayrıntıları
- **Bölüm:** K-020, K-021.
- **Uygulanan:**
  - **Tersi tanımsız ilişki:** Şemada ters adayı boş olan bir ilişki için ters çelişkisi ve ters tutarlılığı denetlenmez; tersi bilinmiyor, uydurulmaz.
  - **Aynı kişi:** A = B olan kayıtta ters denetimi yapılmaz; bu durum dışlayıcı denetimine düşer.
  - **Tür uyumlu yedek:** aynı ilişki ve aynı güven; varlıklar bölümdeki en büyük kimlikten sonraki ilk iki yeni kimlik.
  - **Sorgu yolu varlıkları:** cevabın ispatlarının kök epitoplarındaki varlıklar.
  - **Karşı-olgusal koşular:** bellekte (dosyasız) defterle yapılır. Ana deftere yalnız `MUDAHALE` özeti yazılır.
  - **Arayüz:** `calistir` artık onaylı ilişki şemasını zorunlu ister (çelişki denetimi atlanamasın diye). A3/A4 testleri buna göre güncellendi.
- **Felsefi:** hayır (onaylı kuralların uygulanışı). **Durum:** ONAYSIZ.

## V-039: Mutasyon aracının zaman sınırı
- **Bölüm:** KODLAMA_PROMPTU §5 (her döngü için üst sınır), §6 (mutasyon sınaması).
- **Durum:** "tur sınırı yok" mutasyonu A4 testlerinden birinde (döngüsel kural) çekirdeği sonsuz döngüye soktu. Testler bu hatayı gerçekte yakalıyor (takım bitmiyor), ama araç sonsuza kadar bekliyordu.
- **Uygulanan:** bir kopya koşusu 600 sn'yi aşarsa durdurulur ve mutasyon "yakalandı (zaman aşımı)" sayılır. Normal koşu yaklaşık 25 sn.
- **Felsefi:** hayır (araç). **Durum:** ONAYSIZ.

---

# A5 varsayımları

## V-040: PyTorch hızlı yolunun yöntemi
- **Bölüm:** sistem.md §3 ("vektörleştirilmiş maskeli matmul"), KODLAMA_PROMPTU §4 (referans = hızlı, birebir aynı çıktı), §5 (tensör şekilleri, no_grad, .item() yok), K-014, K-015, K-022.
- **Uygulanan:**
  - **Evrişim:** sabit rol vektörü p ile toplu evrişim, int64 dairesel (circulant) matrisle matris çarpımıdır: M[j,k] = p[(k−j) mod d], sonuç = E @ M. Değişme özelliğinden p⊛E ile aynıdır, tamsayıyla tamdır.
  - **Kosinüs:** nokta çarpımları ve normlar int64. Tek kayan nokta adımı: nokta / √(norm·norm), float64. Tamsayılar 2^53'ten küçük olduğu sürece float64'e tam çevrilir ve sonuç referansla (Python `int / math.sqrt`) bit düzeyinde aynıdır. 2^53 aşılırsa hata verir, sessizce yaklaşık sonuç üretmez.
  - **Kök:** `torch.sqrt` (float64, CPU) bu derlemede doğru yuvarlanmıyor. Ölçüldü: √36912709632 için 1 ulp sapma; kesin rasyonel hesapla `math.sqrt` doğru çıktı. Bu yüzden payda kökü öğe öğe `math.sqrt` ile alınır, bölme torch'ta yapılır (IEEE, Python'la aynı ölçüldü).
  - **Taşma:** 2^53 sınırı çarpımlardan önce, Python tamsayılarıyla denetlenir. Sınır aşılırsa hata verilir.
  - **Afinite:** kırp(kosinüs · √3, 0, 1), referansla aynı sabit.
  - **Kapsam:** yalnız CPU; GPU ayrı aşamada (K-012). Şekiller SEKILLER eksen adlarıyla denetlenir.
  - **Bit-eşitlik denetimi:** kayan noktalı çıktılar `float.hex` ile karşılaştırılır (prompt §5: bit düzeyinde eşitlikte kayan nokta `==` kullanılmaz).
  - Çekirdek döngüsüne bağlama: V-042.
- **Felsefi:** hayır (referansla aynı sonucu veren hızlandırma). **Durum:** ONAYSIZ.

## V-041: Kurulum için Python 3.13 ve `.venv`
- **Bölüm:** KODLAMA_PROMPTU §8 (tek kurulum betiği), §5 (sabit sürüm ve hash), K-022. V-003'teki "≥3.10" alt sınırını kurulum için daraltır.
- **Durum:** `gereksinimler.txt` içindeki numpy, torch ve MarkupSafe hash'leri yalnız cp313 tekerlekleri (Linux x86_64, Windows amd64) için. Başka Python sürümünde `--require-hashes` kurulumu reddeder. A5 testleri torch ister ve atlanan test kabul edilmediği için torch'suz koşu kırmızıdır.
- **Seçenekler:** (a) kurulum için Python 3.13 zorunlu, paketler proje içindeki `.venv`'e; (b) başka Python sürümlerinin tekerlek hash'lerini de eklemek (her biri ayrıca doğrulanmalı).
- **Uygulanan:** (a). `kur.sh` / `kur.bat`: 3.13 denetimi → `.venv` yoksa kurulur → `pip install --require-hashes --only-binary=:all: -r gereksinimler.txt` → testler `.venv` yorumlayıcısıyla. Tam takım artık `.venv/bin/python araclar/kostur.py` ile koşar; sistem `python3` torch içermiyorsa A5 testleri kırmızı olur.
- **Doğrulama:** `kur.sh` bu ortamda (Linux) boş bir kopyada koşturuldu. `kur.bat` Windows olmadığı için DOĞRULANMADI.
- **Geri alma:** başka sürümlerin hash'lerini `gereksinimler.txt`'ye ekleyip sürüm denetimini gevşetmek.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-042: Hızlı yolun çekirdek döngüsüne bağlanması
- **Bölüm:** sistem.md §3 ("vektörleştirilmiş maskeli matmul"), K-015 (referans = hızlı), K-016 (alıcı = √d·R[gen]), V-040.
- **Durum:** Ölçümde döngü süresinin büyük kısmı, havuza yazılan her kaydın vektörünü saf Python evrişimiyle hesaplamaya gidiyordu.
- **Uygulanan:**
  - Vektör hesabının giriş noktası kod kitabıdır: `kayit_vektoru` ve `benzerlik_matrisi` yöntemleri. `KodKitabi` referans yoldur. `HizliKodKitabi` (`cekirdek/vektor_hizli.py`) aynı yöntemleri PyTorch ile ve bit-eşit ezer, Python türleriyle döner.
  - Havuz, döngü ve müdahale testi kendilerine verilen kod kitabının yolunu kullanır. Deney koşuları `HizliKodKitabi` ile yapılır; referans yol testlerde karşılaştırma için kalır.
  - Afinite tablosu: tur başında bir kez `{(gen, kayıt): afinite}`. Yalnız aynı gendeki canlı kayıtlar girer (sembolik maske). Elle yazılan hücrede alıcı yalnız gene bağlı olduğundan (K-016) bütün hücreler tabloyu paylaşır. Öğrenilen alıcılar (H2) gelince tablonun anahtarı alıcıya göre genişletilmeli.
  - Fark: eskiden afinite yalnız bir bağlamaya giren kayıtlar için hesaplanıyordu; şimdi o gendeki bütün canlı kayıtlar için. Değerler aynı. Tek davranış farkı: sıfır vektörlü bir kayıt (pratikte oluşmaz) hiç bağlanmasa da hata verir.
- **Doğrulama:** `testler/test_a5_dongu_hizli.py`. Dört senaryo (atma, bütçe, hücre sınırı, impasse, çelişki, müdahale) iki yolda koşar; defterin her olayı kanonik JSON ile (bit düzeyinde) aynı. Referans yolun izi, bağlamadan önceki koddan (commit 797eeaa) alınan altın değerlerle aynı.
- **Geri alma:** döngüye `KodKitabi` vermek (referans yol).
- **Ek (2026-10-24):** `HizliKodKitabi` rol vektörlerinin dairesel matrislerini kurulurken bir kez hesaplar. Ölçüm: gerçek DNA ile kayıt başına en pahalı adım bu matrislerin her çağrıda yeniden kurulmasıydı. Çıktı aynı (testle gösterildi).
- **Felsefi:** hayır (sonucu değiştirmeyen hızlandırma). **Durum:** ONAYSIZ.

## V-043: DNA sürüm 2'nin biçimi (K-025)
- **Bölüm:** sistem.md §3 (DNA, sembolik bağlama maskesi), K-025. Şartın biçimi tanımlı değil.
- **Uygulanan:**
  - `sema/dna_v2.schema.json`: sürüm 1'in aynısı, hücrede iki isteğe bağlı alan var. `farkli`: değişken çiftleri listesi (en az bir çift, her çift tam iki değişken). `okunus`: kuralın Türkçe okunuşu, yalnız insan gözden geçirmesi için; çekirdek okumaz.
  - Çiftteki iki değişken ayrı adlar olmalı ve gövdede (halkalarda) geçmeli; değilse DNA reddedilir.
  - Eşleşmede bağlama tamamlanınca her çiftin iki değişkeni farklı varlığa bağlı değilse bağlama atılır.
  - Hangi sürümün kabul edileceğini çağıranın verdiği biçim dosyası belirler. Sürüm 1 dosyaları aynen çalışır; şartsız hücrede davranış değişmez (A3/A4 testleri ve V-042 altın değerleri aynı).
- **Doğrulama:** `testler/test_a5_dna_v2.py`.
- **Felsefi:** K-025 ile onaylandı; buradaki yalnız biçim ayrıntısı. **Durum:** ONAYSIZ (biçim).

## V-044: H1 koşturucusunun ayrıntıları
- **Bölüm:** ÖK-002 (K-023) §2–§6, §9; KODLAMA_PROMPTU §5 (İstatistik, Uzun koşular). Sayılar ve yöntem ayrıntısı ön kayıtta yok.
- **Uygulanan:**
  - `degerlendirme/h1.py`. Kapı bölmeleri için config, DNA ve tohum manifestlerinin (`tohum_N/ozet.json`) özetleri `ONKAYIT.md` "9. Koşu öncesi ek" bölümünde yazılı olmalı; değilse koşu durur. Geliştirme bölmesi (eğitim) için bu şart yok.
  - Kümeler: zincir-bozukta `bozuk`, diğerlerinde `ana` (400'er). Kısa yol dedektörünün çözdüğü `treg` kümesi kapıya girmez.
  - Otomatik hata sınıfları: tur sınırı, havuz (atma ya da yedek olayı), bilmiyorum, yanlış ilişki. ÖK-002 §6'daki "ad yok / türetilemez / DNA / çekirdek" ayrımı incelemede yapılır.
  - Hata oranı aralığı: iki yanlı Clopper–Pearson, ikiye bölmeyle (200 adım). Müdahale puanı: ortalamanın yüzdelik bootstrap aralığı, `bootstrap_tekrar` = 10000, `istatistik_tohum` = 2027.
  - Uzun koşu: her `ara_kayit_araligi` (25) bölümde bir sonuç dosyası atomik yazılır. Sürdürmede eski satırların bölüm özetleri sırayla denetlenir. Duvar saati (`sure_sn`) belirlenim karşılaştırmasının dışındadır.
  - Bölüm dosyalarının özetleri üretecin manifestiyle karşılaştırılır; uyuşmazsa koşu durur.
- **Doğrulama:** `testler/test_a5_h1.py`, `testler/test_a5_istatistik.py`.
- **Felsefi:** hayır (ön kaydın uygulanışı). **Durum:** ONAYSIZ.

## V-045: Üretecin aday sınırı 20000 → 100000
- **Bölüm:** V-017 (üreteç parametreleri), ÖK-002 §4 (tohumlar 7–11 sabit).
- **Durum:** H1 bölümleri üretilirken tohum 8'de önsel-ters bölmesi 20000 adayda 400 bölümün 356'sını doldurdu ve üreteç durdu (doğru davranış: sessizce küçültmez).
- **Seçenekler:** (a) aday sınırını yükseltmek; (b) tohum 8'i atlayıp başka tohum seçmek. (b) veriye bakıp tohum seçmek olur, ön kayda aykırı.
- **Uygulanan:** (a), `aday_siniri` = 100000. Sınır yalnız durdurucudur: sınıra takılmayan bir üretimin çıktısı değişmez. Doğrulandı: tohum 7 manifestinin (`ozet.json`) özeti değişiklikten önce ve sonra aynı.
- **Geri alma:** değeri 20000'e döndürmek (tohum 8 yine durur).
- **Felsefi:** hayır. **Durum:** ONAYSIZ.

## V-046: Aynı ilişkinin yeni kökenle yeniden yazılması (AÇIK SORU, felsefi)
- **Bölüm:** sistem.md §2 ((üçlü, köken) tekilleştirmesi), §3 (yarı-naif eşleşme: önceki turda yazılmış kayıt), §5 (durma: yeni kayıt yok; kopyaları Treg baskılar, H4), §6 (kök-ayrık ispatlar noisy-OR), K-021 (a).
- **Bulgu (ölçüldü, eğitim bölmesi, tohum 7, ilk 60 bölüm, gerçek DNA, havuz 128):** Bütün yeni ilişkiler 2. turda bulunuyor; sonraki turlar aynı ilişkileri yalnız yeni kökenle yeniden yazıyor (bir bölümde 9 ilişki 738 kez, biri 121 kez). Simetrik ve ters kurallar döngü kuruyor. Her yeni köken "yeni kayıt" sayıldığı için döngü 8. tura kadar sürüyor, kopyalar havuzu doldurup doğru cevabı atıyor (aynı bölüm havuz 4096 ile doğru).
- **Ölçülen seçenekler** (ayrı kopyada, depodaki kod değişmeden; süreler A/B/C/bugün paralel koşuda, önbelleksiz):

  | Seçenek | Doğru / 60 | Atma | Ortalama tur | Durma | (a) ortalaması |
  |---|---|---|---|---|---|
  | Bugünkü (şartnamenin harfi) | 33 | 24080 | 8,0 | 60'ı tur sınırı | — |
  | A: kopya yazılır ama yeni tur başlatmaz ("yeni" = yeni üçlü) | 55 | 1628 | 3,0 | 55 yeni yok, 5 impasse | 0,974 |
  | B: aynı üçlü havuzdaysa hiç yazılmaz | 60 | 0 | 2,9 | 60 yeni yok | 1,000 (ikinci kanıt hiç yok) |
  | C: kopya yalnız yeni dayanak getiriyorsa yazılır (kök kümesi mevcut bir ispatınkini kapsamıyorsa) | 60 | 0 | 3,5 | 60 yeni yok | 0,992 |

  C, dairesel matris önbelleğiyle tek başına: bölüm başına 0,13 sn.
- **Öneri:** C. Kısır döngüleri keser, kök-ayrık (bağımsız) ispatları korur; böylece §6 noisy-OR ve K-021 (a) anlamlı kalır.
- **Durum:** KARARA BAĞLANDI: C (K-028, ÖK-002b, 2026-10-24). Uygulama `cekirdek/dongu.py` `yeni_dayanak_mi`; testler `testler/test_a5_kopya_c.py`.

## V-047: H1 hata incelemesi (teşhis)
- **Bölüm:** ÖK-002 §6 (hataların sınıflanması, kâhin tarafında).
- **Uygulanan:** `degerlendirme/h1_inceleme.py`. Hatalı her bölüm sınırlar gevşetilerek yeniden koşturulur: tur sınırı ×4, havuz ×32, ikisi birden. Cevap doğrulaşırsa "tur yetmedi" / "havuz yetmedi" / "ikisi yetmedi" (§6 sınıf 1); hiçbirinde doğrulaşmazsa "sınırdan bağımsız" (§6 sınıf 2–4, elle incelenir). Önce olağan ayarla yeniden koşulur ve aynı cevap çıkmazsa durur (belirlenim denetimi).
- **Kısıt:** Yalnız teşhistir; kapı sonucu, ayarlar ve DNA buna bakılarak değişmez. Rapor test cevapları içerir.
- **Felsefi:** hayır. **Durum:** ONAYSIZ.
