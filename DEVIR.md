# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`.

- **Ne çalışıyor:** A0 ve A1 kapandı (etiketler `asama-0`, `asama-1`; yalnız yerel, uzak depoya etiket gönderimi 403). `python3 araclar/kostur.py` → 147/147, 0 atlanan, 0 xfail.
- **Bekleyen kullanıcı işi:** altın küme cevapları. Sorular `degerlendirme/altin/altin_soru_1.md` ve `_2.md` dosyalarında. Kullanıcı sohbete "1B 2A ..." yazar.
  - Cevap gelince: `degerlendirme.altin.kullanici_cevaplarini_coz` ile ayrıştır, `kaynak=kullanıcı` olarak `degerlendirme/altin/kullanici_cevaplari_<parça>.json` dosyasına yaz.
  - `karsilastir` ile üreteçle uyuşmayanları çıkar ve kullanıcıya üretecin cevabını söylemeden yeniden sor.
  - Kullanıcı `degerlendirme/altin/uretec_cevaplari.jsonl` dosyasını görmemeli.
- **Açık varsayımlar:** V-001…V-005, V-007…V-012, V-014, V-017, V-018, V-021…V-023 ONAYSIZ (felsefi değil). V-005: A2 öncesi sorulacak (numpy/torch).
- **Sıradaki tek adım:** A2 (HRR/VSA vektörleri) için önce V-005 sorusu, sonra `asama-2` dalı ve kabul testleri.
- **Kural hatırlatma:** `testler/`, `config.json` ve `config.json`'daki `kilitli_veri_dosyalari` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
