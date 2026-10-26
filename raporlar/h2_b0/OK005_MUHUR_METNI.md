## ÖK-005 (H2): mühür (Kapı 1)

**Tarih:** 2026-10-26.
**Dayanak:**
- K-041: Kapı 0 onayı; altı soruya evet; sayaç + çekirdek hakem hattı; A6 bağımsız incelemesi Kapı 2'den önce.
- K-042: Kapı 1 onayı.

**Metin:** `ONKAYIT_H2_TASLAK.md`, sha256 `38833917d2b75a3bac89e7520edff8f79ce07c86b2da26bb1785b2ee84d397ea`.
- Kapı 0'da onaylanan taslaktır.
- B0'da yapılan üç yazım düzeltmesi içindedir; hiçbiri bir sayıyı değiştirmedi:
  - V-060: gövde başın kendisini içeremez;
  - V-062: A3'te çift terimde üretim durur;
  - V-063: boş dünyada ileri taraf.
- Dosya kilitlidir (`config_h2.json` `h2_kilitli_veri_dosyalari`).
- Bundan sonraki her değişiklik yalnız aşağıya "ÖK-005 eki" olarak yazılır. Sonuçtan sonra değişen eşik sonuca "keşif" damgası vurdurur.

**Tasarım:** `H2_TASARIM.md`, sha256 `a409858e54b2a0434d0b84a77e15ca4d7ac7063beeea23e179705e180aafb1db`.

### ÖK-005 eki §1: B0 sonuçları ve mühür anındaki özetler (2026-10-26)

1. **M0 (geliştirme havuzu, 16 dünya, K5/21):**
   - aday uzayı 35.544.873 (kâğıt üstü hesapla aynı);
   - süzgeçten geçen 203.124.
   - Üç koşu bit-aynı:
     - `m0_adaylar.jsonl` `1b4388dbfb05cf5bfa55bc6e30a1671a38fcf8b595279bbe8d75227667c5ba0b`;
     - `m0_ozet.json` `9baf3703586c019ca57339387e9e5e22ef48a63f655dc4da7b2d4c1ec4c35fd1` (`raporlar/h2_b0/m0_ozet.json`).
   - Süreler: 885, 901 ve 907 s; ortanca 901 s; 4 iş parçacıklı tek süreç.
   - Koşular `config_h2.json` `7a67eb949240f6f821374d32af49d95d2108d4ca6ceab4a572d8011aa30e0e53` ile yapıldı. Mühürdeki özetle farkı yalnız `h2_kilitli_veri_dosyalari` alanıdır.
2. **Bütçe kademeleri (ÖK-005 §4 madde 23):** 9, 27, 90, 270, 901 s. Birim: 4 iş parçacıklı tek sürecin duvar saniyesi.
3. **Havuzlar:**
   - geliştirme 16, final 24, kontrol 8; 48 dünya özeti tekil;
   - liste `raporlar/h2_b0/havuz_ozetleri.json`, sha256 `f4e81f2a12eb2365c4c3b6b9ab201ef6bebfa873a68babcca28a35e5c76a9be1`.
   - Final ve kontrol dünyaları yalnız özetlendi; içerikleri açılmadı.
4. **Çekirdek dondurma sözleşmesi:**
   - çekirdek özeti (`araclar/cekirdek_ozeti.py`): `db87374f5835af1d37aae951ae9b5f931fe5c6c483da38fb96eedf9595d4aafa`;
   - keşif paketi özeti: `bd28557183f70c7ec290d98f4ffc23588fce08de2247c1ff0d97304f561032b1`.
   - Hiperparametreler H1 değerleridir.
5. **Dosya özetleri:**

   | Dosya | sha256 |
   |---|---|
   | `config_h2.json` | `c48869ca88b4c2026b3c380035ab0dce7e1a05ad01b19c77d66f5350f47ecb59` |
   | `sema/aday_v1.schema.json` | `c20ff73649ee42504fd4ce6e1d84dbee84608063793a8f2691a92ca6a779ef51` |
   | `sema/kirmizi_dosyasi_v1.schema.json` | `b98151939e96b23db7e732673dddded1a521e9f930ad292d443aaef9e9bff83b` |
   | `veri/h2/kirmizi_ornek_v1.json` | `2f993c84541e9bd28443627a34a24a03eaa4fbdd9983bc0ed038f5d62705e095` |
   | `degerlendirme/h2_dunya.py` | `3847838b0484650e17b9846900315bac4a2c9ddd2352feb734f497f32996bb81` |
   | `degerlendirme/ikinci_uretec.py` | `c8dc8147b0c6d2652201aec016c2ad2d57ac14871c292c48bd91b3ad2d9db958` |
   | `degerlendirme/h2_butce.py` | `7fcba03a8809f6e46850963eda8dc1226483d53ee869d15aef229e9e23b32feb` |
   | `degerlendirme/h2_bagla.py` | `ddbf39ce741897b7b65022b0df7c9b0403a30c7b34d6d64d090e1cef2e5b744f` |
   | `degerlendirme/h2_m0.py` | `ea4144173c7a443c782aa1467a5ee33617f674f548108990a80b5f00ba9bc05d` |
   | `degerlendirme/dunya.py` | `e2af2801191c2814676634f26e9d78c75234336a93ef7f1fc013b05f5a242b03` |

6. **Mutasyon sınaması:** 48 mutant, 48 yakalandı. İlk turda 3'ü kaçtı (M0 sırası, M0'da OI sayımı, havuz tohumunun ailesi); üçü için test eklendi, kod değişmedi.
7. **Henüz gelmeyenler:**
   - Gizli kırmızı takım dosyası: B1'den önce danışmandan gelir; özeti §2 olarak eklenir.
   - K değerleri: B1 kalibrasyonundan sonra §3 olarak eklenir.
   - A6 bağımsız inceleme: Kapı 2'nin ön şartı.
