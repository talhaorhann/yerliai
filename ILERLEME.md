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

**Durum:** YARIM. Üreteç tasarımı (V-015), kelime çantası kuralı (V-016) ve ilişki şeması (V-013) kullanıcı onayı bekliyor. A1 kapısı geçilmedi, etiket yok.

**Çalışan (testle gösterilmiş):**
- `cekirdek/altyapi/sema_dogrulayici.py`: JSON Schema alt kümesi. Bozuk kayıtlar reddedilir: eksik/fazla alan, yanlış tip, aralık dışı, NaN, enjeksiyon metni.
- `cekirdek/iliski_semasi.py`: şema yalnız onay kaydındaki hash tutarsa yüklenir. Sonradan eklenen ilişki ve tek bayt değişiklik yakalanır. Ters/simetrik tutarlılığı denetlenir.
- `cekirdek/bilgi_tabani.py`: kabul/ret/karantina. Her karar günlükte. LLM kaydı karantinada kalır.
- Dil veridir taraması: şema verisindeki hiçbir ilişki adı kodda ve testlerde geçmiyor.
- Mutasyon: A1'de 13/13, A0'da 15/15 yakalandı.

**Eksik:** üreteç ve kısa yol dedektörü (`NotImplementedError`), kilitli altın/kalibrasyon kümesi mekanizması (üreteçle birlikte), ad havuzu ve parafraz (Türkçe aşaması).
