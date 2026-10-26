"""sistem.md §13; K-041 (ÖK-005 taslağı §13.4, §5 `ikiz|<dünya etiketi>|<aday kimliği>`), V-065: π-ikizi.

Ters-çift koruyan bijeksiyon = şema otomorfizmi: her r için {π(t) : t ∈ ters(r)} = ters(π(r)), simetrik, işlevsel ve
temel olma korunur. Bütün otomorfizmler geri izlemeyle sayılır (mevcut şemada 1536) ve şema sırasıyla sıralanır; π
tohumla bu listeden düzgün rastgele seçilir. İkiz dünyada her olgu (A, r, B) yerine (A, π(r), B), ikiz adayda bütün
halka ve sonuç adlarına π uygulanır.
"""
from degerlendirme import kural


def _imza(sema, temel, r):
    return sema.simetrik(r), sema.islevsel(r), r in temel, len(sema.ters(r))


def bijeksiyonlar(sema, temel):
    adlar, sonuc = tuple(sema.adlar), []

    def ara(i, pi, kullanilan):
        if i == len(adlar):
            if all({pi[t] for t in sema.ters(r)} == set(sema.ters(pi[r])) for r in adlar):
                sonuc.append(tuple(pi[r] for r in adlar))
            return
        r = adlar[i]
        for q in adlar:
            if q in kullanilan or _imza(sema, temel, q) != _imza(sema, temel, r):
                continue
            if all(pi[t] in sema.ters(q) for t in sema.ters(r) if t in pi):
                pi[r] = q
                ara(i + 1, pi, kullanilan | {q})
                del pi[r]

    ara(0, {}, frozenset())
    return [dict(zip(adlar, g)) for g in sorted(sonuc, key=lambda g: [adlar.index(q) for q in g])]


def sec(liste, rng):
    return liste[rng.randrange(len(liste))]


def dunyaya(pi, olgular):
    return tuple((a, pi[r], b) for a, r, b in olgular)


def kurala(pi, k):
    r, x, y = k.bas
    return kural.Kural([(pi[t], s, a) for t, s, a in k.halkalar], (pi[r], x, y), k.farkli)
