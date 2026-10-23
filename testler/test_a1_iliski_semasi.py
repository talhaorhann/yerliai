"""KODLAMA_PROMPTU §2.6, §6 (şemaya sessizce ilişki eklemek): onaylı tek sürümlü ilişki şeması (V-013).

Testler anlamsız ilişki adlarıyla ("blorp" şeması) yazılır. Çekirdek hiçbir ilişki adını bilmemelidir.
"""
import json
import tempfile
import unittest
from pathlib import Path

from araclar.sema_onayla import onay_kaydi_yaz, okunur_tablo
from cekirdek.altyapi.sema_dogrulayici import SemaHatasi
from cekirdek.iliski_semasi import SemaOnayHatasi, iliski_semasi_yukle
from testler.yardimci import KOK

BICIM = KOK / "sema" / "iliski_semasi_v1.schema.json"


def blorp_semasi():
    return {
        "sema_surumu": "1",
        "okuma": "(A, r, B) = B, A'nın r'sidir.",
        "iliskiler": [
            {"ad": "blorp", "ters": ["zindle", "quax"], "simetrik": False, "islevsel": True},
            {"ad": "zindle", "ters": ["blorp"], "simetrik": False, "islevsel": False},
            {"ad": "quax", "ters": ["blorp"], "simetrik": False, "islevsel": False},
            {"ad": "frumb", "ters": ["frumb"], "simetrik": True, "islevsel": False},
            {"ad": "vonk", "ters": [], "simetrik": False, "islevsel": False},
        ],
        "dislayici_gruplar": [["blorp", "zindle"], ["quax", "frumb", "vonk"]],
    }


class SemaOrtami:
    def __init__(self, veri, onayla=True):
        self._d = tempfile.TemporaryDirectory()
        self.klasor = Path(self._d.name)
        self.sema = self.klasor / "iliskiler_v1.json"
        self.onay = self.klasor / "sema_onayi.json"
        self.sema.write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
        if onayla:
            onay_kaydi_yaz(self.sema, self.onay, "K-001")

    def yukle(self):
        return iliski_semasi_yukle(self.sema, self.onay, BICIM)

    def kapat(self):
        self._d.cleanup()


class OnayTesti(unittest.TestCase):
    def test_onayli_sema_yuklenir(self):
        o = SemaOrtami(blorp_semasi())
        try:
            s = o.yukle()
            self.assertEqual(s.adlar, ("blorp", "zindle", "quax", "frumb", "vonk"))
            self.assertEqual(s.ters("blorp"), ("zindle", "quax"))
            self.assertTrue(s.simetrik("frumb"))
            self.assertTrue(s.islevsel("blorp"))
            self.assertFalse(s.islevsel("zindle"))
            self.assertTrue(s.dislayici_mi("blorp", "zindle"))
            self.assertTrue(s.dislayici_mi("vonk", "quax"))
            self.assertFalse(s.dislayici_mi("blorp", "quax"))
            self.assertFalse(s.dislayici_mi("blorp", "blorp"))
            self.assertIn("blorp", s)
            self.assertNotIn("glim", s)
        finally:
            o.kapat()

    def test_onaysiz_sema_yuklenmez(self):
        o = SemaOrtami(blorp_semasi(), onayla=False)
        try:
            with self.assertRaises(SemaOnayHatasi):
                o.yukle()
        finally:
            o.kapat()

    def test_onaydan_sonra_sessizce_eklenen_iliski_yakalanir(self):
        o = SemaOrtami(blorp_semasi())
        try:
            veri = blorp_semasi()
            veri["iliskiler"].append({"ad": "glim", "ters": [], "simetrik": False, "islevsel": False})
            o.sema.write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(SemaOnayHatasi):
                o.yukle()
        finally:
            o.kapat()

    def test_tek_bayt_degisikligi_yakalanir(self):
        o = SemaOrtami(blorp_semasi())
        try:
            o.sema.write_bytes(o.sema.read_bytes() + b" ")
            with self.assertRaises(SemaOnayHatasi):
                o.yukle()
        finally:
            o.kapat()

    def test_onay_kaydi_karar_kimligi_ister(self):
        o = SemaOrtami(blorp_semasi(), onayla=False)
        try:
            for kotu in ("", "evet", "V-001", "K-1"):
                with self.assertRaises(ValueError):
                    onay_kaydi_yaz(o.sema, o.onay, kotu)
        finally:
            o.kapat()

    def test_bozuk_onay_kaydi_reddedilir(self):
        o = SemaOrtami(blorp_semasi())
        try:
            kayit = json.loads(o.onay.read_text(encoding="utf-8"))
            kayit["fazla"] = 1
            o.onay.write_text(json.dumps(kayit), encoding="utf-8")
            with self.assertRaises(SemaOnayHatasi):
                o.yukle()
        finally:
            o.kapat()


class TutarlilikTesti(unittest.TestCase):
    def reddedilir(self, degistir):
        veri = blorp_semasi()
        degistir(veri)
        o = SemaOrtami(veri)
        try:
            with self.assertRaises(SemaHatasi):
                o.yukle()
        finally:
            o.kapat()

    def test_yinelenen_ad(self):
        self.reddedilir(lambda v: v["iliskiler"].append(dict(v["iliskiler"][0])))

    def test_bilinmeyen_ters(self):
        self.reddedilir(lambda v: v["iliskiler"][0]["ters"].append("glim"))

    def test_tek_yonlu_ters(self):
        self.reddedilir(lambda v: v["iliskiler"][1].update(ters=[]))

    def test_simetrik_ama_tersi_kendisi_degil(self):
        self.reddedilir(lambda v: v["iliskiler"][3].update(ters=["vonk"]))

    def test_dislayici_grupta_bilinmeyen_ad(self):
        self.reddedilir(lambda v: v["dislayici_gruplar"].append(["blorp", "glim"]))

    def test_bicim_ihlali(self):
        self.reddedilir(lambda v: v["iliskiler"][0].update(tanim="yukarı, yukarı"))
        self.reddedilir(lambda v: v.update(sema_surumu="2"))
        self.reddedilir(lambda v: v["iliskiler"][0].update(ad="Blorp"))


class TaslakTesti(unittest.TestCase):
    """Proje şeması kullanıcı onayı olmadan yüklenemez (V-013); onay yoksa sonuç SemaOnayHatasi olmalı."""

    def test_proje_semasi_bicime_uyar_ve_onay_durumu_tutarli(self):
        sema = KOK / "sema" / "iliskiler_v1.json"
        onay = KOK / "kilit" / "sema_onayi.json"
        if onay.exists():
            iliski_semasi_yukle(sema, onay, BICIM)
        else:
            with self.assertRaises(SemaOnayHatasi):
                iliski_semasi_yukle(sema, onay, BICIM)
            from cekirdek.iliski_semasi import _dogrula_ve_kur
            _dogrula_ve_kur(json.loads(sema.read_text(encoding="utf-8")), BICIM)

    def test_okunur_tablo_her_iliskiyi_icerir(self):
        tablo = okunur_tablo(KOK / "sema" / "iliskiler_v1.json")
        for iliski in json.loads((KOK / "sema" / "iliskiler_v1.json").read_text(encoding="utf-8"))["iliskiler"]:
            self.assertIn(f"| {iliski['ad']} |", tablo)


if __name__ == "__main__":
    unittest.main()
