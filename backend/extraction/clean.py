import re
from typing import List

NON_UTF8_RE = re.compile(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]")
MULTI_SPACE_RE = re.compile(r"[ \t\u00A0]+")
HYPHEN_LINEBREAK_RE = re.compile(r"(\w)-\n(\w)")
MULTI_NEWLINES_RE = re.compile(r"\n{3,}")


def fix_hyphenated_words(text: str) -> str:
    # Join hyphenated words split across lines: word-\nword -> wordword
    return HYPHEN_LINEBREAK_RE.sub(r"\1\2", text)


def normalize_whitespace(text: str) -> str:
    # Standardize spaces and newlines, keep paragraph breaks
    text = text.replace("\r", "")
    text = MULTI_SPACE_RE.sub(" ", text)
    text = MULTI_NEWLINES_RE.sub("\n\n", text)
    return text.strip()


def remove_non_utf8(text: str) -> str:
    return NON_UTF8_RE.sub("", text)


def clean_text(raw: str) -> str:
    if not raw:
        return ""
    t = remove_non_utf8(raw)
    t = fix_hyphenated_words(t)
    t = normalize_whitespace(t)
    return t
