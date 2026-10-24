"""V-055: iç dil sürüm 1 (sistem.md §17 kapalı iç form): üçlü + kutup + kip + zaman + kaynak + güven.

Biçim ve onaylı şema denetlenir; kayıt özetle mühürlüdür. Havuza yalnız olumlu + kesin + zamansız kayıt girer;
öteki anlamlar kullanıcı kararıdır (NotImplementedError). LLM kaynaklı kayıt karantinasız giremez.
İlişki adları anlamsızdır (blorp şeması)."""
from pathlib import Path

from cekirdek.havuz import Havuz
from cekirdek.ic_dil import (KESIN, OLASI, OLUMSUZ, IcDilHatasi, KarantinaHatasi, havuza_al, ic_kayit,
                            ic_kayit_dogrula)
import testler.test_a3_cekirdek as t3

BICIM = Path(__file__).resolve().parents[1] / "sema" / "ic_dil_v1.schema.json"
ALG = t3.AYAR.deger("hash_algoritmasi")


class IcDilTesti(t3.Ortam):
    def kayit(self, **ek):
        ayar = dict(kaynak="kullanıcı", guven=0.9, algoritma=ALG)
        ayar.update(ek)
        return ic_kayit(1, "blorp", 2, **ayar)

    def dogrula(self, k):
        return ic_kayit_dogrula(k, self.sema, BICIM, ALG)

    def test_gecerli_kayit_ve_ozet(self):
        k = self.kayit()
        self.assertEqual(self.dogrula(k), k)
        self.assertEqual(self.kayit()["ozet"], k["ozet"])  # aynı içerik, aynı özet
        self.assertNotEqual(self.kayit(guven=0.8)["ozet"], k["ozet"])

    def test_degistirilmis_kayit_reddedilir(self):
        k = self.kayit()
        k["nesne"] = 3
        with self.assertRaises(IcDilHatasi):
            self.dogrula(k)

    def test_bicim_disi_reddedilir(self):
        for bozuk in (dict(self.kayit(), kutup="belki"), dict(self.kayit(), ek_alan=1),
                      {a: d for a, d in self.kayit().items() if a != "kip"}, dict(self.kayit(), guven=1.5)):
            with self.subTest(kayit=bozuk), self.assertRaises(IcDilHatasi):
                self.dogrula(bozuk)

    def test_onaysiz_iliski_reddedilir(self):
        with self.assertRaises(IcDilHatasi):
            self.dogrula(ic_kayit(1, "glim", 2, kaynak="kullanıcı", guven=0.9, algoritma=ALG))

    def test_havuza_olumlu_kesin_kayit_girer(self):
        h = Havuz(t3.PRM.kapasite, t3.KK)
        e = havuza_al(h, self.kayit(), self.sema, BICIM, ALG)
        self.assertEqual((e.uclu, e.guven), ((1, "blorp", 2), 0.9))

    def test_olumsuz_olasi_zamanli_kayit_karar_bekliyor(self):
        h = Havuz(t3.PRM.kapasite, t3.KK)
        for ek in ({"kutup": OLUMSUZ}, {"kip": OLASI}, {"zaman": 3}):
            with self.subTest(ek=ek), self.assertRaises(NotImplementedError):
                havuza_al(h, self.kayit(**ek), self.sema, BICIM, ALG)
        self.assertEqual(h.kayitlar(), [])
        self.assertEqual(self.kayit(kip=KESIN)["kip"], KESIN)

    def test_llm_kaydi_karantinasiz_girmez(self):
        h = Havuz(t3.PRM.kapasite, t3.KK)
        with self.assertRaises(KarantinaHatasi):
            havuza_al(h, self.kayit(kaynak="LLM"), self.sema, BICIM, ALG)
        self.assertEqual(h.kayitlar(), [])
