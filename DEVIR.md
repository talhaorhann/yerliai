# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). A5'te hızlı yol kuruldu (V-040) ve çekirdek döngüsüne bağlandı (V-042), sonuçlar referansla bit-eşit. İlk kurulum `sh kur.sh`; sonra `.venv/bin/python araclar/kostur.py` → 315/315, 0 atlanan, 0 xfail (V-041).
- **Sıradaki tek adım:** ÖK-003 (K-029) uygulanıyor; sıra `ONKAYIT.md` ÖK-003 §5'te.
  - Tohum 15 kısa yol kapısında durdu (V-050); kullanıcı kararı bekleniyor. Karar gelmeden yeni tohum üretilmez.
  - DNA'yı yalnız danışman düzeltir (K-024). Son DNA eski eğitimde (tohum 7–11) %100 olmalı: `.venv/bin/python -m degerlendirme.h1 gelistir uretilen/h1 <dna> <çıkış>`.
  - Sonra sınır seçimi (eski dört test bölmesi): `.venv/bin/python -m degerlendirme.h1_sinir uretilen/h1 <dna> <çıkış>`; seçilen değerler config'e, özetler ÖK-003 ekine; kilitle; kapı bir kez.
  - Altın küme 2. parça cevapları kullanıcıda.
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `.venv/bin/python araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
