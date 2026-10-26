"""sistem.md §13; K-041, K-043 (ÖK-005 taslağı §4 madde 3, 9, 10, 12, 20; K kalibrasyon kuralı), V-065: B1 hesapları.

- K ızgarası: τ × müdahale × T × σ (81 nokta). Girdiler yalnız görünür kırmızı takım ve boş adaylardır (sahte = gerçek
  geliştirme havuzunda yanlış veren) ve geliştirme havuzunda M0 sırasının ilk `kalibrasyon_aday_sayisi` adayı. Seçim:
  sahte kabulü 0 olan noktalar içinden ilk adaylara en çok KABUL veren; eşitlikte başlangıç değeri kalır (V-065: eşit
  noktalar arasında başlangıçtan en az parametresi farklı olan, sonra ızgara sırasınca başlangıca en yakın olan).
- C (talep): geliştirme havuzunda M0 süzgecini ve aşama 1–4'ü geçen, kendinden önce geçenlerce (M0 sırası) kapsanmayan
  aday sayısı; tur anahtarı yalnız C ≤ 2400, ≤ 4800 ya da > 4800 ayrımına baktığından sayım 4801'de durur (V-065).
- P*: boş aday akışında ilk sahte kabule kadar sorgulanan aday sayısı; akışta sahte kabul yoksa P* > akış uzunluğu
  (sansürlü) ve tavan hesabında akış uzunluğu + 1 kullanılır (V-065).
- Boş dünya kuralı: tek koşunun duvar süresi × 100 > `bos_dunya_saat_siniri` ise 50 koşu ve tetik 1.
"""
import itertools

from degerlendirme import h2_gecit as G

ALANLAR = ("tau", "mudahale", "T", "sigma")  # ÖK-005 taslağı §4 madde 9, 10, 12
SAAT = 3600  # V-065: saatte saniye (madde 20'nin saat sınırı için)


def izgara(h2):
    d = h2.deger("esik_izgarasi")
    return [dict(zip(ALANLAR, v)) for v in itertools.product(*(d[a] for a in ALANLAR))]


def nokta_sonucu(esik, sahte_olcumleri, ilk_olcumler, sabit):
    e = G.Esikler.sozlukten(esik)
    sahte = sorted(k for k, o in sahte_olcumleri.items() if G.hukum(o, e, sabit)[0] == G.KABUL)
    kabul = sum(G.hukum(o, e, sabit)[0] == G.KABUL for o in ilk_olcumler.values())
    return {"esik": esik, "sahte_kabul": sahte, "ilk_kabul": kabul}


def sec(sonuclar, baslangic, h2):
    """Kural: sahte kabul 0; en çok ilk KABUL; eşitlikte başlangıç (V-065 ayrıntısı modül başında)."""
    d = h2.deger("esik_izgarasi")
    uygun = [s for s in sonuclar if not s["sahte_kabul"]]
    if not uygun:
        return None
    en_cok = max(s["ilk_kabul"] for s in uygun)
    esit = [s for s in uygun if s["ilk_kabul"] == en_cok]

    def uzaklik(s):
        fark = [a for a in ALANLAR if s["esik"][a] != baslangic[a]]
        adim = sum(abs(d[a].index(s["esik"][a]) - d[a].index(baslangic[a])) for a in ALANLAR)
        return len(fark), adim, [d[a].index(s["esik"][a]) for a in ALANLAR]
    return min(esit, key=uzaklik)


def kalibre_et(sahte_olcumleri, ilk_olcumler, sabit, h2):
    baslangic = dict(h2.deger("esik_baslangic"))
    sonuclar = [nokta_sonucu(e, sahte_olcumleri, ilk_olcumler, sabit) for e in izgara(h2)]
    secilen = sec(sonuclar, baslangic, h2)
    return {"baslangic": baslangic, "secilen": secilen and secilen["esik"], "noktalar": sonuclar}


def talep(on_olcumleri, kapsar_mi, sabit, ust):
    """`on_olcumleri`: M0 sırasıyla (kimlik, aşama 1–4 ölçümü, kural); `kapsar_mi(kural, önceki_kurallar)`.
    Dönüş: (C, sayım tamam mı); sayım `ust`'e ulaşınca durur."""
    gecen = []
    for kimlik, on, k in on_olcumleri:
        if G._gelistirme_hukmu(on, sabit) or ("bag_ikizi" in on and G._bag_ikizi_vetosu(on, sabit)):
            continue
        if kapsar_mi(k, gecen):
            continue
        gecen.append(k)
        if len(gecen) >= ust:
            return len(gecen), False
    return len(gecen), True


def p_yildiz(hukum_sirasi, sahte_mi, akis_uzunlugu):
    """`hukum_sirasi`: sorgu sırasıyla (kimlik, hüküm). Dönüş: (P*, sansürlü mü)."""
    for n, (kimlik, h) in enumerate(hukum_sirasi, 1):
        if h == G.KABUL and sahte_mi(kimlik):
            return n, False
    return akis_uzunlugu + 1, True


def bos_kosu_sayisi(tek_kosu_saniye, h2):
    n = h2.deger("bos_dunya_kosu_sayisi")
    if tek_kosu_saniye * n > h2.deger("bos_dunya_saat_siniri") * SAAT:
        yedek = h2.deger("bos_dunya_yedek")
        return yedek["kosu_sayisi"], yedek["tetik"]
    return n, h2.deger("bos_dunya_tetik")
