"""K-032 §4: H2 kapısı. V-053 kapanmadan ve H1 taze tohumlarla yeniden koşulmadan H2 komutu "V-053 açık" diye reddeder.

Kapı yalnız kayıtlara bakar: VARSAYIMLAR.md (V-053 durumu), KARARLAR.md (kapatan kararın kullanıcı onayı),
ONKAYIT.md ("## ÖK-004 sonucu" altında H1 yeniden koşusunun kapı özetinin sha256'sı) ve o özet dosyası (tohumların
hiçbiri ÖK-002/ÖK-003'te kullanılmamış olmalı). Bu testler kapıyı gevşetmeye karşı kilitlidir.
"""
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from degerlendirme import h2

KOK = Path(__file__).resolve().parents[1]
ACIK = "## V-053: Çıkarılabilirlik\n- **Felsefi:** evet. **Durum:** AÇIK.\n\n## V-054: başka\n- **Durum:** KARARA BAĞLANDI (K-099).\n"
KAPALI = "## V-053: Çıkarılabilirlik\n- **Felsefi:** evet. **Durum:** KARARA BAĞLANDI (K-099, 2026-11-01).\n"
KARAR = "## K-099 (2026-11-01): Çıkarılabilirlik tanımı (V-053'ten)\n- **Karar:** ...\n- **Onaylayan:** kullanıcı.\n"


def ozet_dosyasi(tohumlar):
    satirlar = {f"{b}/{t}": {} for b in ("uzunluk", "yon_ters") for t in tohumlar}
    return json.dumps({"kapi": [True, []], "ozet": {"bolmeler": {}, "satirlar": satirlar}}).encode("utf-8")


class SahteDepo:
    def __init__(self, kok, varsayimlar=KAPALI, kararlar=KARAR, tohumlar=(18, 19, 20, 21, 22), ozet_yaz=True,
                 sonuc=True, yanlis_ozet=False):
        (kok / "raporlar").mkdir()
        (kok / "VARSAYIMLAR.md").write_text(varsayimlar, encoding="utf-8")
        (kok / "KARARLAR.md").write_text(kararlar, encoding="utf-8")
        baytlar = ozet_dosyasi(tohumlar)
        if ozet_yaz:
            (kok / h2.H1_YENIDEN_OZETI).write_bytes(baytlar)
        oz = hashlib.sha256(b"baska" if yanlis_ozet else baytlar).hexdigest()
        metin = "## ÖK-004 (2026-11-01)\n...\n"
        if sonuc:
            metin += f"## ÖK-004 sonucu\n- `{h2.H1_YENIDEN_OZETI}`: `{oz}`\n"
        (kok / "ONKAYIT.md").write_text(metin, encoding="utf-8")


class KapiTesti(unittest.TestCase):
    def setUp(self):
        self._d = tempfile.TemporaryDirectory()
        self.kok = Path(self._d.name)

    def tearDown(self):
        self._d.cleanup()

    def reddeder(self, **ayar):
        SahteDepo(self.kok, **ayar)
        with self.assertRaises(h2.H2KapiHatasi) as h:
            h2.kapi_denetle(self.kok)
        self.assertTrue(str(h.exception).startswith("V-053 açık"), str(h.exception))

    def test_bugunku_depoda_reddeder(self):
        with self.assertRaises(h2.H2KapiHatasi) as h:
            h2.kapi_denetle(KOK)
        self.assertTrue(str(h.exception).startswith("V-053 açık"))

    def test_komut_reddeder(self):
        cikti = io.StringIO()
        with redirect_stdout(cikti):
            kod = h2.main([])
        self.assertNotEqual(kod, 0)
        self.assertIn("V-053 açık", cikti.getvalue())

    def test_v053_acik(self):
        self.reddeder(varsayimlar=ACIK)

    def test_kapatan_karar_yok(self):
        self.reddeder(kararlar="## K-098 (2026-11-01): başka (V-053'ten)\n- **Onaylayan:** kullanıcı.\n")

    def test_kapatan_karar_kullanici_onaysiz(self):
        self.reddeder(kararlar=KARAR.replace("kullanıcı", "kodlayıcı"))

    def test_kapatan_karar_v053_anmiyor(self):
        self.reddeder(kararlar=KARAR.replace("V-053", "V-052"))

    def test_h1_yeniden_kosulmadi(self):
        self.reddeder(sonuc=False)

    def test_ozet_dosyasi_yok(self):
        self.reddeder(ozet_yaz=False)

    def test_ozet_tutmuyor(self):
        self.reddeder(yanlis_ozet=True)

    def test_eski_tohumla_kosu_sayilmaz(self):
        for eski in (7, 11, 12, 15, 17):
            with self.subTest(tohum=eski), tempfile.TemporaryDirectory() as d:
                SahteDepo(Path(d), tohumlar=(18, 19, eski, 21, 22))
                with self.assertRaises(h2.H2KapiHatasi):
                    h2.kapi_denetle(Path(d))

    def test_tohumsuz_ozet_sayilmaz(self):
        self.reddeder(tohumlar=())

    def test_butun_kosullar_tutunca_acilir(self):
        SahteDepo(self.kok)
        self.assertEqual(h2.kapi_denetle(self.kok), {"karar": "K-099", "tohumlar": [18, 19, 20, 21, 22]})


if __name__ == "__main__":
    unittest.main()
