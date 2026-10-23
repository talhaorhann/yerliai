@echo off
rem KODLAMA_PROMPTU §8: tek kurulum betigi. Python 3.13 denetlenir, .venv kurulur, paketler hash denetimiyle
rem yuklenir (K-022, V-041), sonra tum testler .venv icindeki yorumlayiciyla kosar. Windowsta DOGRULANMADI.
cd /d "%~dp0"
python -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 13) else \"Python 3.13 gerekli (V-041)\")" || exit /b 1
if not exist .venv\Scripts\python.exe (
    python -m venv .venv || exit /b 1
)
.venv\Scripts\python -m pip install --require-hashes --only-binary=:all: -r gereksinimler.txt || exit /b 1
.venv\Scripts\python araclar\kostur.py
exit /b %ERRORLEVEL%
