"""KODLAMA_PROMPTU §6 (Mutasyon sınaması): H2 B1–B3 koduna kasıtlı hata sokar (V-065).

Her mutant bir kopyada önce kendi hızlı test modülleriyle sınanır; orada kaçarsa B1–B3 test modüllerinin hepsiyle, yine
kaçarsa bütün test takımıyla yeniden sınanır. Üçünde de yeşil kalırsa KAÇTI. Mutantlar süreçlere bölünür.
Kullanım: .venv/bin/python araclar/mutasyon_b1.py [süreç sayısı] [mutant adı ...]
"""
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK))

from araclar.mutasyon_a0 import ZAMAN_SINIRI, kopyada_kostur  # noqa: E402

D = "degerlendirme/"
KUR, BOL, GEC, IKZ, BAG, TUR = (D + a for a in ("kural.py", "h2_bolum.py", "h2_gecit.py", "h2_ikiz.py", "h2_bagla.py",
                                               "h2_tur.py"))
KIR, KAL, OLC, ONK, B1, B2 = (D + a for a in ("h2_kirmizi.py", "h2_kalibrasyon.py", "h2_olcum.py", "h2_onkayit.py",
                                              "h2_b1.py", "h2_b2.py"))
Z12, Z12B, AKT, RAP, IST = (D + a for a in ("z12.py", "z12_ikinci.py", "h2_aktarim.py", "h2_rapor.py", "istatistik.py"))
T = "testler.test_"
UZUN_KOSU = 3  # V-039: B1–B3 modülleri çekirdek koştuğu için üst sınır üç kat
B1_MODULLERI = tuple(T + m for m in ("b1_kural", "b1_bolum", "b1_istatistik", "b1_gecit", "b1_bagla", "b1_tur",
                                     "b1_kirmizi", "b1_kalibrasyon", "b1_kosucu", "b1_onkayit", "b1_rapor", "b2_olcum",
                                     "b2_kosucu", "b3_z12"))  # V-065: ikinci eleme

