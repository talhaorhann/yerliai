"""KODLAMA_PROMPTU §6: testlerin ortak tarama yardımcıları (kod dosyası listesi, etiket desenleri)."""
import ast
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

# Kod paketleri (testler hariç, V-004)
KOD_KLASORLERI = ("cekirdek", "tercuman", "degerlendirme", "karsilastirma", "araclar", "kesif")  # K-041: kesif

# V-002
ETIKET = r"(sistem\.md §\d+|KODLAMA_PROMPTU §\d+|V-\d{3}|K-\d{3})"
ETIKET_DESENI = re.compile(ETIKET)
BASLIK_DESENI = re.compile(r"(sistem\.md §\d+|KODLAMA_PROMPTU §\d+)")
KIMLIK_DESENI = re.compile(r"\b([VK]-\d{3})\b")


def kod_dosyalari():
    dosyalar = []
    for klasor in KOD_KLASORLERI:
        dosyalar.extend(sorted((KOK / klasor).rglob("*.py")))
    return dosyalar


def goreli(yol):
    return yol.relative_to(KOK).as_posix()


def agac(yol):
    return ast.parse(yol.read_text(encoding="utf-8"), filename=str(yol))


def importlar(yol):
    """(kök modül adı, tam ad, seviye, satır) listesi. Göreli importlarda seviye > 0."""
    sonuc = []
    for dugum in ast.walk(agac(yol)):
        if isinstance(dugum, ast.Import):
            for ad in dugum.names:
                sonuc.append((ad.name.split(".")[0], ad.name, 0, dugum.lineno))
        elif isinstance(dugum, ast.ImportFrom):
            ad = dugum.module or ""
            sonuc.append((ad.split(".")[0], ad, dugum.level, dugum.lineno))
        elif isinstance(dugum, ast.Call) and isinstance(dugum.func, (ast.Name, ast.Attribute)):
            # __import__ ve importlib.import_module ile dolaylı import yasağı
            ad = dugum.func.id if isinstance(dugum.func, ast.Name) else dugum.func.attr
            if ad in ("__import__", "import_module"):
                sonuc.append(("<dinamik>", "<dinamik>", 0, dugum.lineno))
    return sonuc


def kayitli_kimlikler():
    metin = (KOK / "VARSAYIMLAR.md").read_text(encoding="utf-8") + (KOK / "KARARLAR.md").read_text(encoding="utf-8")
    return set(re.findall(r"^## ([VK]-\d{3})", metin, flags=re.MULTILINE))
