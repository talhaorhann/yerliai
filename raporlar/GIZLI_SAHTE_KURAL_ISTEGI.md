# Gizli sahte kural isteği (danışmana)

**Tarih:** 2026-10-26. **Dayanak:** K-041 (3), ÖK-005 taslağı §4 madde 19.
**Amaç:** H2'nin B1 basamağında geçidin sahte kısayol kurallarını kabul etmediği sınanır. Sahte kuralların yarısını kodlayıcı yazar (görünür aileler G1–G4), yarısını siz yazarsınız (gizli aileler). Kodlayıcı gizli dosyayı hiç açmaz; geçidi yazan kişi gizli türleri bilmediği için sınama dürüst olur.

## 1. İstenen

**Sayılar:**
- **En az 4 aile × en az 40 kural** (toplam en az 160).
- Her aile bir sahte kısayol **türüdür**. Türler aşağıdaki görünür ailelerden (G1–G4) **farklı** olmalı.
- Aile adı harf, rakam ve alt çizgiden oluşur. G1, G2, G3, G4 kullanılamaz.

**"Sahte" ne demek:** kural, bugünkü akrabalık dünyalarında (A1, A2 ya da A3) en az bir durumda **yanlış** sonuç verir; ama ilk bakışta doğru ya da işe yarar görünebilir. Tamamen doğru bir kural sahte sayılmaz.

**Sınırlar:**
- Kural 1–3 halkalıdır (çekirdeğin sınırı).
- İlişki adları yalnız aşağıdaki listeden alınır.

## 2. Görünür aileler (kodlayıcı yazar; sizinkiler bunlardan farklı olmalı)

| Aile | Ne |
|---|---|
| G1 bozuk sonuç | Doğru görünen gövde, aynı dışlayıcı gruptan yanlış sonuç ilişkisi |
| G2 aşırı genel | Gerekli bir halkası (ör. cinsiyet tanığı) silinmiş kural |
| G3 kapsam artefaktı | Geliştirme dünyalarında yalnız A1 ailesinde tutan, A2 ya da A3'te yanlışlanan kural |
| G4 gizli ters | Baş çiftine doğrudan dokunmadan, simetrik ve tek değerli bir ilişkinin iki adımlık geri dönüşüyle (ör. eşin eşi kişinin kendisidir) başın tersini okuyan kural |

## 3. İlişkiler (onaylı şema, `sema/iliskiler_v1.json`)

**Okunuş:** (A, r, B) = "B, A'nın r'sidir". Örneğin (X, baba, Y) = "Y, X'in babasıdır".

| İlişki | Tersi | Simetrik | Tek değerli (işlevsel) |
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

## 4. Kayıt biçimi

**Şemalar:** `sema/aday_v1.schema.json` (tek aday) ve `sema/kirmizi_dosyasi_v1.schema.json` (dosya).

**Dosya alanları:**
- `sema_surumu`: "1".
- `dosya_turu`: sizin dosyanızda **"kirmizi_gizli"**.
- `yazan`, `tarih` (YYYY-AA-GG).
- `aileler`: her aile için `ad` ve `aciklama`.
- `adaylar`: kurallar.

**Her kuralın (adayın) alanları; hepsi zorunlu, `okunus` dışında:**

| Alan | Açıklama |
|---|---|
| `sema_surumu` | "1" |
| `kimlik` | Küçük harf, rakam, alt çizgi; dosyada tek |
| `halkalar` | 1–3 halka; her biri `gen` (ilişki adı), `sol`, `sag` (büyük harfli değişken: X, Y, Z, W …) |
| `sonuc` | Baş: `gen`, `sol`, `sag`. Baş değişkenleri gövdede geçmeli ve birbirinden farklı olmalı |
| `farkli` | Farklı kişi olması gereken değişken çiftleri, ör. [["X", "Z"]]; yoksa [] |
| `oi` | true ise gövdedeki bütün değişkenler farklı kişiye bağlanır; o zaman `farkli` [] olmalı |
| `kaynak` | {"tur": "kirmizi_gizli", "aile": "<aile adı>", "tohum": null, "ust": []} |
| `tanik_ozeti` | null |
| `surum` | 1 |
| `okunus` | İsteğe bağlı, önerilir. Kuralın Türkçe okunuşu ve neden sahte olduğu. Kodlayıcı B1 bitene kadar okumaz; sonuç raporunda kullanılır. |

**Ek kurallar:** bir halkanın iki ucu aynı değişken olamaz; aynı halka iki kez yazılamaz.

## 5. Örnek (görünür ailelerden üç kayıt; sizin dosyanızda `dosya_turu` ve `kaynak.tur` "kirmizi_gizli" olur)

