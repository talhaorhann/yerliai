# LİSANSLAR

Her paket, model ve veri kümesi için sürüm, lisans (resmî LICENSE dosyasından doğrulanmış) ve checksum burada tutulur. Lisansı doğrulanmamış hiçbir şey kullanılmaz. Hatırdan lisans yazılmaz.

| Öğe | Sürüm | Lisans | Doğrulama kaynağı (2026-10-23) | Checksum | Durum |
|---|---|---|---|---|---|
| numpy | 2.5.3 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | Kurulu dağıtımın `numpy-2.5.3.dist-info/METADATA` `License-Expression` alanı + `licenses/LICENSE.txt` ("Copyright (c) 2005-2025, NumPy Developers", BSD 3 maddeli metin); PyPI `pypi.org/pypi/numpy/2.5.3/json` aynı ifade | LICENSE.txt sha256 `4860083caa0de2ac3292ca98bd074bd8f45d8b32624e37b1e70a240bff61e488`; tekerlekler `BAGIMLILIKLAR.md`'de | DOĞRULANDI |
| torch (PyTorch) | 2.14.1 | Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT | Resmî depo `github.com/pytorch/pytorch` etiket `v2.14.1` `LICENSE` dosyası (84 satır, "From PyTorch: Copyright (c) 2016- Facebook, Inc ...", 59. satır "Redistribution and use in source and binary forms"); PyPI `pypi.org/pypi/torch/2.14.1/json` `license_expression` | LICENSE sha256 `bd018feef8825e88181c84eb7e3aa4eafb8f08a20d9fd6ef948569610c4a3e43` | DOĞRULANDI (lisans); KURULMADI (bkz. BAGIMLILIKLAR) |
| NVIDIA CUDA pip paketleri (cuda-toolkit, nvidia-cudnn-cu13, nvidia-nccl-cu13, ...) | - | Doğrulanmadı | PyPI Linux torch tekerleği bunları zorunlu bağımlılık olarak çeker | - | KULLANILMIYOR: lisans doğrulanmadı. CPU tekerleği tercih edildi (K-012) |

Python standart kütüphanesi yorumlayıcıyla gelir. torch'un CPU bağımlılıkları (filelock, typing-extensions, setuptools, sympy, networkx, jinja2, fsspec ve onların bağımlılıkları) torch kurulduğunda tek tek buraya eklenecek.
