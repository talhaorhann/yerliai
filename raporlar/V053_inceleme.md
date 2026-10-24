# V-053: olgulardan çıkarılabilirlik, önerilen tanım ve sınama (2026-10-24)

Onay bekliyor (K-032 §3). Üretece henüz bağlanmadı.

## Tanım

- **Girdi:** yalnız olgular, soru ve beklenen cevap. Gerçek aile ağacı fonksiyona hiç verilmez (`degerlendirme/dunya.py` `olgudan_cikarilabilir_mi`).
- **Dünya varsayımları (yalnız bunlar):**
  1. Her kişinin ya hiç ebeveyni yoktur ya da birbiriyle evli iki ebeveyni vardır.
  2. Kimse birden fazla kişiyle evli değildir.
  3. Evli çiftler karşı cinstendir.
- **Zorunlu yapı:** Bu varsayımlardan şunlar çıkar:
  - bir çocuğun iki ebeveyni evlidir;
  - bir kişinin bütün çocukları aynı çiftindir;
  - kardeşlerin iki ebeveyni de ortaktır;
  - adı geçen ebeveynin eşi, o çocukların öteki ebeveynidir. Kardeşler üzerinden çıkan evlilikler de buna dahildir.
  - Adı geçmeyen ebeveyn adsız bir düğümdür.
- **Kullanılmayan bilgi:** Üretecin başka özellikleri (dışarıdan evlenenin ebeveyni olmaması, nesil sayısı, akraba evliliği yokluğu) ve olgularda olmayan hiçbir bilgi kullanılmaz.
- **Karar:** Zorunlu yapıda, cinsiyetlerin olgulara uyan bütün atamalarında sorunun cevabı beklenen cevapsa soru çıkarılabilirdir.

## Kaba kuvvet

Küçük örneklerde (en çok 7 kişi), varsayımlara uyan ve olguları doğrulayan **bütün** dünyalar sayıldı: aile yapısı ve cinsiyetler birlikte.

- 152 üretilmiş örnekte iki yöntem 152'sinde aynı kararı verdi: 93 çıkarılabilir, 58 değil.
- Eski tanım (ağaç sabit) bunların 1'inde yanılıyordu.
- Testte 24 rastgele örnek ve elle örnekler var (`testler/test_a6_olgudan_cikarilabilirlik.py`).

## ÖK-003 yön ters soruları (2000)

| Küme | Beklenen | Sonuç |
|---|---|---|
| (a) 119 hatanın 113'ü (görünmeyen evlilik) | çıkarılamaz | 113/113 çıkarılamaz |
| (b) 6 açıklanamayan hata | incelenecek | 6/6 çıkarılabilir (aşağıda) |
| (c) çekirdeğin doğru bildiği, geçici türün çıkarılamaz saydığı 27 soru | çıkarılabilir | 27/27 çıkarılabilir |
| çekirdeğin doğru bildiği öteki 1854 soru | — | 1854/1854 çıkarılabilir |

Etki: tohum 12'nin eğitim, uzunluk, önsel-ters ve yeniden adlandırma bölmelerinde yeni tanım hiçbir soruyu atmıyor. Yalnız yön ters etkileniyor (2000'de 113).

## (b) 6 hata: neden

Altısında da karar verdiren kişinin cinsiyeti, zincirin dışındaki ayrı bir olgudan geliyor. Örnek: "22, 23'ün oğlu" olgusundan 22 erkek, bu yüzden dede.

- Olgulardan cevap çıkar, ama DNA'da cinsiyeti bir olgudan ötekine taşıyan kural yok. Bu yüzden DNA kapanışında cevap yok.
- Bu bir DNA kapsam açığıdır; çekirdek ya da tanım hatası değil.
- Bu tür bir kural 2 halkayla yazılabilir. Örnek: "W'nin oğlu Y ∧ Y'nin kızı X → X'in babası Y".
- DNA'yı danışman düzeltir (K-024). Bu sorular yeni koşuda da çıkacağı için, H1 yeniden koşusundan önce danışmanın görmesi gerekir.

### Tohum 12, bölüm `49ed749ce804`

Soru: 7 → 10. Beklenen: **dede**.

```
4 —oğul→ 10
10 —kız→ 26
19 —anne→ 22
26 —kız→ 62
36 —kız_kardeş→ 11
46 —kız→ 8
62 —kız_kardeş→ 7
```

### Tohum 12, bölüm `db3cc4591ccd`

Soru: 39 → 22. Beklenen: **dede**.

```
2 —kız→ 54
9 —baba→ 26
22 —eş→ 2
39 —erkek_kardeş→ 28
40 —baba→ 25
53 —oğul→ 22
54 —oğul→ 39
```

### Tohum 13, bölüm `6047601e4c23`

Soru: 4 → 27. Beklenen: **baba**.

```
4 —oğul→ 30
10 —oğul→ 27
18 —kız→ 4
25 —kız_kardeş→ 7
27 —eş→ 18
33 —oğul→ 6
```

### Tohum 14, bölüm `4dbc52e0b3e6`

Soru: 4 → 22. Beklenen: **dede**.

```
0 —oğul→ 20
22 —baba→ 3
22 —kız→ 27
23 —oğul→ 22
27 —kız→ 4
32 —erkek_kardeş→ 33
```

### Tohum 16, bölüm `ff146df79775`

Soru: 43 → 13. Beklenen: **baba**.

```
0 —oğul→ 13
8 —anne→ 30
13 —eş→ 31
26 —kız_kardeş→ 43
30 —kız→ 24
31 —kız→ 26
33 —oğul→ 21
```

### Tohum 16, bölüm `2c3fa3fbcd97`

Soru: 12 → 13. Beklenen: **anne**.

```
3 —erkek_kardeş→ 18
8 —oğul→ 27
13 —eş→ 27
20 —kız_kardeş→ 42
27 —kız→ 12
36 —erkek_kardeş→ 19
```
