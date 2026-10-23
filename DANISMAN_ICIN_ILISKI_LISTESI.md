# Danışman için onaylı ilişki listesi (DNA yazımı)

Bu dosya, akrabalık kurallarını (DNA) yazacak bağımsız danışman içindir (K-024). Yalnız onaylı ilişki listesini,
okuma yönünü, dünya varsayımlarını ve kural biçimini içerir. Projenin gizli tanımlarını İÇERMEZ.

**Danışmandan istenen:** Kuralları yalnız bu dosyaya ve kendi Türkçe akrabalık bilginize dayanarak yazın.
Projenin başka hiçbir dosyasına bakmayın.

- Kaynak: `sema/iliskiler_v1.json` (kullanıcı onaylı, K-006), sha256 `095c57b55458631d86140a86b74677a775240ede52ef3213614ab40fde10b413`.
- "B'nin cinsiyeti" sütunu şemada yoktur. Sözcüğün Türkçe anlamından yazıldı. E: erkek, K: kadın, —: sözcük cinsiyet belirtmez.

## 1. Okuma yönü

**(A, r, B) = "B, A'nın r'sidir."**

Örnek: (A, baba, B) = B, A'nın babasıdır. Kurallarda da aynı: `dede(X, Z)` = Z, X'in dedesidir.

## 2. İlişkiler (21 tane)

| İlişki | B'nin cinsiyeti | Tersleri: (A, r, B) ise (B, ?, A) | Simetrik | İşlevsel |
|---|---|---|---|---|
| `anne` | K | `oğul`, `kız` | hayır | evet |
| `baba` | E | `oğul`, `kız` | hayır | evet |
| `oğul` | E | `anne`, `baba` | hayır | hayır |
| `kız` | K | `anne`, `baba` | hayır | hayır |
| `eş` | — | `eş` | evet | evet |
| `erkek_kardeş` | E | `erkek_kardeş`, `kız_kardeş` | hayır | hayır |
| `kız_kardeş` | K | `erkek_kardeş`, `kız_kardeş` | hayır | hayır |
| `dede` | E | `torun` | hayır | hayır |
| `babaanne` | K | `torun` | hayır | evet |
| `anneanne` | K | `torun` | hayır | evet |
| `torun` | — | `dede`, `babaanne`, `anneanne` | hayır | hayır |
| `amca` | E | `yeğen` | hayır | hayır |
| `dayı` | E | `yeğen` | hayır | hayır |
| `hala` | K | `yeğen` | hayır | hayır |
| `teyze` | K | `yeğen` | hayır | hayır |
| `yeğen` | — | `amca`, `dayı`, `hala`, `teyze` | hayır | hayır |
| `kuzen` | — | `kuzen` | evet | hayır |
| `kayınpeder` | E | `gelin`, `damat` | hayır | evet |
| `kayınvalide` | K | `gelin`, `damat` | hayır | evet |
| `gelin` | K | `kayınpeder`, `kayınvalide` | hayır | hayır |
| `damat` | E | `kayınpeder`, `kayınvalide` | hayır | hayır |

- **Tersleri:** (A, r, B) doğruysa (B, q, A) ilişkisi bu sütundaki q'lardan biridir. Hangisi olduğu genelde A'nın cinsiyetine bağlıdır.
- **Simetrik:** (A, r, B) doğruysa (B, r, A) da doğrudur.
- **İşlevsel:** bir kişinin bu ilişkiden en çok bir tane olur (ör. bir kişinin tek babası vardır).
- **Dışlayıcı grup:** `anne`, `baba`, `oğul`, `kız`, `eş`, `erkek_kardeş`, `kız_kardeş`, `dede`, `babaanne`, `anneanne`, `torun`, `amca`, `dayı`, `hala`, `teyze`, `yeğen`, `kuzen`, `kayınpeder`, `kayınvalide`, `gelin`, `damat`. Aynı iki kişi arasında bu gruptaki ilişkilerden en çok biri olur.

