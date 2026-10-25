# A6 önerisi: bellek geçidi + iç dil (2026-10-24, onay bekliyor)

> **Not (2026-10-25):** Bu öneri K-035 ve K-036 ile karara bağlandı; geçidin kanıt kaynağı değişti (maskeli gözlem, çekirdek dışı doğruluk). Güncel tarif: `VARSAYIMLAR.md` V-054, V-057, V-058; gerçek DNA sonucu: `raporlar/A6_gosterim_v8.md`. Aşağısı tarihsel kayıttır.

Kayıtlar: V-054 (bellek geçidi), V-055 (iç dil), V-056 (bellek deposu). Kod `cekirdek/bellek_gecidi.py`, `cekirdek/bellek.py`, `cekirdek/ic_dil.py`. Testler `testler/test_a6_*.py`.

## Bellek geçidi

Aday kural yalnız veriyle sınanır; etiket ve kâhin yoktur. Her bölümde çekirdek bellekle ve bellek + adayla koşar.

**Kanıt:**
- **destek:** adayın türettiği üçlü gözlenmiş bir olguyla aynı, ve o olgu kendi türetmesinin dayanağı değil.
- **karşıtlık:** türetilen üçlü bir olguyla şema çelişkisinde.
- **çelişki:** türetilen üçlü bellekten türemiş bir kayıtla çelişiyor.
- **katkı:** yeni üçlü ya da daha erken türetme.
- **eşleşme:** adayın gövdesinin eşleştiği sayı.
- **müdahale:** müdahale testi puanı.

Ortam başına doğruluk = destek / (destek + karşıtlık). En kötü ortam esas alınır (kaydırılmış doğrulama).

**Karar sırası:**
1. Bellekte yapıca aynı kural varsa → gereksiz.
2. Her ortamda doğruluk < eşik → yanlış. Bir ortamda tutup en kötü ortamda tutmuyorsa → kısayol.
3. Çelişki varsa → çelişkili.
4. Hiç eşleşme yoksa → sınanamadı. Eşleşip katkı yapmıyorsa → gereksiz.
5. Bir ortam ölçülemediyse ya da müdahale kanıtı az ise → sınanamadı.
6. Müdahale puanı < eşik → kısayol. Hiçbiri değilse → kabul.

**Eşikler (öneri):** doğruluk 1,0; en az kanıt 3; müdahale 0,9.

**Testle gösterilenler (sentetik blorp dünyası):**
- Doğru üç kural sırayla kabul edildi.
- Reddedilenler:
  - yanlış sonuç; şemayla çelişen sonuç (ikisi: yanlış);
  - kısayol (yalnız kaydırılmış ortamda yakalanıyor; tek ortamla görünmüyor);
  - yapıca eşdeğer ve katkısız (ikisi: gereksiz);
  - bellekle çelişkili.
- Sınanamadı kalanlar: gözlenmeyen sonuç, hiç eşleşmeyen gövde, müdahale kanıtı olmayan bölümler.
- Kendi kendini doğrulayan türetme destek sayılmıyor. Bölüme konan sahte cevap alanı kararı değiştirmiyor (etiket okunmuyor).
- Bellek: sadece ekleme, hash zinciri, geri alma. Yeni veri kuralı yalanlayınca gözden geçirmede geri alınıyor.

**Gerçek DNA ölçümü (eski eğitim bölümleri, cevap okunmadı):**

| | Bellek boş | Bellek = öteki 169 DNA kuralı |
|---|---|---|
| 170 doğru kural | 170 sınanamadı | 122 sınanamadı, 48 gereksiz |
| 73 bozuk kural | 7 yanlış, 1 çelişkili, 65 sınanamadı | 62 yanlış, 8 çelişkili, 3 sınanamadı |

- Doğru hiçbir kural yanlış sayılmadı. Bellekle birlikte bozukların 70'i reddedildi.
- Ama doğru hiçbir kural kabul edilemedi: hepsinde destek 0.
- Nedeni veri: bölümlerdeki olgular seyrek ve yalnız 7 temel ilişkiden; kuralın sonucu hiç gözlenmiyor, türetilmiş ilişkiler (dede, amca, …) hiç olgu olarak geçmiyor.

## İç dil (sürüm 1)

- **Kayıt alanları:** özne, ilişki, nesne, kutup (olumlu/olumsuz), kip (kesin/olası), zaman (yok ya da sıra numarası), kaynak, güven, özet.
- **Denetim:** Onaylı şema ve biçim denetlenir; özet tutmazsa kayıt reddedilir.
- **Havuza giren:** yalnız olumlu + kesin + zamansız kayıt. Olumsuz, olası ve zamanlı kayıtların çekirdekteki anlamı karar bekliyor.
- **LLM kaynaklı kayıt:** karantinasız girmez (karantina A7'de).