```json
{
  "sema_surumu": "1",
  "dosya_turu": "kirmizi_gorunur",
  "yazan": "kodlayıcı (örnek dosya)",
  "tarih": "2026-10-26",
  "aileler": [
    {
      "ad": "G1",
      "aciklama": "Bozuk sonuç: doğru görünen gövde, aynı dışlayıcı gruptan yanlış sonuç ilişkisi."
    },
    {
      "ad": "G2",
      "aciklama": "Aşırı genel: gerekli bir halkası (ör. cinsiyet tanığı) silinmiş kural."
    },
    {
      "ad": "G3",
      "aciklama": "Kapsam artefaktı: geliştirme havuzunda yalnız A1 ailesinde tutan, A2 ya da A3'te yanlışlanan kural."
    },
    {
      "ad": "G4",
      "aciklama": "Gizli ters: baş çiftine dokunmadan, simetrik ve işlevsel bir ilişkinin iki adımlık geri dönüşüyle başın tersini okuyan kural."
    }
  ],
  "adaylar": [
    {
      "sema_surumu": "1",
      "kimlik": "ornek_g1_bozuk_sonuc",
      "halkalar": [
        {
          "gen": "baba",
          "sol": "X",
          "sag": "Y"
        },
        {
          "gen": "baba",
          "sol": "Y",
          "sag": "Z"
        }
      ],
      "sonuc": {
        "gen": "dayı",
        "sol": "X",
        "sag": "Z"
      },
      "farkli": [],
      "oi": false,
      "kaynak": {
        "tur": "kirmizi_gorunur",
        "aile": "G1",
        "tohum": null,
        "ust": []
      },
      "tanik_ozeti": null,
      "surum": 1,
      "okunus": "Y, X'in babası; Z, Y'nin babası ise Z, X'in dayısıdır. (Sahte: Z, X'in dedesidir.)"
    },
    {
      "sema_surumu": "1",
      "kimlik": "ornek_g2_asiri_genel",
      "halkalar": [
        {
          "gen": "kız",
          "sol": "X",
          "sag": "Y"
        }
      ],
      "sonuc": {
        "gen": "baba",
        "sol": "Y",
        "sag": "X"
      },
      "farkli": [],
      "oi": false,
      "kaynak": {
        "tur": "kirmizi_gorunur",
        "aile": "G2",
        "tohum": null,
        "ust": []
      },
      "tanik_ozeti": null,
      "surum": 1,
      "okunus": "Y, X'in kızı ise X, Y'nin babasıdır. (Sahte: X kadın olabilir; cinsiyeti gösteren halka yok.)"
    },
    {
      "sema_surumu": "1",
      "kimlik": "ornek_g4_gizli_ters",
      "halkalar": [
        {
          "gen": "oğul",
          "sol": "Z",
          "sag": "X"
        },
        {
          "gen": "eş",
          "sol": "Z",
          "sag": "W"
        },
        {
          "gen": "eş",
          "sol": "W",
          "sag": "Y"
        }
      ],
      "sonuc": {
        "gen": "baba",
        "sol": "X",
        "sag": "Y"
      },
      "farkli": [],
      "oi": false,
      "kaynak": {
        "tur": "kirmizi_gorunur",
        "aile": "G4",
        "tohum": null,
        "ust": []
      },
      "tanik_ozeti": null,
      "surum": 1,
      "okunus": "X, Z'nin oğlu; W, Z'nin eşi; Y, W'nin eşi ise Y, X'in babasıdır. (Sahte: eşin eşi Z'nin kendisidir; Z, X'in annesi de olabilir.)"
    }
  ]
}
```

## 6. Teslim (önemli)

1. **Dosyayı sohbete ek olarak göndermeyin.** Sohbet ekleri kodlayıcıya otomatik gösterilir ve gizlilik bozulur.
2. Dosyayı depoya doğrudan koyun:
   - yol: `degerlendirme/kirmizi_gizli/kirmizi_gizli_v1.json`
   - dal: `asama-6`
   - GitHub'da: "Add file" → "Upload files".
3. Sonra yalnız "gizli dosya depoda" deyin.
4. Kodlayıcı yalnız şu denetimi çalıştırır: `python3 -m kesif.aday degerlendirme/kirmizi_gizli/kirmizi_gizli_v1.json kirmizi_gizli`.
   - Araç yalnız aile sayısını, kural sayısını, en küçük ailenin boyunu ve dosyanın sha256 özetini yazar.
   - Biçim hatası varsa yalnız hatanın yerini yazar (ör. `dosya.adaylar[12].halkalar[0].gen: onaylı şemada yok`). Değeri yazmaz. Düzeltip yeniden koyarsınız.
5. Denetim geçince özet `config_h2.json`'a yazılır ve kilitlenir. Dosya B1'de geçide yalnız kırmızı takım koşucusu tarafından verilir.
6. **Sonuç:** B1 sonunda aile başına yakalama sayısı raporlanır.

**Ne zaman:** B1 başlamadan önce. B0'ı beklemez.
