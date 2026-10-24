# Akrabalık DNA'sı: 9 grup

Dosya: `veri/dna/akrabalik_dna_v2_final.json`, 170 kural, sha256 `624b073c826650401cf85df00e92c8569c1ce25d0609625f1970946e804a7f4e`.
Kaynak: bağımsız danışman (LLM), beş bağımsız gözetmen denetledi (K-024). Gruplar sonuç ilişkisine göredir.
İşaretler: **[3]** 3 halkalı kural, **[≠]** "farklı kişi" şartı var.

| Grup | Kural sayısı | 3 halkalı | Farklı kişi şartlı |
|---|---|---|---|
| Eş | 6 | 0 | 4 |
| Anne ve baba | 21 | 0 | 0 |
| Oğul ve kız | 18 | 0 | 0 |
| Kardeşler | 28 | 0 | 14 |
| Dede, babaanne, anneanne ve torun | 39 | 8 | 0 |
| Amca, dayı, hala, teyze | 4 | 0 | 0 |
| Yeğen | 24 | 4 | 4 |
| Kuzen | 24 | 0 | 4 |
| Evlilikle akrabalar: kayınpeder, kayınvalide, gelin, damat | 6 | 0 | 0 |

## 1. Eş (6 kural)

- Y, X'in eşi ise X, Y'nin eşidir.
- X, Y'nin babası; Z, Y'nin annesi ise Z, X'in eşidir.
- X, Y'nin babası; Y, Z'nin oğlu ise Z, X'in eşidir (X ve Z farklı kişi). **[≠]**
- X, Y'nin babası; Y, Z'nin kızı ise Z, X'in eşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in oğlu; Y, Z'nin oğlu ise Z, X'in eşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in kızı; Y, Z'nin kızı ise Z, X'in eşidir (X ve Z farklı kişi). **[≠]**

## 2. Anne ve baba (21 kural)

- Y, X'in babası; Z, Y'nin eşi ise Z, X'in annesidir.
- Y, X'in annesi; Z, Y'nin eşi ise Z, X'in babasıdır.
- Y, X'in erkek kardeşi; Z, Y'nin babası ise Z, X'in babasıdır.
- Y, X'in erkek kardeşi; Z, Y'nin annesi ise Z, X'in annesidir.
- Y, X'in kız kardeşi; Z, Y'nin babası ise Z, X'in babasıdır.
- Y, X'in kız kardeşi; Z, Y'nin annesi ise Z, X'in annesidir.
- Y, X'in oğlu; X, P'nin oğlu ise X, Y'nin babasıdır.
- Y, X'in oğlu; X, P'nin babası ise X, Y'nin babasıdır.
- Y, X'in oğlu; X, P'nin erkek kardeşi ise X, Y'nin babasıdır.
- Y, X'in oğlu; X, P'nin kızı ise X, Y'nin annesidir.
- Y, X'in oğlu; X, P'nin annesi ise X, Y'nin annesidir.
- Y, X'in oğlu; X, P'nin kız kardeşi ise X, Y'nin annesidir.
- Y, X'in kızı; X, P'nin babası ise X, Y'nin babasıdır.
- Y, X'in kızı; X, P'nin erkek kardeşi ise X, Y'nin babasıdır.
- Y, X'in kızı; X, P'nin kızı ise X, Y'nin annesidir.
- Y, X'in kızı; X, P'nin annesi ise X, Y'nin annesidir.
- Y, X'in kızı; X, P'nin kız kardeşi ise X, Y'nin annesidir.
- Y, X'in babası; Z, X'in erkek kardeşi ise Y, Z'nin babasıdır.
- Y, X'in babası; Z, X'in kız kardeşi ise Y, Z'nin babasıdır.
- Y, X'in annesi; Z, X'in erkek kardeşi ise Y, Z'nin annesidir.
- Y, X'in annesi; Z, X'in kız kardeşi ise Y, Z'nin annesidir.

