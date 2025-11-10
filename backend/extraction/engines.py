import io
from typing import Optional

# PyMuPDF (fitz)
try:
    import fitz  # type: ignore
    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False

# pdfminer.six
try:
    from pdfminer.high_level import extract_text as pdfminer_extract_text  # type: ignore
    HAS_PDFMINER = True
except Exception:
    HAS_PDFMINER = False


def extract_with_pymupdf(path: str) -> str:
    if not HAS_PYMUPDF:
        raise RuntimeError("PyMuPDF not available")
    text_parts = []
    with fitz.open(path) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)


def extract_with_pdfminer(path: str) -> str:
    if not HAS_PDFMINER:
        raise RuntimeError("pdfminer.six not available")
    # pdfminer high-level will read the file and return text
    return pdfminer_extract_text(path) or ""


def extract_text(path: str, engine: str) -> str:
    eng = (engine or "pymupdf").lower()
    if eng == "pdfminer":
        return extract_with_pdfminer(path)
    # default
    return extract_with_pymupdf(path)