## 3. Dünya varsayımları

Kullanıcının altın küme cevaplarında kullandığı varsayımlar (ÖK-001) ve onaylı şemanın notu:

- Kardeşler aynı anne babanın çocuğudur (üvey ya da yarım kardeş yok).
- Bir çocuğun iki ebeveyni birbirinin eşidir; eşin çocuğu kişinin kendi çocuğudur.
- Akraba evliliği yok.

## 4. Çekirdek kuralları nasıl kullanır

- **Olgular** (A, r, B) biçiminde gelir. **Soru:** iki kişi (A, B) arasındaki ilişki. **Cevap:** listedeki ilişkilerden biri ya da "bilmiyorum".
- **Kural (hücre):** 1–3 halka. Her halka bir ilişki ve iki değişkenden oluşur. Bütün halkalar tutunca sonuç ilişkisi yazılır. Örnek (şartnameden): `baba(X, Y) ∧ baba(Y, Z) → dede(X, Z)`.
- **Zincirleme:** Çekirdek kuralları tekrar tekrar uygular; bir kuralın yazdığı sonuç başka bir kuralın girdisi olur. 10 adıma kadar uzun zincirler böyle çözülür. Bu yüzden ara sonuçlar da listedeki ilişkilerden biri olmalıdır; listede olmayan bir ilişki (ör. "büyük dede") yazılamaz.
- **Sınırlar:** en çok 8 tur, havuzda en çok 64 kayıt.
- **Yalnız her durumda doğru kural:** Bir kural, halkaları tutan her durumda doğruysa yazılır. Sonuç bazen doğru bazen yanlış oluyorsa (ör. A'nın cinsiyeti bilinmiyorsa) o kural yazılmaz; çekirdek o durumda "bilmiyorum" der.
- **Farklı kişi şartı:** Kuraldaki ayrı harfler aynı kişiye bağlanabilir. Bir kuralda X ile Z aynı kişi olabiliyor ve o durumda sonuç yanlış oluyorsa kurala `"farkli": [["X", "Z"]]` ekleyin. Birden çok çift yazılabilir. Şart gerekmiyorsa yazmayın.

## 5. Teslim biçimi (DNA sürüm 2, JSON)

Tek bir JSON dosyası, örneğin `akrabalik_dna_v2.json`:

```json
{
  "sema_surumu": "2",
  "hucreler": [
    {
      "kimlik": "dede_1",
      "halkalar": [
        {
          "gen": "baba",
          "sol": "X",
          "sag": "Y",
          "esik": 0.5
        },
        {
          "gen": "baba",
          "sol": "Y",
          "sag": "Z",
          "esik": 0.5
        }
      ],
      "sonuc": {
        "gen": "dede",
        "sol": "X",
        "sag": "Z"
      },
      "guvenilirlik": 1.0,
      "okunus": "Y, X'in babası; Z, Y'nin babası ise Z, X'in dedesidir."
    }
  ]
}
```

Alanlar:

- `sema_surumu`: her zaman `"2"`.
- `kimlik`: kuralın benzersiz adı. Yalnız küçük harf (a–z), rakam ve alt çizgi; Türkçe harf yok.
- `halkalar`: 1–3 halka. `gen`: listedeki ilişki adı, aynen. `sol` / `sag`: büyük harfle başlayan değişken (X, Y, Z, W…). `esik`: 0.5 yazın (değiştirmeyin).
- `sonuc`: sonuç ilişkisi ve değişkenleri. Sonuçtaki değişkenler halkalarda da geçmeli.
- `guvenilirlik`: 1.0 yazın (değiştirmeyin).
- `okunus`: kuralın tek Türkçe cümleyle okunuşu. Kullanıcı her kuralı bu cümleye bakarak evet/hayır diye onaylayacak.
- `farkli`: isteğe bağlı, yukarıdaki farklı kişi şartı.
