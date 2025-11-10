import os
import io
import time
from datetime import datetime
from typing import List
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from PIL import Image

from config import Config
from db import db
from models.extracted_image import ExtractedImage

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False

image_bp = Blueprint('image_bp', __name__)

def _sanitize_filename(name: str) -> str:
    return secure_filename(name or '')

def _resolve_pdf_path(filename: str) -> str:
    candidates = [
        os.path.join(Config.UPLOAD_FOLDER, filename),
        os.path.join(Config.UPLOAD_FOLDER, 'temp', filename),
    ]
    for p in candidates:
        ap = os.path.abspath(p)
        if ap.startswith(os.path.dirname(Config.UPLOAD_FOLDER)) and os.path.exists(ap):
            return ap
    return ''

def _save_png(img: Image.Image, base_dir: str, out_name: str) -> str:
    os.makedirs(base_dir, exist_ok=True)
    out_path = os.path.join(base_dir, out_name)
    img.save(out_path, format='PNG')
    # compress if > 2MB by reducing size ~25%
    try:
        if os.path.getsize(out_path) > 2 * 1024 * 1024:
            w, h = img.size
            resized = img.resize((int(w * 0.75), int(h * 0.75)), Image.LANCZOS)
            resized.save(out_path, format='PNG')
    except Exception:
        pass
    return out_path

@image_bp.route('/extract-images', methods=['POST'])
def extract_images():
    start = time.time()
    if not HAS_PYMUPDF:
        return jsonify({'status': 'error', 'message': 'PyMuPDF not available'}), 500

    filename = _sanitize_filename(request.args.get('filename', '').strip())
    if not filename:
        return jsonify({'status': 'error', 'message': 'filename query param required'}), 400

    reextract = (request.args.get('reextract', 'false').lower() == 'true')

    # if already extracted and not forcing, return existing
    if not reextract:
        existing: List[ExtractedImage] = (
            ExtractedImage.query.filter_by(filename=filename).order_by(ExtractedImage.id.asc()).all()
        )
        if existing:
            images = []
            for rec in existing:
                images.append({
                    'id': rec.id,
                    'filename': rec.filename,
                    'page_number': rec.page_number,
                    'dimensions': f"{rec.width}x{rec.height}",
                    'url': rec.file_path,
                })
            duration = round((time.time() - start) * 1000)
            current_app.logger.info('image extract cached', extra={"context": {"file": filename, "total": len(images), "duration_ms": duration}})
            return jsonify({'status': 'success', 'total_images': len(images), 'images': images}), 200

    pdf_path = _resolve_pdf_path(filename)
    if not pdf_path:
        return jsonify({'status': 'error', 'message': 'File not found'}), 400

    images_dir = os.path.abspath(os.path.join(os.path.dirname(Config.UPLOAD_FOLDER), 'images'))

    # If reextract, delete existing DB rows for this filename
    if reextract:
        try:
            ExtractedImage.query.filter_by(filename=filename).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()

    extracted_count = 0
    results = []
    try:
        doc = fitz.open(pdf_path)
        base_name, _ = os.path.splitext(os.path.basename(filename))
        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            imgs = page.get_images(full=True)
            for img_index, img in enumerate(imgs, start=1):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image.get('image')
                    pil_img = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
                    w, h = pil_img.size
                    out_name = f"{base_name}_page{page_index+1}_img{img_index}.png"
                    out_path = _save_png(pil_img, images_dir, out_name)
                    rel_url = f"/static/images/{out_name}"
                    rec = ExtractedImage(
                        filename=out_name,
                        page_number=page_index + 1,
                        width=w,
                        height=h,
                        file_path=rel_url,
                    )
                    db.session.add(rec)
                    db.session.flush()
                    results.append({
                        'id': rec.id,
                        'filename': out_name,
                        'page_number': page_index + 1,
                        'dimensions': f"{w}x{h}",
                        'url': rel_url,
                    })
                    extracted_count += 1
                except Exception:
                    continue
        db.session.commit()
    except Exception:
        current_app.logger.error('image extract failed', extra={"context": {"file": filename}})
        return jsonify({'status': 'error', 'message': 'Failed to extract images from PDF'}), 500

    if extracted_count == 0:
        return jsonify({'status': 'error', 'message': 'No images found in PDF.'}), 200

    duration = round((time.time() - start) * 1000)
    current_app.logger.info('image extract success', extra={"context": {"file": filename, "total": extracted_count, "duration_ms": duration}})
    return jsonify({'status': 'success', 'total_images': extracted_count, 'images': results}), 200
