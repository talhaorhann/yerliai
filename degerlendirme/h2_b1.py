"""sistem.md §13, §18; K-041, K-043 (ÖK-005 taslağı §4 madde 3, 9–12, 19, 20; K kalibrasyon kuralı; §9 madde 3), V-065:
B1 koşucusu.

Evreler (her biri `<çıkış>/<evre>.json`'a yazılır; koşu kesilirse kaldığı yerden sürer):
1. talep: C (geliştirme havuzunda M0 sırasıyla aşama 1–4'ü geçen, öncekilerce kapsanmayan; 4801'de durur).
2. kirmizi_gorunur: G1–G4 (G3 için şablon sayacı geliştirme havuzunda aile başına koşar).
3. bos_adaylar: 1. boş koşunun M0'ı (boş geliştirme havuzu); ilk `p_yildiz_aday_sayisi` aday P* akışıdır. Akışta
   yalnız sahte (gerçek geliştirme havuzunda yanlış veren) adaylar geçitte ölçülür: sahte olmayanın hükmü ne K
   seçimine (girdisi yalnız sahteler ve ilk adaylar) ne P*'a (ilk sahte kabul) girer (V-065 madde 15).
4. kalibrasyon_olcum: B1 taze akışında kalibrasyon kipinde turlar: tur 1 M0'ın ilk 200 adayı, tur 2 görünür kırmızı
   takım, sonra boş aday akışı. Obiterin indirgenmişleri sıraya girmez (ölçüm akışıdır, arama değil). B1'de sorgu
   bütçesi yoktur (kalibrasyon bütçeden düşmez); taze dünyalar tur özetlerine özetleriyle yazılır ve yinelenmez.
5. k: K ızgarası ve seçim (yalnız görünür kırmızı takım ve boş adaylar sahte sayılır; DNA ve gizli aileler girmez).
6. kirmizi: görünür ailelerin seçilen K ile hükmü; gizli aileler seçilen K ile ayrı turda (yalnız sayılar yazılır,
   kimlik ve içerik yazılmaz, ölçüm dosyaları geçici klasörde kalır ve silinir).
7. p_yildiz: boş aday akışında ilk sahte kabul.
8. bos_kosular: boş dünyada arama (M0 + 12 tur, seçilen K); şemadan okunabilir sınıf sayılmadığı için sıraya girmez;
   bir koşuda okunabilir olmayan ilk kabulde o koşu durur; tetik sayısına ulaşılınca bütün koşular durur.
9. sonuc: B1'in önkayıttaki başarı aralığında olup olmadığı (kaçak 0, alt sınır ≥ %98, boş tetik yok, K seçildi).
Kullanım: python3 -m degerlendirme.h2_b1 <m0_adaylar.jsonl> <çıkış klasörü> [süreç sayısı] [evre]
"""
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from degerlendirme import h2_bagla, h2_butce, h2_gecit as G, h2_kalibrasyon as KAL, h2_kirmizi as KR
from degerlendirme import h2_onkayit, h2_tur, istatistik, kural
from kesif import aday, m0, sablon

BASAMAK = "B1"  # ÖK-005 taslağı §5: taze dünya etiketi
M0_IS_PARCACIGI = 4  # V-057: M0 süreç başına iş parçacığı (sonucu değiştirmez)
TALEP_PARCA = 256  # V-065: C sayımında paralel parça (sonucu değiştirmez)
VARSAYILAN_IS_SAYISI = 4  # V-057: makinedeki çekirdek sayısı
KALIBRASYON, KIRMIZI_GORUNUR, BOS_AKIS, KIRMIZI_GIZLI = "kalibrasyon", "kirmizi_gorunur", "bos_akis", "kirmizi_gizli"
EVRELER = ("talep", "kirmizi_gorunur", "bos_adaylar", "kalibrasyon_olcum", "k", "kirmizi", "p_yildiz", "bos_kosular",
           "sonuc")


class B1Hatasi(RuntimeError):
    pass


