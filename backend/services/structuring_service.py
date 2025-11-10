import os
import re
import json
import time
from typing import Tuple, Dict, Any, List

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # library may not be installed yet
    genai = None  # type: ignore


REQUIRED_TOP_KEYS = [
    "project_overview",
    "amenities",
    "connectivity",
    "floor_plans",
    "faqs",
]


def _english_only(text: str) -> str:
    if not text:
        return ""
    # Keep basic ASCII + common punctuation; drop non-English letters
    return re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", " ", text)


def _dedupe_lines(text: str) -> str:
    seen = set()
    out = []
    for line in (text or "").splitlines():
        s = line.strip()
        if not s:
            continue
        if s not in seen:
            seen.add(s)
            out.append(s)
    return "\n".join(out)


def _strip_boiler(text: str) -> str:
    t = re.sub(r"\s+", " ", text or " ").strip()
    # Drop common watermarks/boilerplate tokens
    t = re.sub(r"(confidential|watermark|all rights reserved)", " ", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def normalize_inputs(pdf_text: str, ocr_text: str, image_metadata: Dict[str, Any] | None) -> Dict[str, Any]:
    pdf_norm = _dedupe_lines(_strip_boiler(_english_only(pdf_text or "")))
    ocr_norm = _dedupe_lines(_strip_boiler(_english_only(ocr_text or "")))
    merged = _merge_conflicts(pdf_norm, ocr_norm)
    return {
        "pdf_text": pdf_norm,
        "ocr_text": ocr_norm,
        "merged_text": merged,
        "image_metadata": image_metadata or {},
    }


def _merge_conflicts(pdf_text: str, ocr_text: str) -> str:
    # Prefer OCR numeric/context lines when duplicate keys found
    pdf_lines = set((pdf_text or "").splitlines())
    ocr_lines = set((ocr_text or "").splitlines())
    numeric = {l for l in ocr_lines if re.search(r"\d", l)}
    merged = list((pdf_lines - numeric) | ocr_lines)
    return "\n".join(sorted(s for s in merged if s))


def build_prompt(input_data: Dict[str, Any]) -> str:
    schema = {
        "project_overview": {
            "project_name": "",
            "developer_name": "",
            "location": "",
            "description": "",
            "launch_date": "",
            "possession_date": "",
            "rera_number": "",
            "total_towers": "",
            "total_units": "",
            "project_type": "",
        },
        "amenities": [],
        "connectivity": {
            "nearby_schools": [],
            "nearby_hospitals": [],
            "nearby_malls": [],
            "transport_facilities": [],
        },
        "floor_plans": [
            {
                "tower_name": "",
                "bhk_type": "",
                "carpet_area": "",
                "super_area": "",
                "price_range": "",
                "image_reference": "",
            }
        ],
        "faqs": [
            {"question": "", "answer": ""}
        ],
    }
    lead = (
        "You are a structured data extraction expert for real estate brochures. "
        "Return JSON ONLY, strictly following the schema provided. If data is unavailable, use empty strings or empty arrays."
    )
    content = {
        "instruction": lead,
        "input": {
            "pdf_text": input_data.get("pdf_text", ""),
            "ocr_text": input_data.get("ocr_text", ""),
            "image_metadata": input_data.get("image_metadata", {}),
            "project_name": input_data.get("project_name", ""),
        },
        "schema": schema,
    }
    return json.dumps(content, ensure_ascii=False)


def _try_repair_json(txt: str) -> Dict[str, Any]:
    # Attempt to locate first and last braces
    try:
        start = txt.find("{")
        end = txt.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(txt[start : end + 1])
    except Exception:
        pass
    return {}


def _validate_top_shape(obj: Dict[str, Any]) -> bool:
    return all(k in obj for k in REQUIRED_TOP_KEYS)


def _extract_bhk_area(text: str) -> Tuple[str, str]:
    bhk = ""
    area = ""
    m = re.search(r"(\d)\s*BHK", text, re.I)
    if m:
        bhk = f"{m.group(1)} BHK"
    m = re.search(r"(\d{3,5})\s*(sq\.?\s*ft|sqft)", text, re.I)
    if m:
        area = f"{m.group(1)} sq.ft"
    return bhk, area


def _best_image_ref(image_metadata: Dict[str, Any]) -> str:
    # Try to pick first image flagged as Floor Plan; else any key
    if not isinstance(image_metadata, dict):
        return ""
    for k, v in image_metadata.items():
        label = ""
        if isinstance(v, dict):
            label = (v.get("category") or v.get("label") or "").lower()
        elif isinstance(v, str):
            label = v.lower()
        if "floor" in label and "plan" in label:
            return str(k)
    # Fallback to first key
    for k in image_metadata.keys():
        return str(k)
    return ""


def enhance_structured(input_bundle: Dict[str, Any], obj: Dict[str, Any]) -> Dict[str, Any]:
    """Fill missing fields using merged_text heuristics and attach image_reference."""
    text = (input_bundle or {}).get("merged_text", "")
    img_meta = (input_bundle or {}).get("image_metadata", {})
    # Ensure shapes
    obj.setdefault("amenities", [])
    obj.setdefault("connectivity", {})
    obj.setdefault("floor_plans", [])
    obj.setdefault("faqs", [])
    conn = obj["connectivity"]
    for k in ["nearby_schools", "nearby_hospitals", "nearby_malls", "transport_facilities"]:
        conn.setdefault(k, [])

    # Floor plans: fill bhk/area if empty, attach image ref
    if isinstance(obj["floor_plans"], list) and not obj["floor_plans"]:
        # Create one inferred item if text suggests
        bhk, area = _extract_bhk_area(text)
        if bhk or area:
            obj["floor_plans"].append({
                "tower_name": "",
                "bhk_type": bhk,
                "carpet_area": area,
                "super_area": "",
                "price_range": "",
                "image_reference": _best_image_ref(img_meta),
            })
    else:
        for it in obj["floor_plans"]:
            if isinstance(it, dict):
                if not it.get("bhk_type") or not it.get("carpet_area"):
                    bhk, area = _extract_bhk_area(text)
                    it.setdefault("bhk_type", bhk)
                    it.setdefault("carpet_area", area)
                if not it.get("image_reference"):
                    it["image_reference"] = _best_image_ref(img_meta)

    return obj


def call_gemini(prompt: str, timeout_seconds: int = 12) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    meta: Dict[str, Any] = {"duration_ms": 0, "model": "gemini-2.5-flash"}
    start = time.time()
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or genai is None:
        # Fallback: return empty skeleton to keep system functional without API
        obj = {
            "project_overview": {"project_name": "", "developer_name": "", "location": ""},
            "amenities": [],
            "connectivity": {"nearby_schools": [], "nearby_hospitals": [], "nearby_malls": [], "transport_facilities": []},
            "floor_plans": [],
            "faqs": [],
        }
        meta.update({"fallback": True})
        meta["duration_ms"] = round((time.time() - start) * 1000)
        return obj, meta

    genai.configure(api_key=api_key)
    txt = ""
    last_err: Exception | None = None
    delays = [1, 2]  # exponential backoff 1s, 2s (max 2 retries)
    for attempt in range(1 + len(delays)):
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            resp = model.generate_content(
                [
                    {"role": "user", "parts": [prompt]},
                ],
                generation_config={"temperature": 0.25},
            )
            txt = getattr(resp, "text", "") or (resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else "")
            if txt:
                last_err = None
                break
        except Exception as e:
            last_err = e
        # backoff if not last attempt
        if attempt < len(delays):
            try:
                time.sleep(delays[attempt])
            except Exception:
                pass
    if last_err is not None:
        meta["error"] = str(last_err)

    meta["duration_ms"] = round((time.time() - start) * 1000)

    try:
        obj = json.loads(txt)
    except Exception:
        obj = _try_repair_json(txt)
    if not isinstance(obj, dict) or not obj:
        obj = {
            "project_overview": {"project_name": "", "developer_name": "", "location": ""},
            "amenities": [],
            "connectivity": {"nearby_schools": [], "nearby_hospitals": [], "nearby_malls": [], "transport_facilities": []},
            "floor_plans": [],
            "faqs": [],
        }
        meta["repaired"] = True
    return obj, meta


def validate_output(obj: Dict[str, Any]) -> Tuple[bool, str]:
    if not isinstance(obj, dict) or not _validate_top_shape(obj):
        return False, "Top-level keys missing"
    pov = obj.get("project_overview", {}) or {}
    for k in ["project_name", "developer_name", "location"]:
        if k not in pov:
            pov[k] = ""
    return True, "ok"
