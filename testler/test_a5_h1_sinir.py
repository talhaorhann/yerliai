"""K-029, ÖK-003 §3.4, V-049: tur ve havuz sınırlarının geliştirme verisinde, önceden belirlenen kuralla seçimi.

Kural: önce en büyük havuzda, doğru sayısı en büyük turdakine eşit olan en küçük tur; sonra o turla, doğru sayısı
en büyük havuzdakine eşit olan en küçük havuz. Ölçüm yalnız çekirdek + plazmadır (müdahale yok).
İlişki adları anlamsızdır (blorp şeması).
"""
from pathlib import Path

from cekirdek.vektor_hizli import HizliKodKitabi
from degerlendirme import h1_sinir
from testler.test_a3_temel import halka, hucre
from testler.test_a5_h1 import GUNLUK, bolum, cevap, klasor_yaz
import testler.test_a3_cekirdek as t3

KK = HizliKodKitabi(t3.AYAR.deger("vektor_tohum"), t3.AYAR.deger("vektor_boyutu"))
BB = hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z"))
QZ = hucre("h_qz", [halka("quax", "X", "Y"), halka("zindle", "Y", "Z")], ("vonk", "X", "Z"))


class SecimKuraliTesti(t3.Ortam):
    def test_kural_harfiyen(self):
        tablo = {(8, 1024): 90, (12, 1024): 95, (16, 1024): 97, (32, 1024): 97,
                 (16, 128): 96, (16, 256): 97, (16, 512): 97}
        olculen = []

        def olc(tur, havuz):
            olculen.append((tur, havuz))
            return tablo[(tur, havuz)]

        secim = h1_sinir.sec(olc, [8, 12, 16, 24, 32], [128, 256, 512, 1024])
        self.assertEqual((secim["tur"], secim["havuz"]), (16, 256))
        self.assertEqual(secim["olcum"][(32, 1024)], 97)
        self.assertNotIn((24, 1024), olculen)  # gerekenden fazla ölçülmez
        self.assertEqual(len(olculen), len(set(olculen)))  # aynı ölçüm iki kez yapılmaz

    def test_kucuk_deger_daha_cok_dogru_verse_de_esitlik_aranir(self):
        """Ön kayıt "eşit" der; tekdüze olmayan durum seçilmez ama tabloda görünür."""
        tablo = {(8, 64): 10, (16, 64): 9, (16, 16): 9}
        secim = h1_sinir.sec(lambda t, h: tablo[(t, h)], [8, 16], [16, 32, 64])
        self.assertEqual((secim["tur"], secim["havuz"]), (16, 16))
        self.assertEqual(secim["olcum"][(8, 64)], 10)

    def test_gercek_olcum_tur_siniri(self):
        b = bolum([(1, "blorp", 2), (2, "blorp", 3), (3, "zindle", 4)], (1, 4))
        k = klasor_yaz(Path(self._d.name) / "veri", 7, {("uzunluk", "ana"): [(b, cevap(b, "uzunluk", "vonk"))]})
        hucreler = self.hucreler(BB, QZ)

        def olc(tur, havuz):
            prm = h1_sinir.sinirli(t3.PRM, tur, havuz)
            return h1_sinir.dogru_sayisi(k.parent, [7], ["uzunluk"], hucreler, self.sema, KK, prm, GUNLUK)

        self.assertEqual(olc(1, 64), 0)
        self.assertEqual(olc(2, 64), 1)
        secim = h1_sinir.sec(olc, [1, 2, 4], [8, 64])
        self.assertEqual((secim["tur"], secim["havuz"]), (2, 8))
