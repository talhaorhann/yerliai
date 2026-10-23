# ÖN KAYIT

Hipotez, metrik, eşik ve bölmeler veriye bakmadan buraya yazılır ve hash'lenir (KODLAMA_PROMPTU §5 İstatistik). H1 ön kaydı A5 öncesinde yazılacak.

## ÖK-001 (2026-10-23): Altın küme bağımsızlık kısıtı (K-013)

1. **Kaynak:** Altın küme 1. parçanın (50 soru) cevapları LLM ön cevabıdır, kullanıcı gözden geçirip kabul etmiştir. Bağımsız insan cevabı DEĞİLDİR. Kayıt dosyası: `degerlendirme/altin/kullanici_cevaplari_1.json` (sha256 `306ee0a0c54d3d6972695ae8a0c8c14e8dff12e2d6ef084884a9fd345a5c45ff`).
2. **Raporlama:** Altın kümeyle ölçülen her sonuç, 1. parça için "LLM ön cevaplı, kullanıcı onaylı" etiketiyle ayrı satırda raporlanır. 2. parçanın kaynağı ayrıca kaydedilir.
3. **Uyuşma kanıt değildir:**
   - 1. parça cevaplarının 50'si de üreteçle uyuştu.
   - Bu uyuşma gizli tanımların (V-019) doğruluğuna bağımsız kanıt sayılmaz. Tanımlar da bir LLM taslağıdır, ortak yanılgı riski vardır (sistem.md §17: "Çoklu LLM uyuşması doğruluk kanıtı sayılmaz").
4. **Dünya varsayımları:**
   - Cevaplarda iki varsayım kullanıldı: kardeşler aynı anne babanın çocuğudur; çocuğun iki ebeveyni birbirinin eşidir.
   - Bunlar üretecin dünya kurallarıyla (V-017) aynıdır. Etkilenen sorular: 3, 4, 5, 9, 10, 13, 17, 24, 27, 37, 39, 41, 46, 47.
   - Bu sorulardaki başarı, yalnız bu dünya varsayımları altında anlamlıdır.
5. **Kalibrasyon sınırı:**
   - sistem.md §15/§17 ve KODLAMA_PROMPTU §5'e göre LLM etiketi kalibrasyona (τ, T, θ seçimi) giremez.
   - Bu yüzden 1. parça, kullanıcı ayrıca karar vermedikçe yalnız değerlendirme ve otomatik durdurma ölçümünde, yukarıdaki etiketle kullanılır. Kalibrasyonda kullanılmaz.
