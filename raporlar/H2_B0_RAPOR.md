# H2 B0 raporu (2026-10-26)

**Dayanak:** K-041 (Kapı 0), ÖK-005 taslağı (`ONKAYIT_H2_TASLAK.md`), `H2_TASARIM.md` §7. B0'da deney yok; yalnız altyapı kuruldu ve M0 geliştirme havuzunda koştu. DNA v8 kullanılmadı: M0'ın DNA kurallarından kaçını bulduğuna bakılmadı; o yalnız B2b finalinde ölçülür.

## Yapılanlar

| Parça | Dosya | Durum |
|---|---|---|
| Tek aday şeması, kırmızı takım dosyası şeması, içerik göstermeyen denetleyici | `sema/aday_v1.schema.json`, `sema/kirmizi_dosyasi_v1.schema.json`, `kesif/aday.py` | testli |
| Danışmana istek (kayıt biçimi, 3 örnek, görünür aileler G1–G4, teslim yolu) | `raporlar/GIZLI_SAHTE_KURAL_ISTEGI.md` | gönderildi |
| H2 ayar dosyası (H1 config'i değişmedi) | `config_h2.json` | kilitli |
| Tohum türetme (etiketten, değiştirilemez) | `kesif/tohum.py` | testli |
| Tipli şablon ailesi T ve kademeleri K1–K5 | `kesif/sablon.py` | sayılar kâğıt üstü tabloyla aynı |
| Sembolik sayaç (referans + hızlı, birebir aynı) | `kesif/sayac.py` | testli |
| M0 ve koşucusu | `kesif/m0.py`, `degerlendirme/h2_m0.py` | 3 koşu bit-aynı |
| Dünya aileleri A1, A2 (evlilik oranı), A3 (ikinci, bağımsız üretici) | `degerlendirme/dunya.py`, `degerlendirme/ikinci_uretec.py`, `degerlendirme/h2_dunya.py` | H1 dünyaları bit-aynı kaldı |
| Havuzlar 16/24/8 ve dünya özetleri | `raporlar/h2_b0/havuz_ozetleri.json` | 48 dünya, hepsi tekil |
| Sorgu bütçesi defteri | `degerlendirme/h2_butce.py` | testli |
| Derece-koruyan yeniden bağlama, boş dünya, boş-dünya sayacı | `degerlendirme/h2_bagla.py` | testli |
| Çekirdek kod özeti (dondurma) | `araclar/cekirdek_ozeti.py` | testli |
| Mutasyon sınaması | `araclar/mutasyon_b0.py` | bkz. aşağı |

## M0 (geliştirme havuzu, 16 dünya, K5/21)

| Ölçü | Değer |
|---|---|
| Aday uzayı | 35.544.873 (kâğıt üstü hesapla aynı) |
| Süzgeçten geçen (yanlış 0, tanık ≥ 3) | 203.124 |
| Üç koşunun çıktı özeti | `1b4388db…` (üçü aynı); özet dosyası `9baf3703…` (üçü aynı) |
| Süre | 885 / 901 / 907 s (ortanca 901 s; 4 iş parçacıklı tek süreç) |
| Bellek | ≈1,4 GB |

- Süre tahmini (5–35 dk) tuttu: ≈15 dk.
- **203.124 sayısı aşama 5 talebi değildir.** Aşama 1–4 (özellikle fazla halkayı atan aşama 2 ve yedeklilik) bunu küçültecek. Tur anahtarı için gereken talep C, B1'de bu aşamalardan sonra ölçülür (ÖK-005 §4 madde 3).
- Aday listesi (112 MB) depoya konmadı; aynı girdiyle bit-aynı yeniden üretilir.

## Bütçe kademeleri (ÖK-005 §4 madde 23)

M0 tam koşu süresinin (ortanca 901 s) %1, %3, %10, %30 ve %100'ü, aşağı yuvarlanmış: **9, 27, 90, 270, 901 s.** Birim: 4 iş parçacıklı tek sürecin duvar saniyesi.

## Dünya boyları (geliştirme havuzu, kişi sayısı)

| Aile | Kişi sayıları | Ortalama |
|---|---|---|
| A1 | 28, 73, 68, 34, 53, 67 | 54 |
| A2 | 50, 22, 69, 12, 56 | 42 |
| A3 | 53, 62, 73, 38, 39 | 53 |

## Bulunan ve düzeltilen

1. **Şablon kuralı yazımı:** ÖK taslağında "tek halkalı gövde başla aynı olamaz" yazıyordu. Onaylı sayılar baştan beri "gövde başın kendisini içeremez" kuralıyla hesaplanmıştı. Metin sayılara uyduruldu; sayılar değişmedi (V-060).
2. **A3'te çift terim:** taslakta "eş adayı atlanır" yazıyordu; "üretim durur" oldu (daha temkinli; V-062).
3. **Boş dünyada "temsilci":** ikiden çok ilişkili sınıflarda kodlanamıyordu; "ileri taraf" kuralı yazıldı (V-063).
4. **Aracın komut satırı:** var olmayan bir ayar anahtarını okuyordu; elle denemede yakalandı, düzeltildi, test eklendi.

## Kapı 1 için

- Mühürlenecek metin: `raporlar/h2_b0/OK005_MUHUR_METNI.md`.
- Mühürden sonra B1 başlar.
- B1'in ön şartı: danışmanın gizli kırmızı takım dosyası.
