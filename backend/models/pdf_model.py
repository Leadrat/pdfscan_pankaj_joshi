from db import db

class PDFUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    size = db.Column(db.Float)
    path = db.Column(db.String(255))
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
