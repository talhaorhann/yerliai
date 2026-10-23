# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0, A1, A2 kapandı (etiketler yerel). `python3 araclar/kostur.py` → 169/169, 0 atlanan, 0 xfail.
- **A2:** yalnız saf Python tamsayı referans yolu (K-014, K-015). PyTorch hızlı yolu ve bit-eşitlik testi A5 öncesinde yazılacak. Ağ izni (`download.pytorch.org`) gerekiyor (V-025).
- **Altın küme:** 1. parça kaydedildi (K-013, ÖK-001). 2. parça A5'e kadar gelecek; gelince kaynağını sor, `karsilastir` ile yalnız uyuşmayanları raporla, tanımlara dokunma.
- **Sıradaki tek adım:** A3 (LLM'siz çekirdek) için `sistem.md` §2–§8'i oku, boşlukları V kaydına yaz, felsefi olanları tek soruda sor. Ardından `asama-3` dalında kabul testleri.
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
