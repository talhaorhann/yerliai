"""sistem.md §10, §13; K-041 (ÖK-005 taslağı §2.2, §4 madde 7, 13, 20; §13.6), V-063: derece-koruyan yeniden bağlama,
boş dünya, şemadan okunabilir kural sınıfı ve boş-dünya sayacı.

Yeniden bağlama (bir ilişki r için): r olgularından (A, r, B) ve (C, r, D) tohumla seçilir, yerlerine (A, r, D) ve
(C, r, B) yazılır. Kendine bağ, var olan olgunun yinelenmesi ve aynı çiftte aynı dışlayıcı gruptan ikinci ilişki doğuran
takas reddedilir; r olgu sayısının `bagla_deneme_carpani` katı kadar denenir. Her kişinin r'deki giriş ve çıkış sayısı
korunur.
- Veto ikizi ve null: yalnız istenen ilişkiler yeniden bağlanır, tersleri yeniden yazılmaz.
- Boş dünya: her ters sınıfının ileri tarafındaki ilişkiler yeniden bağlanır, tersleri onlardan yeniden yazılır.
  - Ters olgunun adı, A'nın özgün dünyadaki ters adıdır; takas yalnız ters adları aynı iki olgu arasında yapılır. Böylece
    ters ilişkilerin dereceleri de korunur ve şema tutarlı kalır.
  - İleri taraf: sınıf iki yana ayrılıyorsa (r ile tersleri ayrı kümeler), sözlük sırasında ilk ilişkinin yanı; ayrılmıyorsa
    (kendi tersi olan sınıf) sınıfın tamamı.
"""

def _iliski_kumeleri(olgular):
    cift = {}
    for a, r, b in olgular:
        cift.setdefault((a, b), set()).add(r)
    return cift


def _cakisir(cift, a, b, r, sema, cikan):
    """(a, r, b) yazılırsa aynı çiftte aynı dışlayıcı gruptan başka ilişki ya da yineleme olur mu (çıkacaklar hariç)."""
    for diger in cift.get((a, b), ()):
        if (a, diger, b) in cikan:
            continue
        if diger == r or sema.dislayici_mi(diger, r):
            return True
    return False


def yeniden_bagla(olgular, iliskiler, sema, rng, tersleri_yaz, deneme_carpani):
    olgu = set(olgular)
    ters_adi = {}
    if tersleri_yaz:
        for a, r, b in olgu:
            for t in sema.ters(r):
                if (b, t, a) in olgu:
                    ters_adi[(a, r)] = t
    cift = _iliski_kumeleri(olgu)
    for r in [x for x in sema.adlar if x in iliskiler]:
        kenarlar = sorted((a, b) for a, rr, b in olgu if rr == r)
        for _ in range(deneme_carpani * len(kenarlar)):
            if len(kenarlar) < 2:  # V-063: takas için iki olgu gerekir
                break
            (a, b), (c, d) = rng.sample(kenarlar, 2)  # V-063: iki olgu
            if a == d or c == b or (tersleri_yaz and ters_adi[(a, r)] != ters_adi[(c, r)]):
                continue
            cikan = {(a, r, b), (c, r, d)}
            giren = [(a, r, d), (c, r, b)]
            if tersleri_yaz:
                t = ters_adi[(a, r)]
                cikan |= {(b, t, a), (d, t, c)}
                giren += [(d, t, a), (b, t, c)]
            if len(set(giren)) != len(giren) or any(_cakisir(cift, x, y, z, sema, cikan) for x, z, y in giren):
                continue
            for x, z, y in cikan:
                olgu.discard((x, z, y))
                cift[(x, y)].discard(z)
            for x, z, y in giren:
                olgu.add((x, z, y))
                cift.setdefault((x, y), set()).add(z)
            kenarlar = sorted((x, y) for x, rr, y in olgu if rr == r)
    return sorted(olgu)


def ters_siniflari(sema):
    siniflar, gorulen = [], set()
    for r in sema.adlar:
        if r in gorulen:
            continue
        sinif, yigin = {r}, [r]
        while yigin:
            for t in sema.ters(yigin.pop()):
                if t not in sinif:
                    sinif.add(t)
                    yigin.append(t)
        gorulen |= sinif
        siniflar.append(sinif)
    return siniflar


def ileri_taraflar(sema):
    """Boş dünyada yeniden bağlanacak ilişkiler (her sınıfın ileri tarafı)."""
    secilen = set()
    for sinif in ters_siniflari(sema):
        ilk = min(sinif)
        yan, yigin = {ilk}, [ilk]
        while yigin:  # ilk ilişkiyle aynı yanda olanlar: tersin tersi
            for t in sema.ters(yigin.pop()):
                for u in sema.ters(t):
                    if u not in yan:
                        yan.add(u)
                        yigin.append(u)
        ayrilir = not any(t in yan for r in yan for t in sema.ters(r))
        secilen |= yan if ayrilir else sinif
    return secilen


def bos_dunya(olgular, sema, rng, deneme_carpani):
    return yeniden_bagla(olgular, ileri_taraflar(sema), sema, rng, True, deneme_carpani)


def semadan_okunabilir_mi(aday, sema):
    """Tek halkalı ve gövdesi başın şemadaki tersi ya da simetriği olan kural (DNA v8'de 9 tane)."""
    if len(aday["halkalar"]) != 1:
        return False
    h, s = aday["halkalar"][0], aday["sonuc"]
    ters_yon = (h["sol"], h["sag"]) == (s["sag"], s["sol"])
    return ters_yon and (s["gen"] in sema.ters(h["gen"]) or (s["gen"] == h["gen"] and sema.simetrik(h["gen"])))


class BosDunyaSayaci:
    """Boş dünya koşularında, şemadan okunabilir sınıf dışında kabul olan koşuları sayar; tetik → arama donar."""

    def __init__(self, h2_ayar, sema):
        self.tetik = h2_ayar.deger("bos_dunya_tetik")
        self.sema = sema
        self.kosu = self.kabullu_kosu = 0

    def kaydet(self, kabul_edilenler):
        self.kosu += 1
        self.kabullu_kosu += any(not semadan_okunabilir_mi(a, self.sema) for a in kabul_edilenler)
        return self.kabullu_kosu >= self.tetik
