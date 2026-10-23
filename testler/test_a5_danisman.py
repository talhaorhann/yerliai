"""K-024: bağımsız danışmana verilen ilişki listesi onaylı şemayla aynı olmalı, gizli tanım içermemeli.

Tablo satırları `sema/iliskiler_v1.json`'dan (K-006) denetlenir; örnek JSON, DNA sürüm 2 biçimine ve onaylı şemaya
uymalı. Gizli tanımların okunur hâlinden (`okunur_tanimlar`) hiçbir tanım metni dosyada geçmemeli.
Testte ilişki adı yazılmaz (KODLAMA_PROMPTU §2.4): adlar veri dosyalarından okunur.
"""
import hashlib
import json
import re
import unittest

from cekirdek.dna import dna_kur
from cekirdek.iliski_semasi import iliski_semasi_yukle
from degerlendirme.dunya import okunur_tanimlar, tanimlar_yukle
from testler.yardimci import KOK

DOSYA = KOK / "DANISMAN_ICIN_ILISKI_LISTESI.md"
SEMA_YOLU = KOK / "sema" / "iliskiler_v1.json"
SEMA = iliski_semasi_yukle(SEMA_YOLU, KOK / "kilit" / "sema_onayi.json", KOK / "sema" / "iliski_semasi_v1.schema.json")
SATIR = re.compile(r"^\| `(?P<ad>[^`]+)` \| (?P<cinsiyet>[^|]+) \| (?P<ters>[^|]+) \| (?P<simetrik>evet|hayır) \| "
                   r"(?P<islevsel>evet|hayır) \|$")


class DanismanDosyasiTesti(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metin = DOSYA.read_text(encoding="utf-8")

    def test_tablo_onayli_semayla_ayni(self):
        veri = json.loads(SEMA_YOLU.read_text(encoding="utf-8"))
        satirlar = [m.groupdict() for m in map(SATIR.match, self.metin.splitlines()) if m]
        self.assertEqual([s["ad"] for s in satirlar], [r["ad"] for r in veri["iliskiler"]])
        for s, r in zip(satirlar, veri["iliskiler"]):
            self.assertEqual(re.findall(r"`([^`]+)`", s["ters"]), r["ters"], s["ad"])
            self.assertEqual(s["simetrik"] == "evet", r["simetrik"], s["ad"])
            self.assertEqual(s["islevsel"] == "evet", r["islevsel"], s["ad"])
            self.assertIn(s["cinsiyet"].strip(), ("E", "K", "—"), s["ad"])

    def test_sema_ozeti_dogru(self):
        self.assertIn(hashlib.sha256(SEMA_YOLU.read_bytes()).hexdigest(), self.metin)

    def test_ornek_dna_surum_2_ve_onayli_semaya_uyar(self):
        (blok,) = re.findall(r"```json\n(.*?)```", self.metin, flags=re.S)
        hucreler = dna_kur(json.loads(blok), KOK / "sema" / "dna_v2.schema.json", SEMA)
        self.assertEqual(len(hucreler), 1)

    def test_gizli_tanim_metni_yok(self):
        tanimlar = tanimlar_yukle(KOK / "degerlendirme" / "veri" / "tanimlar_v1.json",
                                  KOK / "degerlendirme" / "veri" / "tanimlar_v1.schema.json", SEMA)
        aciklamalar = [satir.split(" | ")[1] for satir in okunur_tanimlar(tanimlar).splitlines()[2:]]
        self.assertEqual(len(aciklamalar), len(SEMA.adlar))
        for aciklama in aciklamalar:
            for secenek in aciklama.rstrip(" |").split(" ya da "):
                self.assertNotIn(secenek, self.metin)


if __name__ == "__main__":
    unittest.main()
