# BAĞIMLILIKLAR

Çekirdekte yalnız Python standart kütüphanesi + K-012 ile izinli numpy ve torch kullanılır. Başka her paket önce burada gerekçe, sürüm ve hash ile yazılır ve onay beklenir.

| Paket | Sürüm | Hash (sha256, PyPI) | Gerekçe | Kullanan | Durum |
|---|---|---|---|---|---|
| Python (yorumlayıcı) | kurulum 3.13 (hash'li tekerlekler cp313); kod ≥3.10 | - | standart kütüphane, `sys.stdlib_module_names` | tümü | V-003, V-041 ONAYSIZ |
| numpy | 2.5.3 | linux x86_64 cp313 `a5fa86b80fd24bcd1aff83ad23be44ea323de3f787be8f8b15d4a65621e25321`; win_amd64 cp313 `71cad2b2a7451ab79d8f5e71b453485b6775963d5cf794179144a7463fe6e8ec` | sistem.md (PyTorch/NumPy), K-012 | henüz kullanan yok | ONAYLI (K-012), bu ortamda kurulu |
| torch | 2.14.1+cpu | linux x86_64 cp313 `331fa474e26e428e2e6af1143b2fdab19cee492d7d21897b8899ce1c14755662`; win_amd64 cp313 `4eec5a4fadd7a18f9c75b97fdb374fbb579ce4b1604bf66eeb14dc2201d54def` (ikisi de `download.pytorch.org/whl/cpu` dizin sayfasındaki sha256) | sistem.md (Python/PyTorch), hızlı (toplu) yol, K-012, K-022 | `cekirdek/vektor_hizli.py` | ONAYLI (K-022) |
| filelock | 4.2.4 | `301241438c57936ef93f4243a94f2559022268bfcf9b375a9a72eb0f8db8358e` | torch bağımlılığı | torch | ONAYLI (K-022) |
| typing_extensions | 4.16.0 | `481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8` | torch bağımlılığı | torch | ONAYLI (K-022) |
| setuptools | 84.2.1 | `ca140b45d5325a9478f880e351484f62fef15f336462e449ca0c03c873d589c2` | torch bağımlılığı (≥77.0.3) | torch | ONAYLI (K-022) |
| sympy | 1.14.0 | `e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5` | torch bağımlılığı | torch | ONAYLI (K-022) |
| mpmath | 1.3.0 | `a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c` | sympy bağımlılığı | sympy | ONAYLI (K-022) |
| networkx | 3.7 | `e3fd2c13a7814cee3746340d8d7f8598a67f16a58bf47fb7f8793fab6efca1b0` | torch bağımlılığı | torch | ONAYLI (K-022) |
| jinja2 | 3.1.6 | `85ece4451f492d0c13c5dd7c13a64681a86afae63a5f347908daf103ce6d2f67` | torch bağımlılığı | torch | ONAYLI (K-022) |
| MarkupSafe | 3.0.4 | linux x86_64 cp313 `434139499bb20b502ed3baa1f169e618f924a97e7a777fea1a49446d80106cf6` | jinja2 bağımlılığı | jinja2 | ONAYLI (K-022) |
| fsspec | 2026.9.0 | `8dd6e646e99ea382bd85f97a45e6b526a442d79423a7dc673f1e2756d05fcb5f` | torch bağımlılığı | torch | ONAYLI (K-022) |

Sabit sürüm dosyası: `gereksinimler.txt` (hash'li).
