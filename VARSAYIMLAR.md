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
- **Felsefi:** EVET (izin ve yalıtım). Şu anki değer en kısıtlayıcı olandır, bu yüzden hiçbir davranışı serbest bırakmıyor. **Durum:** ONAYSIZ, A2 öncesi sorulacak.

## V-006: Zaman damgası ile determinizm çelişkisi
- **Bölüm:** KODLAMA_PROMPTU §5. "Her kayda ... zaman damgası" deniyor, ama aynı bölüm "saat yok" ve "aynı girdi ve tohum aynı çıktı" da diyor. Bağımsızlık testi (sistem.md §16) bit düzeyinde eşitlik istiyor.
- **Seçenekler:** (a) zaman damgası yok, yalnız sıra numarası, (b) duvar saati, ama karşılaştırma ve hash dışında tutulur, (c) mantıksal saat (tur/adım numarası).
- **Öneri:** (c) çekirdek kayıtlarında, (b) yalnız çekirdek dışı (besleme, tercüman) kayıtlarında.
- **Uygulanan (A0):** (a). Olay günlüğünde zaman alanı yok, en dar ve geri alınabilir seçenek.
- **Dosyalar:** `cekirdek/altyapi/olay_gunlugu.py`.
- **Geri alma:** kayda alan eklemek. Bu, şema sürümünü artırır.
- **Felsefi:** EVET (determinizm, bağımsızlık testi). **Durum:** ONAYSIZ, A1 başlamadan sorulacak (veri kayıtları buna bağlı).

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
