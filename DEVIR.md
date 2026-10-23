# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`.

- **Ne çalışıyor:** A0 tamam (etiket `asama-0`). A1 yarım, dal `asama-1`. `python3 araclar/kostur.py` → 104/104 geçti, 0 atlanan, 0 xfail.
- **Açık varsayımlar:** V-001…V-005 ve V-007…V-016 ONAYSIZ. Felsefi olup bekleyenler: V-013 (taslak şema `sema/TASLAK_ONAY.md`), V-015 (üreteç tasarımı), V-016 (kelime çantası kuralı). V-005: A2'ye kadar kısıtlı.
- **A0 bağımsız incelemesi:** kullanıcı kararıyla ertelendi (K-005). İstem: `inceleme/A0_istemi.md`.
- **Sıradaki tek adım:** kullanıcının V-013/V-015/V-016 cevabını al. Şema onaylanırsa K-kararı yaz ve `python3 araclar/sema_onayla.py K-nnn` çalıştır. Üreteç onaylanırsa önce kabul testlerini yaz: kelime çantası dedektörü ilk ölçüt.
- **Kural hatırlatma:** `testler/` ve `config.json` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