def m0_ozeti_denetle(kok, m0_yolu):
    """M0 aday dosyası ÖK-005 eki §1'deki özetle aynı olmalı."""
    metin = h2_onkayit.bolum((Path(kok) / "ONKAYIT.md").read_text(encoding="utf-8"))
    m = re.search(r"`m0_adaylar\.jsonl` `([0-9a-f]{64})`", metin)
    if m is None or hashlib.sha256(Path(m0_yolu).read_bytes()).hexdigest() != m.group(1):
        raise B1Hatasi("M0 aday dosyası ÖK-005'teki özetle aynı değil")


def _sema_okunur(kayit, sema):
    return h2_bagla.semadan_okunabilir_mi(kayit, sema)


def okunur_disi(kimlikler, bellek, sema):
    """ÖK-005 taslağı §4 madde 20: tetikte şemadan okunabilir sınıf sayılmaz. Sıra süzülse de obiterin indirgenmişi
    sıraya sonradan girebilir; bu yüzden kabul edilen (ya da tabuyla uyutulan) kural burada ayrıca denetlenir."""
    sonuc = []
    for kim in kimlikler:
        k = bellek.kabul.get(kim) or bellek.uyuyan[kim]
        r, x, y = k.bas
        kayit = {"halkalar": [{"gen": g, "sol": s, "sag": a} for g, s, a in k.halkalar],
                 "sonuc": {"gen": r, "sol": x, "sag": y}}
        if not _sema_okunur(kayit, sema):
            sonuc.append(kim)
    return sonuc


