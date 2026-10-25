# DNA v8: 170 kurallı sürümle kimlik karşılaştırması (2026-10-25)

Dosya: `veri/dna/akrabalik_dna_v8.json` (danışmanın gönderdiği, 2026-10-24). **Kilitli değil:** danışman "son sürüm" demeden kilitlenmez (K-033).

| | Dosya | Kural | sha256 |
|---|---|---|---|
| Önceki (H1 kapı koşularında kullanılan) | `veri/dna/akrabalik_dna_v2_final.json` | 170 | `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e` |
| Yeni | `veri/dna/akrabalik_dna_v8.json` | 244 | `4a4af6b83c58e33d9971f9d84ed6c440fbb2341d14ec70dc4710128d74bfaa75` |

**Not:** Mesajda "176 kurallı sürüm (v7)" yazıyordu; gelen ek v8 ve 244 kurallı.

## Sonuç

- 170 eski kuralın 170'i v8'de var, içerikleri bayt bayt aynı, sıraları aynı. Silinen kural yok.
- 74 yeni kural eklenmiş, yinelenen kimlik yok. Biçim: DNA sürüm 2.
- ÖK-003'te açıklanamayan 6 hatanın nedeni olan 6 kural (danışman: DNA'dan silinmişti) yenilerin ilk altısı: `anne_ogul_es`, `anne_kiz_es`, `anneanne_torun`, `hala_baba_dede`, `teyze_kiz_kuzen`, `kiz_ogul_baba`.
- Öteki 68 yeni kural cinsiyeti bir olgudan ötekine taşıyan 3 halkalı kurallar (ör. `baba_es_ogul_kiz`, `erkek_kardes_baba_ogul_torun`, `kiz_kardes_kiz_kardes_kiz_yegen`).

## Yeni kimlikler (74, dosyadaki sırayla)

anne_ogul_es, anne_kiz_es, anneanne_torun, hala_baba_dede, teyze_kiz_kuzen, kiz_ogul_baba, baba_es_ogul_kiz, baba_es_baba_kiz, baba_es_erkek_kardes_kiz, baba_es_kiz_ogul, baba_es_anne_ogul, baba_es_kiz_kardes_ogul, anne_es_ogul_kiz, anne_es_baba_kiz, anne_es_erkek_kardes_kiz, anne_es_kiz_ogul, anne_es_anne_ogul, anne_es_kiz_kardes_ogul, ogul_es_ogul_anne, ogul_es_baba_anne, ogul_es_erkek_kardes_anne, ogul_es_kiz_baba, ogul_es_anne_baba, ogul_es_kiz_kardes_baba, kiz_es_ogul_anne, kiz_es_baba_anne, kiz_es_erkek_kardes_anne, kiz_es_kiz_baba, kiz_es_anne_baba, kiz_es_kiz_kardes_baba, baba_es_ogul_damat, baba_es_baba_damat, baba_es_erkek_kardes_damat, baba_es_kiz_gelin, baba_es_anne_gelin, baba_es_kiz_kardes_gelin, anne_es_ogul_damat, anne_es_baba_damat, anne_es_erkek_kardes_damat, anne_es_kiz_gelin, anne_es_anne_gelin, anne_es_kiz_kardes_gelin, erkek_kardes_es_ogul_kiz_kardes, erkek_kardes_es_baba_kiz_kardes, erkek_kardes_es_erkek_kardes_kiz_kardes, erkek_kardes_es_kiz_erkek_kardes, erkek_kardes_es_anne_erkek_kardes, erkek_kardes_es_kiz_kardes_erkek_kardes, kiz_kardes_es_ogul_kiz_kardes, kiz_kardes_es_baba_kiz_kardes, kiz_kardes_es_erkek_kardes_kiz_kardes, kiz_kardes_es_kiz_erkek_kardes, kiz_kardes_es_anne_erkek_kardes, kiz_kardes_es_kiz_kardes_erkek_kardes, erkek_kardes_baba_ogul_torun, erkek_kardes_anne_ogul_torun, erkek_kardes_baba_kiz_torun, erkek_kardes_anne_kiz_torun, kiz_kardes_baba_ogul_torun, kiz_kardes_anne_ogul_torun, kiz_kardes_baba_kiz_torun, kiz_kardes_anne_kiz_torun, erkek_kardes_baba_ogul_dede, erkek_kardes_baba_kiz_dede, kiz_kardes_baba_ogul_dede, kiz_kardes_baba_kiz_dede, erkek_kardes_erkek_kardes_ogul_yegen, erkek_kardes_kiz_kardes_ogul_yegen, erkek_kardes_erkek_kardes_kiz_yegen, erkek_kardes_kiz_kardes_kiz_yegen, kiz_kardes_erkek_kardes_ogul_yegen, kiz_kardes_kiz_kardes_ogul_yegen, kiz_kardes_erkek_kardes_kiz_yegen, kiz_kardes_kiz_kardes_kiz_yegen
