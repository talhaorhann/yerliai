# SİSTEM ŞARTNAMESİ (tek dosya)

Bu dosya projenin tüm tasarım belgelerini birleştirir.
- **KISIM 1 = asıl şartname** (bölüm 1–19). Kodlama AI'ı bunu esas alır. "sistem.md §N" atıfları bu kısmın bölüm numaralarıdır.
- **EK A–G = bağlam.** Önceki kararların özetleri ve panellere sorulan soruların kısa özetleri. Karar değildir. Ek'lerle KISIM 1 çelişirse KISIM 1 kazanır.
- Prompt'taki "karar1.md, dil.md, katilik.md, sifir.md, besleme.md, llm.md" atıfları bu dosyadaki Ek bölümlerine karşılık gelir.

---

# KISIM 1: ASIL ŞARTNAME (eski sistem.md)

# Sistem tanımı: Bağışıklık esinli, kendi kendini sınayan nedensellik mimarisi
(55 yapay zekâ denetçisinin önceki panellerde vardığı ortak kararların birleşimi)

## Fikir sahibinin kuralları
- Fikri ORİJİNALLİĞİNDE tut: havuz, bağışıklık hücreleri, DNA = nedensellik zinciri, döngü, klonal seçilim, sitokin, Treg, bellek ve plazma hücreleri korunur. Gerçekten yanlış olan çıkarılabilir.
- Hız ve verimlilik çok önemli. Tek kişi + tek GPU (24 GB), Python/PyTorch.
- BU TURDA PROTOTİP KOD YAZILMAYACAK: sınama kâğıt üzerinde (el ile iz sürme, düşünce deneyi, hata modu analizi, maliyet hesabı) yapılır.

## 1. Girdi
Mesaj → donmuş küçük cümle kodlayıcı (MiniLM sınıfı) → "antijen" bloğu → antijen sunan hücre (APC) cümle başına bir "epitop" çıkarır: vektör (~128–384 boyut) + sembolik üçlü (özne, ilişki, nesne). İlk aşamada (sentetik soy ağacı) üçlüler doğrudan verilir.

## 2. Havuz
2 katman (0: epitoplar, 1: çıkarımlar). Kapasite 64; dolunca YALNIZ çıkarım katmanından en düşük güven × yaş kaydı atılır. Her kayıt: vektör, üçlü, katman, köken (zincir kimliği + ebeveyn kayıt kimlikleri), güven, yaş. Her turda en yüksek skorlu ~4 öğe "yayın sahnesi"ne çıkar.

## 3. Hücreler (DNA = nedensellik zinciri)
- DNA: 1–3 halkalı değişkenli zincir, ör. baba(X,Y) ∧ baba(Y,Z) → dede(X,Z). Her halka: ilişki geni + reseptör vektörü + eşik θ. Ek genler: sitokin şiddeti (0..s_max).
- Popülasyon 300–500 hücre.
- Eşleşme: sembolik bağlama maskesi (tüm halkalar farklı kayıtlara tutarlı bağlanmalı) × kosinüs afinitesi > θ (sitokinle kaydırılmış). Vektörleştirilmiş maskeli matmul.
- Yarı-naif (delta) eşleşme: en az bir halka bir önceki turda yazılmış kayıttan eşleşmeli. İlişki dizini (ilişki → kayıt listesi). Hücre başına tur başına ≤8 yazma. Eşleşme öncesi karma tabloyla tekilleştirme. Tur başına eşleşme bütçesi (aşılırsa en düşük afinite × güven atılır).
- Yazma: hücre yakaladığını SİLMEZ; havuza yeni kayıt yazar (sonuç vektörü + üçlü, köken, güven = min-t-norm(afiniteler) × hücre güvenilirliği).

## 4. Sitokin
İdiotipik ağ kuralı: tetiklenen hücre, çıktısını tüketecek hücrelerin (sonuç ilişkisi onların öncülü) eşiğini düşürür; aynı çıktıyı üreten rakiplerinkini yükseltir. Seyrek scatter ile DNA'dan hesaplanır. tanh/kırpma ile sınırlı, sönümlü (γ<1), toplam sitokin bütçesi. Kararlılık izleyicisi: etkileşim matrisi J'nin spektral yarıçapı ρ(J)<1 (güç iterasyonu); aşılırsa kazanç otomatik yarılanır.

## 5. Treg ve durma
Treg: kopya (kosinüs>0.95 veya aynı (üçlü, köken)) ve çelişen yazımları baskılar (eşiklerini yükseltir). Durma: (a) yeni kayıt yok, (b) yanıt güveni > τ (τ = güven dağılımının yüzdeliği), (c) 8 tur. Yanıt yokken yeni kayıt da yoksa bir kez eşik düşürülür (impasse), sonra durur.

## 6. Plazma hücresi
Sorguyu üst katmanla eşleştirir; aynı sonuca giden ispatların güvenini noisy-OR ile birleştirir; yanıt etiketi + köken DAG'ından gerekçe zinciri. (Sonraki aşama: plan → şablon → küçük model akıcılaştırır → geri ayrıştırma sadakat kapısı.)

