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
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A1) | `araclar/mutasyon_a1.py` | `testler/test_a0_yasak_kaliplar.py` |
| sistem.md §11 (soy ağacı, gizli tanımlar; K-007, V-019) | `degerlendirme/dunya.py`, `degerlendirme/veri/tanimlar_v1.json`, `degerlendirme/veri/tanimlar_v1.schema.json` | `testler/test_a1_uretec.py` |
| sistem.md §10, §11 (bölmeler, bölüm biçimi; V-017) | `degerlendirme/uretec.py`, `sema/bolum_v1.schema.json`, `sema/cevap_v1.schema.json` | `testler/test_a1_uretec.py`, `testler/test_a1_uretec_iskelet.py` |
| sistem.md §10, KODLAMA_PROMPTU §6 (kelime çantası kapısı; K-008, V-018) | `degerlendirme/kisa_yol.py` | `testler/test_a1_uretec.py` |
| KODLAMA_PROMPTU §5 (kilitli kümeler; V-021) | `degerlendirme/kilitli_kumeler.py` | `testler/test_a1_uretec.py` |
| sistem.md §10, §11 (üreteç mutasyonları) | `araclar/mutasyon_a1.py` | `testler/test_a1_uretec.py` |
| sistem.md §17, K-011 (altın küme; V-023) | `degerlendirme/altin.py`, `degerlendirme/altin/altin_bolumler.jsonl`, `kilit/kilitli_kumeler.json` | `testler/test_a1_altin.py` |
| sistem.md §10, K-010 (önsel-ters; V-022) | `degerlendirme/uretec.py` | `testler/test_a1_uretec_iskelet.py` |
| sistem.md §1, §3 (HRR/VSA vektörleri; K-014, V-026) | `cekirdek/vektor.py` | `testler/test_a2_vektor.py` |
| KODLAMA_PROMPTU §5 (tensör şekilleri, SEKILLER) | `cekirdek/sekiller.py` | `testler/test_a2_vektor.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A2) | `araclar/mutasyon_a2.py` | `testler/test_a2_vektor.py` |
| sistem.md §3 (DNA; V-032) | `cekirdek/dna.py`, `sema/dna_v1.schema.json` | `testler/test_a3_temel.py` |
| sistem.md §2 (havuz; V-031 atma onayda) | `cekirdek/havuz.py` | `testler/test_a3_temel.py` |
| sistem.md §3 (sembolik yarı-naif eşleşme; V-032) | `cekirdek/eslesme.py` | `testler/test_a3_temel.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A3) | `araclar/mutasyon_a3.py` | `testler/test_a3_temel.py` |
| sistem.md §3 (afinite, θ, güven; K-016) | `cekirdek/eslesme.py` | `testler/test_a3_cekirdek.py` |
| sistem.md §3, §5 (döngü, durma, impasse; K-016, K-017, V-034) | `cekirdek/dongu.py` | `testler/test_a3_cekirdek.py` |
| sistem.md §6 (plazma, noisy-OR, gerekçe; K-018) | `cekirdek/plazma.py` | `testler/test_a3_cekirdek.py` |
| sistem.md §2 (havuzdan atma, mezar taşı; K-019, V-033) | `cekirdek/havuz.py` | `testler/test_a3_cekirdek.py` |
| KODLAMA_PROMPTU §5 (Defter), sistem.md §18 (V-035) | `cekirdek/defter.py`, `cekirdek/altyapi/olay_gunlugu.py`, `cekirdek/dongu.py`, `cekirdek/plazma.py` | `testler/test_a4_defter.py` |
| KODLAMA_PROMPTU §5 (çelişki defteri; K-020, V-038) | `cekirdek/defter.py` | `testler/test_a4_mudahale.py` |
| sistem.md §9 (müdahale testi; K-021, V-038) | `cekirdek/mudahale.py` | `testler/test_a4_mudahale.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A4) | `araclar/mutasyon_a4.py` | `testler/test_a4_mudahale.py` |
| sistem.md §3 (vektörleştirilmiş matmul; K-015, K-022, V-040) | `cekirdek/vektor_hizli.py`, `araclar/hiz_olc.py` | `testler/test_a5_hizli_yol.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A5) | `araclar/mutasyon_a5.py` | `testler/test_a5_hizli_yol.py` |
| sistem.md §3 (hızlı yol çekirdek döngüsünde; V-042) | `cekirdek/eslesme.py`, `cekirdek/dongu.py`, `cekirdek/havuz.py`, `cekirdek/vektor.py`, `cekirdek/vektor_hizli.py`, `testler/yardimci_senaryo.py` | `testler/test_a5_dongu_hizli.py` |
| sistem.md §3 (DNA sürüm 2, farklı kişi şartı; K-025, V-043) | `cekirdek/dna.py`, `cekirdek/eslesme.py`, `sema/dna_v2.schema.json` | `testler/test_a5_dna_v2.py` |
| sistem.md §13 (H1 DNA'sı: bağımsız danışmana ilişki listesi, gizli tanım yok; K-024) | `DANISMAN_ICIN_ILISKI_LISTESI.md` | `testler/test_a5_danisman.py` |
| sistem.md §13 (H1 koşturucusu; K-023, V-044) | `degerlendirme/h1.py`, `degerlendirme/istatistik.py` | `testler/test_a5_h1.py`, `testler/test_a5_istatistik.py` |
| sistem.md §3, §5, §6 (kopya kuralı C: yeni dayanak; K-028, V-046) | `cekirdek/dongu.py` | `testler/test_a5_kopya_c.py` |
| sistem.md §13 (H1 hata incelemesi; ÖK-002 §6, V-047) | `degerlendirme/h1_inceleme.py` | `testler/test_a5_h1_inceleme.py` |
| sistem.md §10, §11 (çıkarılabilirlik denetimi; K-029, V-048) | `degerlendirme/dunya.py`, `degerlendirme/uretec.py` | `testler/test_a5_cikarilabilirlik.py` |
| sistem.md §13 (H1 sınır seçimi; ÖK-003 §3.4, V-049) | `degerlendirme/h1_sinir.py` | `testler/test_a5_h1_sinir.py` |
| sistem.md §13 (H1 tohum değişimi; K-030) | `degerlendirme/h1.py` | `testler/test_a5_tohum_degisimi.py` |
| sistem.md §3 (C hücre sınırından önce; K-031, V-051) | `cekirdek/dongu.py` | `testler/test_a5_sinir_c.py` |
| sistem.md §13 (H2 kapısı: V-053 kapanmadan H2 yok; K-032 §4) | `degerlendirme/h2.py` | `testler/test_a6_h2_kapisi.py` |
| KODLAMA_PROMPTU §6 (Mutasyon sınaması, A6) | `araclar/mutasyon_a6.py` | `testler/test_a6_h2_kapisi.py` |
| sistem.md §10, §11 (olgulardan çıkarılabilirlik; K-032 §3, V-053) | `degerlendirme/dunya.py` | `testler/test_a6_olgudan_cikarilabilirlik.py` |
| sistem.md §8, §18, EK A P7 (bellek geçidi, çekirdek tarafı: maskeli koşu, eşikler; V-054, K-035) | `cekirdek/bellek_gecidi.py` | `testler/test_a6_bellek_gecidi.py` |
| sistem.md §8, §18 (bellek geçidinin doğruluk hesabı, çekirdek dışı ve kâhinsiz; K-035, V-057) | `degerlendirme/gozlem_puani.py` | `testler/test_a6_bellek_gecidi.py`, `testler/test_a6_bellek_hatti.py` |
| sistem.md §8, §15, §16, EK A P7 (bellek hattı, anlatıcı yeri, bağımsızlık testi; K-035, V-056) | `degerlendirme/bellek_hatti.py` | `testler/test_a6_bellek_hatti.py`, `testler/test_a6_bellek.py` |
| sistem.md §10, §11 (gözlem bölümleri; K-035, V-057) | `degerlendirme/uretec.py` | `testler/test_a6_gozlem_bolumu.py` |
| sistem.md §8, §18 (A6 gösterimi: gerçek DNA, gözlemli veri; K-035, V-057, V-058) | `degerlendirme/a6_gosterim.py` | `testler/test_a6_gosterim.py` |
| sistem.md §2, §3, §5 (havuz ve eşleşme bütçesi baskısı ölçümü; ÖK-004 §4) | `degerlendirme/h1_baski.py` | `testler/test_a6_h1_baski.py` |
| sistem.md §17 (altın küme parça soru dosyası, JSON cevap biçimi; K-039, ÖK-001) | `degerlendirme/altin.py` | `testler/test_a6_altin_soru.py` |
| sistem.md §8, §15 (bellek deposu: salt ekleme, sürüm kilidi, geri alma; V-056) | `cekirdek/bellek.py` | `testler/test_a6_bellek.py` |
| sistem.md §17, §15, §18 (iç dil sürüm 1; V-055) | `cekirdek/ic_dil.py`, `sema/ic_dil_v1.schema.json` | `testler/test_a6_ic_dil.py` |
| sistem.md §13 (H2 tek aday şeması, kanonik kimlik, kırmızı takım dosyası denetimi; K-041, V-060) | `kesif/aday.py`, `sema/aday_v1.schema.json`, `sema/kirmizi_dosyasi_v1.schema.json`, `veri/h2/kirmizi_ornek_v1.json` | `testler/test_b0_aday.py` |
| sistem.md §13 (H2 tohum türetme; K-041, ÖK-005 taslağı §5) | `kesif/tohum.py` | `testler/test_b0_sablon.py` |
| sistem.md §3, §13 (tipli şablon ailesi T ve kademeleri K1–K5; K-041, ÖK-005 taslağı §6) | `kesif/sablon.py` | `testler/test_b0_sablon.py` |
| sistem.md §3, §13 (sembolik sayaç: tanık, kapalı dünya, OI; referans + hızlı; K-041, V-061) | `kesif/sayac.py`, `cekirdek/sekiller.py` | `testler/test_b0_sayac.py` |
| sistem.md §13 (M0: şablon uzayının kaba kuvvet sayımı, süzgeç, sıra, bit-aynı çıktı; K-041, V-061) | `kesif/m0.py` | `testler/test_b0_m0.py` |
