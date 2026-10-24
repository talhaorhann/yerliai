# H1 sonucu (2026-10-24)

**Kapı (ÖK-002 §6): GEÇMEDİ.** Ön kayda göre ayarlar ve DNA değiştirilmedi; karar kullanıcının.

Koşu: kilitli DNA (`624b073c…`, 170 kural), havuz 128 (ÖK-002a), kopya kuralı C (ÖK-002b), kod `91591f3`, 4 kapı bölmesi × 5 tohum × 400 = 8000 bölüm, 23 dk. Bütün sonuçlar LLM'siz çekirdeğindir.

| Bölme | Doğru | Hata | Hata sınıfı (otomatik) | Teşhis (V-047) |
|---|---|---|---|---|
| önsel-ters | 2000/2000 | 0 | — | — |
| zincir-bozuk | 2000/2000 | 0 | — | — |
| uzunluk (k=4–10) | 1980/2000 | 20 | 20 bilmiyorum (6'sı tur sınırında) | 3 tur yetmedi, 3 havuz yetmedi, 14 sınırdan bağımsız |
| yön ters | 573/2000 | 1427 | 1427 bilmiyorum | 1427 sınırdan bağımsız |
| eğitim (geliştirme, kapıya girmez) | 2000/2000 | 0 | — | — |

- Hiçbir bölmede yanlış ilişki söylenmedi; bütün hatalar "bilmiyorum". Zincir-bozukta yanlış pozitif 0.
- Müdahale (K-021): puanlı soruların ortalama puanı her bölmede 0,99–1,00. "Sınanamadı": önsel-ters 1, uzunluk 1, yön ters 2 (başarı sayılmadı). Zincir-bozukta cevap olmadığı için 2000 cevapsız.

## Yön ters hatalarının kaynağı (ölçüldü)

| Cevap | Cevabı belirleyen kişinin cinsiyeti olgularda (doğrudan ya da eş üzerinden) | Doğru | Yanlış |
|---|---|---|---|
| cinsiyet belirtmeyen ilişki (eş, torun, yeğen, kuzen) | — | 415 | 0 |
| cinsiyet belirten ilişki | var | 86 | 1 |
| cinsiyet belirten ilişki | yok | 72 | 1426 |

Yorum: 1427 hatanın 1426'sında cevabı belirleyen kişinin cinsiyetine olgularda basit kanıt yok; büyük olasılıkla cevap olgulardan türetilemiyor (ÖK-002 §6 sınıf 2) ve çekirdek doğru biçimde "bilmiyorum" diyor. Üreteç (V-017) cevabın olgulardan türetilebilir olmasını şart koşmuyordu. Kesin değil: 72 soruda çekirdek cinsiyeti dolaylı yoldan buldu; basit denetimin kaçırdığı dolaylı kanıtlar olabilir.

## Uzunluk hataları

20 hatanın 6'sı sınırla ilgili (3'ü 8 tur, 3'ü 128 havuz yetmedi; ikisi de ön kayıtta sabit). 14'ünde cevabı belirleyen kişinin cinsiyeti olgularda var. İlk örnek elle izlendi: doğru cevap için zincirdeki kişilerin birbirinden farklı olduğu bilgisinin bir kuralla kullanılması gerekiyor; tur ve havuz büyütülünce de çıkmıyor. DNA eksiği ya da kural biçiminin sınırı olabilir; ön kayda göre bu hatalara bakılarak DNA değiştirilmedi.

## Altın küme (kapıya girmez)

- 1. parça (kaynak=LLM, onaylayan=kullanıcı; bağımsız insan cevabı değil, ÖK-001): 50/50 kullanıcıyla aynı.
- 2. parça: kullanıcı cevabı henüz yok; çekirdek üreteçle 50/50 aynı.

Ayrıntılar: `raporlar/H1_kapi_RAPOR.md`, `raporlar/H1_kapi_ozet.json`, `raporlar/H1_altin_RAPOR.md`. Bölüm bölüm hata incelemesi (test cevapları içerir) git dışında: `uretilen/h1_kapi_1/RAPOR_hatalar.md`.
