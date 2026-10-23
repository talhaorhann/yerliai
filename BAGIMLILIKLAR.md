# BAĞIMLILIKLAR

Çekirdekte yalnız Python standart kütüphanesi (+ onaylanırsa şartnamenin gerektirdiği PyTorch/NumPy) kullanılır. Başka her paket önce burada gerekçe, sürüm ve hash ile yazılır ve onay beklenir.

| Paket | Sürüm | Hash | Gerekçe | Kullanan | Durum |
|---|---|---|---|---|---|
| Python (yorumlayıcı) | ≥3.10 (geliştirme: 3.13) | - | standart kütüphane, `sys.stdlib_module_names` | tümü | V-003 ONAYSIZ |

A0'da dış paket YOK. numpy/torch kararı A2 öncesi sorulacak (V-005).
