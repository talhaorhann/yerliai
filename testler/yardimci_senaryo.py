"""K-015, V-042: çekirdek döngüsü için sabit senaryolar; kod kitabı (referans ya da hızlı) parametre olarak verilir.

Senaryolar döngünün bütün dallarını çalıştırır: hücre sınırı ve bütçe atmaları, havuzdan atma, impasse ve eşik
düşürme, çelişki, müdahale testi. Yalnız A4'te var olan API'ler kullanılır; böylece aynı senaryo bağlamadan önceki
kodda da koşturulup sonucu altın değer olarak saklanabilir. İlişki adları anlamsızdır (blorp şeması).
"""
import dataclasses
import hashlib
import random

from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.defter import Defter
from cekirdek.dna import dna_kur
from cekirdek.dongu import CekirdekParametreleri, calistir
from cekirdek.havuz import Havuz
from cekirdek.mudahale import mudahale_testi
from testler.test_a3_temel import DNA_BICIMI, dna_verisi, halka, hucre
from testler.yardimci import KOK

AYAR = ayar_yukle(KOK / "config.json")
PRM = CekirdekParametreleri.ayardan(AYAR)
DUNYA = [(1, "blorp", 2, 1.0), (2, "blorp", 3, 1.0), (3, "zindle", 4, 1.0), (7, "frumb", 8, 1.0)]


@dataclasses.dataclass(frozen=True)
class Ozet:
    sonuc: tuple
    satirlar: tuple
    vektorler: tuple
    mudahale: tuple

    def altin(self):
        """Bağlamadan önceki kodla karşılaştırılan kısa iz: olay sayısı, son zincir özeti, vektörlerin özeti."""
        return (len(self.satirlar), self.satirlar[-1]["ozet"] if self.satirlar else None,
                hashlib.sha256(kanonik_json([list(v) for v in self.vektorler])).hexdigest())


def _defter():
    return Defter(None, AYAR.deger("hash_algoritmasi"), AYAR.deger("olay_sema_surumu"), AYAR.deger("kaynaklar"))


def _kos(kk, sema, olgular, dna, prm, sorgu, mudahale=False):
    hucreler = dna_kur(dna_verisi(*dna), DNA_BICIMI, sema)
    h = Havuz(prm.kapasite, kk)
    for s, r, o, g in olgular:
        h.epitop_ekle(s, r, o, guven=g)
    d = _defter()
    sonuc = calistir(hucreler, h, kk, prm, d, iliski_semasi=sema, sorgu=sorgu)
    m = mudahale_testi(h, d, hucreler, olgular, kk, prm, sema, sorgu) if mudahale else None
    return Ozet(dataclasses.astuple(sonuc), tuple(d.kayitlar()), tuple(k.vektor for k in h.kayitlar()),
                dataclasses.astuple(m) if m else ())


def _kalabalik(kk, sema):
    rng = random.Random(7)
    adlar = sema.adlar
    olgular = [(rng.randrange(5), rng.choice(adlar), rng.randrange(5), rng.choice((1.0, 0.9, 0.7)))
               for _ in range(16)]
    dna = []
    for i in range(6):
        a, b, c = (rng.choice(adlar) for _ in range(3))
        dna.append(hucre(f"h{i}", [halka(a, "X", "Y"), halka(b, "Y", "Z")], (c, "X", "Z"),
                         guvenilirlik=rng.choice((1.0, 0.9))))
    a, b, c, e = (rng.choice(adlar) for _ in range(4))
    dna.append(hucre("h_uc", [halka(a, "X", "Y"), halka(b, "Y", "Z"), halka(c, "Z", "W")], (e, "X", "W")))
    prm = dataclasses.replace(PRM, kapasite=24, hucre_yazma_siniri=3, butce=6, tur_siniri=5)
    return _kos(kk, sema, olgular, dna, prm, sorgu=None)


def _impasse(kk, sema, sorgu):
    dna = [hucre("h_bb", [halka("blorp", "X", "Y", 1.0), halka("blorp", "Y", "Z", 1.0)], ("quax", "X", "Z")),
           hucre("h_qz", [halka("quax", "X", "Y", 1.0), halka("zindle", "Y", "Z", 1.0)], ("vonk", "X", "Z"))]
    return _kos(kk, sema, DUNYA, dna, PRM, sorgu)


def _celiski_mudahale(kk, sema):
    olgular = DUNYA + [(1, "blorp", 5, 0.9), (9, "vonk", 6, 1.0), (4, "quax", 1, 0.8)]
    dna = [hucre("h_bb", [halka("blorp", "X", "Y"), halka("blorp", "Y", "Z")], ("quax", "X", "Z")),
           hucre("h_qz", [halka("quax", "X", "Y"), halka("zindle", "Y", "Z")], ("vonk", "X", "Z"), guvenilirlik=0.9),
           hucre("h_ters", [halka("vonk", "X", "Y")], ("zindle", "Y", "X"))]
    return _kos(kk, sema, olgular, dna, PRM, sorgu=(1, 4), mudahale=True)


def senaryolar(kk, sema):
    return {"kalabalik": _kalabalik(kk, sema), "impasse_cevapli": _impasse(kk, sema, (1, 4)),
            "impasse_cevapsiz": _impasse(kk, sema, (1, 8)), "celiski_mudahale": _celiski_mudahale(kk, sema)}
