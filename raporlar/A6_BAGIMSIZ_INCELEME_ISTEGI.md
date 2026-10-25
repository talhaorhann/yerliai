# A6 sonu bağımsız inceleme isteği (hazır metin)

KODLAMA_PROMPTU §4 "Bağımsız inceleme" kuralı: bu metni yazan oturumdan bağımsız yeni bir oturuma (mümkünse farklı bir modele) olduğu gibi verin. İnceleyen yalnız şartname, kod ve testlere bakar; konuşma geçmişi verilmez.

---

**Görev.** `asama-6` dalındaki depoyu incele. Yalnız `sistem.md`, `KODLAMA_PROMPTU.md`, `KARARLAR.md`, `VARSAYIMLAR.md`, kod ve testleri kullan. Aşağıdaki her madde için KARŞILANDI / KARŞILANMADI / ŞARTNAMEDE YOK yaz ve `dosya:satır` kanıtı ver. Emin olmadığın yerde "emin değilim" de; tahminle doldurma.

**Kurallar.**
- `degerlendirme/altin/` altındaki cevap dosyalarını açma (kâhin kayıtları).
- Kodu değiştirme. Kasıtlı hata denemelerini depo kopyasında yap (`araclar/mutasyon_a0.py` içindeki `kopyada_kostur` bunu yapar).
- Testler: `.venv/bin/python araclar/kostur.py` (kurulum `sh kur.sh`).

**İncelenecek maddeler.**
1. sistem.md §8: bellek hücresi yalnız müdahale testi ve karşı-kısayol testlerinden geçince kabul ediliyor mu? (`cekirdek/bellek_gecidi.py` `karar_ver`, `degerlendirme/bellek_hatti.py`)
2. EK A P7: mutlak bellek kapısı (doğruluk ≥ eşik, müdahale ≥ eşik, net çelişki ≤ 0), kaydırılmış doğrulama ve en kötü ortam (grup-DRO) zorunlu mu? Statü geri alınabilir mi (`gozden_gecir`, `cekirdek/bellek.py` geri alma olayı)?
3. sistem.md §18 ve K-035: kabul/ret yalnız çekirdeğin kendi kurallarıyla mı? Geçit etiket ya da kâhin kullanıyor mu? Kuralın tahmin ettiği gözlem maskeleniyor mu (çekirdeğe hiç verilmiyor mu)? Doğruluk hesabı çekirdek dışında mı (`degerlendirme/gozlem_puani.py`) ve kâhin modüllerini (üreteç, dünya, altın küme) içe aktarıyor mu?
4. sistem.md §16: bağımsızlık testi var mı ve anlatıcısız, sahte (rastgele) ve başka anlatıcıyla kararlar, bellek baytları ve sürüm bit düzeyinde aynı mı? Anlatıcı belleğe ya da karara yazabiliyor mu? (`testler/test_a6_bellek_hatti.py`)
5. sistem.md §15: bellek salt okunur ve sürüm kilitli mi (hash zinciri, kurcalanmış dosya açılmıyor mu)? LLM kaynaklı kayıt karantinasız havuza girebiliyor mu (`cekirdek/ic_dil.py`)?
6. sistem.md §17: iç form kapalı, tipli, sürümlü mü (`sema/ic_dil_v1.schema.json`, özet denetimi)?
7. K-032 §4: H2 komutu V-053 kapanmadan ve H1 taze tohumlarla yeniden koşulmadan "V-053 açık" diye reddediyor mu? Kapıyı gevşeten bir yol var mı? (`degerlendirme/h2.py`)
8. K-034: V-053 çıkarılabilirlik tanımı (yalnız olgular + üç dünya varsayımı) kodda doğru mu, kaba kuvvetle denetleniyor mu? (`degerlendirme/dunya.py`, `testler/test_a6_olgudan_cikarilabilirlik.py`)
9. K-036: eşikler (doğruluk 1,0; en az 3 kanıt; müdahale 0,9) config'ten mi geliyor, kodda gevşetilmiş bir yer var mı?
10. KODLAMA_PROMPTU §2 (dil veridir, sihirli sayı, kâhin yalıtımı) ve §6 (mutasyon): A6 kodunda ihlal var mı?
11. Açık varsayımlar V-057 ve V-058: kodda tarif edildiği gibi mi uygulanmış? V-058'de onaylı formül (a·b·c) mi kullanılıyor, b·c yalnız raporda mı?

**Kasıtlı hata denemesi.** En az 5 kendi seçtiğin kasıtlı hatayı A6 koduna (yukarıdaki dosyalara) tek tek sok ve test takımının yakalayıp yakalamadığını yaz. `araclar/mutasyon_a6.py` listesindekileri tekrarlama.

**Çıktı biçimi.** Her madde: numara, karar, kanıt (`dosya:satır`), bir cümle gerekçe. Sonda: yakalanmayan kasıtlı hatalar ve önerilen en fazla 5 düzeltme.