## 3. Oğul ve kız (18 kural)

- Y, X'in eşi; Z, Y'nin oğlu ise Z, X'in oğludur.
- Y, X'in eşi; Z, Y'nin kızı ise Z, X'in kızıdır.
- Y, X'in oğlu; Z, Y'nin erkek kardeşi ise Z, X'in oğludur.
- Y, X'in oğlu; Z, Y'nin kız kardeşi ise Z, X'in kızıdır.
- Y, X'in kızı; Z, Y'nin erkek kardeşi ise Z, X'in oğludur.
- Y, X'in kızı; Z, Y'nin kız kardeşi ise Z, X'in kızıdır.
- Y, X'in babası; X, P'nin oğlu ise X, Y'nin oğludur.
- Y, X'in babası; X, P'nin babası ise X, Y'nin oğludur.
- Y, X'in babası; X, P'nin erkek kardeşi ise X, Y'nin oğludur.
- Y, X'in babası; X, P'nin kızı ise X, Y'nin kızıdır.
- Y, X'in babası; X, P'nin annesi ise X, Y'nin kızıdır.
- Y, X'in babası; X, P'nin kız kardeşi ise X, Y'nin kızıdır.
- Y, X'in annesi; X, P'nin oğlu ise X, Y'nin oğludur.
- Y, X'in annesi; X, P'nin babası ise X, Y'nin oğludur.
- Y, X'in annesi; X, P'nin erkek kardeşi ise X, Y'nin oğludur.
- Y, X'in annesi; X, P'nin kızı ise X, Y'nin kızıdır.
- Y, X'in annesi; X, P'nin annesi ise X, Y'nin kızıdır.
- Y, X'in annesi; X, P'nin kız kardeşi ise X, Y'nin kızıdır.

## 4. Kardeşler (28 kural)

- Y, X'in babası; Z, Y'nin oğlu ise Z, X'in erkek kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in babası; Z, Y'nin kızı ise Z, X'in kız kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in annesi; Z, Y'nin oğlu ise Z, X'in erkek kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in annesi; Z, Y'nin kızı ise Z, X'in kız kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in erkek kardeşi; Z, Y'nin erkek kardeşi ise Z, X'in erkek kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in erkek kardeşi; Z, Y'nin kız kardeşi ise Z, X'in kız kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in kız kardeşi; Z, Y'nin erkek kardeşi ise Z, X'in erkek kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, X'in kız kardeşi; Z, Y'nin kız kardeşi ise Z, X'in kız kardeşidir (X ve Z farklı kişi). **[≠]**
- Y, P'nin oğlu; Z, P'nin oğlu ise Z, Y'nin erkek kardeşidir (Y ve Z farklı kişi). **[≠]**
- Y, P'nin oğlu; Z, P'nin kızı ise Z, Y'nin kız kardeşidir.
- Y, P'nin kızı; Z, P'nin oğlu ise Z, Y'nin erkek kardeşidir.
- Y, P'nin kızı; Z, P'nin kızı ise Z, Y'nin kız kardeşidir (Y ve Z farklı kişi). **[≠]**
- Y, X'in erkek kardeşi; X, P'nin oğlu ise X, Y'nin erkek kardeşidir.
- Y, X'in erkek kardeşi; X, P'nin babası ise X, Y'nin erkek kardeşidir.
- Y, X'in erkek kardeşi; X, P'nin erkek kardeşi ise X, Y'nin erkek kardeşidir.
- Y, X'in erkek kardeşi; X, P'nin kızı ise X, Y'nin kız kardeşidir.
- Y, X'in erkek kardeşi; X, P'nin annesi ise X, Y'nin kız kardeşidir.
- Y, X'in erkek kardeşi; X, P'nin kız kardeşi ise X, Y'nin kız kardeşidir.
- Y, X'in kız kardeşi; X, P'nin oğlu ise X, Y'nin erkek kardeşidir.
- Y, X'in kız kardeşi; X, P'nin babası ise X, Y'nin erkek kardeşidir.
- Y, X'in kız kardeşi; X, P'nin erkek kardeşi ise X, Y'nin erkek kardeşidir.
- Y, X'in kız kardeşi; X, P'nin kızı ise X, Y'nin kız kardeşidir.
- Y, X'in kız kardeşi; X, P'nin annesi ise X, Y'nin kız kardeşidir.
- Y, X'in kız kardeşi; X, P'nin kız kardeşi ise X, Y'nin kız kardeşidir.
- Y, X'in erkek kardeşi; Z, X'in erkek kardeşi ise Z, Y'nin erkek kardeşidir (Y ve Z farklı kişi). **[≠]**
- Y, X'in erkek kardeşi; Z, X'in kız kardeşi ise Z, Y'nin kız kardeşidir (Y ve Z farklı kişi). **[≠]**
- Y, X'in kız kardeşi; Z, X'in erkek kardeşi ise Z, Y'nin erkek kardeşidir (Y ve Z farklı kişi). **[≠]**
- Y, X'in kız kardeşi; Z, X'in kız kardeşi ise Z, Y'nin kız kardeşidir (Y ve Z farklı kişi). **[≠]**

