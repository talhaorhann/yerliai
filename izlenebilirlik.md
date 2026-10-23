# İzlenebilirlik: şartname → kod → test

`testler/test_a0_yapi.py` bu tabloyu otomatik tarar: her kod modülü tabloda olmalı, tablodaki her dosya var olmalı, her satırın testi olmalı.

| Şartname | Kod | Test |
|---|---|---|
| KODLAMA_PROMPTU §5 (Config) | `cekirdek/altyapi/ayar.py`, `config.json` | `testler/test_a0_ayar.py` |
| KODLAMA_PROMPTU §5 (Determinizm, hash) | `cekirdek/altyapi/kanonik.py` | `testler/test_a0_olay_gunlugu.py` |
| KODLAMA_PROMPTU §5 (Defter, Hata yutma yok) | `cekirdek/altyapi/olay_gunlugu.py` | `testler/test_a0_olay_gunlugu.py` |
| KODLAMA_PROMPTU §5 (Uzun koşular) | `cekirdek/altyapi/atomik.py` | `testler/test_a0_atomik.py` |
| KODLAMA_PROMPTU §5 (Kilitli kümeler) | `araclar/kilitle.py`, `kilit/kilitler.json` | `testler/test_a0_kilit.py` |
| KODLAMA_PROMPTU §9 (Rapor) | `araclar/kostur.py` | `testler/test_a0_yasak_kaliplar.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması) | `araclar/mutasyon_a0.py` | `testler/test_a0_yasak_kaliplar.py` |
| KODLAMA_PROMPTU §2 (Çekirdek–LLM ayrımı, kâhin yalıtımı) | `cekirdek/__init__.py`, `tercuman/__init__.py`, `degerlendirme/__init__.py`, `karsilastirma/__init__.py` | `testler/test_a0_yasak_kaliplar.py` |
| KODLAMA_PROMPTU §3 (izlenebilirlik, başlık atfı) | `izlenebilirlik.md` | `testler/test_a0_yapi.py` |
| KODLAMA_PROMPTU §4 (A0 iskeleti) | `kur.sh`, `kur.bat` | `testler/test_a0_yapi.py` |
| KODLAMA_PROMPTU §5 (Şema ve veri; V-011) | `cekirdek/altyapi/sema_dogrulayici.py`, `sema/uclu_kaydi_v1.schema.json` | `testler/test_a1_sema_dogrulayici.py` |
| sistem.md §14 (şema onayı; V-013) | `cekirdek/iliski_semasi.py`, `araclar/sema_onayla.py`, `sema/iliski_semasi_v1.schema.json`, `sema/iliskiler_v1.json` | `testler/test_a1_iliski_semasi.py` |
| sistem.md §1, §14 (bilgi tabanı; V-012, V-014) | `cekirdek/bilgi_tabani.py` | `testler/test_a1_bilgi_tabani.py` |
| KODLAMA_PROMPTU §2.4 (dil veridir) | `sema/iliskiler_v1.json` | `testler/test_a1_dil_veridir.py` |
| sistem.md §10 (önsel-ters; V-020 onay bekliyor) | `degerlendirme/uretec.py` | `testler/test_a1_uretec_iskelet.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A1) | `araclar/mutasyon_a1.py` | `testler/test_a0_yasak_kaliplar.py` |
| sistem.md §11 (soy ağacı, gizli tanımlar; K-007, V-019) | `degerlendirme/dunya.py`, `degerlendirme/veri/tanimlar_v1.json`, `degerlendirme/veri/tanimlar_v1.schema.json` | `testler/test_a1_uretec.py` |
| sistem.md §10, §11 (bölmeler, bölüm biçimi; V-017) | `degerlendirme/uretec.py`, `sema/bolum_v1.schema.json`, `sema/cevap_v1.schema.json` | `testler/test_a1_uretec.py`, `testler/test_a1_uretec_iskelet.py` |
| sistem.md §10, KODLAMA_PROMPTU §6 (kelime çantası kapısı; K-008, V-018) | `degerlendirme/kisa_yol.py` | `testler/test_a1_uretec.py` |
| KODLAMA_PROMPTU §5 (kilitli kümeler; V-021) | `degerlendirme/kilitli_kumeler.py` | `testler/test_a1_uretec.py` |
| sistem.md §10, §11 (üreteç mutasyonları) | `araclar/mutasyon_a1.py` | `testler/test_a1_uretec.py` |
