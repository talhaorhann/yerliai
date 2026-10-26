"""sistem.md §13, §18; K-041, K-043 (ÖK-005 taslağı §3, §4 madde 2, 3, 15–18, 21; §8; §9 madde 4–6), V-065: B2 koşucusu.

Ön şartlar: ön kayıt tutar (`h2_onkayit`), M0 dosyası ÖK-005 eki §1'deki özetle aynı, B1 sonucu önkayıttaki başarı
aralığında; K ve tur başına aday B1 sonucundan okunur (ÖK-005 eki §3 ile aynı olmalı).
- B2a (duman testi, kapı değil): hedef kuralların (DNA v8) `sha256("ÖK-005|B2a|" + kimlik)` sırasında en küçük
  `b2a_silinen` tanesi silinir, kalanlar bellekte "b2a_tohumu" olarak durur (yalnız yedeklilikte kullanılır; çekirdek
  adımı bellek boş, V-065). Arama M0 sırasıyla, sorgu defteriyle, en çok 12 tur. Ölçüm geliştirme havuzunda (V-065):
  silinen kuralların sınıfları (kabul kümesi = tohumlar + yeni kabuller).
- B2b (tek atış): bellek boş; aynı arama; her tur sonunda makas (kontrol havuzu); tetiklenirse arama donar. Sonra final
  havuzunda bir kez ölçüm: hedef sınıfları, kabul sınıfları, bilmiyorum (kabul kümesi ve hedef kümesi), kapı kararı ve
  A3 aktarımı (aile başına kapanış geri bulması; A3 ikinci üreticidir).
Hedef kurallar yalnız B2a tohumlarında ve ölçümde kullanılır; arama sırası ve kalibrasyona girmez.
Kullanım: python3 -m degerlendirme.h2_b2 <m0_adaylar.jsonl> <B1 çıkış klasörü> <çıkış klasörü> <B2a|B2b> [süreç sayısı]
"""
import hashlib
import json
import sys
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from cekirdek.dna import dna_yukle
from degerlendirme import h2_b1, h2_bagla, h2_butce, h2_gecit as G, h2_kirmizi as KR, h2_olcum as O, h2_onkayit
from degerlendirme import h2_tur, kural

B2A, B2B = "B2a", "B2b"  # ÖK-005 taslağı §5: taze dünya etiketleri
DNA_YOLU = Path("veri") / "dna" / "akrabalik_dna_v8.json"  # K-038
DNA_BICIMI = Path("sema") / "dna_v2.schema.json"  # K-025
B2A_ONEKI = "ÖK-005|B2a|"  # ÖK-005 taslağı §5: B2a seçimi
TOHUM_KAYNAGI = "b2a_tohumu"  # ÖK-005 taslağı §8
FINAL, KONTROL = "final", "kontrol"
VARSAYILAN_IS_SAYISI = 4  # V-057: makinedeki çekirdek sayısı


class B2Hatasi(RuntimeError):
    pass


def b2a_silinenler(kimlikler, sayi):
    return sorted(kimlikler, key=lambda k: hashlib.sha256((B2A_ONEKI + k).encode("utf-8")).hexdigest())[:sayi]


