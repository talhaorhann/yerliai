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
