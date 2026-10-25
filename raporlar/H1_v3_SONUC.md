# H1 son deneme (ÖK-004): sonuç (2026-10-25)

**Kapı (ÖK-002 §6, ÖK-004 §4): GEÇTİ.** Kapıya giren dört bölmenin her birinde, beş taze tohumun her birinde 400/400 doğru; toplam 8000/8000. Yanlış ilişki 0, "bilmiyorum" 0 (zincir-bozukta beklenen "bilmiyorum" doğru sayılır). Tolerans uygulanmadı.

- **Ön kayıt:** ÖK-004 ve eki §1–§5 (`ONKAYIT.md`). Kod commit `60e38f3`. DNA v8 (`4a4af6b8…`, 244 kural). Config `feae4096…`.
- **Tohumlar:** 18, 19, 20, 23, 22. Tohum 21 önsel-ters bölmesinde kısa yol kapısında durdu (0,445 > 0,370 + 0,05); kullanıcı ve danışman onayıyla yerine 23 geçti (ÖK-004 eki §4). Değişim hakkı 1 kaldı.
- **Çekirdek sınırları:** tur 8, havuz 256, bütçe 1024, hücre 8, kopya kuralı C hücre sınırından önce (ÖK-003 eki §6, K-031). Hiçbir ayar sonuca bakılarak değiştirilmedi.
- **Süre:** 29 dakika (tek süreç, müdahale testiyle).
- **Kapı özeti:** `raporlar/H1_v3_kapi_ozet.json`, sha256 `935cea7b47dcccb319e86bf68f02b3be7312cf9b924334ce9a449cc446cf11cf`. Ayrıntı: `raporlar/H1_v3_kapi_RAPOR.md`.

## Kapı bölmeleri

| Bölme | Doğru | Yanlış | Bilmiyorum | Hata %95 üst sınır | Müdahale: puanlı / sınanamadı / cevapsız | Ortalama müdahale puanı |
|---|---|---|---|---|---|---|
| uzunluk | 2000/2000 | 0 | 0 | 0,0018 | 2000 / 0 / 0 | 0,995 |
| yön ters | 2000/2000 | 0 | 0 | 0,0018 | 1998 / 2 / 0 | 0,987 |
| önsel-ters | 2000/2000 | 0 | 0 | 0,0018 | 1998 / 2 / 0 | 0,997 |
| zincir-bozuk | 2000/2000 | 0 | 0 | 0,0018 | 0 / 0 / 2000 | — |

- Müdahale kapıya girmez (ÖK-004 §4). "Sınanamadı" olan 4 soru başarı sayılmadı, ayrı satırda (K-021): yön ters tohum 19 ve 22'de birer, önsel-ters tohum 23'te iki. Zincir-bozukta cevap "bilmiyorum" olduğu için müdahale yok (cevapsız).
- Hata %95 üst sınırı: 0 hatada Clopper-Pearson üst sınırı; tohum başına 0,0092, bölme başına 0,0018.

## Kapıya girmeyen satırlar

- **Yeni tohumların eğitim bölmesi:** 2000/2000 (her tohumda 400/400); müdahale 2000 puanlı, ortalama 0,995. `raporlar/H1_v3_yeni_egitim_RAPOR.md`.
- **Altın küme** (`raporlar/H1_v3_altin_RAPOR.md`):
  - Parça 1: 50 soru, kullanıcı cevabıyla 50/50 aynı. Kaynak LLM, kullanıcı onaylı; bağımsız insan cevabı değil (ÖK-001).
  - Parça 2: 50 soru, kullanıcı cevabıyla 50/50 aynı. **Cevapların 50'si de LLM taslağı, kullanıcı onaylı** (danışman kaba kuvvet denetleyicisiyle hesapladı; 5 gözetçi aynı cevabı buldu); bağımsız insan cevabı değil (ÖK-001).
  - İki parçada da emin değil 0, seçenek dışı 0, üreteçle aynı 50/50.
- **Baskı ölçümü (kapı tohumları, eğitim + dört kapı bölmesi, 10.000 bölüm; `raporlar/H1_v3_baski_ozet.json`):** tur sınırına ulaşan 0 (en çok 7/8), havuz dolan 0 (en çok 202/256), bütçe aşılan 0, sınırla ilişkili hata 0. Hücre sınırı 841 bölümde kesti; hepsinde cevap doğru.

## Üç koşunun karşılaştırması

| Koşu | Tohum | DNA | Uzunluk | Yön ters | Önsel-ters | Zincir-bozuk | Kapı |
|---|---|---|---|---|---|---|---|
| ÖK-002 (birinci) | 7–11 | v2, 170 kural | 1980/2000 | 573/2000 | 2000/2000 | 2000/2000 | geçmedi |
| ÖK-003 (ikinci) | 12, 13, 14, 17, 16 | v2, 170 kural | 2000/2000 | 1881/2000 | 2000/2000 | 2000/2000 | geçmedi |
| ÖK-004 (son) | 18, 19, 20, 23, 22 | v8, 244 kural | 2000/2000 | 2000/2000 | 2000/2000 | 2000/2000 | **geçti** |

- Üç koşuda da yanlış ilişki 0.
- İkinciden sonuncuya değişenler yalnız ÖK-004 §3'tekiler: üretecin çıkarılabilirlik tanımı (V-053, K-034) ve DNA v8 (K-038). Çekirdek ve sınırlar ikinci koşudakiyle aynı.

## H2 kapısı

Kapalı: `.venv/bin/python -m degerlendirme.h2` → "V-053 açık: H1 taze tohumlarla yeniden koşulmadı (ÖK-004 sonucu yok)". H2 kapısını açan "## ÖK-004 sonucu" başlığı yazılmadı; kullanıcı kararı bekliyor.
