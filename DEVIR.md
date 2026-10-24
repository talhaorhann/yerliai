# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). A5'te hızlı yol kuruldu (V-040) ve çekirdek döngüsüne bağlandı (V-042), sonuçlar referansla bit-eşit. İlk kurulum `sh kur.sh`; sonra `.venv/bin/python araclar/kostur.py` → 287/287, 0 atlanan, 0 xfail (V-041).
- **Sıradaki tek adım:** Kullanıcının H1 sonrası kararı (`raporlar/H1_SONUC.md`). Kapı geçmedi; ön kayda göre ayar ve DNA bu sonuca bakılarak değiştirilmez. Bir aşama kapısı geçmeden sonraki aşama (A6/H2) başlamaz (KODLAMA_PROMPTU §4).
  - Yeniden deneme ancak yeni bir ön kayıtla (ÖK-003) ve yeni tohumlarla olur; eski test bölümleri o zaman geliştirme verisi sayılır.
  - Altın küme 2. parça cevapları kullanıcıda; gelince `.venv/bin/python -m degerlendirme.h1 altin veri/dna/akrabalik_dna_v2_final.json <çıkış>`.
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `.venv/bin/python araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