## 7. Öğrenme
- CLONALG: klon sayısı uygunlukla orantılı, hipermutasyon afiniteyle ters orantılı, her nesil en kötü ~%10 rastgele yenilenir. Niş koruma. Elitizm %10.
- Mutasyon: tür-uyumlu (yalnız havuzda gerçekten zincirlenen ilişki çiftleri); bellek hücrelerinden öğrenilen alt-zincir kütüphanesi + MDL önseli (kısa/sık kalıplar önce). Rekombinasyon ("uyku"): iki başarılı zinciri birleştirme operatörü; yüklem icadı (başarılı zincir yeni tek halkaya katlanır).
- Gradyan: reseptör vektörleri ve eşikler; evrimle eşzamanlı ama zaman ölçeği ayrı (sitokin hızlı / gradyan orta / evrim yavaş).
- Timus hunisi: (1) her mutant 16–64 örneklik ORTAK mini-grupta yalnız sembolik eşleşmeyle (gradyansız) sınanır; öz-tepkisiz/aşırı tepkili elenir. (2) Ardışık yarılama 8→32→128→tam. (3) Gradyan ısınması yalnız hayatta kalan %10–20'ye, 3–5 adım, ebeveynden ağırlık mirası. (4) Kaçış payı %5, ön eleme–gerçek uygunluk sıra korelasyonu düşerse %10'a çıkar. (5) Zincir sicili: ortak önekler önek ağacında örnek başına bir kez hesaplanır (sürüm anahtarı + LRU).
- Müfredat: halka sayısı 1→2→3; üst düzey, alt düzeyin bellek hücreleri oluşunca açılır.

## 8. Kredi ve uygunluk
- Her turda köken DAG'ı üzerinde tahmin tabanlı bucket brigade (taban çıkarılmış, EMA).
- Her E adımda yalnız yanıt kökenindeki / elit hücrelerde karşı-olgusal susturma + do(X) müdahale testi.
- Uygunluk = doğruluk × (ε + müdahale puanı). Kısa yol cezası uygunluğa GİRMEZ; yalnız bellek kapısı ve test ölçütüdür.
- Negatif seçilim: deneyim eşiğini (~20 tetiklenme) geçip hâlâ katkısız ya da dikkat dağıtıcılara tepki veren zincirler elenir.
- Bellek hücresi: uygunlukta üst ~%5 VE müdahale testi VE karşı-kısayol testleri geçilmiş olmalı; mutasyondan korunur, düşük eşikle hızlı tetiklenir.

## 9. Müdahale testi (kopya kâğıdı yok)
Sistem bir epitopu siler / tür uyumlu yedekle değiştirir, aşağı akışı KENDİ zincirleriyle yeniden hesaplar (yalnız etkilenen köken alt grafı). Ölçülen: (a) ilgili bağ kesilince yanıt güveni düşüyor mu, (b) ilgisiz bilgi (sorgu yolundaki varlıklarla kenar paylaşmayan) değişince yanıt sabit mi, (c) mantıksal tutarlılık (ters ilişki, geçişlilik). CLUTRR etiketleri yalnız ~500 örneklik AYRI kalibrasyon kümesinde (hedef r>0.8), eğitime asla sızmaz. Öğrenilmiş dünya modeli sonraki aşama.

## 10. Ezber önleme ve değerlendirme
Bölmeler: uzunluk genellemesi (eğitim k=2–3, test k=4–10), isim/şablon karıştırma, önsel-ters, zincir-bozuk ("bilmiyorum"), yön ters çevirme, ilişki yeniden adlandırma. Kelime çantası kısa yol dedektörünün çözdüğü örnekler Treg'e (verisi test bölmelerinden ayrı). Sadakat metrikleri: comprehensiveness/sufficiency. ≥5 tohum, bootstrap GA, permütasyon testi + Holm.

## 11. Veri
Sentetik soy ağacı üreteci (gizli kurallar; yalnız son cevabı bilir) + parafraz çeşitlendirme. Ara etiketler yalnız ilk oyuncak aşamasında iskele, sonra kaldırılır (ablasyonla raporlanır). Maskeli üçlü tamamlama CLUTRR aşamasında.

## 12. Ölçüm
FLOP kalemleri ayrı (ileri, geri, eşleşme, müdahale) + duvar saati. Transformer aynı toplam FLOP ve aynı örnek sayısıyla, 3–4 boyut, 3 tohum; "doğruluk–FLOP" ve "doğruluk–örnek" eğrileri. Karşılaştırmalar: küçük Transformer, GNN, saf XCS, rastgele arama. Ablasyonlar: sitokinsiz, müdahalesiz, Treg'siz, evrimsiz, şablonlu (germline) varyant.

## 13. Yol haritası
H1: çekirdek + elle doğru DNA ile %100 birim testi + ön kayıt. H2: klonal seçilim kuralı sıfırdan buluyor mu. H3: müdahale + bellek + rekombinasyon + kısa yol yemleri + küçük yüklem icadı; NDM prototip takvimi. H4: sitokin + Treg + ablasyonlar + karar. Sonra CLUTRR (2–3 hafta), sonra açık ilişki/metin üretimi.

## Önceki panellerin tahminleri (ölçülmemiş)
Sorgu başına hesap 10–100× az; eğitim hesabı ~3–10× azalma (huni); veri ~2–4× azalma; en güçlü vaat uzun zincir genellemesi + gerekçe.

---

## 14. Besleme kararı (50 uzman paneli, hipotez)

- Ana kaynak: hazır yapılandırılmış bilgi tabanları (KeNet, Wikidata, ConceptNet, UD); 16/50 oy LLM yardımlı çıkarım + insan örnek denetimi istedi. Akrabalıkta yedek: sentetik aile ağacı üreteci (test kümesi ayrı kaynaktan/elle).
- Şema: LLM taslak (~20–30 ilişki), kullanıcı bir kez onaylar (ters/simetrik/dışlayıcı işaretleri dahil).
- Tohum etiket: ~100–200, aktif öğrenmeyle seçilir, kullanıcı etiketler. LLM etiketi ikinci halka, "kanıtlanmamış" damgalı.
- Otomasyon: tek komutlu hat; kullanıcı haftada ~20–25 dk (20–30 belirsiz örneğe evet/hayır/bilmiyorum, rapor okuma). İlk hafta +30–40 dk şema onayı, bir kerelik tohum etiketleme ~2–3 saat.
- Türkçe sözlük PDF'leri: şimdilik kullanılmaz (telif, dairesel tanım, OCR). İleride yalnız küçük yerel deneme; çıkan kural "aday" sayılır, onaysız kurala dönüşmez.
- İnternet araştırması: ilk aşamada yok; sonra yalnız güvenilir yapılandırılmış kaynaklar.
- Tuzak ve önlem: kalibrasyon/kâhin sızıntısı ve dairesel doğrulama. Kalibrasyon kümesi ilk gün ayrılıp kilitlenir (salt okunur, hash kayıtlı), her koşuda çakışma kontrolü, kaynak damgası, hata eşiği (~%10) aşılırsa hat durur, sabit "altın küme".

