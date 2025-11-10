import re
import os
from functools import lru_cache


def normalize_text(text: str) -> str:
    if not text:
        return ""
    # Remove watermark-like repeats and excessive whitespace
    text = re.sub(r"[\t\r]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def safe_join(base: str, *paths: str) -> str:
    p = os.path.abspath(os.path.join(base, *paths))
    if not p.startswith(os.path.abspath(base)):
        raise ValueError("Unsafe path traversal detected")
    return p


@lru_cache(maxsize=1)
def get_ocr_langs() -> list[str]:
    langs = os.getenv("OCR_LANGS", "en,hi")
    return [s.strip() for s in langs.split(",") if s.strip()]