## 5. Dede, babaanne, anneanne ve torun (39 kural)

- Y, X'in babası; Z, Y'nin babası ise Z, X'in dedesidir.
- Y, X'in annesi; Z, Y'nin babası ise Z, X'in dedesidir.
- Y, X'in babası; Z, Y'nin annesi ise Z, X'in babaannesidir.
- Y, X'in annesi; Z, Y'nin annesi ise Z, X'in anneannesidir.
- Z, X'in dedesi ise X, Z'nin torunudur.
- Z, X'in babaannesi ise X, Z'nin torunudur.
- Y, X'in oğlu; Z, Y'nin oğlu ise Z, X'in torunudur.
- Y, X'in oğlu; Z, Y'nin kızı ise Z, X'in torunudur.
- Y, X'in kızı; Z, Y'nin oğlu ise Z, X'in torunudur.
- Y, X'in kızı; Z, Y'nin kızı ise Z, X'in torunudur.
- Y, X'in amcası; Z, Y'nin babası ise Z, X'in dedesidir.
- Y, X'in amcası; Z, Y'nin annesi ise Z, X'in babaannesidir.
- Y, X'in halası; Z, Y'nin annesi ise Z, X'in babaannesidir.
- Y, X'in dayısı; Z, Y'nin babası ise Z, X'in dedesidir.
- Y, X'in dayısı; Z, Y'nin annesi ise Z, X'in anneannesidir.
- Y, X'in teyzesi; Z, Y'nin babası ise Z, X'in dedesidir.
- Y, X'in teyzesi; Z, Y'nin annesi ise Z, X'in anneannesidir.
- Y, X'in oğlu; Y, Z'nin babası ise Z, X'in torunudur.
- Y, X'in oğlu; Y, Z'nin annesi ise Z, X'in torunudur.
- Y, X'in kızı; Y, Z'nin babası ise Z, X'in torunudur.
- Y, X'in kızı; Y, Z'nin annesi ise Z, X'in torunudur.
- X, Y'nin oğlu; Z, Y'nin babası ise Z, X'in dedesidir.
- X, Y'nin kızı; Z, Y'nin babası ise Z, X'in dedesidir.
- X, Y'nin babası; Z, Y'nin oğlu ise Z, X'in torunudur.
- X, Y'nin babası; Z, Y'nin kızı ise Z, X'in torunudur.
- X, Y'nin annesi; Z, Y'nin oğlu ise Z, X'in torunudur.
- X, Y'nin annesi; Z, Y'nin kızı ise Z, X'in torunudur.
- X, Y'nin babası; Y, Z'nin babası ise Z, X'in torunudur.
- X, Y'nin babası; Y, Z'nin annesi ise Z, X'in torunudur.
- X, Y'nin annesi; Y, Z'nin babası ise Z, X'in torunudur.
- X, Y'nin annesi; Y, Z'nin annesi ise Z, X'in torunudur.
- Y, X'in oğlu; Y, Z'nin erkek kardeşi; W, Z'nin oğlu ise W, X'in torunudur. **[3]**
- Y, X'in oğlu; Y, Z'nin erkek kardeşi; W, Z'nin kızı ise W, X'in torunudur. **[3]**
- Y, X'in oğlu; Y, Z'nin kız kardeşi; W, Z'nin oğlu ise W, X'in torunudur. **[3]**
- Y, X'in oğlu; Y, Z'nin kız kardeşi; W, Z'nin kızı ise W, X'in torunudur. **[3]**
- Y, X'in kızı; Y, Z'nin erkek kardeşi; W, Z'nin oğlu ise W, X'in torunudur. **[3]**
- Y, X'in kızı; Y, Z'nin erkek kardeşi; W, Z'nin kızı ise W, X'in torunudur. **[3]**
- Y, X'in kızı; Y, Z'nin kız kardeşi; W, Z'nin oğlu ise W, X'in torunudur. **[3]**
- Y, X'in kızı; Y, Z'nin kız kardeşi; W, Z'nin kızı ise W, X'in torunudur. **[3]**

