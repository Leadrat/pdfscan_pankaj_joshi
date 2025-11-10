import pytesseract
import easyocr
import numpy as np
from .utils import get_ocr_langs

_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        langs = get_ocr_langs()
        _reader = easyocr.Reader(langs, gpu=False)
    return _reader


def ocr_pytesseract(image: np.ndarray) -> str:
    return pytesseract.image_to_string(image)


def ocr_easyocr(image: np.ndarray) -> str:
    reader = _get_reader()
    result = reader.readtext(image)
    # result is list of (bbox, text, conf)
    lines = [r[1] for r in result if len(r) > 1]
    return "\n".join(lines)
