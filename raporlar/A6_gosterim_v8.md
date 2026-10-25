# A6 gösterimi: maskeli bellek geçidi, gerçek DNA v8, gözlemli veri (2026-10-25)

Araç: `degerlendirme/a6_gosterim.py` (V-057). Ham sonuç: `raporlar/A6_gosterim_v8.json`. Süre: 88 dakika (3 süreç).

- **DNA:** `veri/dna/akrabalik_dna_v8.json`, 244 kural (kilitli değil). Bozuk sürüm: sonucu temel ilişki olan 112 kuralın sonucu, temel ilişkiler listesinde bir sonrakiyle değiştirildi.
- **Veri:** gözlem bölümleri (K-035): seçilen kişiler arasındaki bütün ilişkiler, türetilmişler dahil, olgu olarak. Sorgu ve cevap yok. İki ortam, her biri 8 bölüm: olağan (zincir uzunluğu 2–3) ve kaydırılmış (4–10).
- **Geçit:** bellek boş, her kural tek başına. Kuralın sonuç ilişkisindeki her gözlem birer birer maskelendi. Eşikler K-036 (geçici): doğruluk 1,0; en az 3 kanıt; müdahale 0,9.
- Geçit "doğru/bozuk" etiketini görmez; ayrım yalnız bu rapordadır.

> **Karar (2026-10-25):** K-037 ile V-058 önerisi kabul edildi. Bellek geçidinin kararı artık aşağıdaki tablonun sağ sütunudur (müdahale b·c). Sol sütun (a·b·c) yalnız karşılaştırma için kalır. Koşul: H2'de bozuk bir kural kabul edilirse K-037 yeniden açılır. Ham sonuç K-037'den önce üretildi; b·c değerleri orada `mudahale_bc` alanındadır.

## Yöntem (V-057, kodlayıcı kararı)

### Gözlem bölümü nasıl kurulur (`degerlendirme/uretec.py` `gozlem_bolumu`)

1. Üreteçle (V-017) bir soy ağacı kurulur: 4 nesil, çift başına 2–4 çocuk.
2. Kişiler, sorulu bölümlerdeki gibi seçilir:
   - ağaçta rastgele bir zincir yürüyüşü (olağan ortamda 2–3, kaydırılmış ortamda 4–10 adım; sistem.md §10);
   - artı 4 dikkat dağıtıcı doğrudan bağ (V-017); bunların uçları da kişilere katılır.
3. Bölüm, seçilen kişiler arasındaki **bütün** ilişkileri içerir: temel ilişkiler (ebeveyn, çocuk, eş, kardeş) ve türetilmiş ilişkiler (dede, amca, kuzen, …). Her biri gerçek ağaçta doğrudur ve olgu olarak yazılır.
   - Bunlar kâhin etiketi değil, bağımsız gözlemdir (K-035): bölümde sorgu yok, cevap yok, kâhin kaydı yazılmaz.
   - Bir çift için en çok bir gözlem olur.
4. Kişi numaraları rastgele karıştırılır; olguların sırası karıştırılır. Bölüm özeti (sha256) bölüme yazılır.
5. Her ortamın bölümleri, ortam adıyla tohumlanmış ayrı bir rastgele sayı üretecinden gelir (`gozlem_bolumleri`); aynı tohum aynı bölümleri verir.

### Maskeleme kuralı (`degerlendirme/gozlem_puani.py`, `cekirdek/bellek_gecidi.py` `maskeli_kos`)

1. Her bölümde çekirdek önce maskesiz koşar.
2. Sonra adayın sonuç ilişkisindeki her gözlem **birer birer** maskelenir. Maskelenen gözlem çekirdeğe hiç verilmez; kural onu kendi kendine onaylayamaz. Her maske için çekirdek iki kez koşar: yalnız bellekle ve bellek + adayla (bellek boşsa yalnız bir kez).
3. Adayın soyu: adayın yazdığı kayıtlar ve onlardan (bellekteki kurallarla) türeyenler.
4. Sayım çekirdek dışında yapılır:
   - **doğru:** maskelenen gözlem soyca yeniden türetildi;
   - **yanlış:** soydan bir tahmin görünen bir gözlemle şema çelişkisinde (dışlayıcı, işlevsel ya da ters). Aynı (tahmin, gözlem) çifti bölümde bir kez sayılır. Maskelenen gözlemle çelişki ayrıca sayılmaz: çekirdek tekdüze olduğundan aynı çelişki maskesiz koşuda zaten görünür;
   - **çelişki:** soydan bir tahmin bellekten türemiş bir kayıtla ya da soyun kendisiyle çelişiyor;
   - **katkı:** soyun ürettiği, bellekte olmayan ya da bellekte daha geç turda çıkan üçlüler;
   - **müdahale:** cevabı soydan gelen maskeli sorularda b·c (K-037); (a) ve a·b·c kanıtta saklanır.
5. Soydan türeyen başka ilişkilerdeki gözlemler maskelenmez. Bu yüzden onlar için "doğru" sayılmaz ama çelişkiler "yanlış" sayılır (temkinli yön).
6. Ortam doğruluğu = doğru / (doğru + yanlış). Kanıt (doğru + yanlış) 3'ten azsa ortam "ölçülmedi" sayılır. Kararı çekirdeğin `karar_ver`'i verir: en kötü ortam esas alınır (EK A P7).

## Sonuç

| | Eski formül (müdahale a·b·c, karşılaştırma) | **Geçidin kararı (müdahale b·c, K-037)** |
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
