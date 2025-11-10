import os
import json
import time
from flask import Blueprint, request, jsonify, current_app
from config import Config
from services.structuring_service import (
    normalize_inputs,
    build_prompt,
    call_gemini,
    validate_output,
    enhance_structured,
)

structure_bp = Blueprint('structure_bp', __name__)


def _summarize(text: str, max_len: int = 300) -> str:
    text = (text or '').replace('\n', ' ')
    return text[:max_len]


@structure_bp.route('/structure-data', methods=['POST'])
def structure_data():
    ts = time.time()
    payload = request.get_json(silent=True) or {}
    pdf_text = payload.get('pdf_text', '') or ''
    ocr_text = payload.get('ocr_text', '') or ''
    image_metadata = payload.get('image_metadata', {}) or {}
    project_name = payload.get('project_name', '') or ''

    # Guards
    combined_len = len(pdf_text) + len(ocr_text) + len(json.dumps(image_metadata, ensure_ascii=False)) + len(project_name)
    if combined_len > Config.STRUCTURE_MAX_CHARS:
        return jsonify({'status': 'error', 'message': 'Input too large'}), 400

    # Normalize
    norm = normalize_inputs(pdf_text, ocr_text, image_metadata)
    norm['project_name'] = project_name

    # Build prompt
    prompt = build_prompt({
        'pdf_text': norm['pdf_text'],
        'ocr_text': norm['ocr_text'],
        'image_metadata': norm['image_metadata'],
        'project_name': norm.get('project_name', ''),
    })

    # Call model (retry once if invalid)
    try:
        current_app.logger.info('gemini_request sent', extra={'context': {'size': combined_len}})
    except Exception:
        pass
    obj, meta = call_gemini(prompt, timeout_seconds=Config.STRUCTURE_TIMEOUT_SECONDS)
    # Postprocess to enrich floor plans and references
    obj = enhance_structured(norm, obj)
    ok, reason = validate_output(obj)
    if not ok:
        obj, meta2 = call_gemini(prompt, timeout_seconds=Config.STRUCTURE_TIMEOUT_SECONDS)
        obj = enhance_structured(norm, obj)
        meta['retry'] = True
        meta['second'] = meta2
        ok, reason = validate_output(obj)
    duration_ms = round((time.time() - ts) * 1000)

    # Structured logging (summaries only)
    try:
        current_app.logger.info('gemini_request received', extra={'context': {'ok': ok, 'meta': {k: meta.get(k) for k in ['duration_ms','model','fallback','repaired','retry'] if k in meta}}})
        current_app.logger.info('structure-data', extra={
            'context': {
                'duration_ms': duration_ms,
                'size': combined_len,
                'ok': ok,
                'meta': {k: v for k, v in meta.items() if k in ['duration_ms', 'model', 'fallback', 'repaired', 'retry']},
                'pdf_summary': _summarize(norm['pdf_text']),
                'ocr_summary': _summarize(norm['ocr_text']),
            }
        })
    except Exception:
        pass

    if not ok:
        try:
            current_app.logger.error('gemini_request error', extra={'context': {'reason': reason}})
        except Exception:
            pass
        return jsonify({'status': 'error', 'message': 'Failed to structure data'}), 500

    return jsonify({'status': 'success', 'message': 'Structured successfully', 'data': obj}), 200
