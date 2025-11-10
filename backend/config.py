import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    _BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    _DB_PATH = os.path.join(_BASE_DIR, 'database.db')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{_DB_PATH}")
    _UPLOAD_DIR = os.path.join(_BASE_DIR, 'static', 'uploads')
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", _UPLOAD_DIR)
    TEXT_ENGINE = os.getenv("TEXT_ENGINE", "pymupdf")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    # Structuring limits
    STRUCTURE_MAX_CHARS = int(os.getenv("STRUCTURE_MAX_CHARS", "1000000"))
    STRUCTURE_TIMEOUT_SECONDS = int(os.getenv("STRUCTURE_TIMEOUT_SECONDS", "12"))
