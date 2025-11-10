# Quickstart: Leadrat Spec 1 — Base Environment Setup

## Prerequisites
- Python 3.11
- Node.js 18+

## Backend (Flask)
1. Create venv and activate
   - Windows: `python -m venv venv && .\venv\Scripts\activate`
2. Install deps
   - `pip install flask flask-cors flask-sqlalchemy python-dotenv requests PyMuPDF pdfminer.six`
3. Create `.env` from example
   - Copy `.env.example` → `.env` and set values (e.g., `FRONTEND_ORIGIN`, `GEMINI_API_KEY` placeholder)
4. Run server
   - `python app.py`
5. Test endpoint
   - GET `http://localhost:5000/test` → `{ "message": "Backend connected successfully!" }`

## Frontend (Vite React)
1. Install deps
   - `npm install`
2. Env
   - Create `.env` from `.env.example` with `VITE_API_BASE=http://localhost:5000`
3. Run dev server
   - `npm run dev`
4. Open app
   - http://localhost:5173 — page shows heading and backend message.

## Notes
- CORS defaults to `http://localhost:5173` via env.
- Logs are structured JSON (level, message, context) in backend.