class B1:
    def __init__(self, kok, m0_yolu, cikis, is_sayisi, onkayit=True):
        self.kok, self.cikis, self.is_sayisi = Path(kok), Path(cikis), is_sayisi
        self.h2 = ayar_yukle(self.kok / "config_h2.json")
        if onkayit:
            h2_onkayit.tam_denetim(self.kok, self.h2)
            m0_ozeti_denetle(self.kok, m0_yolu)
        self.m0 = KR.M0Listesi.dosyadan(m0_yolu)
        self.kurulum = h2_tur.Kurulum(str(self.kok))
        self.ortam, self.taze_fn = h2_tur.ortam_kur(self.kurulum)
        self.sabit = self.ortam.sabit
        self.cikis.mkdir(parents=True, exist_ok=True)

    # ---- yardımcılar ----

    def evre(self, ad, fn):
        yol = self.cikis / f"{ad}.json"
        if not yol.exists():
            atomik_yaz(yol, kanonik_json(fn()))
        return json.loads(yol.read_text(encoding="utf-8"))

    def _jsonl_yaz(self, ad, kayitlar):
        atomik_yaz(self.cikis / ad, b"".join(kanonik_json(k) + b"\n" for k in kayitlar))

    def _jsonl_oku(self, ad):
        return [json.loads(s) for s in (self.cikis / ad).read_text(encoding="utf-8").splitlines()]

    def _tur_basina(self):
        return self.h2.deger("sorgu_tur_basina_aday")

    def _yasak(self):
        oz = json.loads((self.kok / "raporlar" / "h2_b0" / "havuz_ozetleri.json").read_text(encoding="utf-8"))
        return [o for v in oz.values() for o in v]

    def _kosucu(self, klasor, kurulum=None, defter=None, obiter_sirala=False):
        kurulum = kurulum or self.kurulum
        if self.is_sayisi <= 1:
            ortam, taze_fn = h2_tur.ortam_kur(kurulum)
            return h2_tur.Kosucu(klasor, ortam, taze_fn, None, defter, self._yasak(), obiter_sirala)
        return h2_tur.Kosucu.paralel(klasor, kurulum, self.is_sayisi, defter, self._yasak(), obiter_sirala)

    def _m0_kayitlari(self, n):
        return [self.m0[i] for i in range(min(n, len(self.m0)))]

    # ---- 1. talep ----

    def talep(self):
        tur = self.h2.deger("sorgu_tur_siniri")
        ust = 2 * self._tur_basina() * tur + 1  # ÖK-005 taslağı §4 madde 3: 2400 ve 4800 eşikleri; 4801'de durur
        kos = self._kosucu(self.cikis / "talep")
        bellek, eklenen = h2_tur.Bellek(), [0]

        def kapsar(k, onceki):
            for j in range(eklenen[0], len(onceki)):
                bellek.kabul_et(f"c{j}", onceki[j])
            eklenen[0] = len(onceki)
            return bellek.kapsar_mi(k, self.ortam)

        taranan = [0]

        def akis():
            for bas in range(0, len(self.m0), TALEP_PARCA):
                parca = [self.m0[j] for j in range(bas, min(bas + TALEP_PARCA, len(self.m0)))]
                for kayit, on in zip(parca, kos._esle(h2_tur.on_is, parca, kos.on)):
                    taranan[0] += 1
                    yield kayit["kimlik"], on, kural.Kural.kayittan(kayit)
        try:
            c, tamam = KAL.talep(akis(), kapsar, self.sabit, ust)
        finally:
            kos.kapat()
        return {"C": c, "sayim_tamam": tamam, "sayim_ustu": ust, "taranan": taranan[0], "m0_aday": len(self.m0)}

    # ---- 2. görünür kırmızı takım ----

    def kirmizi_gorunur(self):
        import torch
        torch.set_num_threads(M0_IS_PARCACIGI)
        adlar = tuple(self.ortam.sema.adlar)
        en_cok, zincir = self.h2.deger("sablon_kademeleri")[self.h2.deger("sablon_uretim_kademesi")]
        govdeler = sablon.govdeler(len(adlar), tuple(self.h2.deger("sablon_degiskenleri")), en_cok, zincir)
        liste = KR.g3_listesi([d for _, d, _ in self.ortam.gelistirme], adlar, self.h2, govdeler)
        mutantlar, sayilar = KR.gorunur(self.m0, self.ortam.gelistirme, liste, govdeler, self.ortam.sema, self.h2)
        sahte = [k["kimlik"] for k in mutantlar
                 if KR._gelistirmede_yanlis(kural.Kural.kayittan(k), self.ortam.gelistirme) > 0]
        self._jsonl_yaz("kirmizi_gorunur.jsonl", mutantlar)
        return {"sayilar": sayilar, "toplam": len(mutantlar), "sahte": sahte, "g3_aday_sayisi": len(liste)}

    # ---- 3. boş adaylar ----

    def bos_adaylar(self):
        adaylar, sure, oz = self._bos_m0(1)
        n = self.h2.deger("p_yildiz_aday_sayisi")
        akis = [a["aday"] for a in adaylar[:n]]
        self._jsonl_yaz("bos_adaylar.jsonl", akis)
        sahte = [k["kimlik"] for k in akis if KR._gelistirmede_yanlis(kural.Kural.kayittan(k), self.ortam.gelistirme) > 0]
        return {"m0_aday": len(adaylar), "akis": len(akis), "sahte": sahte, "m0_sure_s": sure, "m0_ozet": oz}

    def _bos_m0(self, k):
        """Boş geliştirme havuzunda M0 (dosyaya yazılır; varsa okunur). Dönüş: (adaylar, süre, özet)."""
        klasor = self.cikis / "bos"
        yol, ozet_yolu = klasor / f"k{k:03d}_m0.jsonl", klasor / f"k{k:03d}_m0_ozet.json"
        if not ozet_yolu.exists():
            import torch
            torch.set_num_threads(M0_IS_PARCACIGI)
            bas = time.time()
            ortam, _ = h2_tur.ortam_kur(h2_tur.Kurulum(str(self.kok), bos=k))
            sonuc = m0.m0([d for _, d, _ in ortam.gelistirme], tuple(ortam.sema.adlar), self.h2)
            klasor.mkdir(parents=True, exist_ok=True)
            atomik_yaz(yol, sonuc.cikti)
            atomik_yaz(ozet_yolu, kanonik_json({"ozet": sonuc.ozet, "sure_s": round(time.time() - bas)}))
        oz = json.loads(ozet_yolu.read_text(encoding="utf-8"))
        adaylar = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()]
        return adaylar, oz["sure_s"], oz["ozet"]

    # ---- 4. kalibrasyon ölçümü ----

    def _turlar(self, kos, kuyruk, ilk_tur, esik, defter_turu=None):
        """Kuyruk bitene dek turlar; dönüş: (son tur, {kimlik: ölçüm}, {kimlik: hüküm})."""
        tur, olcumler, hukumler = ilk_tur, {}, {}
        kimlikler = [k["kimlik"] for k in kuyruk]
        while kuyruk:
            oz, olc = kos.tur_kos(kuyruk, h2_tur.TurIsi(BASAMAK, tur, self._tur_basina(), esik), h2_tur.Bellek())
            hukumler.update(oz["hukumler"])
            olcumler.update(olc)
            tur += 1
        return tur, {k: kos.olcum(k, olcumler) for k in kimlikler}, hukumler

    def kalibrasyon_olcum(self):
        kos = self._kosucu(self.cikis / "kalibrasyon")
        try:
            ilk = self._m0_kayitlari(self.h2.deger("kalibrasyon_aday_sayisi"))
            tur, ilk_olc, _ = self._turlar(kos, list(ilk), 1, None)
            tur, gorunur_olc, _ = self._turlar(kos, self._jsonl_oku("kirmizi_gorunur.jsonl"), tur, None)
            sahte = set(self.evre("bos_adaylar", self.bos_adaylar)["sahte"])  # V-065 madde 15
            tur, bos_olc, _ = self._turlar(kos, [k for k in self._jsonl_oku("bos_adaylar.jsonl") if k["kimlik"] in sahte],
                                           tur, None)
        finally:
            kos.kapat()
        self._jsonl_yaz("kalibrasyon_olcumleri.jsonl", [{"grup": g, "kimlik": k, "olcum": o}
                                                        for g, d in (("ilk", ilk_olc), ("gorunur", gorunur_olc),
                                                                     ("bos", bos_olc)) for k, o in d.items()])
        return {"son_tur": tur - 1, "ilk": len(ilk_olc), "gorunur": len(gorunur_olc), "bos": len(bos_olc)}

    def _olcumler(self):
        self.evre("kalibrasyon_olcum", self.kalibrasyon_olcum)
        d = {"ilk": {}, "gorunur": {}, "bos": {}}  # bir grup boş olabilir (ör. akışta sahte yok)
        for s in self._jsonl_oku("kalibrasyon_olcumleri.jsonl"):
            d[s["grup"]][s["kimlik"]] = s["olcum"]
        return d

    # ---- 5. K ----

    def k(self):
        olc = self._olcumler()
        sahte = set(self.evre("kirmizi_gorunur", self.kirmizi_gorunur)["sahte"]) | set(
            self.evre("bos_adaylar", self.bos_adaylar)["sahte"])
        sahte_olc = {k: o for g in ("gorunur", "bos") for k, o in olc[g].items() if k in sahte}
        sonuc = KAL.kalibre_et(sahte_olc, olc["ilk"], self.sabit, self.h2)
        sonuc["sahte_sayisi"] = len(sahte_olc)
        return sonuc

    def _esik(self):
        secilen = self.evre("k", self.k)["secilen"]
        if secilen is None:
            raise B1Hatasi("sahte kabulü 0 olan K noktası yok")
        return G.Esikler.sozlukten(secilen)

    # ---- 6. kırmızı takım ----

    def kirmizi(self, gizli_yolu):
        esik = self._esik()
        olc = self._olcumler()["gorunur"]
        g = self.evre("kirmizi_gorunur", self.kirmizi_gorunur)
        sahte = set(g["sahte"])
        gorunur = self._jsonl_oku("kirmizi_gorunur.jsonl")
        aile = {k["kimlik"]: k["kaynak"]["aile"] for k in gorunur}
        hukum = {k: G.hukum(o, esik, self.sabit)[0] for k, o in olc.items()}
        gorunur_ozet = {}
        for kim, a in aile.items():
            s = gorunur_ozet.setdefault(a, {"mutant": 0, "sahte": 0, "kacak": 0, "sahte_olmayan_kabul": 0})
            s["mutant"] += 1
            s["sahte"] += kim in sahte
            s["kacak"] += kim in sahte and hukum[kim] == G.KABUL
            s["sahte_olmayan_kabul"] += kim not in sahte and hukum[kim] == G.KABUL
        gizli_ozet = self._gizli(gizli_yolu, esik)
        n = sum(s["sahte"] for s in gorunur_ozet.values()) + sum(s["etkin"] for s in gizli_ozet.values())
        kacak = sum(s["kacak"] for s in gorunur_ozet.values()) + sum(s["kacak"] for s in gizli_ozet.values())
        r = self.h2.deger("kirmizi_alt_sinir")
        alt = istatistik.clopper_pearson(n - kacak, n, 1 - 2 * (1 - r["guven"]))[0] if n else 0.0  # K-041: tek yanlı %95
        return {"gorunur": gorunur_ozet, "gizli": gizli_ozet, "sahte_toplam": n, "kacak": kacak, "alt_sinir": alt,
                "alt_sinir_gecti": alt >= r["oran"]}

    def _gizli(self, gizli_yolu, esik):
        """Gizli aileler: yalnız sayılar döner; ölçümler geçici klasörde kalır ve silinir."""
        kayitlar = KR.gizli_yukle(gizli_yolu, frozenset(self.ortam.sema.adlar), self.h2)
        sayim, etkin = KR.gelistirme_sayimi(kayitlar, self.ortam.gelistirme)
        aileler = sorted({k["kaynak"]["aile"] for k in kayitlar})
        etkin_kimlik = {id(k) for k in etkin}
        takma = []
        for i, k in enumerate(kayitlar):
            t = dict(k, kimlik=f"gizli_{i:04d}")
            takma.append((aileler.index(k["kaynak"]["aile"]) + 1, id(k) in etkin_kimlik, t))
        gecici = Path(tempfile.mkdtemp(prefix="h2_gizli_"))
        try:
            kos = self._kosucu(gecici)
            try:
                son = self.evre("kalibrasyon_olcum", self.kalibrasyon_olcum)["son_tur"]
                _, olc, _ = self._turlar(kos, [t for _, _, t in takma], son + 1, esik)
            finally:
                kos.kapat()
            hukum = {t["kimlik"]: G.hukum(olc[t["kimlik"]], esik, self.sabit)[0] for _, _, t in takma}
        finally:
            shutil.rmtree(gecici, ignore_errors=True)
        ozet = {}
        for no, etkin_mi, t in takma:
            s = ozet.setdefault(no, {**sayim[no], "etkin": 0, "kacak": 0, "etkin_olmayan_kabul": 0})
            s["etkin"] += etkin_mi
            s["kacak"] += etkin_mi and hukum[t["kimlik"]] == G.KABUL
            s["etkin_olmayan_kabul"] += (not etkin_mi) and hukum[t["kimlik"]] == G.KABUL
        return ozet

    # ---- 7. P* ----

    def p_yildiz(self):
        esik = self._esik()
        olc = self._olcumler()["bos"]
        b = self.evre("bos_adaylar", self.bos_adaylar)
        sahte = set(b["sahte"])
        sira = [(k["kimlik"], G.hukum(olc[k["kimlik"]], esik, self.sabit)[0] if k["kimlik"] in sahte else None)
                for k in self._jsonl_oku("bos_adaylar.jsonl")]  # V-065 madde 15: sahte olmayanın hükmü P*'ı değiştirmez
        p, sansur = KAL.p_yildiz(sira, lambda k: k in sahte, b["akis"])
        c = self.evre("talep", self.talep)
        return {"P*": p, "sansurlu": sansur, "tur_basina_aday": h2_butce.tur_basina_aday(c["C"], p, self.h2)}

    # ---- 8. boş koşular ----

    def _bos_kosu(self, k, esik, tur_basina):
        adaylar, m0_sure, _ = self._bos_m0(k)
        bas = time.time()
        sema = self.ortam.sema
        kuyruk = [a["aday"] for a in adaylar if not _sema_okunur(a["aday"], sema)]
        klasor = self.cikis / "bos" / f"k{k:03d}"
        defter = h2_butce.SorguDefteri(klasor / "sorgu_defteri.jsonl", self.h2, tur_basina)
        kos = self._kosucu(klasor, kurulum=h2_tur.Kurulum(str(self.kok), bos=k), defter=defter, obiter_sirala=True)
        bellek, kabul, okunur, tur = h2_tur.Bellek(), [], 0, 1
        sira_boyu = len(kuyruk)
        try:
            while kuyruk and tur <= self.h2.deger("sorgu_tur_siniri") and not kabul:
                oz, _ = kos.tur_kos(kuyruk, h2_tur.TurIsi(BASAMAK, tur, tur_basina, esik), bellek)
                hepsi = [kim for kim, h in oz["hukumler"].items() if h[0] == G.KABUL]
                kabul = okunur_disi(hepsi, bellek, sema)
                okunur += len(hepsi) - len(kabul)
                tur += 1
        finally:
            kos.kapat()
        return {"k": k, "m0_aday": len(adaylar), "okunur_disi": sira_boyu, "tur": tur - 1, "kabul": kabul,
                "okunur_kabul": okunur, "sure_s": round(m0_sure + time.time() - bas)}

    def bos_kosular(self):
        esik = self._esik()
        tur_basina = self.evre("p_yildiz", self.p_yildiz)["tur_basina_aday"]
        sonuclar = []
        for k in range(1, self.h2.deger("bos_dunya_kosu_sayisi") + 1):
            yol = self.cikis / "bos" / f"k{k:03d}.json"
            if yol.exists():
                s = json.loads(yol.read_text(encoding="utf-8"))
            else:
                s = self._bos_kosu(k, esik, tur_basina)
                atomik_yaz(yol, kanonik_json(s))
            sonuclar.append(s)
            sayi, tetik = KAL.bos_kosu_sayisi(sonuclar[0]["sure_s"], self.h2)
            kabullu = sum(bool(x["kabul"]) for x in sonuclar)
            if kabullu >= tetik or len(sonuclar) >= sayi:
                break
        return {"kosu_sayisi": sayi, "tetik": tetik, "yapilan": len(sonuclar), "kabullu_kosu": kabullu,
                "tetiklendi": kabullu >= tetik, "ilk_kosu_s": sonuclar[0]["sure_s"],
                "kosular": [{"k": x["k"], "kabul": len(x["kabul"]), "sure_s": x["sure_s"], "tur": x["tur"]}
                            for x in sonuclar]}

    # ---- 9. sonuç ----

    def sonuc(self, gizli_yolu):
        k = self.evre("k", self.k)
        kr = self.evre("kirmizi", lambda: self.kirmizi(gizli_yolu))
        p = self.evre("p_yildiz", self.p_yildiz)
        bos = self.evre("bos_kosular", self.bos_kosular)
        c = self.evre("talep", self.talep)
        sartlar = {"k_secildi": k["secilen"] is not None, "kacak_0": kr["kacak"] == 0,
                   "alt_sinir": kr["alt_sinir_gecti"], "bos_tetik_yok": not bos["tetiklendi"]}
        return {"basari_araliginda": all(sartlar.values()), "sartlar": sartlar, "K": k["secilen"], "C": c["C"],
                "P*": p["P*"], "P*_sansurlu": p["sansurlu"], "tur_basina_aday": p["tur_basina_aday"]}


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    m0_yolu, cikis, *secenek = arg
    is_sayisi = int(secenek[0]) if secenek else VARSAYILAN_IS_SAYISI
    son = secenek[1] if len(secenek) > 1 else EVRELER[-1]
    h2 = ayar_yukle(kok / "config_h2.json")
    gizli = kok / h2.deger("kirmizi_gizli_dosyasi")["yol"]
    b1 = B1(kok, m0_yolu, cikis, is_sayisi)
    islevler = {"talep": b1.talep, "kirmizi_gorunur": b1.kirmizi_gorunur, "bos_adaylar": b1.bos_adaylar,
                "kalibrasyon_olcum": b1.kalibrasyon_olcum, "k": b1.k, "kirmizi": lambda: b1.kirmizi(gizli),
                "p_yildiz": b1.p_yildiz, "bos_kosular": b1.bos_kosular, "sonuc": lambda: b1.sonuc(gizli)}
    for ad in EVRELER[:EVRELER.index(son) + 1]:
        bas = time.time()
        s = b1.evre(ad, islevler[ad])
        ozet = {a: v for a, v in s.items() if a not in ("noktalar", "sahte", "kosular")} if isinstance(s, dict) else s
        print(json.dumps({"evre": ad, "sure_s": round(time.time() - bas), **ozet}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
