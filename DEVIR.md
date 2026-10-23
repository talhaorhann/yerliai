# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` ilgili bölüm, `ILERLEME.md`, `VARSAYIMLAR.md`, `KARARLAR.md`.

- **Ne çalışıyor:** A0 altyapısı (ayrıntı `ILERLEME.md`). `python3 araclar/kostur.py` → 57/57 geçti, 0 atlanan, 0 xfail.
- **Açık varsayımlar:** V-001…V-005, V-007…V-010 ONAYSIZ. Felsefi olan: V-005 (izinli paketler; kullanıcı: A2'ye kadar kısıtlı kalsın). V-006 onaylandı → K-004 (çekirdekte saat yerine adım numarası).
- **Sıradaki tek adım:** A0 bağımsız incelemesi (`inceleme/A0_istemi.md`). Kullanıcı: inceleme bitmeden A1'e başlanmaz. İnceleme sonucu gelince bulgular ele alınır, sonra `asama-1` dalında A1 (bilgi tabanı + sentetik soy ağacı üreteci) başlar. A1'in ilk kabul ölçütü: kelime çantası kısa yol dedektörü (prompt §6).
- **Kural hatırlatma:** `testler/` ve `config.json` hash kilitli. Değişiklik kullanıcı onayı ister, sonra `python3 araclar/kilitle.py` çalıştırılır.
