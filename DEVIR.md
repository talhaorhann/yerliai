# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). A5'te hızlı yol kuruldu (V-040) ve çekirdek döngüsüne bağlandı (V-042), sonuçlar referansla bit-eşit. İlk kurulum `sh kur.sh`; sonra `.venv/bin/python araclar/kostur.py` → 287/287, 0 atlanan, 0 xfail (V-041).
- **Sıradaki tek adım:** A5 (H1 deneyi). Önce yapılacaklar:
  1. Danışmanın DNA'sı gelince: `dna_kur` (sürüm 2) ile doğrula; her kuralın `okunus` cümlesini kullanıcıya evet/hayır listesi olarak getir.
  2. Onaylanan DNA ile `.venv/bin/python -m degerlendirme.h1 gelistir uretilen/h1 <dna> <çıkış>` (yalnız eğitim bölmesi). Hataları kullanıcı aracılığıyla danışmana götür. DNA'yı bu oturum düzeltmez (K-024: gizli tanımları bu oturum yazdı).
  3. Eğitimde %100 olunca DNA kilitlenir: `ozetler uretilen/h1 <dna>` çıktısını `ONKAYIT.md` "9. Koşu öncesi ek" bölümüne yaz, kullanıcıya bildir, kilidi yenile.
  4. Sonra bir kez `kapi` ve `altin` komutları. Kapı geçmezse ayar ve DNA değişmez; rapor kullanıcıya gider (ÖK-002 §6).
  - Yeni oturumda `uretilen/h1` yoksa `uret` ile yeniden üret (2 dk) ve manifest özetlerinin `ILERLEME.md`'dekilerle aynı olduğunu denetle.
  - Altın küme 2. parça cevapları kullanıcıda.
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `.venv/bin/python araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
