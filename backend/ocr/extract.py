import re
import json
from typing import Dict, Any

from .utils import normalize_text


def merge_texts(t1: str, t2: str) -> str:
    # Prefer longer content after normalization
    s1 = normalize_text(t1)
    s2 = normalize_text(t2)
    if len(s2) > len(s1):
        base = s2
        other = s1
    else:
        base = s1
        other = s2
    # Deduplicate by lines
    lines = set([l.strip() for l in base.split("\n") if l.strip()])
    for l in other.split("\n"):
        l = l.strip()
        if l:
            lines.add(l)
    return "\n".join(sorted(lines))


def categorize_text(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["bhk", "sq.ft", "sqft", "floor plan", "carpet area", "built-up"]):
        return "Floor Plan"
    if any(k in t for k in ["gym", "club", "amenities", "pool", "play area", "garden"]):
        return "Amenities"
    if any(k in t for k in ["map", "road", "location", "avenue"]):
        return "Location Map"
    return "General"


def extract_fields(text: str) -> Dict[str, Any]:
    out = {}
    # tower
    m = re.search(r"tower\s*([A-Za-z0-9-]+)", text, re.I)
    if m:
        out["tower"] = m.group(1)
    # bhk
    m = re.search(r"(\d)\s*BHK", text, re.I)
    if m:
        out["bhk"] = int(m.group(1))
    # areas
    m = re.search(r"(\d{3,5})\s*(sq\.?\s*ft|sqft)", text, re.I)
    if m:
        out["area_sqft"] = int(m.group(1))
    # price (very rough)
    m = re.search(r"₹?\s*([0-9]+(?:,[0-9]{2,3})*(?:\.[0-9]+)?)\s*(lac|lakh|cr|crore|rs|inr)?", text, re.I)
    if m:
        out["price_raw"] = m.group(0)
    # amenities
    amns = []
    for k in ["gym", "club", "pool", "garden", "play", "security"]:
        if re.search(rf"\b{k}\b", text, re.I):
            amns.append(k)
    if amns:
        out["amenities"] = sorted(set(amns))
    return out


def build_structured(image_name: str, merged_text: str) -> dict:
    return {
        "image": image_name,
        "category": categorize_text(merged_text),
        "details": extract_fields(merged_text),
        "raw_text": merged_text,
    }
