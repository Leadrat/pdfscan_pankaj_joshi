from datetime import datetime
from db import db


class OCRExtracted(db.Model):
    __tablename__ = 'ocr_extracted_data'
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(64), nullable=True)
    extracted_text = db.Column(db.Text, nullable=True)
    structured_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
