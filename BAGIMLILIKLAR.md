# BAĞIMLILIKLAR

Çekirdekte yalnız Python standart kütüphanesi + K-012 ile izinli numpy ve torch kullanılır. Başka her paket önce burada gerekçe, sürüm ve hash ile yazılır ve onay beklenir.

| Paket | Sürüm | Hash (sha256, PyPI) | Gerekçe | Kullanan | Durum |
|---|---|---|---|---|---|
| Python (yorumlayıcı) | ≥3.10 (geliştirme: 3.13) | - | standart kütüphane, `sys.stdlib_module_names` | tümü | V-003 ONAYSIZ |
| numpy | 2.5.3 | linux x86_64 cp313 `a5fa86b80fd24bcd1aff83ad23be44ea323de3f787be8f8b15d4a65621e25321`; win_amd64 cp313 `71cad2b2a7451ab79d8f5e71b453485b6775963d5cf794179144a7463fe6e8ec` | sistem.md (PyTorch/NumPy), K-012 | henüz kullanan yok | ONAYLI (K-012), bu ortamda kurulu |
| torch | 2.14.1 | win_amd64 cp313 (PyPI, CPU) `711713391d26a1ce5e9fbc6c996d954a8c12e8825374cc77b809a6af29539b8c`; linux x86_64 CPU tekerleği `download.pytorch.org/whl/cpu`'dan alınacak, hash DOĞRULANMADI | sistem.md (Python/PyTorch), A2 hızlı (toplu) yol, K-012 | A2 hızlı yol | ONAYLI (K-012), KURULMADI: bu ortamın ağ politikası `download.pytorch.org`'u engelliyor (403). PyPI'daki Linux tekerleği lisansı doğrulanmamış NVIDIA paketlerini zorunlu çektiği için kullanılmadı |

Sabit sürüm dosyası: `gereksinimler.txt` (hash'li).
