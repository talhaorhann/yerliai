"""sistem.md §3, §13; K-043 (ÖK-005 taslağı §7, §8, §13.2): genel kural değerlendiricisi.

Her değişken adıyla, `farkli` şartıyla ve OI ile (bütün gövde değişkenleri farklı kişi) çalışır; açık geri izlemedir.
Şablon adaylarında sembolik sayaçla birebir aynı tahmin kümesini verir (test). Kullanım yerleri: gizli ve görünür kırmızı
takım kuralları, geliştirme havuzu aşama 1–4, taze bölümler, çift kısıtlı kapanış ve B2 ölçümü.
- Tahmin kümesi: gövdenin X ile Y'ye bağladığı (A, B) çiftleri; her çift bir kez (tanık).
- `turetir_mi`: X = a, Y = b ile, `haric` olgular kullanılmadan ve `ek` olgular eklenerek bir bağlama var mı.
- Çift kısıtlı kapanış: tam gözlemli bir olgu kümesinde yalnız bir çiftin olguları maskeliyse, kapanışta değişebilecek
  olgular yalnız o çiftin olgularıdır; kurallar o çifte (iki yönde) tur sınırına kadar uygulanır (V-065).
- θ-kapsama: genel kuralın değişkenleri özel kuralınkilere, baş başa, her halka bir halkaya, her farklılık şartı bir
  farklılık şartına gidecek biçimde eşlenebiliyorsa genel kural özeli kapsar.
"""
import itertools


class Indeks:
    def __init__(self, olgular):
        self.olgu = frozenset(olgular)
        self.cikis, self.giris, self.iliski = {}, {}, {}
        for a, r, b in sorted(self.olgu, key=repr):
            self.cikis.setdefault((r, a), []).append(b)
            self.giris.setdefault((r, b), []).append(a)
            self.iliski.setdefault(r, []).append((a, b))


class Kural:
    def __init__(self, halkalar, bas, farkli, kimlik=None):
        self.halkalar = tuple(halkalar)
        self.bas = tuple(bas)
        self.farkli = frozenset(frozenset(c) for c in farkli)
        self.kimlik = kimlik
        self.degiskenler = tuple(sorted({d for _, s, a in self.halkalar for d in (s, a)}))

    @classmethod
    def kayittan(cls, kayit):
        halkalar = [(h["gen"], h["sol"], h["sag"]) for h in kayit["halkalar"]]
        s = kayit["sonuc"]
        degisken = sorted({d for _, a, b in halkalar for d in (a, b)})
        farkli = itertools.combinations(degisken, 2) if kayit["oi"] else kayit["farkli"]  # K-041: OI = bütün çiftler
        return cls(halkalar, (s["gen"], s["sol"], s["sag"]), farkli, kayit.get("kimlik"))

    @property
    def ters_dayanakli(self):
        """Gövdede baş çiftini (X ile Y'yi) doğrudan bağlayan halka var mı (ÖK-005 taslağı §7)."""
        _, x, y = self.bas
        return any({s, a} == {x, y} for _, s, a in self.halkalar)

    def _uyar(self, bag):
        return all(len({bag[u] for u in c}) == len(c) for c in self.farkli if all(u in bag for u in c))

    def baglamalar(self, idx, bag=None, haric=frozenset(), ek=frozenset()):
        ek_cikis, ek_giris = {}, {}
        for a, r, b in ek:
            ek_cikis.setdefault((r, a), []).append(b)
            ek_giris.setdefault((r, b), []).append(a)
        yield from self._ara(idx, dict(bag or {}), frozenset(range(len(self.halkalar))), haric, ek, ek_cikis, ek_giris)

    def _ara(self, idx, bag, kalan, haric, ek, ek_cikis, ek_giris):
        if not self._uyar(bag):
            return
        if not kalan:
            yield bag
            return
        i = max(kalan, key=lambda j: (sum(v in bag for v in self.halkalar[j][1:]), -j))
        r, s, a = self.halkalar[i]
        kalan = kalan - {i}
        if s in bag and a in bag:
            f = (bag[s], r, bag[a])
            if (f in idx.olgu and f not in haric) or f in ek:
                yield from self._ara(idx, bag, kalan, haric, ek, ek_cikis, ek_giris)
            return
        if s in bag:
            adaylar = [(bag[s], q) for q in idx.cikis.get((r, bag[s]), []) + ek_cikis.get((r, bag[s]), [])]
        elif a in bag:
            adaylar = [(p, bag[a]) for p in idx.giris.get((r, bag[a]), []) + ek_giris.get((r, bag[a]), [])]
        else:
            adaylar = idx.iliski.get(r, []) + [(p, q) for p, rr, q in ek if rr == r]
        for p, q in adaylar:
            if (p, r, q) in haric or (s == a and p != q):
                continue
            yield from self._ara(idx, {**bag, s: p, a: q}, kalan, haric, ek, ek_cikis, ek_giris)

    def tahminler(self, idx, haric=frozenset(), ek=frozenset()):
        _, x, y = self.bas
        return {(b[x], b[y]) for b in self.baglamalar(idx, None, haric, ek)}

    def turetir_mi(self, idx, a, b, haric=frozenset(), ek=frozenset()):
        _, x, y = self.bas
        if x == y or (a == b and frozenset((x, y)) in self.farkli):
            return False
        return next(self.baglamalar(idx, {x: a, y: b}, haric, ek), None) is not None


def cift_kapanisi(kurallar, idx, a, b, tur_siniri, haric=frozenset(), maske=None):
    """{a, b} çiftine kuralların tur sınırına kadar türettiği, görünür olmayan olgular (V-065). `maske(kural)` verilirse
    her kural kendi maskesini görmez (ör. yalnız ters-dayanaklı olmayanlar tersleri görmez); verilmezse hepsi `haric`."""
    turetilen = set()
    for _ in range(tur_siniri):
        yeni = set()
        for k in kurallar:
            h = haric if maske is None else maske(k)
            for p, q in ((a, b), (b, a)):
                f = (p, k.bas[0], q)
                gorunur = (f in idx.olgu and f not in h) or f in turetilen
                if not gorunur and f not in yeni and k.turetir_mi(idx, p, q, h, frozenset(turetilen)):
                    yeni.add(f)
        if not yeni:
            break
        turetilen |= yeni
    return turetilen


def kapsar_mi(genel, ozel):
    """θ-kapsama: genel kural özel kuralı kapsıyor mu (ÖK-005 taslağı §8, "daha genel")."""
    if genel.bas[0] != ozel.bas[0]:
        return False
    (_, gx, gy), (_, ox, oy) = genel.bas, ozel.bas
    sabit = {gx: ox, gy: oy}
    if gx == gy and ox != oy:
        return False
    serbest = [v for v in genel.degiskenler if v not in sabit]
    ozel_halka, ozel_farkli = set(ozel.halkalar), ozel.farkli
    for secim in itertools.product(ozel.degiskenler, repeat=len(serbest)):
        theta = {**sabit, **dict(zip(serbest, secim))}
        if not all((r, theta[s], theta[a]) in ozel_halka for r, s, a in genel.halkalar):
            continue
        if all(frozenset(theta[u] for u in c) in ozel_farkli for c in genel.farkli):
            return True
    return False
