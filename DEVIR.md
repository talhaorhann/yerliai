# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Güncel durum (2026-10-25):** `DURUM.md`. A6'da K-035 maskeli bellek geçidi yazıldı; gerçek DNA gösterimi `raporlar/A6_gosterim_v8.md`. Açık: V-058 (kullanıcı), DNA "son sürüm" (danışman), altın küme 2. parça, A6 bağımsız incelemesi.
- **DNA:** v8 depoda ama kilitli değil; danışman "son sürüm" demeden kilitlenmez. "Son sürüm" gelince sıra K-033'te: V-053'ü üretece bağla, ÖK-004'ü (ilk iki koşunun sonuçları ve nedenleri, DNA ve config özetleri) yaz ve kilitle, H1'i taze tohumlarla (≥ 18) tek sefer koş. Geçmezse dur, kullanıcıya dön.
- **FİKİRLER:** Her aşama kapanışında `FIKIRLER.md`'ye bak; yaklaşan madde varsa kullanıcıya hatırlat.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). A5'te hızlı yol kuruldu (V-040) ve çekirdek döngüsüne bağlandı (V-042), sonuçlar referansla bit-eşit. İlk kurulum `sh kur.sh`; sonra `.venv/bin/python araclar/kostur.py` → 389/389, 0 atlanan, 0 xfail (V-041).
- **H1 durumu:** H1 iki kez kapıyı geçmedi. İkinci koşuda uzunluk, önsel-ters, zincir-bozuk bölmeleri 5 tohumda 2000/2000, yön ters 1881/2000 (ilk koşuda 573/2000). Yanlış ilişki iki koşuda da 0. 119 hatanın hepsi 'bilmiyorum'; 113'ü üretecin çıkarılabilirlik tanımının olgularda görünmeyen evliliği kullanmasından. H1 resmen KANITLANMAMIŞTIR; çekirdek lehine güçlü kanıt vardır.
- **Sıradaki adım (K-032):** A6 (bellek geçidi + iç dil) ve V-053 (çıkarılabilirlik tanımı, kullanıcı onayına).
  - V-053 onaylanınca: ÖK-004 yazılır, H1 taze tohumlarla tek sefer koşar (tohum değişim hakkı 2). Altın küme 2. parça cevapları bu koşudan önce gelir.
  - **H2 kapısı:** V-053 kapanmadan ve H1 yeniden koşulmadan H2 başlatılamaz (kodda zorunlu). Bu kapıyı kapatan ya da gevşeten kod yazılmaz.
  - Aşama sonu bağımsız inceleme A6 sonunda yapılır.
  - A6 kodu: `cekirdek/bellek_gecidi.py`, `cekirdek/bellek.py`, `cekirdek/ic_dil.py` (öneri; V-054–V-056 onaysız). V-053 tanımı `degerlendirme/dunya.py` `olgudan_cikarilabilir_mi` (üretece bağlanmadı; onaydan sonra `uretec.Parametreler.cikarilabilirlik` buna geçer).
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `.venv/bin/python araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
