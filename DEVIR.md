# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0 ve A1 kapandı (etiketler yerel). Dal `asama-2`. `python3 araclar/kostur.py` → 147/147, 0 atlanan, 0 xfail.
- **Altın küme:**
  - 1. parça kaydedildi (K-013, ÖK-001): LLM ön cevabı, kullanıcı onaylı, üreteçle 50/50 uyumlu. Kalibrasyonda kullanılmaz.
  - 2. parça A5'e kadar gelecek. Gelince: `kullanici_cevaplarini_coz` → `kullanici_cevaplari_2.json` (kaynağı sor ve yaz) → `karsilastir` → yalnız uyuşmayanları raporla. Tanımlara kullanıcı kararı olmadan dokunma.
- **Bekleyen kullanıcı kararları:** V-024 (A2 temsili, felsefi), V-025 (`download.pytorch.org` izni).
- **Sıradaki tek adım:** V-024 onayı gelince önce A2 kabul testleri (kırmızı), sonra saf Python tamsayı referans yolu. torch gelince hızlı yol ve bit-eşitlik testi.
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
