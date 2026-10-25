# A6 gösterimi: maskeli bellek geçidi, gerçek DNA v8, gözlemli veri (2026-10-25)

Araç: `degerlendirme/a6_gosterim.py` (V-057). Ham sonuç: `raporlar/A6_gosterim_v8.json`. Süre: 88 dakika (3 süreç).

- **DNA:** `veri/dna/akrabalik_dna_v8.json`, 244 kural (kilitli değil). Bozuk sürüm: sonucu temel ilişki olan 112 kuralın sonucu, temel ilişkiler listesinde bir sonrakiyle değiştirildi.
- **Veri:** gözlem bölümleri (K-035): seçilen kişiler arasındaki bütün ilişkiler, türetilmişler dahil, olgu olarak. Sorgu ve cevap yok. İki ortam, her biri 8 bölüm: olağan (zincir uzunluğu 2–3) ve kaydırılmış (4–10).
- **Geçit:** bellek boş, her kural tek başına. Kuralın sonuç ilişkisindeki her gözlem birer birer maskelendi. Eşikler K-036 (geçici): doğruluk 1,0; en az 3 kanıt; müdahale 0,9.
- Geçit "doğru/bozuk" etiketini görmez; ayrım yalnız bu rapordadır.

## Sonuç

| | Onaylı formül (müdahale a·b·c) | V-058 önerisi (müdahale b·c) |
|---|---|---|
| 244 doğru kural | **69 kabul**, 45 kısayol, 130 sınanamadı | **114 kabul**, 130 sınanamadı |
| 112 bozuk kural | **93 yanlış**, 19 sınanamadı | 93 yanlış, 19 sınanamadı |

- Doğru kuralların hiçbiri "yanlış" ya da "çelişkili" çıkmadı. Maskelenen gözlemlerden 3847'sini yeniden türettiler; yanlış tahmin 0.
- Bozuk kuralların hiçbiri kabul edilmedi. 93'ü yanlış diye reddedildi; 91'inde en kötü ortam doğruluğu 0.
- Eski 170 kural: 65 kabul, 38 kısayol, 67 sınanamadı (öneriyle 103 kabul). Yeni 74 kural: 4 kabul, 7 kısayol, 63 sınanamadı (öneriyle 11 kabul).

## 45 "kısayol" (doğru kurallar)

- 45'inin hepsinde iki ortamda da doğruluk 1,0.
- Düşük olan yalnız müdahalenin (a) bileşeni. Aynı cevap birden çok bağımsız yoldan çıkıyor (ör. iki çocuğu olan çiftin eşliği iki çocuktan ayrı ayrı). Bir kök silinince öteki yol kalıyor, güven düşmüyor.
- Bu kurallarda a·b·c ortalaması 0,9'un altında; tek tek değerler 0'a kadar iniyor. Bütün doğru kurallarda müdahale ölçülen 3847 cevabın 3839'unda b·c = 1,0, en düşük 0,8.
- V-058 önerisiyle 45'inin hepsi kabul.

## 130 "sınanamadı" (doğru kurallar)

- 46'sının gövdesi 16 bölümün hiçbirinde eşleşmedi: 38'i 3 halkalı, 34'ü v8'de yeni eklenen kural. Bu küçük ailelerde o desen çıkmıyor.
- 84'ünde bir ortamda kanıt 3'ten az: 75'i olağan ortamda (kısa zincirde az kişi var), 1'i kaydırılmışta, 8'i ikisinde.
- Daha çok bölümle bunların bir kısmı ölçülebilir. Bölüm sayısı sürenin sınırıdır (V-057).

## 19 "sınanamadı" (bozuk kurallar)

- 16'sı hiç eşleşmedi, 3'ünde kanıt 3'ten az.
- Örnek: `baba_baba_ogul_bozuk` 3 yanlış tahmin yaptı (kaydırılmışta 2, olağanda 1). Ama hiçbir ortamda kanıt 3'e ulaşmadığı için doğruluk "ölçülmüş" sayılmadı. Kapı reddetmek için de en az 3 kanıt istiyor.

## Önceki ölçümde reddedilmeyen 3 bozuk kural (B5)

Önceki ölçüm 2026-10-24'teydi: eski eğitim bölümleri, bellek = öteki 169 kural. Üçü de kanıt olmadığı için "sınanamadı" kalmıştı:

| Kural | Ne bozuk | O zaman | Şimdi (gözlemli veri, bellek boş) |
|---|---|---|---|
| `baba_baba_ogul_bozuk` | X, Y'nin oğlu yerine kızı | 40 bölümde 2 eşleşme, kanıt 0 | sınanamadı: 3 yanlış, kanıt eşiğin altında |
| `anne_baba_ogul_bozuk` | X, Y'nin oğlu yerine kızı | 40 bölümde 2 eşleşme, kanıt 0 | **ret: yanlış** (6 yanlış, 0 doğru) |
| `erkek_kardes_anne_kiz_kardes_bozuk` | X, Y'nin kız kardeşi yerine annesi | hiç eşleşmedi | **ret: yanlış** (18 yanlış, 0 doğru) |

Neden o zaman reddedilmediler: eski bölümler seyrek zincir olgularıydı. Bozuk sonuç (ör. "X kızdır") ile çelişecek bir gözlem aynı çift için hiç yoktu. Şema da cinsiyet çelişkisini çiftler arası göremez. Gözlemli veride aynı çiftin gerçek ilişkisi görünür; bozuk tahmin onunla şema çelişkisine düşer.
