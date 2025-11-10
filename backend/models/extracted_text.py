from datetime import datetime
from db import db

class ExtractedText(db.Model):
    __tablename__ = 'extracted_text'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, index=True)
    raw_text = db.Column(db.Text, nullable=False)
    structured_data = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
