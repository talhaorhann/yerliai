# Havuz ve eşleşme bütçesi baskısı: DNA v8, 244 kural (2026-10-25)

ÖK-004 §4'teki ek rapor; kapıya girmez. **Sınırlar değiştirilmedi** (ÖK-003 eki §6'da kilitli).

- **Araç:** `degerlendirme/h1_baski.py`. Komut: `.venv/bin/python -m degerlendirme.h1_baski uretilen/h1 veri/dna/akrabalik_dna_v8.json uretilen/h1_baski_v8`. Özet: `raporlar/H1_baski_v8_ozet.json`.
- **Veri:** geliştirme verisi (tohum 7–11; birinci koşunun bölümleri). Eğitim + dört kapı bölmesi, 10.000 bölüm. H1 son denemesinin taze tohumlarına (18–22) bakılmadı.
- **Sınırlar (kapı ayarı):** tur 8, havuz 256, eşleşme bütçesi 1024, hücre başına tur başına 8 yazma, kopya kuralı C hücre sınırından önce (K-031).
- **Süre:** 3 dakika (4 süreç; müdahale testi yok).

## Sonuç

| Bölme | Doğru | Tur sınırına ulaşan | Havuz dolan | Bütçe aşılan | Hücre sınırı kesen | En çok tur | En çok havuz doluluğu | Bütçeye giren en çok aday | Sınırla ilişkili hata |
|---|---|---|---|---|---|---|---|---|---|
| eğitim | 2000/2000 | 0 | 0 | 0 | 63 | 5 | 63 | 76 | 0 |
| uzunluk | 2000/2000 | 0 | 0 | 0 | 636 | 7 | 186 | 232 | 0 |
| yön ters | 574/2000 | 0 | 0 | 0 | 49 | 6 | 93 | 132 | 0 |
| önsel-ters | 2000/2000 | 0 | 0 | 0 | 24 | 5 | 82 | 66 | 0 |
| zincir-bozuk | 2000/2000 | 0 | 0 | 0 | 3 | 6 | 46 | 50 | 0 |

- **Tur:** hiçbir bölüm tur sınırına (8) ulaşmadı; en çok 7 tur (uzunlukta).
- **Havuz:** hiçbir bölümde havuz dolmadı, hiçbir kayıt atılmadı. En yüksek doluluk 186/256 (%73). Uzunlukta 33 bölüm genel ayardaki 128'i aşardı; kapı ayarı 256 bu yüzden gerekli.
- **Bütçe:** hiçbir turda bütçe aşılmadı. Bütçe, C ve hücre süzgecinden sonraki adaylara uygulanır; bir turda bütçeye giren en çok aday 232 (uzunluk), bütçe 1024 (yaklaşık 4,4 kat boşluk). Süzgeçten önceki ham eşleşme bir turda 2179'a kadar çıkıyor.
  - Bütçeye giren aday sayısı ayrı bir geçici ölçümle alındı (çekirdek değiştirilmeden, aday listesinin uzunluğu sayıldı; betik depoda değil).
- **Hücre sınırı:** 775 bölümde kesti (toplam 9232 eşleşme). Bunların 768'inde cevap doğru. Kalan 7'si yön terste "bilmiyorum"; hücre sınırı kaldırılınca da cevap "bilmiyorum" kalıyor, yani nedenleri sınır değil (ayrı geçici denetim).
- **Yön ters 574/2000:** birinci koşuyla aynı ölçüde (573/2000). Bu eski verinin soruları çıkarılabilirlik denetimi olmadan üretildi (ÖK-003 §1). 1426 hatanın hepsi "bilmiyorum", hiçbiri bir sınıra ulaşmadı. Taze tohumlarda üreteç V-053 tanımıyla bu soruları ayıklar (ÖK-004 §3.1).
- Aynı ölçüm H1 son denemesinde kapı tohumlarıyla da raporlanacak: `.venv/bin/python -m degerlendirme.h1_baski uretilen/h1_v3 veri/dna/akrabalik_dna_v8.json <çıkış> kapi`.
