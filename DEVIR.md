# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). A5 1. adım bitti: PyTorch CPU hızlı yolu, referansla bit-eşit (V-040). İlk kurulum `sh kur.sh`; sonra `.venv/bin/python araclar/kostur.py` → 244/244, 0 atlanan, 0 xfail (V-041).
- **Sıradaki tek adım:** A5 (H1 deneyi). Önce yapılacaklar:
  1. Hızlı yolu çekirdek döngüsüne bağlamak (döngü şimdilik referans yolu kullanıyor), sonuçlar referansla aynı kalmalı.
  2. Altın küme 2. parça cevapları (kullanıcıda).
  3. H1 ön kaydı `ONKAYIT.md`'ye (veriye bakmadan): hipotez, metrik, eşik, bölmeler.
  4. Akrabalık için elle doğru DNA (sistem.md §13 H1). Gizli tanımlardan (kâhin) türetilmemeli; nasıl yazılacağı felsefi, kullanıcıya sorulacak.
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `.venv/bin/python araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