MUTASYONLAR = [
    # genel değerlendirici
    ("farklılık şartı uygulanmıyor", KUR,
     "        return all(len({bag[u] for u in c}) == len(c) for c in self.farkli if all(u in bag for u in c))",
     "        return True", ("b1_kural",)),
    ("maskeli olgu kullanılıyor", KUR, "            if (f in idx.olgu and f not in haric) or f in ek:",
     "            if f in idx.olgu or f in ek:", ("b1_kural",)),
    ("kapanış tek tur", KUR, "    for _ in range(tur_siniri):", "    for _ in range(1):", ("b1_kural",)),
    ("θ-kapsama farklılık şartını saymıyor", KUR,
     "        if all(frozenset(theta[u] for u in c) in ozel_farkli for c in genel.farkli):", "        if True:",
     ("b1_kural",)),
    ("ters-dayanaklı hiç yok", KUR, "        return any({s, a} == {x, y} for _, s, a in self.halkalar)",
     "        return False", ("b1_kural", "b1_gecit")),
    # bölüm
    ("bölüm kapalı dünya değil", BOL,
     "    olgular = [(esleme[a], r, esleme[b]) for a, r, b in dunya.olgular if a in esleme and b in esleme]",
     "    olgular = [(esleme[a], r, esleme[b]) for a, r, b in dunya.olgular if a in esleme and b in esleme and a < b]",
     ("b1_bolum",)),
    # geçit
    ("yol-kesme maskesinde tersler yok", GEC,
     "    return frozenset({f} | (set() if k.ters_dayanakli else _ters_olgular(sema, olgu_kumesi, f)))",
     "    return frozenset({f})", ("b1_gecit",)),
    ("ters-dayanaklıda da tersler maskeli", GEC,
     "    return frozenset({f} | (set() if k.ters_dayanakli else _ters_olgular(sema, olgu_kumesi, f)))",
     "    return frozenset({f} | _ters_olgular(sema, olgu_kumesi, f))", ("b1_gecit",)),
    ("geliştirme yanlışı sayılmıyor", GEC, "        yanlis += len(tah) - len(dogrular)", "        yanlis += 0",
     ("b1_gecit",)),
    ("obiterde yanlış 0 şartı yok", GEC, '        if d["yanlis"] == 0 and d["tanik"] >= tanik:',
     '        if d["tanik"] >= tanik:', ("b1_gecit",)),
    ("yol-kesme eşiği yok", GEC, '    if g["yolkesme_tanik"] < sabit.en_az_tanik:', "    if False:", ("b1_gecit",)),
    ("bağ ikizi vetosu yok", GEC,
     '    return (BILMIYORUM, "bag_ikizi") if b["tanik"] >= sabit.en_az_tanik and b["yanlis"] == 0 else None',
     "    return None", ("b1_gecit",)),
    ("tek aile vetosu RET", GEC, '    if veto:\n        return BILMIYORUM, "aile_vetosu"',
     '    if veto:\n        return RET, "aile_vetosu"', ("b1_gecit",)),
    ("kapsam şartı yok", GEC, "    if len(kapsam(o, sabit)) < sabit.kapsam_en_az_aile:", "    if False:", ("b1_gecit",)),
    ("Thresholdout hep T_gel", GEC, "    return t_taze + eta2 if abs(t_gel - t_taze) > esik.T + eta1 else t_gel",
     "    return t_gel", ("b1_gecit",)),
    ("WY p formülünde +1 yok", GEC,
     "    return {k: (1 + sum(m >= t for m in maks)) / (toplam_cekilis + 1) for k, t in T.items()}",
     "    return {k: sum(m >= t for m in maks) / toplam_cekilis for k, t in T.items()}", ("b1_gecit",)),
    ("null yeniden bağlanmıyor", GEC,
     "            bagli[(et, r)] = set(h2_bagla.kenar_bagla(kenarlar, dolu, simetrik, rng, ortam.sabit.bagla_deneme_carpani))",
     "            bagli[(et, r)] = set(kenarlar)", ("b1_gecit",)),
    ("alfa tur sınırına bölünmüyor", GEC, "        return self.fwer / self.tur_siniri", "        return self.fwer",
     ("b1_gecit",)),
    ("uyum şartı yok", GEC, '    if not c["uyum"]:', "    if False:", ("b1_gecit",)),
    ("müdahale kanıt sayısı yok", GEC, "    if len(mud) < sabit.mudahale_en_az_kanit:", "    if False:", ("b1_gecit",)),
    ("π-ikizinde sayılar denetlenmiyor", GEC, '    if not pi["sayilar_ayni"] or (', "    if (", ("b1_gecit",)),
    ("iki ailede yanlışta durmuyor", GEC,
     '        if sum(v["yanlis"] > 0 for v in aileler.values()) >= ortam.sabit.ret_aile_sayisi:\n            break',
     "        if False:\n            break", ("b1_gecit",)),
    ("havuz aşımı yutulmuyor", GEC, "    except HavuzHatasi:", "    except ZeroDivisionError:", ("b1_gecit",)),
    # π-ikizi, yeniden bağlama
    ("π temel olmayı korumuyor", IKZ, "    return sema.simetrik(r), sema.islevsel(r), r in temel, len(sema.ters(r))",
     "    return sema.simetrik(r), sema.islevsel(r), len(sema.ters(r))", ("b1_gecit",)),
    ("simetrik ilişki yönlü bağlanıyor", BAG,
     "            yeni = kenar_bagla(kenarlar, dolu_ciftler(olgu, r, sema), sema.simetrik(r), rng, deneme_carpani)",
     "            yeni = kenar_bagla(kenarlar, dolu_ciftler(olgu, r, sema), False, rng, deneme_carpani)", ("b1_bagla",)),
    ("dolu çift denetlenmiyor", BAG,
     "        if any((x, y) in dolu or (simetrik and (y, x) in dolu) for x, y in giren):", "        if False:",
     ("b1_bagla",)),
    # tur koşucusu
    ("yedeklilik yok", TUR, "                if bellek.kapsar_mi(k, self.ortam):", "                if False:", ("b1_tur",)),
    ("turda aday sınırı yok", TUR,
     '            while kuyruk and kuyruk[0]["kimlik"] in parca and len(sorgulanacak) < is_.aday_siniri:',
     '            while kuyruk and kuyruk[0]["kimlik"] in parca:', ("b1_tur",)),
    ("obiter sıraya girmiyor", TUR, "                        kuyruk[0:0] = yeni", "                        pass",
     ("b1_tur",)),
    ("taze dünya yinelemesi denetlenmiyor", TUR, "            if h2_dunya.dunya_ozeti(d, ALGORITMA) in self.yasak:",
     "            if False:", ("b1_tur",)),
    ("tabu yok", TUR, "            if self.kapsar_mi(self.kabul[kimlik], ortam, haric=kimlik):", "            if False:",
     ("b1_tur",)),
    # kırmızı takım
    ("G1 başı değiştirmiyor", KIR,
     "            secenek = sorted(r for r in sema.adlar if r != bas[0] and sema.dislayici_mi(r, bas[0]))",
     "            secenek = [bas[0]]", ("b1_kirmizi",)),
    ("G2 yanlış şartı yok", KIR,
     "            if k[\"kimlik\"] in gorulen or not bagli_mi(kk) or _gelistirmede_yanlis(kk, gelistirme) == 0:",
     "            if k[\"kimlik\"] in gorulen or not bagli_mi(kk):", ("b1_kirmizi",)),
    ("G3 öteki ailede yanlış şartı yok", KIR, "        for i, bas in zip(*np.nonzero(uygun & yanlis_baska)):",
     "        for i, bas in zip(*np.nonzero(uygun)):", ("b1_kirmizi",)),
    ("gizli sayımda yanlış yerine tahmin", KIR, '        s["yanlis"] += yanlis > 0', '        s["yanlis"] += tahmin > 0',
     ("b1_kirmizi",)),
    ("gizli kaçakta etkin şartı yok", B1, '            s["kacak"] += etkin_mi and hukum[t["kimlik"]] == G.KABUL',
     '            s["kacak"] += hukum[t["kimlik"]] == G.KABUL', ("b1_kosucu",)),
    # kalibrasyon
    ("sahte kabul elemesi yok", KAL, '    uygun = [s for s in sonuclar if not s["sahte_kabul"]]',
     "    uygun = list(sonuclar)", ("b1_kalibrasyon",)),
    ("eşitlikte başlangıç kalmıyor", KAL,
     '        return len(fark), adim, [d[a].index(s["esik"][a]) for a in ALANLAR]',
     '        return [d[a].index(s["esik"][a]) for a in ALANLAR]', ("b1_kalibrasyon",)),
    ("boş koşu maliyet kuralı yok", KAL, '    if tek_kosu_saniye * n > h2.deger("bos_dunya_saat_siniri") * SAAT:',
     "    if False:", ("b1_kalibrasyon",)),
    # ölçüm
    ("daha genelde yanlışsız şartı yok", OLC,
     "        elif any(yanlissiz[a] and kural.kapsar_mi(k, d) for a, k in kabul.items()):",
     "        elif any(kural.kapsar_mi(k, d) for a, k in kabul.items()):", ("b2_olcum",)),
    ("bozuk kapsam ailesine bakmıyor", OLC, "        kendi = [(a, idx) for a, idx in dunyalar if a in kapsamlar[kim]]",
     "        kendi = dunyalar", ("b2_olcum",)),
    ("CP tek yanlı değil", OLC, '1 - 2 * (1 - k["cp_guven"])', 'k["cp_guven"]', ("b2_olcum",)),
    ("bilmiyorum farkı şartı yok", OLC, '"bilmiyorum": fark <= k["bilmiyorum_farki"]}', '"bilmiyorum": True}',
     ("b2_olcum",)),
    ("ara bölge alt sınırı yok", OLC, '    if nokta < k["ara_bolge_alt"]:', "    if False:", ("b2_olcum",)),
    ("makas hep tetikler", OLC, '"tetik": alt > m["tetik"]}', '"tetik": True}', ("b2_olcum",)),
    ("kümeli Wilson küme etkisi yok", IST, "    n_etkin = N / (1 + (m0 - 1) * rho)", "    n_etkin = N",
     ("b1_istatistik",)),
    # ön kayıt, B2, Z12, rapor
    ("sonraki ek öncekinin yerine geçmiyor", ONK, "        sonuc[yol] = oz", "        sonuc.setdefault(yol, oz)",
     ("b1_onkayit",)),
    ("özet karşılaştırılmıyor", ONK, "        if gercek != oz:", "        if False:", ("b1_onkayit",)),
    ("B1 başarısızken B2 başlıyor", B2, '        if not b1["basari_araliginda"]:', "        if False:", ("b2_kosucu",)),
    ("B2a seçimi özetsiz", B2,
     '    return sorted(kimlikler, key=lambda k: hashlib.sha256((B2A_ONEKI + k).encode("utf-8")).hexdigest())[:sayi]',
     "    return sorted(kimlikler)[:sayi]", ("b2_kosucu",)),
    ("iki yönlü ötelemede ters yön yok", Z12,
     '        return (b - a - tanim["fark"]) % n == 0 or (b - a + tanim["fark"]) % n == 0',
     '        return (b - a - tanim["fark"]) % n == 0', ("b3_z12",)),
    ("Z12-b kalanda ebob yok", Z12B,
     '        return x != y and all((a - b) % math.gcd(tanim["modul"], q) == 0 for a, b, q in zip(x, y, moduller))',
     '        return x != y and all((a - b) % tanim["modul"] == 0 for a, b, q in zip(x, y, moduller))', ("b3_z12",)),
    ("B3 onaysız başlıyor", AKT,
     '    if not re.fullmatch(r"K-\\d{3}", karar) or m is None or "B3" not in m.group(0) or "Onaylayan:** kullanıcı" not in m.group(0):',
     "    if False:", ("b3_z12",)),
    ("Z12 dikkat sayısı akrabalıktaki gibi", AKT,
     '    sabit = dataclasses.replace(G.Sabitler.ayardan(h2), dikkat_sayisi=h2.deger("z12_dikkat_sayisi"))',
     "    sabit = G.Sabitler.ayardan(h2)", ("b3_z12",)),
    ("raporda gizli aile sınırı yok", RAP, '        f"- {GIZLI_SINIR}",\n        "",\n        "## Boş dünya",',
     '        "",\n        "## Boş dünya",', ("b1_rapor",)),
]


