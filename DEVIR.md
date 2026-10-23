# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). `python3 araclar/kostur.py` → 230/230, 0 atlanan, 0 xfail.
- **Sıradaki tek adım:** A5 (H1 deneyi). Önce yapılacaklar:
  1. PyTorch hızlı yolu ve bit-eşitlik testi (K-015). Ağ izni (`download.pytorch.org`) kullanıcıda.
  2. Altın küme 2. parça cevapları (kullanıcıda).
  3. H1 ön kaydı `ONKAYIT.md`'ye (veriye bakmadan): hipotez, metrik, eşik, bölmeler.
  4. Akrabalık için elle doğru DNA (sistem.md §13 H1). Gizli tanımlardan (kâhin) türetilmemeli; nasıl yazılacağı felsefi, kullanıcıya sorulacak.
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `python3 araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
