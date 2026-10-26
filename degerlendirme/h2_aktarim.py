"""sistem.md §11, §13, §18; K-041, K-043 (ÖK-005 taslağı §2.3, §3, §4.4 "aktarım"; §5), V-066: A3 ve Z12 aktarım ölçümü.

Ölçü kapanış geri bulmadır (elle yazılmış hedef kural kümesi gerekmez): bir dünya ailesinin final dünyalarında her olgu
maskelenir; kabul kümesi en çok 8 turda türetirse doğru, dünyada olmayan bir şey türetirse yanlış, değilse bilmiyorum
(`h2_olcum.olgu_olcusu`).
- A3 aktarımı: B2b kabul kümesinin final havuzunda aile başına (A1, A2, A3) kapanış geri bulması; A3 ikinci üreticidir.
- Z12 aktarımı (B3, Kapı 2 onayı gerekir): çekirdek dondurma sözleşmesi; alan başına değişenler yalnız üçlü dosyası,
  ilişki şeması ve şablon kademesidir. Z12 alanında M0 + aynı geçit (K değerleri B1'den, değişmez) + 12 tur arama;
  ölçüm Z final havuzunda aile başına (Z12-a, Z12-b, Z24). Bölümde dikkat dağıtıcı bağ 2 (ÖK §2.3).
  Alan şeması: altı_öte n = 24'te işlevsel olmadığından alan şemasında işlevsel değildir (V-066).
Kullanım (B3): python3 -m degerlendirme.h2_aktarim <B1 çıkış> <çıkış> <K-nnn: B3 onayı> [süreç sayısı]
"""
import dataclasses
import json
import random
import re
import sys
from pathlib import Path

from cekirdek.altyapi.atomik import atomik_yaz
from cekirdek.altyapi.ayar import ayar_yukle
from cekirdek.altyapi.kanonik import kanonik_json
from degerlendirme import h2_gecit as G, h2_olcum as O, h2_tur, kural, z12, z12_ikinci
from kesif import m0, tohum

ALAN = "z12"  # ÖK-005 taslağı §5: `havuzB3|<alan>|...`
HAVUZ_B3 = "havuzB3"  # ÖK-005 taslağı §5
BASAMAK = "B3"  # ÖK-005 taslağı §5: taze dünya etiketi
DOGRUDAN, CIN_KALAN = "dogrudan", "cin_kalan"  # V-066: config_h2 z12_aileleri üretici adları
VARSAYILAN_IS_SAYISI = 4  # V-057: makinedeki çekirdek sayısı


class AktarimHatasi(RuntimeError):
    pass


# ---- ölçü ----

def aile_kirilimi(kume, dunyalar, sema, tur):
    """`dunyalar`: [(aile, Indeks)] → {aile: {doğru, yanlış, bilmiyorum, toplam, geri_bulma}}."""
    return O.aileye_gore([O.olgu_olcusu(kume, idx, sema, tur) for _, idx in dunyalar], [a for a, _ in dunyalar])


# ---- Z12 alanı ----

def z12_dunyasi(aile, ayar, tanimlar, tohum_degeri):
    rng = random.Random(tohum_degeri)
    if ayar["uretec"] == DOGRUDAN:
        return z12.dunya(aile, ayar["n"], tanimlar, rng)
    if ayar["uretec"] == CIN_KALAN:
        return z12_ikinci.dunya(aile, ayar["moduller"], tanimlar, rng)
    raise ValueError("bilinmeyen Z12 üreticisi")


def z12_havuz(h2, tanimlar, havuz_adi):
    dagilim, aileler = h2.deger("z12_havuz_dagilimi")[havuz_adi], h2.deger("z12_aileleri")
    return [(tohum.etiket(HAVUZ_B3, ALAN, havuz_adi, a, i),
             z12_dunyasi(a, aileler[a], tanimlar, tohum.tohum(h2, HAVUZ_B3, ALAN, havuz_adi, a, i)))
            for a in sorted(dagilim) for i in range(1, dagilim[a] + 1)]


