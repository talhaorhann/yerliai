# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`.

- **Ne çalışıyor:** A0 tamam (etiket `asama-0`). A1'de kelime çantası kapısı geçti, dal `asama-1`. `python3 araclar/kostur.py` → 134/134, 0 atlanan, 0 xfail.
- **Açık varsayımlar:** V-001…V-005, V-007…V-012, V-014, V-017…V-021 ONAYSIZ. Felsefi olup bekleyenler: V-019 (gizli tanımlar, `degerlendirme/veri/TANIMLAR_OKUNUR.md`), V-020 (önsel-ters tanımı), altın küme (V-021). V-005: A2'ye kadar kısıtlı.
- **A0 bağımsız incelemesi:** ertelendi (K-005), istem `inceleme/A0_istemi.md`.
- **Sıradaki tek adım:** kullanıcının V-019/V-020/altın küme cevabını al. Önsel-ters onaylanırsa test önce yazılır. Sonra `asama-1` etiketi, ardından A2 öncesi V-005 (numpy/torch) sorusu.
- **Kural hatırlatma:** `testler/` ve `config.json` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