class B2:
    def __init__(self, kok, m0_yolu, b1_klasoru, cikis, is_sayisi, onkayit=True):
        self.kok, self.cikis, self.is_sayisi = Path(kok), Path(cikis), is_sayisi
        self.h2 = ayar_yukle(self.kok / "config_h2.json")
        if onkayit:
            h2_onkayit.tam_denetim(self.kok, self.h2)
            h2_b1.m0_ozeti_denetle(self.kok, m0_yolu)
        b1 = json.loads((Path(b1_klasoru) / "sonuc.json").read_text(encoding="utf-8"))
        if not b1["basari_araliginda"]:
            raise B2Hatasi("B1 önkayıttaki başarı aralığında değil: B2 başlamaz")
        self.esik = G.Esikler.sozlukten(b1["K"])
        self.tur_basina = b1["tur_basina_aday"]
        self.m0 = KR.M0Listesi.dosyadan(m0_yolu)
        self.kurulum = h2_tur.Kurulum(str(self.kok))
        self.ortam, self.taze_fn = h2_tur.ortam_kur(self.kurulum)
        self.sabit = self.ortam.sabit
        self.cikis.mkdir(parents=True, exist_ok=True)

    def _kosucu(self, klasor, defter):
        yasak = [o for v in json.loads((self.kok / "raporlar" / "h2_b0" / "havuz_ozetleri.json").read_text(
            encoding="utf-8")).values() for o in v]
        if self.is_sayisi <= 1:
            return h2_tur.Kosucu(klasor, self.ortam, self.taze_fn, None, defter, yasak)
        return h2_tur.Kosucu.paralel(klasor, self.kurulum, self.is_sayisi, defter, yasak)

    def _dunyalar(self, havuz_adi):
        from degerlendirme.dunya import tanimlar_yukle
        tanimlar = tanimlar_yukle(self.kok / "degerlendirme" / "veri" / "tanimlar_v1.json",
                                  self.kok / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", self.ortam.sema)
        return [(d.aile, kural.Indeks(d.olgular)) for _, d in h2_tur.havuz_kayitlari(self.h2, tanimlar, havuz_adi)]

    def hedefler(self):
        """Hedef kurallar (DNA v8): yalnız B2a tohumları ve ölçüm için."""
        hucreler = dna_yukle(self.kok / DNA_YOLU, self.kok / DNA_BICIMI, self.ortam.sema)
        return {h.kimlik: O.dna_kurali(h) for h in hucreler}

    # ---- arama ----

    def arama(self, basamak, bellek, klasor, makas_fn=None):
        defter = h2_butce.SorguDefteri(klasor / "sorgu_defteri.jsonl", self.h2, self.tur_basina)
        kos = self._kosucu(klasor, defter)
        kuyruk = h2_tur.TembelKuyruk(self.m0)
        turlar, kapsam, donma = [], {}, None
        try:
            for tur in range(1, self.h2.deger("sorgu_tur_siniri") + 1):
                if not kuyruk:
                    break
                oz, _ = kos.tur_kos(kuyruk, h2_tur.TurIsi(basamak, tur, self.tur_basina, self.esik), bellek)
                for kim, h in oz["hukumler"].items():
                    if h[0] == G.KABUL:
                        kapsam[kim] = h[1].split(",")
                kayit = {"tur": tur, "sorgulanan": len(oz["sorgulanan"]), "kabul": len(oz["kabul"]),
                         "tabu_uyutulan": len(oz["tabu_uyutulan"]),
                         "hukum": {h: sum(v[0] == h for v in oz["hukumler"].values())
                                   for h in (G.KABUL, G.RET, G.BILMIYORUM, h2_tur.UYUTULDU)}}
                if makas_fn is not None:
                    kayit["makas"] = makas_fn(tur, bellek)
                    if kayit["makas"]["tetik"]:
                        donma = {"tur": tur, "neden": "makas"}
                        turlar.append(kayit)
                        break
                turlar.append(kayit)
        finally:
            kos.kapat()
        return {"turlar": turlar, "donma": donma, "kalan_sira": bool(kuyruk), "kapsam": kapsam}

    def _makas(self, basamak, klasor):
        kontrol = self._dunyalar(KONTROL)

        def fn(tur, bellek):
            yol = klasor / f"{basamak}_tur{tur:02d}" / "makas.json"
            if yol.exists():
                return json.loads(yol.read_text(encoding="utf-8"))
            sorgulanan = [(a, idx) for t in range(1, tur + 1) for _, a, _, idx in self.taze_fn(basamak, t)]
            m = O.makas(list(bellek.kabul.values()), sorgulanan, kontrol, self.ortam.sema,
                        self.sabit.kapanis_tur_siniri, self.h2, basamak, tur)
            atomik_yaz(yol, kanonik_json(m))
            return m
        return fn

    # ---- B2a ----

    def b2a(self):
        hedef = self.hedefler()
        silinen = b2a_silinenler(hedef, self.h2.deger("b2a_silinen"))
        bellek = h2_tur.Bellek()
        for kim in sorted(set(hedef) - set(silinen)):
            bellek.kabul_et(f"{TOHUM_KAYNAGI}|{kim}", hedef[kim])
        tohumlar = set(bellek.kabul)
        klasor = self.cikis / B2A
        a = self.arama(B2A, bellek, klasor)
        gel = [(d.aile, idx) for _, d, idx in self.ortam.gelistirme]
        siniflar = O.hedef_siniflari({k: hedef[k] for k in silinen}, bellek.kabul, bellek.uyuyan, gel,
                                     self.ortam.sema, self.sabit.kapanis_tur_siniri)
        yeni = {k: v for k, v in bellek.kabul.items() if k not in tohumlar}
        return {"silinen": len(silinen), "silinen_siniflari": {s: sum(v == s for v in siniflar.values())
                                                               for s in sorted(set(siniflar.values()))},
                "yeni_kabul": len(yeni), "uyutulan": len(bellek.uyuyan), "arama": {k: v for k, v in a.items()
                                                                                 if k != "kapsam"}}

    # ---- B2b ----

    def b2b(self):
        klasor = self.cikis / B2B
        bellek = h2_tur.Bellek()
        a = self.arama(B2B, bellek, klasor, self._makas(B2B, klasor))
        olcum = self.olcum(bellek, a["kapsam"])
        return {"arama": {k: v for k, v in a.items() if k != "kapsam"}, **olcum}

    def olcum(self, bellek, kapsamlar):
        """Final havuzunda bir kez (ÖK-005 taslağı §8)."""
        yol = self.cikis / "b2b_olcum.json"
        if yol.exists():
            return json.loads(yol.read_text(encoding="utf-8"))
        hedef = self.hedefler()
        final = self._dunyalar(FINAL)
        tur = self.sabit.kapanis_tur_siniri
        hs = O.hedef_siniflari(hedef, bellek.kabul, bellek.uyuyan, final, self.ortam.sema, tur)
        ks = O.kabul_siniflari(bellek.kabul, {k: kapsamlar[k] for k in bellek.kabul}, bellek.uyuyan, hedef, final)
        b_kume = O.bilmiyorum_olcusu(list(bellek.kabul.values()), final, self.ortam.sema, tur)
        b_hedef = O.bilmiyorum_olcusu(list(hedef.values()), final, self.ortam.sema, tur)
        karar = O.b2_karari(hs, hedef, ks, b_kume, b_hedef, self.h2, self.sabit.wilson_z)
        okunur = {k for k, d in hedef.items() if h2_bagla.semadan_okunabilir_mi(_kayit(d), self.ortam.sema)}
        ornekli = {k for k, s in hs.items() if s != O.ORNEKSIZ}
        bulunan = {k for k, s in hs.items() if s in (O.OZDES, O.GENEL, O.KAPANIS)}
        sonuc = {"karar": karar, "hedef_siniflari": hs, "kabul_siniflari": ks,
                 "bilmiyorum": {"kabul_kumesi": {a: v for a, v in b_kume.items() if a != "dunyalar"},
                                "hedef": {a: v for a, v in b_hedef.items() if a != "dunyalar"}},
                 "a3_aktarim": {"kabul_kumesi": O.aileye_gore(b_kume["dunyalar"], [a for a, _ in final]),
                                "hedef": O.aileye_gore(b_hedef["dunyalar"], [a for a, _ in final])},
                 "ikincil_paydalar": {"okunur_haric": [len(bulunan - okunur), len(set(hedef) - okunur)],
                                      "ornekli": [len(bulunan & ornekli), len(ornekli)]},
                 "kabul_sayisi": len(bellek.kabul), "uyutulan_sayisi": len(bellek.uyuyan)}
        atomik_yaz(yol, kanonik_json(sonuc))
        return sonuc


def _kayit(k):
    r, x, y = k.bas
    return {"halkalar": [{"gen": g, "sol": s, "sag": a} for g, s, a in k.halkalar], "sonuc": {"gen": r, "sol": x, "sag": y}}


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    m0_yolu, b1_klasoru, cikis, basamak, *secenek = arg
    b2 = B2(kok, m0_yolu, b1_klasoru, cikis, int(secenek[0]) if secenek else VARSAYILAN_IS_SAYISI)
    sonuc = b2.b2a() if basamak == B2A else b2.b2b()
    atomik_yaz(Path(cikis) / f"{basamak}_sonuc.json", kanonik_json(sonuc))
    ozet = sonuc.get("karar", sonuc)
    print(json.dumps(ozet, ensure_ascii=False), flush=True)  # V-057: okunur çıktı
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
