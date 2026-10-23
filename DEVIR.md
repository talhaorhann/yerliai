# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A4 kapandı (etiketler yerel: `asama-0`…`asama-4`). A5'te hızlı yol kuruldu (V-040) ve çekirdek döngüsüne bağlandı (V-042), sonuçlar referansla bit-eşit. İlk kurulum `sh kur.sh`; sonra `.venv/bin/python araclar/kostur.py` → 254/254, 0 atlanan, 0 xfail (V-041).
- **Sıradaki tek adım:** A5 (H1 deneyi). Önce yapılacaklar:
  1. Kullanıcının onay listesine cevabı: (1) `H1_ONKAYIT_TASLAGI.md` ÖK-002 olarak kilitlensin mi, (2) DNA'yı bağımsız oturum mu yazsın, bu oturum mu, (3) DNA'ya "farklı kişi" şartı eklensin mi. Cevap gelmeden H1 koşturulmaz.
  2. Altın küme 2. parça cevapları (kullanıcıda).
  3. Onaydan sonra: DNA (eğitim bölmesinde geliştirme), H1 koşturucusu (`degerlendirme/` içinde), ek tohumlar, sonra test bölmeleri bir kez.
- **H1 raporu şartı (K-021):** müdahalede "sınanamadı" sorular başarı sayılmaz, ayrı satırda sayıyla gösterilir (`mudahale_ozeti`).
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli. Değişiklikten sonra `.venv/bin/python araclar/kilitle.py` çalıştırılır ve raporda bildirilir.
