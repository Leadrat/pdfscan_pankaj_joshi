import os
import json
import time
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from config import Config
from db import db
from models.extracted_text import ExtractedText
from extraction.engines import extract_text as extract_engine_text
from extraction.clean import clean_text
from extraction.structure import structure_text

extract_bp = Blueprint('extract_bp', __name__)

SAFE_UPLOADS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static', 'uploads')
SAFE_UPLOADS_DIR = os.path.abspath(os.path.join(SAFE_UPLOADS_DIR))
TEMP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static', 'uploads', 'temp')
TEMP_DIR = os.path.abspath(TEMP_DIR)


def _sanitize_filename(name: str) -> str:
    # Use werkzeug secure_filename and ensure no path traversal remains
    name = secure_filename(name or '')
    return name


def _resolve_pdf_path(filename: str) -> str:
    # Try main uploads dir first, then temp dir
    candidates = [
        os.path.join(Config.UPLOAD_FOLDER, filename),
        os.path.join(TEMP_DIR, filename),
    ]
    for p in candidates:
        ap = os.path.abspath(p)
        # ensure under uploads root
        if ap.startswith(os.path.dirname(Config.UPLOAD_FOLDER)) and os.path.exists(ap):
            return ap
    return ''


def _purge_temp_and_db():
    try:
        cutoff = datetime.utcnow() - timedelta(hours=24)
        # DB purge
        ExtractedText.query.filter(ExtractedText.created_at < cutoff).delete()
        db.session.commit()
        # Files purge
        if os.path.isdir(TEMP_DIR):
            for f in os.listdir(TEMP_DIR):
                fp = os.path.join(TEMP_DIR, f)
                try:
                    if os.path.isfile(fp):
                        mtime = datetime.utcfromtimestamp(os.path.getmtime(fp))
                        if mtime < cutoff:
                            os.remove(fp)
                except Exception:
                    pass
    except Exception:
        pass


@extract_bp.route('/extract-text', methods=['GET'])
def extract_text_route():
    start = time.time()
    filename = request.args.get('filename', '').strip()
    filename = _sanitize_filename(filename)
    if not filename:
        return jsonify({'status': 'error', 'message': 'filename query param required'}), 400

    # Fast path: return existing if present
    existing = ExtractedText.query.filter_by(filename=filename).order_by(ExtractedText.id.desc()).first()
    if existing:
        try:
            data = json.loads(existing.structured_data)
        except Exception:
            data = {}
        duration = round((time.time() - start) * 1000)
        current_app.logger.info('extract fetch cached', extra={"context": {"file": filename, "duration_ms": duration}})
        return jsonify({
            'status': 'success',
            'message': 'Text fetched successfully',
            'data': data,
            'raw_text_length': len(existing.raw_text or '')
        }), 200

    # Resolve path
    path = _resolve_pdf_path(filename)
    if not path:
        return jsonify({'status': 'error', 'message': 'File not found'}), 400

    # Extraction
    try:
        engine = Config.TEXT_ENGINE
        raw = extract_engine_text(path, engine)
        cleaned = clean_text(raw)
        structured = structure_text(cleaned)
    except Exception:
        current_app.logger.error('extract failed', extra={"context": {"file": filename}})
        return jsonify({'status': 'error', 'message': 'Failed to extract text from PDF'}), 500

    # Store
    rec = ExtractedText(
        filename=filename,
        raw_text=cleaned,
        structured_data=json.dumps(structured, ensure_ascii=False),
    )
    db.session.add(rec)
    db.session.commit()

    # Purge (best-effort)
    _purge_temp_and_db()

    duration = round((time.time() - start) * 1000)
    current_app.logger.info('extract success', extra={"context": {"file": filename, "duration_ms": duration}})
    return jsonify({
        'status': 'success',
        'message': 'Text extracted successfully',
        'data': structured,
        'raw_text_length': len(cleaned)
    }), 200
