# DEVİR (sonraki oturum için)

Oturum başında oku: `sistem.md` §2–§6, `ILERLEME.md`, `VARSAYIMLAR.md` (V-027..V-032), `KARARLAR.md`, `ONKAYIT.md`.

- **Ne çalışıyor:** A0–A2 kapandı. A3 yarım, dal `asama-3`: DNA, havuz, sembolik eşleşme. `python3 araclar/kostur.py` → 184/184.
- **Bekleyen kullanıcı onayı (3 madde):**
  1. V-028: afinite, θ, güven, bütçe.
  2. V-029 + V-030: durma ve plazma.
  3. V-031: havuzdan atma ve yayın sahnesi.
- **Sıradaki tek adım:** onay gelince önce kabul testleri (kırmızı), sonra:
  - afinite süzgeci ve güven (`cekirdek/eslesme.py`'ye),
  - havuz atma (`Havuz._at`),
  - döngü ve durma (`cekirdek/dongu.py`),
  - plazma (`cekirdek/plazma.py`).
  A3 kabulü: blorp DNA'lı oyuncak dünyalarda doğru çıkarım, "bilmiyorum", noisy-OR'un elle hesaba eşitliği ve çift sayımda güvenin değişmemesi.
- **Kural hatırlatma:** `testler/`, `config.json` ve `kilitli_veri_dosyalari` hash kilitli.
