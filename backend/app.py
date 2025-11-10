from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime
import os

load_dotenv()

# Config
from config import Config
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB

# CORS (ENV-configurable, default to localhost:5173)
CORS(app, resources={r"/*": {"origins": [Config.FRONTEND_ORIGIN]}})

# DB
db.init_app(app)

# Structured JSON logging
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Optional context
        if hasattr(record, "context") and isinstance(record.context, dict):
            payload["context"] = record.context
        return json.dumps(payload, ensure_ascii=False)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.setLevel(logging.INFO)
app.logger.handlers = [handler]
logging.getLogger("werkzeug").handlers = [handler]

# Routes
from routes.upload_routes import upload_bp  # noqa: E402
from routes.extract_routes import extract_bp  # noqa: E402
from routes.image_routes import image_bp  # noqa: E402
from routes.ocr_routes import ocr_bp  # noqa: E402
from routes.structure_routes import structure_bp  # noqa: E402
from routes.chatbot_routes import chatbot_bp  # noqa: E402
app.register_blueprint(upload_bp)
app.register_blueprint(extract_bp)
app.register_blueprint(image_bp)
app.register_blueprint(ocr_bp)
app.register_blueprint(structure_bp)
app.register_blueprint(chatbot_bp)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# Ensure temp directory exists
temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
os.makedirs(temp_dir, exist_ok=True)
# Ensure images directory exists
images_dir = os.path.join(os.path.dirname(app.config['UPLOAD_FOLDER']), 'images')
os.makedirs(images_dir, exist_ok=True)
# Ensure processed images directory exists
processed_dir = os.path.join(images_dir, 'processed')
os.makedirs(processed_dir, exist_ok=True)

# Rotating file logger (JSON) under /logs
try:
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    file_path = os.path.join(logs_dir, 'app.log')
    rfh = RotatingFileHandler(file_path, maxBytes=10 * 1024 * 1024, backupCount=5)
    rfh.setFormatter(JsonFormatter())
    app.logger.addHandler(rfh)
    # 7-day cleanup (best-effort)
    try:
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=7)
        for name in os.listdir(logs_dir):
            fp = os.path.join(logs_dir, name)
            try:
                if os.path.isfile(fp) and name.startswith('app.log'):
                    mtime = datetime.utcfromtimestamp(os.path.getmtime(fp))
                    if mtime < cutoff:
                        os.remove(fp)
            except Exception:
                pass
    except Exception:
        pass
except Exception:
    pass

# Models (import after db created)
from models.pdf_model import PDFUpload  # noqa: E402,F401
from models.ocr_extracted import OCRExtracted  # noqa: E402,F401

# DB init
with app.app_context():
    db.create_all()
    app.logger.info("database initialized", extra={"context": {"db": app.config['SQLALCHEMY_DATABASE_URI']}})


@app.after_request
def _after_request_log(response):
    try:
        app.logger.info('ui_render', extra={"context": {"path": getattr(getattr(response, 'request', None), 'path', ''), "status": response.status_code}})
    except Exception:
        pass
    return response


if __name__ == "__main__":
    app.logger.info("starting server", extra={"context": {"port": 5000}})
    app.run(debug=True, port=5000)
