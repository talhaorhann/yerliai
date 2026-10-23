@echo off
rem KODLAMA_PROMPTU §8: tek kurulum betigi. A0da dis paket yok, yalniz Python 3.10+ denetlenir ve testler kosar (V-003).
cd /d "%~dp0"
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else \"Python 3.10 ya da ustu gerekli\")" || exit /b 1
python araclar\kostur.py
exit /b %ERRORLEVEL%
