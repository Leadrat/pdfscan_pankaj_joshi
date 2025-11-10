import re
from typing import Dict, List

PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[- ]?)?(?:\d{10}|\d{3}[- ]\d{3}[- ]\d{4})\b")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
WEB_RE = re.compile(r"\b(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/[A-Za-z0-9._%/#-]*)?\b")
RERA_RE = re.compile(r"\b(?:RERA|HRERA|MHADA)[- ]?[:#]?[ ]?([A-Za-z0-9-]+)\b", re.IGNORECASE)

AMENITY_KEYWORDS = [
    "gym", "swimming pool", "clubhouse", "security", "parking", "garden",
    "playground", "spa", "theatre", "wifi", "power backup", "lift", "elevator"
]


def _find_first_line_containing(text: str, keys: List[str]) -> str:
    lower = text.lower().splitlines()
    for line in lower:
        for k in keys:
            if k in line:
                return line.strip()
    return ""


def structure_text(cleaned: str) -> Dict:
    amenities: List[str] = []
    low = cleaned.lower()
    for kw in AMENITY_KEYWORDS:
        if kw in low and kw not in amenities:
            amenities.append(kw.title())

    phones = list(set(PHONE_RE.findall(cleaned)))
    emails = list(set(EMAIL_RE.findall(cleaned)))
    websites = list(set(WEB_RE.findall(cleaned)))

    # naive project/developer heuristics
    project_name = _find_first_line_containing(cleaned, ["project", "residency", "heights", "apartments", "residence"]).title() or None
    developer = _find_first_line_containing(cleaned, ["builder", "developers", "developer", "constructions", "infra"]).title() or None

    rera_match = RERA_RE.search(cleaned)
    rera_number = rera_match.group(1) if rera_match else None

    # simple location heuristic
    location = _find_first_line_containing(cleaned, ["sector", "gurgaon", "mumbai", "pune", "bangalore", "delhi", "noida"]).title() or None

    contact = {
        "phone": phones[0] if phones else None,
        "email": emails[0] if emails else None,
        "website": websites[0] if websites else None,
        "address": None,
    }

    # pricing/highlights: naive keyword snippets
    highlights: List[str] = []
    for key in ["near metro", "24x7 security", "spacious", "park facing", "clubhouse"]:
        if key in low:
            highlights.append(key.title())

    data = {
        "project_name": project_name,
        "developer": developer,
        "amenities": amenities,
        "location": location,
        "contact": contact,
        "highlights": highlights,
        "rera_number": rera_number,
    }

    # Apply missing-field policy: ensure lists/objects present
    if data["amenities"] is None:
        data["amenities"] = []
    if data["contact"] is None:
        data["contact"] = {}

    return data