## 6. Amca, dayı, hala, teyze (4 kural)

- Y, X'in babası; Z, Y'nin erkek kardeşi ise Z, X'in amcasıdır.
- Y, X'in babası; Z, Y'nin kız kardeşi ise Z, X'in halasıdır.
- Y, X'in annesi; Z, Y'nin erkek kardeşi ise Z, X'in dayısıdır.
- Y, X'in annesi; Z, Y'nin kız kardeşi ise Z, X'in teyzesidir.

## 7. Yeğen (24 kural)

- Z, X'in amcası ise X, Z'nin yeğenidir.
- Z, X'in dayısı ise X, Z'nin yeğenidir.
- Z, X'in halası ise X, Z'nin yeğenidir.
- Z, X'in teyzesi ise X, Z'nin yeğenidir.
- Y, X'in erkek kardeşi; Z, Y'nin oğlu ise Z, X'in yeğenidir.
- Y, X'in erkek kardeşi; Z, Y'nin kızı ise Z, X'in yeğenidir.
- Y, X'in kız kardeşi; Z, Y'nin oğlu ise Z, X'in yeğenidir.
- Y, X'in kız kardeşi; Z, Y'nin kızı ise Z, X'in yeğenidir.
- Y, X'in erkek kardeşi; Y, Z'nin babası ise Z, X'in yeğenidir.
- Y, X'in erkek kardeşi; Y, Z'nin annesi ise Z, X'in yeğenidir.
- Y, X'in kız kardeşi; Y, Z'nin babası ise Z, X'in yeğenidir.
- Y, X'in kız kardeşi; Y, Z'nin annesi ise Z, X'in yeğenidir.
- Z, Y'nin erkek kardeşi; X, Y'nin oğlu ise X, Z'nin yeğenidir.
- Z, Y'nin erkek kardeşi; X, Y'nin kızı ise X, Z'nin yeğenidir.
- Z, Y'nin kız kardeşi; X, Y'nin oğlu ise X, Z'nin yeğenidir.
- Z, Y'nin kız kardeşi; X, Y'nin kızı ise X, Z'nin yeğenidir.
- X, Y'nin erkek kardeşi; Y, Z'nin babası ise Z, X'in yeğenidir.
- X, Y'nin erkek kardeşi; Y, Z'nin annesi ise Z, X'in yeğenidir.
- X, Y'nin kız kardeşi; Y, Z'nin babası ise Z, X'in yeğenidir.
- X, Y'nin kız kardeşi; Y, Z'nin annesi ise Z, X'in yeğenidir.
- P, X'in babası; P, Y'nin babası; W, Y'nin oğlu ise W, X'in yeğenidir (X ve Y farklı kişi). **[3]** **[≠]**
- P, X'in babası; P, Y'nin babası; W, Y'nin kızı ise W, X'in yeğenidir (X ve Y farklı kişi). **[3]** **[≠]**
- P, X'in annesi; P, Y'nin annesi; W, Y'nin oğlu ise W, X'in yeğenidir (X ve Y farklı kişi). **[3]** **[≠]**
- P, X'in annesi; P, Y'nin annesi; W, Y'nin kızı ise W, X'in yeğenidir (X ve Y farklı kişi). **[3]** **[≠]**

