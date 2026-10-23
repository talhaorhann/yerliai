# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A3 kapandı (etiketler yerel: `asama-0`…`asama-3`). `python3 araclar/kostur.py` → 205/205, 0 atlanan, 0 xfail. Mutasyon: A0 15/15, A1 30/30, A2 11/11, A3 25/25.
- **Sıradaki tek adım:** A4 (destek/çelişki defteri + müdahale testi).
  - Oku: sistem.md §8–§9, Ek A (defter omurgası: kök epitop kümesi, kökleri ayrık ispat sayısı, şema çelişkisi, sorgu uzaklığı).
  - Felsefi boşlukları (müdahale ölçütleri, çelişki tanımı, uygunluk formülü) tek onay listesinde sor; felsefi olmayanlarda sormadan ilerle (kullanıcı tercihi).
- **Bekleyenler:** altın küme 2. parça (A5'e kadar); PyTorch ağ izni (A5 öncesi, K-015).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `python3 araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
