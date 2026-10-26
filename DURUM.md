# DURUM: nerede kaldık

- **H1 son deneme (ÖK-004): KAPI GEÇTİ (2026-10-25).** Uzunluk, yön ters, önsel-ters ve zincir-bozuk bölmelerinde tohum 18, 19, 20, 23, 22 ile 8000/8000; yanlış 0, "bilmiyorum" 0. Eğitim satırı 2000/2000; altın küme 50/50 ve 50/50 (parça 2'nin cevapları LLM taslağı, kullanıcı onaylı). Sınırlara ulaşılmadı. `raporlar/H1_v3_SONUC.md`.
  - Önceki iki koşu geçmedi (K-033). Değişenler: V-053 üreteçte (K-034), DNA v8 (K-038). Tohum 21 → 23 onaylı değişim (hak 1 kaldı).
- **H2 kapısı: AÇIK (K-040).** "## ÖK-004 sonucu" kapı özetinin sha256'sıyla yazıldı. **H2 koduna başlanmaz:** önce (a) A6 bağımsız incelemesinin sonucu, (b) H2 tasarım tartışması (danışman + kullanıcı, literatür taraması), (c) H2 ön kayıt belgesi (yeni ÖK). Girdiler: `H2_TASARIM_TASLAGI.md`, `raporlar/ONSEL_TERS_KISA_YOL_TESHIS.md`.
- **H2 B0 TAMAM (2026-10-26, K-041):**
  - Altyapı kuruldu: şablon, sayaç, M0, aileler A1–A3, havuzlar, sorgu defteri, yeniden bağlama, çekirdek özeti.
  - M0 geliştirme havuzunda üç kez bit-aynı (≈15 dk); mutasyon 48/48.
  - **Kapı 1 bekleniyor:** mühür metni `raporlar/h2_b0/OK005_MUHUR_METNI.md`.
  - B1 için danışmanın gizli kırmızı takım dosyası gerekir (`raporlar/GIZLI_SAHTE_KURAL_ISTEGI.md`). A6 bağımsız incelemesi Kapı 2'den önce.
  - Rapor: `raporlar/H2_B0_RAPOR.md`.
- **H2 tasarımı (2026-10-26):** `H2_TASARIM.md` (nihai öneri, v1'e sadık, 20 gerekçeli sapma) ve `ONKAYIT_H2_TASLAK.md` (ÖK-005 taslağı, mühürsüz). Kapı 0 bekleniyor: kullanıcı onayı + 6 evet/hayır sorusu + A6 bağımsız inceleme sonucu. Onaya kadar B0 yok.
- Kilitli kalanlar: DNA v8, config, ÖK-004. Kalan tohum değişim hakkı 1, onaysız kullanılmaz.
- **A6:** maskeli bellek geçidi (K-035, K-037); bağımsız inceleme isteği kullanıcıda (`raporlar/A6_BAGIMSIZ_INCELEME_ISTEGI.md`).
- İlk kurulum: `sh kur.sh`; testler: `.venv/bin/python araclar/kostur.py`.
