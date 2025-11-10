# Data Model: Leadrat Spec 1 — Base Environment Setup

Scope: Minimal entities to support environment bootstrapping and future specs. No business logic yet.

## Entities

### PDFUpload
- id: Integer (PK)
- filename: String(120), required
- upload_date: DateTime, default current_timestamp

Notes:
- Table creation validated in Spec 1 via `db.create_all()`.
- Additional fields (filesize, mime_type, checksum, status) deferred to Spec 2.

### Config (runtime)
- FRONTEND_ORIGIN (for CORS)
- GEMINI_API_KEY (placeholder for later specs)
- SQLALCHEMY_DATABASE_URI = sqlite:///database.db
- UPLOAD_FOLDER = static/uploads
- VITE_API_BASE (frontend)

Notes:
- `.env.example` supplies placeholders; `.env` is gitignored.
- Secrets MUST NOT be logged.