## 8. Kuzen (24 kural)

- Y, X'in amcası; Z, Y'nin oğlu ise Z, X'in kuzenidir.
- Y, X'in amcası; Z, Y'nin kızı ise Z, X'in kuzenidir.
- Y, X'in dayısı; Z, Y'nin oğlu ise Z, X'in kuzenidir.
- Y, X'in dayısı; Z, Y'nin kızı ise Z, X'in kuzenidir.
- Y, X'in halası; Z, Y'nin oğlu ise Z, X'in kuzenidir.
- Y, X'in halası; Z, Y'nin kızı ise Z, X'in kuzenidir.
- Y, X'in teyzesi; Z, Y'nin oğlu ise Z, X'in kuzenidir.
- Y, X'in kuzeni ise X, Y'nin kuzenidir.
- Y, X'in babası; Z, Y'nin yeğeni ise Z, X'in kuzenidir.
- Y, X'in annesi; Z, Y'nin yeğeni ise Z, X'in kuzenidir.
- Y, X'in amcası; Y, Z'nin babası ise Z, X'in kuzenidir.
- Y, X'in amcası; Y, Z'nin annesi ise Z, X'in kuzenidir.
- Y, X'in dayısı; Y, Z'nin babası ise Z, X'in kuzenidir.
- Y, X'in dayısı; Y, Z'nin annesi ise Z, X'in kuzenidir.
- Y, X'in halası; Y, Z'nin babası ise Z, X'in kuzenidir.
- Y, X'in halası; Y, Z'nin annesi ise Z, X'in kuzenidir.
- Y, X'in teyzesi; Y, Z'nin babası ise Z, X'in kuzenidir.
- Y, X'in teyzesi; Y, Z'nin annesi ise Z, X'in kuzenidir.
- X, Y'nin oğlu; Z, Y'nin yeğeni ise Z, X'in kuzenidir.
- X, Y'nin kızı; Z, Y'nin yeğeni ise Z, X'in kuzenidir.
- Y, X'in kuzeni; Y, Z'nin erkek kardeşi ise Z, X'in kuzenidir (X ve Z farklı kişi). **[≠]**
- Y, X'in kuzeni; Y, Z'nin kız kardeşi ise Z, X'in kuzenidir (X ve Z farklı kişi). **[≠]**
- Y, X'in kuzeni; X, Z'nin erkek kardeşi ise Y, Z'nin kuzenidir (Y ve Z farklı kişi). **[≠]**
- Y, X'in kuzeni; X, Z'nin kız kardeşi ise Y, Z'nin kuzenidir (Y ve Z farklı kişi). **[≠]**

## 9. Evlilikle akrabalar: kayınpeder, kayınvalide, gelin, damat (6 kural)

- Y, X'in eşi; Z, Y'nin babası ise Z, X'in kayınpederidir.
- Y, X'in eşi; Z, Y'nin annesi ise Z, X'in kayınvalidesidir.
- Y, X'in oğlu; Z, Y'nin eşi ise Z, X'in gelinidir.
- Y, X'in kızı; Z, Y'nin eşi ise Z, X'in damadıdır.
- Y, X'in kayınpederi; Z, Y'nin eşi ise Z, X'in kayınvalidesidir.
- Y, X'in kayınvalidesi; Z, Y'nin eşi ise Z, X'in kayınpederidir.
