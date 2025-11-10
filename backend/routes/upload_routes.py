from flask import Blueprint, jsonify

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend connected successfully!"})

# --- Spec 2: PDF Upload ---
import os
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from db import db
from models.pdf_model import PDFUpload

ALLOWED_EXT = {'.pdf'}
MAX_MB = 20

def _is_pdf_content(file_stream: bytes) -> bool:
    try:
        head = file_stream.read(4)
        file_stream.seek(0)
        # PDF files begin with %PDF
        return head == b'%PDF'
    except Exception:
        return False

def _unique_rename(dest_dir: str, filename: str) -> str:
    name, ext = os.path.splitext(filename)
    i = 1
    candidate = filename
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{name}({i}){ext}"
        i += 1
    return candidate

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    current_app.logger.info('upload attempt', extra={"context": {"route": "/upload"}})
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    # Content-type and magic header check for extra safety
    if file.mimetype not in ('application/pdf', 'application/x-pdf') or not _is_pdf_content(file.stream):
        return jsonify({'error': 'Invalid PDF content'}), 400

    # Size limit (in case MAX_CONTENT_LENGTH not triggered)
    file.stream.seek(0, os.SEEK_END)
    size_bytes = file.stream.tell()
    file.stream.seek(0)
    if size_bytes > MAX_MB * 1024 * 1024:
        return jsonify({'error': 'File too large (max 20MB)'}), 400

    uploads_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(uploads_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    filename = _unique_rename(uploads_dir, filename)
    file_path = os.path.join(uploads_dir, filename)

    try:
        file.save(file_path)
    except Exception:
        current_app.logger.error('file save failed', extra={"context": {"path": file_path}})
        return jsonify({'error': 'Upload failed. Please try again.'}), 500

    size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 2)
    rel_path = f"/static/uploads/{filename}"

    # Persist metadata
    new_file = PDFUpload(filename=filename, size=size_mb, path=rel_path)
    db.session.add(new_file)
    db.session.commit()

    current_app.logger.info('upload success', extra={"context": {"file": filename, "size_mb": size_mb}})
    return jsonify({
        'status': 'success',
        'filename': filename,
        'path': rel_path,
        'size': size_mb,
        'uploaded_at': str(new_file.upload_date)
    }), 200
