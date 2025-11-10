import os
import json
from typing import Dict, Any, Tuple

try:
    import google.generativeai as genai  # type: ignore
except Exception:
    genai = None  # type: ignore

FALLBACK = "No idea based on brochure."


def _system_instruction() -> str:
    return (
        "You are a real estate chatbot that answers user questions only using the provided project data JSON. "
        "Never invent information. If the answer is not present in the JSON, respond exactly: \"No idea based on brochure.\" "
        "Keep responses short, clear, and friendly. Output JSON only in the form {\"answer\": \"...\"}."
    )


def build_prompt(question: str, context: Dict[str, Any]) -> str:
    payload = {
        "system": _system_instruction(),
        "context_data": context or {},
        "user_question": question or "",
        "output_format": {"answer": "..."},
    }
    return json.dumps(payload, ensure_ascii=False)


def call_gemini(prompt: str) -> Tuple[str, Dict[str, Any]]:
    meta: Dict[str, Any] = {"model": "gemini-2.5-flash"}
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or genai is None:
        # Safe fallback
        return json.dumps({"answer": FALLBACK}), {"fallback": True}
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        resp = model.generate_content([
            {"role": "user", "parts": [prompt]}
        ], generation_config={"temperature": 0.3})
        txt = getattr(resp, "text", "") or (resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else "")
        return txt or "", meta
    except Exception as e:
        meta["error"] = str(e)
        return json.dumps({"answer": FALLBACK}), meta


def _try_parse_answer(txt: str) -> Dict[str, Any]:
    try:
        return json.loads(txt)
    except Exception:
        # Attempt to slice JSON
        s = txt.find("{")
        e = txt.rfind("}")
        if s != -1 and e != -1 and e > s:
            try:
                return json.loads(txt[s:e+1])
            except Exception:
                return {}
        return {}


def validate_response(obj: Dict[str, Any]) -> Tuple[bool, str]:
    if not isinstance(obj, dict):
        return False, "not an object"
    if "answer" not in obj or not isinstance(obj["answer"], str):
        return False, "missing answer"
    return True, "ok"


def ground_answer(question: str, context: Dict[str, Any], raw_txt: str) -> Dict[str, Any]:
    # Parse and enforce fallback behavior
    obj = _try_parse_answer(raw_txt)
    ok, _ = validate_response(obj)
    if not ok:
        return {"answer": FALLBACK}
    ans = (obj.get("answer") or "").strip()
    if not ans:
        return {"answer": FALLBACK}
    # Keep concise
    return {"answer": ans}
