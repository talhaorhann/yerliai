"""sistem.md §13, §18; K-041, K-043 (ÖK-005 taslağı §8 rapor kalıbı, §12 yasak iddialar), V-065: H2 rapor metinleri.

Metinler yalnız koşu dosyalarındaki sayılardan kurulur. Gizli kırmızı takım için yalnız aile sırası ve sayılar yazılır.
Her raporda zorunlu cümleler: "sayaç + çekirdek hakem hattı" kalıbı ve gizli ailelerin yazarının danışman olduğu
(model ailesi aynı) sınırı. Yasak iddialar (§12) yazılmaz; `YASAK_IFADELER` testte denetlenir.
"""
import json
from pathlib import Path

HAT = "sayaç + çekirdek hakem hattı"  # K-041
GIZLI_SINIR = ("Gizli sahte kural ailelerinin yazarı danışmandır; danışman kodlayıcıyla aynı model ailesindendir. "
               "Bu yüzden gizli aileler tam bağımsız bir sınama sayılmaz.")  # K-043
KESIF = ("KEŞİF DAMGASI (K-044): boş-dünya tetiğinin tanımı B1 sonucundan sonra değişti (\"şema-türevi\" kabuller "
         "tetiğe sayılmaz); bu nedenle B1 ve sonraki sonuçlar önkayıta göre başarı sayılmaz, keşif olarak raporlanır. "
         "İki onarım turundan biri harcandı.")  # K-044
COK_ESLESME = ("Ayrı kaynak (K-044 madde 7): çekirdek bir turda bir kural için en çok 8 sonuç yazar (mühürlü H1 değeri) ve "
               "ilk turda sığmayan eşleşmeleri sonraki turlarda yeniden denemez; çok eşleşen kurallarda maskelenen olgu "
               "türetilemeyebilir, sembolik sayımla uyum bozulur ve aday BİLMİYORUM olur.")
YASAK_IFADELER = ("kendi buldu", "genel zekâ", "genel zeka", "çekirdeğin tek başına keşfi", "kısayol yok",
                  "geçit güvenilir", "bağımsız doğrulama")  # ÖK-005 taslağı §12


def _oku(klasor, ad):
    return json.loads((Path(klasor) / ad).read_text(encoding="utf-8"))


def _k(k):
    return f"τ = {k['tau']}, müdahale = {k['mudahale']}, T = {k['T']}, σ = {k['sigma']}"


def ek3_metni(b1, baslik="### ÖK-005 eki §3: B1 sonuçları ve K değerleri"):
    """ÖK-005 eki (B1 sonuçları ve K değerleri). `b1`: B1 çıkış klasörü."""
    s, k, p, c, bos = (_oku(b1, a) for a in ("sonuc.json", "k.json", "p_yildiz.json", "talep.json", "bos_kosular.json"))
    c_metni = f"{c['C']}" + ("" if c["sayim_tamam"] else f" (sayım {c['sayim_ustu']}'de durdu: C > {c['sayim_ustu'] - 1})")
    p_metni = f"> {p['P*'] - 1} (sansürlü; akışta sahte kabul yok)" if p["sansurlu"] else f"{p['P*']}"
    return "\n".join([
        baslik,
        "",
        f"1. **K değerleri (kalibrasyon kuralıyla):** {_k(k['secilen'])}. Başlangıç: {_k(k['baslangic'])}. "
        f"Kalibrasyonda sahte aday sayısı {k['sahte_sayisi']}; seçilen noktada sahte kabul 0.",
        f"2. **Talep C:** {c_metni}. **P\\*:** {p_metni}. **Tur başına aday:** {p['tur_basina_aday']} (12 tur).",
        f"3. **Boş dünya:** {bos['kosu_sayisi']} koşu kuralı, tetik {bos['tetik']}; yapılan {bos['yapilan']}, "
        f"kabullü koşu {bos['kabullu_kosu']}; tetik {'oldu' if bos['tetiklendi'] else 'olmadı'}.",
        f"4. **B1 sonucu:** {'önkayıttaki başarı aralığında' if s['basari_araliginda'] else 'başarı aralığı dışında'} "
        f"({', '.join(f'{a}: {v}' for a, v in s['sartlar'].items())}).",
        "5. Bu değerler bundan sonra donar; sonuçtan sonra değişirse sonuç \"keşif\" damgası taşır.",
    ])