def _kostur(kopya, moduller):
    try:
        r = subprocess.run([sys.executable, "-m", "unittest", *moduller], cwd=kopya, capture_output=True, text=True,
                           timeout=ZAMAN_SINIRI * UZUN_KOSU, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    except subprocess.TimeoutExpired:
        return 1, "ZAMAN AŞIMI (V-039)"
    return r.returncode, (r.stderr.strip().splitlines() or ["?"])[-1]


def mutant_kostur(m):
    ad, dosya, eski, yeni, hizli = m
    with tempfile.TemporaryDirectory() as d:
        kopya = Path(d) / "proje"
        shutil.copytree(KOK, kopya, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "uretilen"))
        yol = kopya / dosya
        yol.write_text(yol.read_text(encoding="utf-8").replace(eski, yeni, 1), encoding="utf-8")
        kod, sayac = _kostur(kopya, [T + h for h in hizli])
        if kod == 0:
            kod, sayac = _kostur(kopya, B1_MODULLERI)
    if kod == 0:
        kod, sayac = kopyada_kostur((dosya, eski, yeni))
    return ad, kod, sayac


def main(arg):
    is_sayisi = int(arg[0]) if arg and arg[0].isdigit() else 4  # V-057: makinedeki çekirdek sayısı
    secilen = [a for a in arg if not a.isdigit()]
    liste = [m for m in MUTASYONLAR if not secilen or m[0] in secilen]
    capasiz = [ad for ad, dosya, eski, _, _ in liste if (KOK / dosya).read_text(encoding="utf-8").count(eski) != 1]
    for ad in capasiz:
        print(f"ÇAPA YOK  {ad}")
    if capasiz:
        return 1
    kacan = 0
    with ProcessPoolExecutor(is_sayisi) as havuz:
        for ad, kod, sayac in havuz.map(mutant_kostur, liste):
            kacan += kod == 0
            print(f"{'YAKALANDI' if kod else 'KAÇTI':9} {ad:44} {sayac}", flush=True)
    print(f"MUTASYON: toplam={len(liste)} yakalanan={len(liste) - kacan} kaçan={kacan}")
    return 1 if kacan else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
