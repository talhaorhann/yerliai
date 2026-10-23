# LİSANSLAR

Her paket, model ve veri kümesi için sürüm, lisans (resmî LICENSE dosyasından doğrulanmış) ve checksum burada tutulur. Lisansı doğrulanmamış hiçbir şey kullanılmaz. Hatırdan lisans yazılmaz.

| Öğe | Sürüm | Lisans | Doğrulama kaynağı (2026-10-23) | Checksum | Durum |
|---|---|---|---|---|---|
| numpy | 2.5.3 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | Kurulu dağıtımın `numpy-2.5.3.dist-info/METADATA` `License-Expression` alanı + `licenses/LICENSE.txt` ("Copyright (c) 2005-2025, NumPy Developers", BSD 3 maddeli metin); PyPI `pypi.org/pypi/numpy/2.5.3/json` aynı ifade | LICENSE.txt sha256 `4860083caa0de2ac3292ca98bd074bd8f45d8b32624e37b1e70a240bff61e488`; tekerlekler `BAGIMLILIKLAR.md`'de | DOĞRULANDI |
| torch (PyTorch) | 2.14.1+cpu | Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT | Resmî depo `github.com/pytorch/pytorch` etiket `v2.14.1` `LICENSE` dosyası (84 satır, "From PyTorch: Copyright (c) 2016- Facebook, Inc ...", 59. satır "Redistribution and use in source and binary forms"); PyPI `pypi.org/pypi/torch/2.14.1/json` `license_expression` | LICENSE sha256 `bd018feef8825e88181c84eb7e3aa4eafb8f08a20d9fd6ef948569610c4a3e43` | DOĞRULANDI (lisans). CPU tekerleği: K-022 |
| NVIDIA CUDA pip paketleri (cuda-toolkit, nvidia-cudnn-cu13, nvidia-nccl-cu13, ...) | - | Doğrulanmadı | PyPI Linux torch tekerleği bunları zorunlu bağımlılık olarak çeker | - | KULLANILMIYOR: CPU tekerleği kullanılıyor (K-022) |
| filelock | 4.2.4 | MIT | Tekerlek METADATA `License-Expression: MIT` + `licenses/LICENSE` | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| typing_extensions | 4.16.0 | PSF-2.0 | Tekerlek METADATA `License-Expression: PSF-2.0` + `licenses/LICENSE` | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| setuptools | 84.2.1 | MIT | Tekerlek METADATA `License-Expression: MIT` | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| sympy | 1.14.0 | BSD-3-Clause (içinde paketlenmiş kod için ek BSD bölümleri) | Tekerlek `licenses/LICENSE` ("Copyright (c) 2006-2023 SymPy Development Team", "Neither the name" maddeli) + Classifier "BSD License" | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| mpmath | 1.3.0 | BSD-3-Clause | Tekerlek `LICENSE` ("Copyright (c) 2005-2021 Fredrik Johansson and mpmath contributors", 3 madde) | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| networkx | 3.7 | BSD-3-Clause | Tekerlek METADATA `License-Expression: BSD-3-Clause` + `licenses/LICENSE.txt` | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| jinja2 | 3.1.6 | BSD-3-Clause | Tekerlek `licenses/LICENSE.txt` ("Copyright 2007 Pallets", 3 madde) + Classifier "BSD License" | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| MarkupSafe | 3.0.4 | BSD-3-Clause | Tekerlek METADATA `License-Expression: BSD-3-Clause` + `licenses/LICENSE.txt` | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |
| fsspec | 2026.9.0 | BSD-3-Clause | Tekerlek METADATA `License-Expression: BSD-3-Clause` + `licenses/LICENSE` | tekerlek `BAGIMLILIKLAR.md` | DOĞRULANDI |

Python standart kütüphanesi yorumlayıcıyla gelir. torch'un CPU bağımlılıkları yukarıdadır (torch 2.14.1 `requires_dist`: filelock, typing-extensions, setuptools, sympy, networkx, jinja2, fsspec; dolaylı: mpmath, MarkupSafe). Çekirdek bunları doğrudan import etmez.
