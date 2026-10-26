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
YASAK_IFADELER = ("kendi buldu", "genel zekâ", "genel zeka", "çekirdeğin tek başına keşfi", "kısayol yok",
                  "geçit güvenilir", "bağımsız doğrulama")  # ÖK-005 taslağı §12


def _oku(klasor, ad):
    return json.loads((Path(klasor) / ad).read_text(encoding="utf-8"))


def _k(k):
    return f"τ = {k['tau']}, müdahale = {k['mudahale']}, T = {k['T']}, σ = {k['sigma']}"


def ek3_metni(b1):
    """ÖK-005 eki §3 (B1 sonuçları ve K değerleri). `b1`: B1 çıkış klasörü."""
    s, k, p, c, bos = (_oku(b1, a) for a in ("sonuc.json", "k.json", "p_yildiz.json", "talep.json", "bos_kosular.json"))
    c_metni = f"{c['C']}" + ("" if c["sayim_tamam"] else f" (sayım {c['sayim_ustu']}'de durdu: C > {c['sayim_ustu'] - 1})")
    p_metni = f"> {p['P*'] - 1} (sansürlü; akışta sahte kabul yok)" if p["sansurlu"] else f"{p['P*']}"
    return "\n".join([
        "### ÖK-005 eki §3: B1 sonuçları ve K değerleri",
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
    for a, v in sorted(kr["gizli"].items()):
        satirlar.append(f"| gizli {a} | {v['kural']} | {v['etkin']} | {v['kacak']} |")
    satirlar += [
        "",
        f"- Toplam sahte {kr['sahte_toplam']}, kaçak {kr['kacak']}; yakalama oranı için tek yanlı %95 alt sınır "
        f"{kr['alt_sinir']:.4f} (eşik 0,98).",
        f"- {GIZLI_SINIR}",
        "",
        "## Boş dünya",
        f"- {bos['yapilan']} koşu; kabullü koşu {bos['kabullu_kosu']}; tetik {'oldu' if bos['tetiklendi'] else 'olmadı'}.",
    ]
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
    return "\n".join(satirlar) + "\n"


def yasak_var_mi(metin):
    kucuk = metin.lower()
    return [y for y in YASAK_IFADELER if y in kucuk]
