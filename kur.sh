#!/bin/sh
# KODLAMA_PROMPTU §8: tek kurulum betiği. Python 3.13 denetlenir, `.venv` kurulur, paketler hash denetimiyle
# yüklenir (K-022, V-041), sonra tüm testler `.venv` içindeki yorumlayıcıyla koşar.
set -e
cd "$(dirname "$0")"
python3 -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 13) else "Python 3.13 gerekli (V-041)")'
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r gereksinimler.txt
.venv/bin/python araclar/kostur.py