## 15. Dil ve hazır LLM kararı (20 uzman + 10 gözetçi, hipotez)

Hedef: serbest Türkçe konuşan, düşünmesi çekirdekten gelen AI. Hibrit mimari:
- Çekirdek LLM'siz derlenir ve çalışır; tüm karar, öğrenme, bellek ve "bilmiyorum" çekirdekte.
- Girdi çevirmeni (yerel LLM): serbest Türkçe -> şemalı üçlü ADAYLARI (kaynak cümle + kalibre güven + top-3); yalnız metinde yazanı çıkarır.
- Çıktı çevirmeni (yerel LLM): yalnız ispat üçlülerini anlatır; her cümle ispat kaydına bağlı; geri ayrıştırma kapısı eşleşmeyeni reddeder.
- Sınır: tipli, şemalı, imzalı arayüz; LLM çekirdek belleğine/defterine yazamaz; bellek salt okunur, sürüm kilitli.
- LLM'den gelen üçlü, insan onayı ve "kaynak=LLM" etiketi olmadan öğrenmeye girmez; onay ekranında adaylar karıştırılmış sırada.
- Şema, tohum etiket, kalibrasyon kümesi kullanıcıdan gelir, LLM'den değil.
- Yerel model ana, API yalnız yedek/karşılaştırma; sürüm sabit.
- Cevapta çekirdekten gelmeyen cümle "doğrulanmadı" diye işaretlenir.
- Dürüst sınır: "LLM hiç karışmaz" mümkün değil; hedef "LLM çekirdeğe yazamaz, etkisi sınırlı ve ölçülmüş". Kalan en büyük açık: LLM'in aday seçimi (gizli kâhin) -> çoklu LLM çevirisi, uyuşmazlıkta "bilmiyorum", rastgele örneklem denetimi, kapsam raporu.

Türkçe öğrenme zahmeti (tahmin): Seviye 1 kontrollü Türkçe (1–3 saat denetim), Seviye 2 dar alan doğal (200–400 cümle, 5–8 saat bir kerelik), Seviye 3 serbest Türkçe yalnız LLM eşliğinde. Türkçe özellikleri: kök (lemma) bazlı ilişki sözlüğü, düşen özne/eş gönderim, serbest sözcük sırası; tamlamalar akrabalıkta işe yarar.

## 16. Bağımsızlık kanıtı ve test kuralları

- Bağımsızlık testi: aynı elle yazılmış üçlü akışı LLM'siz, başka LLM'le ve sahte (rastgele çıktı) LLM'le çalıştırılır; kural, defter, bellek özeti ve güven değerleri bit düzeyinde aynı olmalı. Eğitim hattında LLM çağrısı sahte nesneyle değiştirilir, fark sıfır.
- Uydurma kural testi: LLM'in bilemeyeceği uydurma kurallarla ("blorp" gibi) çekirdeğin kendi ürettiği cevaplar ölçülür.
- LLM'siz taban hattı ayrı raporlanır; LLM'li sonuç ayrı.
- Sıra: (1) LLM'siz çekirdek + H1 kapısı, (2) kontrollü Türkçe, (3) dar alan doğal Türkçe, (4) serbest Türkçe (yalnız önceki kanıtlar tutarsa).
- Sosyal açık: kullanıcı akıcılığı kanıt sanabilir -> her cümlede ispat bağlantısı, varsayılan "doğrulanmadı".

## 17. Hâkim–tercüman ve "sıfır rutin iş" kararı (20 denetçi, hipotez)

Oylar: S1 (LLM karışması önlenir mi) 20/20 "kısmen"; S2 (sıfır insan denetimi güvenli mi) 20/20 "ancak seyrek örnek denetimiyle"; S3 (yalnız KeNet/Wikidata kalibrasyonu) 20/20 "yeterli değil, bir kerelik insan etiketi şart"; S4 (kendi kendini denetleme birlikte-çökme riski) 12 orta, 8 büyük; S5 (en çok hata) 19 sessiz kayma (drift); S6 (genel karar) 13 "küçük değişiklikle ilerle", 7 "önemli değişiklik".

Karar: mimari (hâkim–tercüman, kapalı iç form) kalır. "Sıfır rutin iş" yerine "neredeyse sıfır rutin iş":
- Bir kerelik insan etiketli, dondurulmuş "altın küme" (~100–300 örnek). Sistem ona asla yazamaz, eğitime/ayara girmez. Kalibrasyon ve eşikler buna dayanır (KeNet/Wikidata tek başına yetmez).
- Altın küme her sürümde ve düzenli (gece/ay) otomatik koşar. Doğruluk eşiğin altına inerse sistem kendini durdurur, kullanıcıya tek satır haber verir (sapma güven aralığı üst sınırıyla; ör. 0/60 hatada %95 üst sınır ≈ %5).
- Tercüman ve denetleyici farklı model ailelerinden; en az bir denetim LLM'siz, kural tabanlı (ör. geri anlatımı kaynak cümleyle biçimsel eşleştirme). Çoklu LLM uyuşması doğruluk kanıtı sayılmaz, yalnız "belki doğru".
- "Bilmiyorum" varsayılan kalır ama kendinden emin yanlışları yakalamaz; bu yüzden altın küme ve seyrek örnek şart.
- Kaynak metin "veri" olarak yalıtılır (prompt injection); kabul edilen her şey sürümlü ve geri alınabilir.
- Kullanıcı yükü: bir kerelik etiketleme (birkaç saat) + isteğe bağlı ayda ~5 dk (20 rastgele örnek); alarm yoksa sormaz. Yeni bilgi eklemeyi durdurma kuralı denetim yapılmazsa devreye girebilir.

