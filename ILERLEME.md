# İLERLEME

## A0: klasör iskeleti, config, rapor/kayıt altyapısı (dal `asama-0`)

**Durum:** testler yeşil, etiket `asama-0` (yalnız yerel; uzak depoya etiket gönderimi 403 ile reddedildi, kullanıcı: bir şey yapma). Bağımsız inceleme bekliyor (`inceleme/A0_istemi.md`); inceleme bitmeden A1'e başlanmaz.

**Çalışan (testle gösterilmiş):**
- Klasörler: `cekirdek/` (+ `altyapi/`), `tercuman/`, `degerlendirme/`, `karsilastirma/`, `veri/`, `sema/`, `kilit/`, `araclar/`, `testler/`.
- `config.json` + `cekirdek/altyapi/ayar.py`: her değer kaynaklı, en fazla 5 bayrak, riskli bayraklar kapalı, bozuk ayar reddedilir.
- `cekirdek/altyapi/olay_gunlugu.py`: sadece-ekleme, sıra numaralı, hash zincirli. Değiştirme, silme, yarım satır yakalanır. `YEDEK_KULLANILDI` sayacı var.
- `cekirdek/altyapi/atomik.py`: atomik kayıt. Öldürülüp devam ettirilen koşu kesintisiz koşuyla aynı sonucu verir.
- Yasak kalıp taramaları: çekirdek importları, kâhin yalıtımı, sihirli sayı, modül başlığı, izlenebilirlik, test atlatma, hash kilidi.
- Mutasyon sınaması: 15 kasıtlı hatanın 15'i yakalandı (`python3 araclar/mutasyon_a0.py`).

**Komutlar:**
- Tüm testler: `python3 araclar/kostur.py` (ya da `./kur.sh`)
- Mutasyon sınaması: `python3 araclar/mutasyon_a0.py`
- Test/eşik dosyası değişirse (onaydan sonra): `python3 araclar/kilitle.py`

**Eksik / sonraki aşamalara bırakılan:**
- "Kodda ilişki sözcüğü geçmez" taraması: sözlük verisi A1'de gelince yazılacak.
- "LLM paketi kurulu olmadan testler geçer" ve bağımsızlık testi: LLM yok, A7'de anlamlı. Şimdilik çekirdek yalnız standart kütüphane kullanıyor.
- Ağ kapalı temiz ortamda kurulum denemesi ve `kur.bat` (Windows): DOĞRULANMADI.
- Aşama öncesi/sonrası test sayısı karşılaştırması: A0 sıfırdan başladı (önce 0, şimdi 57 test).

## A1: bilgi tabanı + sentetik soy ağacı üreteci (dal `asama-1`, etiket `asama-1`)

**Durum:** KAPANDI. Kelime çantası kapısı altı bölmenin hepsinde geçti. Altın küme soruları hazır ve kilitli; kullanıcının cevapları bekleniyor (A1 kapısı değil, K-011).

**Çalışan (testle gösterilmiş):**
- Şema doğrulayıcı, onay kilitli ilişki şeması (K-006), bilgi tabanı (ret/karantina/günlük).
- `degerlendirme/dunya.py`: soyut soy ağacı ve onaylı gizli tanımlar (K-009, hash kilitli). Her ağaçta tanımların şemayla tutarlılığı sınanır.
- `degerlendirme/uretec.py`: bölmeler eğitim, uzunluk, zincir-bozuk, yön ters, yeniden adlandırma ve önsel-ters (K-010). Önsel-ters'te cevap dağılımının ters döndüğü Spearman testiyle gösterildi.
  - Cevaplar `kahin/` klasöründe.
  - Kimlikler ve olgu sırası karıştırılıyor.
  - En kısa yol tam k.
- `degerlendirme/kisa_yol.py`: dedektör, Treg ayrımı ve kapı. Dedektör ham veride kısa yolu yakalıyor.
- `degerlendirme/altin.py`: 2 × 50 altın soru (40 zincirli + 10 zincir-bozuk), A/B/C/D seçenekli.
  - Kayıtlı ve kilitli (`kilit/kilitli_kumeler.json`). Eğitim üretimi bu kümeyle kesişirse durur.
  - Kullanıcı cevabı ayrıştırıcısı ve karşılaştırıcısı hazır.
- Tam üretim: `python3 -m degerlendirme.uretec <klasör>` (~27 sn), deterministik.

**Kapı sonuçları (config boyutu):**

| Bölme | Dedektör doğruluğu | Şans | Sınır |
|---|---|---|---|
| eğitim | 0,135 | 0,140 | 0,190 |
| uzunluk | 0,105 | 0,150 | 0,200 |
| zincir-bozuk (karışım) | 0,453 | 0,500 | 0,550 |
| yön ters | 0,085 | 0,125 | 0,175 |
| yeniden adlandırma | 0,105 | 0,160 | 0,210 |
| önsel-ters | 0,295 | 0,295 | 0,345 |

**Kilitli dosya değişiklikleri (bildirim):**
- `config.json`'a üreteç (K-007/K-008), altın küme (K-011) ve kilitli veri listesi (K-009) için yalnız yeni anahtarlar eklendi.
- `testler/test_a1_uretec_iskelet.py` artık önsel-ters testi.
- `testler/test_a1_uretec.py`'den eski "önsel-ters yazılmadı" testi çıkarıldı. Yerine üç önsel-ters testi geldi. Toplam test sayısı arttı: 134 → 147.

**Mutasyon:** A0 15/15, A1 30/30 yakalandı (`python3 araclar/mutasyon_a0.py`, `python3 araclar/mutasyon_a1.py`).

**Eksik:**
- Altın küme kullanıcı cevapları (2 parça).
- Kalibrasyon kümesi: ~500 örnek, CLUTRR aşamasında (sistem.md §9).
- Kesişim yalnız birebir aynı bölümü yakalar.
- İsim/parafraz Türkçe aşamasında.
