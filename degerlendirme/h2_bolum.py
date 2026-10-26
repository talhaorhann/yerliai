"""sistem.md §10, §13; K-041, K-043 (ÖK-005 taslağı §2.1 gövde-merkezli bölüm, §5 tohumlar), V-065: aşama 5 bölümleri.

Gövde-merkezli bölüm: adayın gövdesinin dünyadaki eşleşmelerinden tohumla biri seçilir; o kişilerden birinden temel
ilişkilerle 2–3 adımlık, kişi tekrarlamayan bir yürüyüş ve uçlarından en az biri seçilenlerin dışında kalan dikkat
dağıtıcı temel bağlar eklenir. Bölüm, seçilen kişiler arasındaki bütün olguları içerir (kapalı dünya). Kişi kimlikleri
dünyanın kişi sayısı aralığından tohumla karıştırılır; olguların sırası da karıştırılır. Maskeleme geçitte yapılır.
"""
import dataclasses

from cekirdek.altyapi.kanonik import kanonik_json, ozet
from degerlendirme import kural

ALGORITMA = "sha256"  # V-007


@dataclasses.dataclass(frozen=True)
class Bolum:
    etiket: str
    olgular: tuple  # (a, r, b), karıştırılmış kimliklerle
    esleme: dict  # dünya kişisi → bölüm kimliği
    ozet: str


def bolum_ozeti(olgular):
    return ozet(kanonik_json(sorted([list(o) for o in olgular])), ALGORITMA)


def _temel_komsular(olgular, temel):
    komsu = {}
    for a, r, b in olgular:
        if r in temel:
            komsu.setdefault(a, set()).add(b)
    return komsu


def bolum_kur(dunya, secili, rng, etiket):
    kisiler = sorted(secili)
    hedef = rng.sample(sorted(dunya.kisiler), len(kisiler))
    esleme = dict(zip(kisiler, hedef))
    olgular = [(esleme[a], r, esleme[b]) for a, r, b in dunya.olgular if a in esleme and b in esleme]
    olgular.sort()
    rng.shuffle(olgular)
    return Bolum(etiket, tuple(olgular), esleme, bolum_ozeti(olgular))


def govde_merkezli(dunya, aday, temel, rng, adim_araligi, dikkat_sayisi, etiket, idx=None):
    """Gövde eşleşmesi yoksa None (bu dünyadan kanıt yok)."""
    idx = idx or kural.Indeks(dunya.olgular)
    eslesmeler = sorted(tuple(sorted(b.items())) for b in aday.baglamalar(idx))
    if not eslesmeler:
        return None
    secili = {p for _, p in rng.choice(eslesmeler)}
    komsu = _temel_komsular(dunya.olgular, temel)
    yol = [rng.choice(sorted(secili))]
    for _ in range(rng.randint(*adim_araligi)):
        secenek = sorted(komsu.get(yol[-1], set()) - set(yol))
        if not secenek:
            break
        yol.append(rng.choice(secenek))
    secili |= set(yol)
    bag_adaylari = sorted({tuple(sorted((a, b))) for a, r, b in dunya.olgular if r in temel
                           and not (a in secili and b in secili)})
    for a, b in rng.sample(bag_adaylari, min(dikkat_sayisi, len(bag_adaylari))):
        secili |= {a, b}
    return bolum_kur(dunya, secili, rng, etiket)
