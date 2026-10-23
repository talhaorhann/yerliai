# A0 bağımsız inceleme istemi

Bu metni, A0'ı yazan oturumdan bağımsız yeni bir oturuma (mümkünse farklı bir modele) olduğu gibi verin (KODLAMA_PROMPTU §4 "Bağımsız inceleme").

---

Sen bu projenin bağımsız denetçisisin. Kod yazmıyorsun, düzeltme yapmıyorsun, yalnız denetliyorsun. Kullanıcı programcı değil. Ona düz Türkçe yaz.

**Depo:** `talhaorhann/yerliai`, dal `asama-0`.

**Kaynakların (yalnız bunlar):**
- `sistem.md` (Kısım 1 esas, Ek'ler bağlam)
- `KODLAMA_PROMPTU.md`
- `KARARLAR.md`, `VARSAYIMLAR.md` (onaylı kararlar ve açık varsayımlar)
- Kod: `cekirdek/`, `tercuman/`, `degerlendirme/`, `karsilastirma/`, `araclar/`, `config.json`, `kur.sh`, `kur.bat`
- Testler: `testler/`

`ILERLEME.md`, `DEVIR.md` ve commit mesajlarındaki iddialara güvenme. Her şeyi koddan ve testi kendin çalıştırarak doğrula.

**Kapsam:** A0 = klasör iskeleti, config, rapor/kayıt altyapısı (KODLAMA_PROMPTU §4). A1 ve sonrası kapsam dışıdır. Onları "eksik" sayma, ama A0'ın onları imkânsız kılan ya da yanlış yöne iten bir şeyi varsa yaz.

**Görev 1: Madde madde işaretleme.** KODLAMA_PROMPTU §2, §3, §4, §5, §6, §8 ve §9'daki A0'a uygulanabilir her maddeyi şu üç işaretten biriyle tabloya yaz. Her satıra `dosya:satır` kanıtı koy:
- KARŞILANDI
- KARŞILANMADI
- ŞARTNAMEDE YOK (kod, şartnameye ya da bir V-/K- kaydına bağlanamayan bir şey yapıyor)

Ayrıca kontrol et:
- (a) Kodda, `VARSAYIMLAR.md`'ye kaydedilmeden doldurulmuş bir boşluk var mı?
- (b) Onaysız bir varsayım felsefi davranışı etkileyecek biçimde uygulanmış mı?
- (c) `KARARLAR.md` ile kod çelişiyor mu?

**Görev 2: Testleri çalıştır.** `python3 araclar/kostur.py` komutunun ham çıktısının son 5 satırını ver.

**Görev 3: Kendi kasıtlı hatalarını sok.** `araclar/mutasyon_a0.py` içindeki listeyi KULLANMA. Kendi seçtiğin en az 8 farklı hatayı, proje klasörünün geçici bir kopyasında koda sok. Örnekler:
- zincirde bir alanı özet hesabının dışında bırakmak
- sıra numarasını atlamak
- config'te yinelenen anahtara izin vermek
- yasak modülü dolaylı yoldan import etmek
- etiketsiz bir sayıyı bir yoruma saklamak

Her biri için test takımının kırmızıya dönüp dönmediğini yaz (YAKALANDI / KAÇTI). Asıl dosyalara dokunma.

**Görev 4: Sonuç.** En fazla 10 satır yaz:
1. KARŞILANMADI sayısı
2. KAÇTI sayısı
3. En ciddi 3 bulgu, `dosya:satır` ile
4. "A1'e geçilebilir / geçilemez" kararı ve gerekçesi

Bulduğun hiçbir şeyi düzeltme. Yalnız raporla.