def z12_ortam_kur(kurulum):
    from cekirdek.dongu import CekirdekParametreleri
    from cekirdek.iliski_semasi import iliski_semasi_yukle
    from degerlendirme import h1, h2_ikiz
    kok = Path(kurulum.kok)
    ayar, _, gunluk = h1._ortam(kok)
    h2 = ayar_yukle(kok / "config_h2.json")
    dosya = h2.deger("z12_dosyalari")
    sema = iliski_semasi_yukle(kok / dosya["sema"], kok / dosya["onay"], kok / "sema" / "iliski_semasi_v1.schema.json")
    tanim = z12.tanimlar_yukle(kok / dosya["tanimlar"])
    if set(tanim["tanimlar"]) != set(sema.adlar):
        raise AktarimHatasi("Z12 tanımları şemayla aynı ilişkileri içermiyor")
    sabit = dataclasses.replace(G.Sabitler.ayardan(h2), dikkat_sayisi=h2.deger("z12_dikkat_sayisi"))
    gel = z12_havuz(h2, tanim["tanimlar"], h2_tur.GELISTIRME)
    temel = tuple(tanim["temel"])
    ortam = G.Ortam(sema, temel, sabit, h2, [(e, d, kural.Indeks(d.olgular)) for e, d in gel],
                    h2_ikiz.bijeksiyonlar(sema, temel),
                    h2_tur.onbellekli_kod_kitabi(ayar.deger("vektor_tohum"), ayar.deger("vektor_boyutu")),
                    CekirdekParametreleri.ayardan(ayar), gunluk)
    aileler = h2.deger("z12_aileleri")

    def taze_fn(basamak, tur):
        return [G.dunya_kaydi(tohum.etiket(h2_tur.TAZE, basamak, tur, a, j),
                              z12_dunyasi(a, aileler[a], tanim["tanimlar"], tohum.tohum(h2, h2_tur.TAZE, basamak, tur, a, j)))
                for a in sorted(aileler) for j in range(1, sabit.taze_aile_basina + 1)]

    return ortam, taze_fn


# ---- B3 koşusu ----

def b3_onayi_denetle(kok, karar):
    """B3 yalnız kullanıcının onayladığı bir kararla başlar (K-043: B3'e onaysız geçilmez)."""
    metin = (Path(kok) / "KARARLAR.md").read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(karar)} .*?(?=^## |\Z)", metin, re.M | re.S)
    if not re.fullmatch(r"K-\d{3}", karar) or m is None or "B3" not in m.group(0) or "Onaylayan:** kullanıcı" not in m.group(0):
        raise AktarimHatasi("B3 için kullanıcı onaylı karar yok")


def z12_aktarimi(kok, b1_klasoru, cikis, is_sayisi, karar):
    from degerlendirme import h2_butce, h2_onkayit
    kok, cikis = Path(kok), Path(cikis)
    b3_onayi_denetle(kok, karar)
    h2 = ayar_yukle(kok / "config_h2.json")
    h2_onkayit.tam_denetim(kok, h2)
    b1 = json.loads((Path(b1_klasoru) / "sonuc.json").read_text(encoding="utf-8"))
    esik, tur_basina = G.Esikler.sozlukten(b1["K"]), b1["tur_basina_aday"]
    kurulum = h2_tur.Kurulum(str(kok), alan=ALAN)
    ortam, taze_fn = z12_ortam_kur(kurulum)
    sonuc_m0 = m0.m0([d for _, d, _ in ortam.gelistirme], tuple(ortam.sema.adlar), h2)
    kuyruk = [a["aday"] for a in sonuc_m0.adaylar]
    defter = h2_butce.SorguDefteri(cikis / "sorgu_defteri.jsonl", h2, tur_basina)
    kos = h2_tur.Kosucu.paralel(cikis, kurulum, is_sayisi, defter) if is_sayisi > 1 else h2_tur.Kosucu(
        cikis, ortam, taze_fn, None, defter)
    bellek = h2_tur.Bellek()
    try:
        for tur in range(1, h2.deger("sorgu_tur_siniri") + 1):
            if not kuyruk:
                break
            kos.tur_kos(kuyruk, h2_tur.TurIsi(BASAMAK, tur, tur_basina, esik), bellek)
    finally:
        kos.kapat()
    final = [(d.aile, kural.Indeks(d.olgular)) for _, d in z12_havuz(h2, z12.tanimlar_yukle(
        kok / h2.deger("z12_dosyalari")["tanimlar"])["tanimlar"], "final")]
    return {"m0_aday": len(sonuc_m0.adaylar), "kabul": len(bellek.kabul), "uyutulan": len(bellek.uyuyan),
            "aile_kirilimi": aile_kirilimi(list(bellek.kabul.values()), final, ortam.sema, ortam.sabit.kapanis_tur_siniri)}


def main(arg):
    kok = Path(__file__).resolve().parents[1]
    b1_klasoru, cikis, karar, *secenek = arg
    sonuc = z12_aktarimi(kok, b1_klasoru, cikis, int(secenek[0]) if secenek else VARSAYILAN_IS_SAYISI, karar)
    atomik_yaz(Path(cikis) / "z12_aktarim.json", kanonik_json(sonuc))
    print(json.dumps(sonuc, ensure_ascii=False))  # V-057: okunur çıktı
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