## 18. LLM'den zincir fikri, çekirdekte doğrulama (kullanıcı önerisi, panelden geçmedi)

- LLM yalnız ADAY zincir fikri üretir (mutasyon üreteci rolü). Hâkim değildir.
- Adaylar "kaynak=LLM" karantina deposuna girer. Kabul/ret yalnız çekirdeğin kendi kurallarıyla: defter (bağımsız, kök-ayrık destek ve çelişki), müdahale testi, şema kuralları, bellek geçidi; ek olarak bağımsız kaynak (KeNet/Wikidata/altın küme).
- Doğrulama veriye dayanır: çekirdek "doğruluk" üretmez, adayın eldeki olgularla tutarlılığını ve gereklilğini ölçer. Veri olmayan alanda aday "doğrulanmadı" kalır.
- Önerilen deney: tek alanda (akrabalık veya temel iktisat) birkaç yüz–birkaç bin aday zincir çıkar, çekirdekte süz, tohumlu/tohumsuz karşılaştır (aynı başarı için gereken örnek sayısı, uzun zincir genellemesi, sızan hatalı kural sayısı). Beklenti: "besleme sıfır" değil, "besleme azalır" (hipotez).

## 19. Hedef: zamanla LLM'siz Türkçe (kullanıcı hedefi + öneri, panelden geçmedi)

- Kullanıcının asıl amacı: sistem zamanla LLM'e ihtiyaç duymasın; en azından doğru Türkçe cümle kurma LLM'siz olsun.
- Çıktı tarafı (iç form -> Türkçe cümle): kural tabanlı gerçekleyici (dilbilgisi + biçimbirim üreteci: ünlü uyumu, ekler, tamlamalar) ile LLM'siz mümkün görünüyor; Türkçe düzenli olduğu için avantajlı. Bedel: doğru ama kalıpçı/katı üslup. Geri ayrıştırma kapısı aynı kalır.
- Girdi tarafı (serbest Türkçe -> iç form): zor kısım. LLM/kodlayıcı "iskele" olarak başlar; dil kalıbı hücreleri (klonal seçilim, kendi defteri, parafraz/geri çeviri testleri) zamanla kapsamı devralır. LLM'in kademeli emekliliği: tutulmuş cümle kümesinde kendi ayrıştırıcının kapsamı ve LLM ile uyumu eşiği (önceden belirlenmiş) geçince o yapı türü için LLM kapatılır.
- Beklenti: gündelik/belirsiz/mecazlı serbest Türkçede tam LLM'siz anlama kısa vadede gerçekçi değil; kontrollü ve dar alan Türkçesinde mümkün. Ölçü: kapsam, doğruluk, "bilmiyorum" oranı, LLM'siz/LLM'li fark.


---

# EK A: karar1.md (bağlam, karar değil)

# AŞAMA 1 SONUCU: 25 sorun çözücünün ortak kararı
(Taslağın tamamı 25/25 kabul edildi: /tmp/claude-0/-home-claude/7a123f44-46da-584d-b1b4-e1c21d6119f0/scratchpad/cozumler.md — ayrıntılar orada. Önceki sistem tanımı: sistem.md, sınama bulguları: bulgular.md, aynı klasörde.)

## Oylama sonuçları
- O1 Kayıt vektörü: HRR/VSA — v = R[ilişki] + P_s⊛E[özne] + P_o⊛E[nesne], sabit d (~256), deterministik (24/25).
- O2 P2 için çekirdeğe giren kâhinsiz mekanizmalar: (i) ÖZ-TEPKİ / şema çelişkisi defteri (25/25) + (ii) MASKELİ YENİDEN TÜRETME / ikinci sinyal (24/25). (iv) ortam değişmezliği (11/25) bir sonraki aşamada ilk eklenecek; (iii) karşıt çiftler ve (v) ayırt edici müdahale sonraki aşama.
- O3 Uygunluk: çarpımsal, her terime ε tabanı (20/25):
  U_ana = Doğruluk × (ε + w(t)·Müdahale) × (ε + 1 − ÖzTepki) × (ε + GeriKazanım)
  U = λ(t)·Yoğun + (1−λ(t))·U_ana ; λ: 1→0.1 ; w: 0→1 (tek bir zaman çizelgesinde tanımlanır)
- O4 Sitokin: tetiklenen tüm hücreler yayar; niş taban kotası (~%10), frekansa bağlı rekabet (1/n), niş >%50 olursa o nişin sitokin kazancı sıfır (19/25). Niş payı bağımsız epizotlar üzerinden ölçülür.
- O5 Merak primi: YOK (15/25).

## Birleştirici omurga: DESTEK/ÇELİŞKİ DEFTERİ
Her (üçlü) kaydı: kök epitop kümesi, kökleri ayrık ispat sayısı (destek), şema çelişkisi sayısı, sorgu uzaklığı d. Küçük elle yazılmış ilişki şeması: ters/simetrik tablo, dışlayıcı çiftler, işlevsellik. Çelişki maskesi eşleşme maskesinin yanında sabit şekilli matris.

