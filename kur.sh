#!/bin/sh
# KODLAMA_PROMPTU §8: tek kurulum betiği. A0'da dış paket yok, yalnız Python ≥3.10 denetlenir ve testler koşar (V-003).
set -e
cd "$(dirname "$0")"
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else "Python 3.10 ya da üstü gerekli")'
python3 araclar/kostur.py
