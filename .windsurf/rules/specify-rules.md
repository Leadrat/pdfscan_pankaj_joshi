# eleven_specs Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-10

## Active Technologies
- Python 3.11 + Flask, Flask-CORS, Flask-SQLAlchemy, google-generativeai, python-dotenv, logging (006-gemini-structuring)
- SQLite (persist structured JSON and minimal audit logs) (006-gemini-structuring)
- React 18 (Vite) + TailwindCSS, Framer Motion, React Image Lightbox (or similar), Axios (008-dynamic-landing)
- None required (client-side only; JSON provided by Spec 6) (008-dynamic-landing)
- React 18+ (frontend), Python 3.11+ (backend) + react-medium-image-zoom, Framer Motion, React.lazy/Suspense, TailwindCSS, WebP, pytesseract/EasyOCR (011-interactive-visualization)
- `/uploads` for PDFs, `/static/images/` for extracted images, SQLite for metadata (011-interactive-visualization)

- Backend Python 3.11; Frontend Vite (Node 18+). + Flask, Flask-CORS, SQLAlchemy, python-dotenv; React, TailwindCSS, Framer Motion, Axios, React Router. (001-base-setup)

## Project Structure

```text
backend/
frontend/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Backend Python 3.11; Frontend Vite (Node 18+).: Follow standard conventions

## Recent Changes
- 011-interactive-visualization: Added React 18+ (frontend), Python 3.11+ (backend) + react-medium-image-zoom, Framer Motion, React.lazy/Suspense, TailwindCSS, WebP, pytesseract/EasyOCR
- 008-dynamic-landing: Added React 18 (Vite) + TailwindCSS, Framer Motion, React Image Lightbox (or similar), Axios
- 006-gemini-structuring: Added Python 3.11 + Flask, Flask-CORS, Flask-SQLAlchemy, google-generativeai, python-dotenv, logging


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