## Diğer uzlaşılar (özet)
- P1: tamsayı varlık kimliği; bağlama kimlik eşitliğiyle; vektör hiç öğrenilmez, üçlüden yeniden kurulur; gradyan yalnız ilişki/rol reseptörlerine.
- P3: yoğun alt sinyal = kısmi halka eşleşmesi + ara halka tutarlılığı + sorguya yakınlık (potansiyel tabanlı). SİNYAL GEÇERLİLİK KAPISI H1 başında (sınıf başına 40–60 zincir: doğru, yanlış-tutarlı, paralel kısa yollu, yarım, rastgele; Spearman ρ≥0.7, ICC≥0.8, yanlış-tutarlı doğrunun altında; öz-tepki sinyali de kapıda ölçülür). Kâhin yalnız burada ve kalibrasyonda.
- P4: işaret-ayrık J, ρ yalnız J⁺ ve döngülü bileşenlerde (SCC), birincil kazanç = eşleşme-sayısı eğimi, anti-windup, sitokin/Treg kısa ömürlü ve bütçeli, zaman ölçekleri sırayla açılır.
- P5: Treg kopyayı reddeder → deftere destek; plazma: kök kümelerine göre bileşenler, bileşen içi MAX, bileşenler arası noisy-OR; τ seçici risk (hata ≤%5) ile kalibre; durma: (yeni kayıt yok VE güven artışı<δ) VEYA SPRT VEYA beklenen kazanç<maliyet VEYA 8 tur; tabu listesi.
- P6: sorgu-yönlü R* (geriye ilişki erişilebilirliği); skor = güven×(1+alt-türev)×γ^d; R* dışı önce atılır; sorgu dışı yazma kotası; sabitleme ≤ kapasitenin yarısı; mezar taşı; 64 kalır, 128'e geçiş eşiği sayısal yazılır.
- P7: mutlak bellek kapısı (doğruluk≥a₀, müdahale≥m₀, net çelişki≤0; eşikler H1'de kalibre) + kaydırılmış doğrulama ve en kötü ortam (grup-DRO) zorunlu; sönümlü, geri alınabilir statü; açılabilir makro; eğitim üreteci her epizotta kural alt kümesi + ilişki adı permütasyonu + ad havuzu.
- P8 (sonraki aşama): APC top-m=3, aynı cümle kimliğinde dışlayıcı küme, güven taşıma, gürültülü üçlü aşaması (%10–30), eleme oranı ölçülür (eşik %40), belirsiz epitop → "bilmiyorum".

## Önceki bağlayıcı kararlar
Kâhin yalnız değerlendirme/kalibrasyon; yoğun sabit şekilli eşleşme motoru; sitokin+Treg ilk 4 haftada saplama, sonra sırayla açılır; 4 hafta daraltılmış kapsam (çekirdek + CLONALG + sinyal geçerlilik kapısı); tek kişi + tek GPU (24 GB), Python/PyTorch.


---

# EK B: dil.md (bağlam, karar değil)

# Dil katmanı: 50 uzman panelinin görevi

Bağlam (oku): sistem.md, karar1.md (aynı klasör: /tmp/claude-0/-home-claude/7a123f44-46da-584d-b1b4-e1c21d6119f0/scratchpad/). Çekirdek sistem üçlüler (özne, ilişki, nesne; tamsayı kimlik) üzerinde çalışan, bağışıklık esinli, kendini sınayan nedensellik-zinciri çıkarım motorudur. Dil şu an YOK: oyuncakta üçlüler verilir.

## Fikir sahibinin kuralları
- Fikri özgünlüğünde tut (havuz, bağışıklık hücreleri, DNA = nedensellik zinciri, klonal seçilim, sitokin, Treg, bellek, plazma hücresi). Yalnız gerçekten yanlış olan çıkarılır.
- Hız ve verimlilik çok önemli. Tek kişi + tek 24 GB GPU, Python/PyTorch. Prototip kodu YOK, kâğıt üzerinde değerlendirme.
- Kâhin (gizli kural/etiket) eğitime girmez.

## Dil katmanı sorunları
L1 GİRDİ: metin → epitop (vektör + üçlü). APC hatası zincirle üstel düşer (0.95^10≈0.60). Çoklu hipotez (top-3, dışlayıcı küme), "bilmiyorum" yolu.
L2 ÇIKTI: üçlü/ispat → doğal cümle. Plan→şablon→küçük model→geri ayrıştırma sadakat kapısı.
L3 AÇIK SÖZLÜK: varlık bağlama, eş gönderim (coreference), ilişki adı çeşitliliği (anne/ana/validem).
L4 TEK ÜÇLÜYÜ AŞAN DİL: olumsuzlama, belirsizlik, zaman, nicelik, çok cümleli bağlam.
L5 EĞİTİM SİNYALİ: ayrıştırıcı etiketsiz/zayıf etiketle nasıl öğrenir? Çıkarım döngüsünün uygunluğu ayrıştırıcıyı eğitebilir mi? (Kâhin yok.)
L6 FELSEFE UYUMU: dil katmanının kendisi de bağışıklık esinli olabilir mi (dil kalıpları = reseptör/DNA, klonal seçilim, bellek)? Yoksa hazır bileşen mi?
L7 VERİMLİLİK: 24 GB GPU, tek kişi; hesap ve veri bütçesi.
L8 DEĞERLENDİRME: CLUTRR, gürültülü üçlü aşaması, Türkçe gibi çekimli dil, ölçütler.

## Oylanacak noktalar
O1 Girdi ayrıştırıcı tipi: (a) küçük eğitilmiş etiketleyici/seq2seq (donmuş kodlayıcı üstünde) (b) bağışıklık esinli: dil kalıbı hücreleri (kalıp-DNA) donmuş kodlayıcı üstünde klonal seçilimle evrilir (c) melez: evrilen kalıplar + küçük model yedeği (d) hazır büyük LLM ayrıştırıcı
O2 Ayrıştırıcının eğitim sinyali: (a) küçük etiketli kümeyle denetimli (b) çıkarım döngüsünün tutarlılığı/geri kazanımı (zayıf, kâhinsiz) (c) kendi kendine eğitim + şema tutarlılığı (d) (b)+(c) üstüne az etiketli tohum
O3 Çıktı: (a) yalnız şablon (b) şablon + küçük model + geri ayrıştırma kapısı (c) hazır LLM (d) çıktı yok (yalnız etiket + gerekçe zinciri)
O4 Sıra: (a) CLUTRR gürültülü üçlü → CLUTRR metni → serbest dil (b) kontrollü doğal dil (CNL) önce (c) doğrudan serbest dil
O5 Dil katmanı özgünlüğü: (a) çekirdek felsefenin parçası (b) değiştirilebilir arayüz (eklenti), hazır parçalar serbest
O6 Türkçe (çekimli) için: (a) morfoloji ön işlemi (b) alt-sözcük kodlayıcı yeter (c) sonraya


---

# EK C: nihai.md (bağlam, karar değil)

# Nihai değerlendirme: fikrin en iyi hali (20 uzman)

Bağlam dosyaları (aynı klasör: /tmp/claude-0/-home-claude/7a123f44-46da-584d-b1b4-e1c21d6119f0/scratchpad/): sistem.md (çekirdek), karar1.md (sorun çözümleri), dil.md (dil katmanı sorunları). Dil katmanı kararı (50 uzman) aşağıda özetlidir.

## Fikir sahibinin kuralları
Fikri özgünlüğünde tut (havuz, bağışıklık hücreleri, DNA = nedensellik zinciri, döngü, klonal seçilim, sitokin, Treg, bellek, plazma hücresi); gerçekten yanlış olan çıkar. Hız ve verimlilik çok önemli. Tek kişi + tek 24 GB GPU, Python/PyTorch. Prototip kodu yok, kâğıt üzerinde değerlendirme. Kâhin (gizli kural/etiket) eğitime girmez.

## Fikrin şimdiki hali (özet)
- Çekirdek: üçlüler (tamsayı varlık kimliği, HRR/VSA vektör d~256) üzerinde, havuz + zincir-hücreler + klonal seçilim + müdahale testi + destek/çelişki defteri (öz-tepki, maskeli yeniden türetme) ile kural keşfeden, gerekçe veren, "bilmiyorum" diyebilen motor. Timus hunisi ile eğitim maliyeti düşürülür. Kapılı takvim H1–H4 (~4 hafta daraltılmış çekirdek; tam kapsam 6–7 hafta). H1 başında sinyal geçerlilik kapısı (yanlış-tutarlı zincir ayrımı).
- Dil katmanı (50 uzman oylamasıyla): melez ayrıştırıcı (evrilen dil kalıbı hücreleri + küçük model yedeği), her cümleden top-3 dışlayıcı aday + kalibre güven + "bilmiyorum", üçlüye kutup/kip/zaman alanı, ayrı eş gönderim modülü, şablon+küçük model+geri ayrıştırma kapısı çıktı; sıra: gürültülü üçlü → CLUTRR metni → serbest dil; Türkçe sonra (alt-sözcük taban, morfoloji ablasyon). Ana risk: ayrıştırıcı ile motorun birlikte tutarlı-yanlışa çökmesi.
- Önerilen eklemeler: tohum zincirler (germline): elle yazılmış küçük Türkçe/dil kalıbı kütüphanesi + kilitli "değer/ahlak" katmanı (sistem okur ama evrim değiştiremez); evrim açık alanda serbest.
- Bilinen sınırlar: serbest sohbet, geniş dünya bilgisi, akıcı üretim, uzun hafıza, güvenlik bu mimarinin kapsamı dışı. Verim rakamları hipotez: sorgu 10–100× az, eğitim 3–10× (CLUTRR'da 1.5–3×), veri 2–4×.
- Yakın akrabalar: XCS/LCS, yapay bağışıklık (CLONALG, idiotipik ağ), ∂ILP, NeuralLP, DreamCoder, blackboard/global workspace, nöro-sembolik, nedensel AI.

## Sorular (her uzman hepsine tek harf oy + kısa gerekçe verir)
Q1 Nihai konumlandırma: (a) üçlü/kontrollü metin üzerinde bağımsız akıl yürütme motoru (b) bir LLM'nin yanında doğrulayıcı/gerekçelendirici eşlikçi (hibrit) (c) sıfırdan genel sohbet AI (d) yalnız araştırma çıktısı (makale/kanıt)
Q2 Tohum zincirler: (a) evet, dil kalıbı tohumu + kilitli değer katmanı (b) yalnız dil tohumu, değer katmanı yok (c) hiç tohum yok, sıfırdan keşif
Q3 İlk kanıtlanacak tek çekirdek iddia: (a) uzun zincir genellemesi (k=4–10) (b) kâhinsiz sinyalle yanlış-tutarlı zincir ayrımı (H1 kapısı) (c) eğitim/veri verimliliği (d) gerekçe/sadakat
Q4 Bileşen kesimi (özgünlük kuralı içinde): (a) hepsi kalsın, sırayla açılsın (b) sitokin ve Treg ablasyonla kanıtlanamazsa çıkar, geri kalan kalsın (c) çekirdeği en aza indir (havuz+zincir+klonal seçilim+defter), diğerleri sonra
Q5 Dur/devam ölçütü: H1 kapısı geçilmezse ne olsun? (a) dur, sinyali yeniden tasarla (b) fikri daralt (c) devam et
Q6 En gerçekçi sonuç dağılımı: iyi/orta/kötü senaryo yüzdeleri (toplam 100).

Ayrıca: (1) fikrin gerçekten YENİ olan kısmı nedir, yeniden keşif olan kısmı nedir (kısa, somut), (2) fikrin en uygun girdiği 2–3 alan/literatür, (3) kesin tek en büyük risk ve önlemi.


---

# EK D: besleme.md (bağlam, karar değil)

# Besleme sorunu: en basit, en zahmetsiz çözüm (50 uzman)

Bağlam: nihai.md, sistem.md, karar1.md, dil.md (aynı klasör: /tmp/claude-0/-home-claude/7a123f44-46da-584d-b1b4-e1c21d6119f0/scratchpad/). Sistem: üçlüler (özne, ilişki, nesne) üzerinde kural/zincir keşfeden, gerekçe veren, "bilmiyorum" diyen bağışıklık esinli motor. Kâhin (gizli doğru cevap) eğitime girmez. Tek kişi (programcı DEĞİL; kodu bir AI yazacak/çalıştıracak), tek 24 GB GPU.

## Sorun (kullanıcının kaygısı)
"Sistemi eğitmek, yani beslemek zor olacak." Sistem ham metin yutmaz; yapılandırılmış üçlü, şema (ters/simetrik/dışlayıcı ilişkiler), küçük etiketli tohum (~100–200), çeşitlilik ve ayrı kalibrasyon kümesi ister. Kullanıcı bunu EN BASİT, EN ZAHMETSİZ yoldan çözmek istiyor. İnternetten kendi araştıran sistem fikri ve Türkçe sözlük PDF'leri de gündemde (sözlükten akrabalık/kavram tanımı, eşanlamlı, ters-simetrik çift çıkarılabilir; telif, dairesel tanım, kâhin sızıntısı riskleri var).

## Sorular (her uzman tek harf oy + kısa gerekçe)
B1 Ana besleme kaynağı (ilk 4 hafta): (a) yalnız sentetik üreteçler (b) hazır yapılandırılmış bilgi tabanları (Wikidata, ConceptNet, KeNet/WordNet, Vikipedi) (c) LLM yardımlı çıkarım + insan örnek denetimi (d) kullanıcının sohbet/form ile öğretmesi (e) ham web taraması
B2 Şemayı kim yazar: (a) elle küçük şema (~20–30 ilişki) (b) LLM taslak + insan onayı (c) otomatik türetme (sözlük/KeNet'ten) 
B3 Tohum etiket: (a) ~100–200 elle, aktif öğrenmeyle seçilmiş (b) LLM öğretmen, süzgeçli (c) hiç
B4 Hedef otomasyon: (a) tek komutlu hat, kullanıcı haftada <30 dk (b) yarı otomatik, kullanıcı onay verir (c) tam özerk
B5 Sözlük PDF'leri: (a) tohum zincir ve eşanlamlı kaynağı olarak kullan (b) kullanma, açık lisanslı kaynaklara (KeNet, Wikidata, UD) git (c) ikisi birden
B6 İnternetten kendi araştırma: (a) ilk aşamada hayır (b) yalnız güvenilir yapılandırılmış kaynaklardan (c) seçili sitelerden öneri olarak (insan onaylı) (d) serbest

Ayrıca: (1) kullanıcı için en az zahmetli TEK somut yol (3 cümle), (2) kullanıcının haftalık yapacağı işin dakikası ve içeriği, (3) en büyük tuzak ve önlemi.


---

# EK E: llm.md (bağlam, karar değil)

# Hazır LLM kullanmanın etkileri (20 uzman)

Bağlam: nihai.md, sistem.md, dil.md, besleme.md (aynı klasör). Sistem: bağışıklık esinli, üçlüler (özne, ilişki, nesne) üzerinde kural/nedensellik zinciri keşfeden, gerekçe veren, "bilmiyorum" diyen motor. Kâhin (gizli doğru cevap) eğitime girmez. Tek kişi (programcı değil, kodu AI yazar), tek 24 GB GPU. Kullanıcının hedefi: SERBEST TÜRKÇE konuşan ama düşünmesi bu sistemden gelen bir AI.

## Önerilen hibrit
Hazır bir LLM (a) serbest Türkçe metni üçlü adaylarına çevirir (girdi), (b) motorun ürettiği ispatı/cevabı akıcı Türkçeye çevirir (çıktı). Motor akıl yürütür, defter/müdahale testi/bellek geçidi ile doğrular, "bilmiyorum" der. Geri ayrıştırma kapısı çıktıyı denetler.

## Sorular (tek harf oy + kısa gerekçe)
H1 Bu hibrit sistemin özgünlüğünü ve değerini korur mu? (a) evet, çekirdek hâlâ özgün (b) kısmen, LLM işin çoğunu yapar (c) hayır, sistem LLM'in süsü olur
H2 En büyük yeni risk: (a) LLM ayrıştırma hataları motora girer (b) LLM'in önyargı/halüsinasyonu kalibrasyonu kirletir (c) LLM çıktısı gerekçeyi bozar/uydurur (d) bağımlılık/maliyet/lisans
H3 LLM'i hangi rolde kullanmak: (a) yalnız girdi ayrıştırıcı (b) yalnız çıktı sözcüleştirici (c) ikisi de (d) ikisi + tohum etiket/şema taslağı
H4 LLM türü: (a) küçük açık model yerelde (24 GB) (b) büyük API modeli (c) ikisi, yerel ana API yedek
H5 Güven/doğrulama: LLM çıktısı motorda nasıl ele alınsın? (a) aday, top-3 + kalibre güven + kaynak cümle (b) doğrudan gerçek (c) yalnız insan onaylıysa
H6 Bu hibrit ilk kanıtlanacak iddiayı (kâhinsiz sinyal) bozar mı? (a) hayır (b) evet, ayrı ölçülmeli (c) bilinmez

Ayrıca: (1) kullanıcıya iki cümlelik "ne kazanır, ne kaybeder", (2) en büyük tuzak ve önlemi (≤ 2 cümle).


---

# EK F: katilik.md (bağlam, karar değil)

# Çekirdeğin LLM'den katı yalıtımı (10 gözetçi profesör)

Bağlam: nihai.md, sistem.md, dil.md, llm.md (aynı klasör). Çekirdek: bağışıklık esinli, üçlüler (özne, ilişki, nesne; tamsayı kimlik) üzerinde kural/nedensellik zinciri keşfeden, defter + müdahale testi + bellek geçidi ile doğrulayan, gerekçe veren, "bilmiyorum" diyen motor. Kâhin eğitime girmez. Tek kişi (programcı değil), tek 24 GB GPU.

Önceki panel (20 uzman) hibrit önerdi: LLM serbest Türkçe girdiyi üçlü ADAYLARINA çevirir, motorun ispatını Türkçeye anlatır. Uzmanlar riskleri sıraladı: sessiz ayrıştırma hatası, LLM ön bilgisinin sinyale sızması, sözcüleştiricinin ispatta olmayanı eklemesi.

## Kullanıcının talebi
"Çekirdek sistem sahip olduğu tüm özelliklere öyle kesin sahip çıkmalıdır ki LLM ile karışmamalıdır." Yani çekirdek ile LLM arasında KATI, denetlenebilir bir sınır: çekirdeğin hiçbir kararı, öğrenmesi, belleği, güveni LLM içeriğinden etkilenmemeli; LLM yalnızca bir çevirmen/arayüz olmalı.

## Sorular (tek harf oy + kısa gerekçe)
K1 Bu kadar katı yalıtım mümkün mü? (a) evet, tam (b) büyük ölçüde, bazı sızıntı kanalları kalır (c) hayır, pratikte olmaz
K2 Hangi mekanizma en sağlam sınırı verir? (a) yalnız tipli/şemalı üçlü arayüzü (LLM metin değil yalnız doğrulanmış yapı üretir) (b) iki yönlü geri ayrıştırma/çift doğrulama kapıları (c) çekirdek LLM'siz, elle/kural yazılmış girdiyle ayrı eğitilir, LLM yalnız çıkarım zamanında (d) kriptografik/sürüm kilitli, salt okunur bellek ve imzalı kayıtlar
K3 Eğitim zamanı: LLM ürettiği üçlüler çekirdeğin ÖĞRENMESİNE (kural keşfi, bellek) girebilir mi? (a) hayır, asla (b) yalnız insan onaylı (c) evet, kalibre güvenle
K4 Kalan en tehlikeli sızıntı kanalı: (a) ayrıştırma hatası (b) LLM ön bilgisinin "gizli kâhin" olması (c) sözcüleştirici uydurması (d) kullanıcının LLM çıktısını gerçek sanması
K5 Bu katılık fikrin özgünlüğünü ve değerini artırır mı? (a) evet (b) nötr (c) azaltır
K6 Bedel (hız, kapsam, kullanılabilirlik): (a) küçük (b) orta (c) büyük

Ayrıca: (1) tek cümleyle "mümkün mü, hangi koşulda", (2) çekirdeğin LLM'den bağımsız olduğunu KANITLAMAK için tek somut test, (3) kalan en büyük açık ve önlemi.


---

# EK G: sifir.md (bağlam, karar değil)

# "Hâkim–tercüman" ve "sıfır rutin iş" önerisi (20 denetçi)

Bağlam (aynı klasör): sistem.md (bölüm 14–16 son kararlar), besleme.md, llm.md, katilik.md. Çekirdek: bağışıklık esinli, üçlü/zincir tabanlı, kâhinsiz kendini sınayan akıl yürütme motoru; "bilmiyorum" diyebilir. Kullanıcı programcı değil, tek kişi, tek 24 GB GPU; yorulmak ve rutin kontrol yapmak İSTEMİYOR.

## Öneri
1. Hâkim–tercüman: çekirdek (hâkim) yalnız kapalı, tipli, sürümlü bir iç forma (üçlü + kutup/kip/zaman + kaynak + güven) bakar. Yerel LLM (tercüman) serbest Türkçeyi bu forma aday olarak çevirir ve ispatı geri anlatır; çekirdek belleğine/defterine yazamaz. Dilin kendi bağışıklık-esinli değerlendirmesi vardır (kalıp hücreleri, parafraz tutarlılığı, geri çeviri, çoklu LLM uyuşması, şema kuralları).
2. Sıfır rutin iş: sistem kendi kendini denetler (çift çeviri, uyuşmazlıkta eleme, geri ayrıştırma, hata eşiğinde otomatik durma). Emin olamadığını kullanıcıya SORMAZ, "bilmiyorum" der ve atlar. Kullanıcıya yalnız ciddi sorunda tek satır haber verir. Başlangıç kalibrasyon/tohum etiketi insan yerine KeNet/Wikidata'dan otomatik türetilir. Bedel: daha çok "bilmiyorum", nadir gizli hata.

## Sorular (tek harf oy + kısa gerekçe)
S1 Bu çözüm LLM karışmasını gerçekten önler mi? (a) evet, yeterince (b) kısmen (c) hayır
S2 "Sıfır rutin iş" (insan denetimi yok) güvenli mi? (a) evet, "bilmiyorum" varsayılanıyla (b) ancak seyrek örnek denetimiyle (c) hayır, düzenli insan gerekir
S3 İnsan yerine KeNet/Wikidata'dan otomatik kalibrasyon: (a) yeterli (b) yeterli değil, bir kerelik küçük insan etiketi şart (c) tehlikeli
S4 Sistemin kendi kendini denetlemesi (kendi çıktısını kendi kurallarıyla) dairesel/birlikte-çökme riski taşır mı? (a) küçük (b) orta, önlem şart (c) büyük
S5 En çok hata çıkaracak bileşen: (a) tercüman/ayrıştırma (b) otomatik kalibrasyon (c) kendi kendine denetim (d) sessiz kayma (drift)
S6 Genel karar: (a) bu hâliyle ilerle (b) küçük değişiklikle ilerle (c) önemli değişiklik gerek (d) vazgeç

Ayrıca: (1) bir cümle: en kritik düzeltme, (2) "az iş" bedelini azaltmak için tek somut önlem.
