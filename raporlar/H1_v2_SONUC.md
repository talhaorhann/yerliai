# H1 yeniden deneme (ÖK-003) sonucu, 2026-10-24

## Sonuç: KAPI GEÇMEDİ

Ön kayıt: ÖK-003 ve ekinin 1–7. bölümleri. Kod `157c1fb`, ek kilidi `6cf0c85`. Çekirdek LLM'siz.

- **Ayarlar:** tur 8, havuz 256, hücre sınırı 8, C kuralı hücre sınırından önce (K-031).
- **DNA:** `624b073c…` (170 kural).
- **Tohumlar:** 12, 13, 14, 17, 16. Tohum 15, kısa yol kapısında durduğu için 17 ile değişti (K-030); 3 değişim hakkından 1'i kullanıldı.

| Bölme (5 tohum × 400) | Doğru | Yanlış ilişki | Bilmiyorum | Müdahale: puanlı / sınanamadı |
|---|---|---|---|---|
| uzunluk | 2000/2000 | 0 | 0 | 1999 / 1 |
| önsel-ters | 2000/2000 | 0 | 0 | 1999 / 1 |
| zincir-bozuk | 2000/2000 ("bilmiyorum" doğru cevap) | 0 | — | — |
| yön ters | **1881/2000** | 0 | 119 | 1880 / 1 |

- **Kapı:** her bölmede ve her tohumda %100, tolerans yok. Yön ters bölmesi beş tohumun hepsinde altında kaldı: 29, 21, 23, 17 ve 29 hata.
- **Yanlış ilişki:** hiç yok. 119 hatanın hepsi "bilmiyorum"; durma nedeni hepsinde impasse.
- **Ayrı satırlar (kapıya girmez):**
  - Yeni tohumların eğitim bölmesi: 2000/2000 (`H1_v2_yeni_egitim_RAPOR.md`).
  - Eski eğitim, olağan sınırlarla: 2000/2000 (`H1_v2_eski_egitim_RAPOR.md`).
  - Altın küme 1. parça: 50/50 kullanıcıyla aynı. 2. parçada kullanıcı cevabı yok (`H1_v2_altin_RAPOR.md`).

ÖK-003 §6'ya göre ayarlar ve DNA bu sonuca bakılarak değiştirilmedi. Karar kullanıcınındır.

## Yön ters hatalarının teşhisi (yalnız rapor; kâhin tarafı)

1. **Sınırsız DNA kapanışı:** 119 hatanın 119'unda cevap kapanışta yok. Bu kapanışta sınır ve afinite yok, farklı kişi şartı var. Yani çekirdek (sınırlar, C, eşleşme) neden değil: olgulardan DNA kurallarıyla bu cevaba varılamıyor.
2. **Örnek (tohum 12, `8353c15a54aa`):**
   - Olgular: 15'in kızı 30, 30'un kız kardeşi 29. Soru: 29 → 15. Cevap: anne.
   - 15'in kadın olduğunu gösteren tek bağ şu: 15, 14 ile evli, ve "12'nin erkek kardeşi 14" olgusundan 14 erkek.
   - Ama 14 ile 15'in evli olduğunu söyleyen bir olgu yok.
   - Üretecin çıkarılabilirlik denetimi (K-029, ÖK-003 §3.1) ağaç yapısını, evlilikler dahil, sabit tutuyor ve yalnız cinsiyetleri değiştiriyor. Bu yüzden soruyu "çıkarılabilir" saydı.
   - Kaba kuvvet de aynı sonucu veriyor: yapı sabitken karşı örnek yok. Yani denetim kendi tanımına göre doğru çalışıyor. Sorun tanımın kendisinde: yapıyı bilen kâhin, yalnız olguları gören çekirdekten fazlasını biliyor.
3. **Ölçüm, bütün yön ters soruları (2000):** Denetimin bir türü koşuldu. Bu türde yalnız olgularda görünen evlilikler sabit; görünür evlilik, ya bir eş olgusu ya da aynı çocuğun iki ebeveyni olarak olgularda geçmesi demek.

   | Çekirdek | Görünür evliliklerle çıkarılabilir | Çıkarılamaz |
   |---|---|---|
   | doğru (1881) | 1854 | 27 |
   | bilmiyorum (119) | 6 | **113** |

   - 119 hatanın 113'ü olgularda görünmeyen bir evliliğe dayanıyor.
   - 6 hatanın nedeni başka bir gizli yapı olmalı; ayrıca incelenmedi.
   - Bu tür denetim kesin bir "yalnız olgulardan çıkarılabilirlik" tanımı değil: çekirdeğin doğru bildiği 27 soruyu da çıkarılamaz sayıyor. Örneğin kardeşler üzerinden çıkarılabilen evlilikleri görmüyor.
4. **Kayıtlar:** `uretilen/h1_v2_kapi_1/` (satırlar, `yon_ters_teshis.json`; git dışında).

## Notlar

- İlk koşuyla kıyas (ÖK-003 §1): yön ters 573 → 1881, uzunluk 1980 → 2000. Önsel-ters ve zincir-bozuk iki koşuda da tam.
- Çıkarılabilirlik denetiminin tanımı ve bu bulgu: V-053.
