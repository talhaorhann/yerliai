# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`.

- **Ne çalışıyor:** A0 altyapısı (ayrıntı `ILERLEME.md`). `python3 araclar/kostur.py` → 57/57 geçti, 0 atlanan, 0 xfail.
- **Açık varsayımlar:** V-001…V-010, hepsi ONAYSIZ. Felsefi olanlar: V-005 (izinli paketler, A2 öncesi sorulacak), V-006 (zaman damgası ile determinizm, A1 öncesi sorulacak).
- **Sıradaki tek adım:** V-006'nın kullanıcı cevabını al. Sonra `asama-1` dalında A1'i (bilgi tabanı + sentetik soy ağacı üreteci) başlat. A1'in ilk kabul ölçütü: kelime çantası kısa yol dedektörü (prompt §6).
- **Kural hatırlatma:** `testler/` ve `config.json` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
