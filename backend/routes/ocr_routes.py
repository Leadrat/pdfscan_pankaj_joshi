import os
import json
import time
from flask import Blueprint, jsonify, current_app
from werkzeug.utils import secure_filename

from db import db
from models.ocr_extracted import OCRExtracted
from ocr.preprocess import preprocess_image, save_processed, ensure_processed_dir
from ocr.engines import ocr_pytesseract, ocr_easyocr
from ocr.extract import merge_texts, build_structured

ocr_bp = Blueprint('ocr_bp', __name__)

IMAGES_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'images'))


def _list_images(root: str) -> list[str]:
    if not os.path.isdir(root):
        return []
    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'}
    return [f for f in os.listdir(root) if os.path.splitext(f.lower())[1] in exts]


@ocr_bp.route('/extract-ocr-data', methods=['POST'])
def extract_ocr_data():
    start = time.time()
    try:
        current_app.logger.info('ocr_extraction started', extra={'context': {}})
    except Exception:
        pass
    os.makedirs(IMAGES_ROOT, exist_ok=True)
    ensure_processed_dir(IMAGES_ROOT)

    files = _list_images(IMAGES_ROOT)
    if not files:
        return jsonify({'status': 'error', 'message': 'No images found in static/images/'}), 400

    results = []
    for name in files:
        safe_name = secure_filename(name)
        try:
            in_path = os.path.join(IMAGES_ROOT, safe_name)
            img = preprocess_image(in_path)
            # Save processed image (best-effort)
            try:
                save_processed(img, IMAGES_ROOT, safe_name)
            except Exception:
                pass
            # OCR
            t1 = ocr_pytesseract(img)
            t2 = ocr_easyocr(img)
            merged = merge_texts(t1, t2)
            payload = build_structured(safe_name, merged)

            # Store
            rec = OCRExtracted(
                image_name=safe_name,
                category=payload.get('category'),
                extracted_text=payload.get('raw_text'),
                structured_json=json.dumps(payload.get('details', {}), ensure_ascii=False),
            )
            db.session.add(rec)
            db.session.commit()

            results.append(payload)
        except Exception as e:
            results.append({
                'image': safe_name,
                'error': 'Text not detected'
            })
            try:
                current_app.logger.error('ocr_extraction failed', extra={'context': {'image': safe_name}})
            except Exception:
                pass
    duration_ms = round((time.time() - start) * 1000)
    try:
        current_app.logger.info('ocr_extraction completed', extra={'context': {'count': len(results), 'duration_ms': duration_ms}})
    except Exception:
        pass
    return jsonify({'status': 'success', 'message': 'OCR complete', 'data': results}), 200
