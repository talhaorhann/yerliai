# Taslak ilişki şeması (onay bekliyor, V-013)

Bu dosya `python3 araclar/sema_onayla.py` çıktısıdır. Asıl veri: `sema/iliskiler_v1.json`.

Okuma: (A, r, B) = B, A'nın r'sidir. Örnek: (A, baba, B) = B, A'nın babasıdır. TASLAK: kullanıcı onayı bekliyor (V-013). Dışlayıcı grup, akraba evliliği olmayan ağaç varsayımıyla tek gruptur.

| İlişki | Tersi (adaylar) | Simetrik | Tek mi (işlevsel) |
|---|---|---|---|
| anne | oğul, kız | hayır | evet |
| baba | oğul, kız | hayır | evet |
| oğul | anne, baba | hayır | hayır |
| kız | anne, baba | hayır | hayır |
| eş | eş | evet | evet |
| erkek_kardeş | erkek_kardeş, kız_kardeş | hayır | hayır |
| kız_kardeş | erkek_kardeş, kız_kardeş | hayır | hayır |
| dede | torun | hayır | hayır |
| babaanne | torun | hayır | evet |
| anneanne | torun | hayır | evet |
| torun | dede, babaanne, anneanne | hayır | hayır |
| amca | yeğen | hayır | hayır |
| dayı | yeğen | hayır | hayır |
| hala | yeğen | hayır | hayır |
| teyze | yeğen | hayır | hayır |
| yeğen | amca, dayı, hala, teyze | hayır | hayır |
| kuzen | kuzen | evet | hayır |
| kayınpeder | gelin, damat | hayır | evet |
| kayınvalide | gelin, damat | hayır | evet |
| gelin | kayınpeder, kayınvalide | hayır | hayır |
| damat | kayınpeder, kayınvalide | hayır | hayır |

Aynı iki kişi arasında bunlardan en fazla biri olabilir: anne, baba, oğul, kız, eş, erkek_kardeş, kız_kardeş, dede, babaanne, anneanne, torun, amca, dayı, hala, teyze, yeğen, kuzen, kayınpeder, kayınvalide, gelin, damat