def b1_raporu(b1):
    s, k, kr, p, c, bos = (_oku(b1, a) for a in ("sonuc.json", "k.json", "kirmizi.json", "p_yildiz.json", "talep.json",
                                                 "bos_kosular.json"))
    satirlar = [
        "# H2 B1 raporu (kabul geçidi, kırmızı takım, kalibrasyon)",
        "",
        f"**Özet:** B1 {'önkayıttaki başarı aralığında' if s['basari_araliginda'] else 'BAŞARI ARALIĞI DIŞINDA'}.",
        "",
        "## Ne yapıldı",
        f"- Geçit: aşama 1–5, {HAT}; K değerleri yalnız görünür sahte kurallar ve boş adaylarla seçildi.",
        f"- Seçilen K: {_k(k['secilen']) if k['secilen'] else 'yok'}.",
        f"- Talep C = {c['C']}; P\\* = {p['P*']}{' (sansürlü)' if p['sansurlu'] else ''}; tur başına {p['tur_basina_aday']} aday.",
        "",
        "## Kırmızı takım",
        "| Aile | Mutant | Sahte | Kaçak |",
        "|---|---|---|---|",
    ]
    for a, v in sorted(kr["gorunur"].items()):
        satirlar.append(f"| {a} (görünür) | {v['mutant']} | {v['sahte']} | {v['kacak']} |")
    gizli = kr["gizli"]
    satirlar.append(f"| gizli (4 aile toplamı) | {sum(v['kural'] for v in gizli.values())} | "
                    f"{sum(v['etkin'] for v in gizli.values())} | {sum(v['kacak'] for v in gizli.values())} |")
    eo = kr.get("etkin_olmayan_gizli")
    satirlar += [
        "",
        f"- Toplam sahte {kr['sahte_toplam']}, kaçak {kr['kacak']}; yakalama oranı için tek yanlı %95 alt sınır "
        f"{kr['alt_sinir']:.4f} (eşik 0,98).",
    ]
    if eo:
        satirlar.append(f"- Geliştirme dünyalarında yanlış vermediği için sahte sayılmayan gizli kural: {eo['sayi']}; "
                        f"geçitteki hükmü: " + ", ".join(f"{h} {n}" for h, n in sorted(eo["hukum"].items())) + ".")
    satirlar += [
        f"- {GIZLI_SINIR}",
        "",
        "## Boş dünya",
        f"- {bos['yapilan']} koşu; tetiğe sayılan kabullü koşu {bos['kabullu_kosu']}; tetik "
        f"{'oldu' if bos['tetiklendi'] else 'olmadı'}.",
    ]
    for x in bos.get("kosular", []):
        satirlar.append(f"  - koşu {x['k']}: sayılan {x['kabul']}, şema-türevi {x.get('sema_turevi_kabul', 0)}, "
                        f"şemadan okunur {x.get('okunur_kabul', 0)}.")
    tani = Path(b1) / "tani_cinsiyet.json"
    if tani.exists():
        t = _oku(b1, "tani_cinsiyet.json")
        satirlar += ["", "## Tanı (c): boş dünyada cinsiyet de karıştırıldı (kapıya girmez)",
                     f"- Kabul {t['kabul_toplam']}: tetiğe sayılacak olan {t['sayilan']}, şema-türevi {t['sema_turevi']}, "
                     f"şemadan okunur {t['okunur']}."]
    if s.get("kesif"):
        satirlar += ["", KESIF]
    return "\n".join(satirlar) + "\n"


def kapi2_ham_raporu(b2):
    r = _oku(b2, "B2b_sonuc.json")
    k = r["karar"]
    a3 = r["a3_aktarim"]["kabul_kumesi"]
    satirlar = [
        "# H2 Kapı 2 ham raporu (B2b, final havuzu, tek atış)",
        "",
        f"**Kalıp (K-041):** {HAT.capitalize()}, K5/21 şablon ailesi içinde, {k['bulunan']}/244 kuralı geri buldu.",
        "",
        f"- Karar: **{k['karar']}** ({', '.join(f'{a}: {v}' for a, v in k['sartlar'].items())}).",
        f"- Geri bulma (özdeş + daha genel + kapanış-eşdeğer): {k['geri_bulma']:.4f}; biçimce (özdeş + daha genel): "
        f"{k['bicimce']:.4f}.",
        f"- Kümeli Wilson alt sınırı ({k['kume_sayisi']} küme): {k['kumeli_wilson']:.4f}.",
        f"- Kabul {k['kabul']}, bozuk {k['bozuk']}; Clopper–Pearson tek yanlı %95 üst sınır {k['cp_ust']:.4f}.",
        f"- Bilmiyorum farkı (kabul kümesi − hedef): {k['bilmiyorum_farki']:.4f}.",
        f"- Sınıflar: {', '.join(f'{a} {v}' for a, v in k['siniflar'].items())}.",
        f"- İkincil paydalar: şemadan okunur 9 hariç {r['ikincil_paydalar']['okunur_haric'][0]}/"
        f"{r['ikincil_paydalar']['okunur_haric'][1]}; örneği olanlar {r['ikincil_paydalar']['ornekli'][0]}/"
        f"{r['ikincil_paydalar']['ornekli'][1]}.",
        "- A3 aktarımı (aile başına kapanış geri bulması): "
        + ", ".join(f"{a} {v['geri_bulma']:.4f}" for a, v in sorted(a3.items())) + ".",
        f"- {GIZLI_SINIR}",
        "- Ön şart: A6 bağımsız inceleme sonucu (K-041) bu raporla birlikte kullanıcıya sunulur.",
    ]
    st = r.get("sema_turevi")
    if st:
        kh = r["karar_sema_turevi_haric"]
        satirlar += [
            f"- Şema-türevi (K-044, ayrı sütun, keşif sayılmaz): kabul edilen {st['kabul']} kuralın {st['kabul_sema_turevi']}'i; "
            f"bulunan {st['bulunan']} hedefin {st['bulunan_sema_turevi']}'i. Şema-türevi bulunanlar hariç geri bulma "
            f"{kh['bulunan']}/244 = {kh['geri_bulma']:.4f} (karar: {kh['karar']}).",
            "  | Sınıf | Bulunan | Şema-türevi |", "  |---|---|---|",
        ] + [f"  | {c} | {v[0]} | {v[1]} |" for c, v in st["bulunan_sinif"].items()]
    nedenler = r.get("arama", {}).get("nedenler", {})
    satirlar += [f"- {COK_ESLESME} Bu koşuda uyum nedeniyle BİLMİYORUM olan aday: {nedenler.get('BİLMİYORUM/uyum', 0)}."]
    if r.get("kesif"):
        satirlar += [f"- {KESIF}"]
    return "\n".join(satirlar) + "\n"


def yasak_var_mi(metin):
    kucuk = metin.lower()
    return [y for y in YASAK_IFADELER if y in kucuk]
