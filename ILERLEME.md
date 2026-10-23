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

## A1: bilgi tabanı + sentetik soy ağacı üreteci (dal `asama-1`)

**Durum:** Kelime çantası kapısı (ilk kabul ölçütü) beş bölmenin hepsinde geçti. Açık kalan: önsel-ters bölmesi (V-020), gizli tanımların kullanıcı okuması (V-019), altın/kalibrasyon kümesi (kullanıcıdan). Bu yüzden etiket atılmadı.

**Çalışan (testle gösterilmiş):**
- Şema doğrulayıcı, onay kilitli ilişki şeması (K-006), bilgi tabanı (ret/karantina/günlük).
- `degerlendirme/dunya.py`: soyut soy ağacı ve gizli yapısal tanımlar. Her ağaçta tanımların onaylı şemayla tutarlı olduğu sınanır: tek ilişki, ters, işlevsellik, simetri.
- `degerlendirme/uretec.py`: bölmeler eğitim (k=2–3), uzunluk (k=4–10), zincir-bozuk, yön ters ve yeniden adlandırma.
  - Bölüm dosyasında cevap ve bölme adı yok. Cevaplar `kahin/` klasöründe.
  - Kimlikler ve olgu sırası karıştırılıyor.
  - Olgu grafiğinde en kısa yol tam k.
- `degerlendirme/kisa_yol.py`: Naive Bayes dedektörü, Treg ayrımı ve kapı. Dikkat dağıtıcısız ham veride dedektör kısa yolu yakalıyor (0,27 > şans 0,15), yani değersiz değil.
- `degerlendirme/kilitli_kumeler.py`: hash denetimi ve kesişim durdurucusu.
- Tam üretim: `python3 -m degerlendirme.uretec <klasör>` (~11 sn). İki koşu birebir aynı çıktı veriyor.

**Kapı sonuçları (config boyutu, ana küme 400, ölçüm ikinci yarı 200):**

| Bölme | Dedektör doğruluğu | Şans | Sınır (şans + 0,05) |
|---|---|---|---|
| eğitim | 0,135 | 0,140 | 0,190 |
| uzunluk | 0,105 | 0,150 | 0,200 |
| zincir-bozuk (karışım) | 0,4525 | 0,500 | 0,550 |
| yön ters | 0,085 | 0,125 | 0,175 |
| yeniden adlandırma | 0,105 | 0,160 | 0,210 |

**Kilitli dosya değişiklikleri (bildirim):**
- `config.json`'a K-007/K-008 için yalnız yeni anahtarlar eklendi, eski değerler aynı.
- `testler/test_a1_uretec_iskelet.py` yeniden yazıldı, artık yalnız önsel-ters iskeletini sınıyor (üreteç artık var).

**Mutasyon:** A0 15/15, A1 25/25 yakalandı.

**Eksik:**
- Önsel-ters bölmesi (`NotImplementedError`, V-020).
- Altın/kalibrasyon kümesi yok, mekanizma hazır.
- Kesişim denetimi yalnız birebir aynı bölümü yakalar, izomorf olanları yakalamaz.
- İsim havuzu ve parafraz Türkçe aşamasında.
- Ek A P7'deki "kural alt kümesi" yok (Ek bağlamdır, karar değildir).
