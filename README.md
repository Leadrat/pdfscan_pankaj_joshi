# 🏗️ AI-Powered Real Estate Brochure Analyzer (Leadrat)

### 🧠 Project Overview
**Leadrat** is an **AI-driven web platform** that intelligently extracts, analyzes, and visualizes real estate brochure data (PDFs & images) into a **beautiful, auto-generated landing page**.  
Using cutting-edge tools like **Gemini 2.5-Flash**, **PyMuPDF**, **EasyOCR**, and **React**, the app transforms static brochures into dynamic, interactive, and performance-optimized web pages.

---

## 🌟 Features at a Glance

| Spec | Feature | Description |
|------|----------|-------------|
| 🧩 **Spec 1** | PDF Upload & Preview | Secure PDF upload system with animated drag-and-drop UI. |
| 🧩 **Spec 2** | PDF Metadata Extraction | Extracts file name, size, page count, and other metadata. |
| 🧩 **Spec 3** | PDF Text Extraction | Uses PyMuPDF/pdfminer.six to extract and structure text content. |
| 🧩 **Spec 4** | Image Extraction | Captures and categorizes images from PDFs (logos, amenities, floor plans). |
| 🧩 **Spec 5** | OCR & Floor Plan Data | Reads text from images (area, BHK, tower names) using pytesseract + EasyOCR. |
| 🧩 **Spec 6** | Gemini LLM Integration | Combines text + OCR results and generates structured data (Overview, Amenities, FAQs). |
| 🧩 **Spec 7** | Chatbot Integration | Gemini-powered chatbot answers user queries based on extracted data. |
| 🧩 **Spec 8** | Dynamic Landing Page | AI generates a real estate landing page automatically from brochure data. |
| 🧩 **Spec 9** | UI/UX Enhancement | Adds glassmorphism theme, Lottie animations, and smooth transitions. |
| 🧩 **Spec 10** | Error Handling & Logging | Graceful fallback for all errors with toast notifications and logs. |
| 🧩 **Spec 11** | Interactive Visualization & Audit | Adds zoomable image viewer + Lighthouse-optimized performance. |

---

## 🧰 Tech Stack

### 💻 Frontend
- **React.js (Vite)**
- **Tailwind CSS** (Glassmorphism UI)
- **Framer Motion** (Animations)
- **React-Medium-Image-Zoom** (Zoomable Image Viewer)
- **Lottie React** (Success & Transition Animations)

### ⚙️ Backend
- **Python Flask**
- **PyMuPDF / pdfminer.six** — Text Extraction
- **pytesseract + EasyOCR** — OCR & Floor Plan Data
- **SQLite3** — Temporary Data Storage
- **Gemini 2.5-Flash API** — LLM Data Structuring & Chatbot Intelligence

---

## 🎨 Design & Theme Guidelines

- **Primary Gradient:** `from-indigo-500 to-purple-600`  
- **Accent Color:** `emerald-400`  
- **Background:** `#0f172a` (Dark Mode)  
- **Font Family:** Inter / Poppins  
- **UI Style:** Glassmorphism + Rounded-2xl + Soft Shadows  
- **Animations:** Fade-in, Slide-up (Framer Motion)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/leadrat-ai-brochure.git
cd leadrat-ai-brochure
2️⃣ Backend Setup
cd backend
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
pip install -r requirements.txt
python app.py

3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

4️⃣ Environment Variables

Create a .env file in the root folder:

GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
PORT=5000

🚀 How It Works

Upload a PDF brochure → System extracts text, metadata & images.

OCR & Gemini AI analyze the content → structured real estate data is created.

Dynamic landing page auto-generates with sections:

Overview 🏙️

Amenities 🏊‍♂️

Connectivity 🚗

Floor Plans 🏢

FAQs ❓

Chatbot answers property-related questions from extracted data.

Users can zoom images, view carousels, and explore the site interactively.

🔍 Performance & Accessibility
✅ Lighthouse Targets
Category	Target	Achieved
Performance	≥ 90	✅
Accessibility	≥ 90	✅
Best Practices	≥ 90	✅
SEO	≥ 90	✅
🧩 Optimizations

Lazy loading for all images

Code splitting and async imports

ARIA labels for accessibility

Image compression & WebP support

Framer Motion animations optimized for GPU

Lighthouse audit automation in CI/CD (optional)

🧪 Test Plan
Test	Description
✅ PDF Upload Testing	Checks file format & handles errors gracefully.
✅ Text & Image Extraction Validation	Ensures correct parsing of brochure data.
✅ OCR Accuracy	Cross-verifies extracted floor plan details.
✅ Gemini JSON Integrity	Validates schema output (Overview, Amenities, FAQs).
✅ Chatbot Contextual Reply	Tests question-answer reliability based on data.
✅ UI Performance	Measures animation smoothness & load time.
✅ Lighthouse Score Audit	Confirms performance score ≥ 90.
⚡ Error Handling Strategy

Frontend: Toast notifications for errors (invalid PDF, OCR failed, Gemini timeout).

Backend: Structured logging with timestamps.

Fallbacks: If OCR or Gemini fails → partial data displayed with placeholders.

Recovery: Never crashes; UI always remains usable.

💬 Chatbot Instructions

Click 💬 icon after data extraction to open chatbot.

Ask questions like:

“What are the amenities in this project?”

“Tell me about Tower A floor plan.”

“Where is this project located?”

If data not found, bot replies: “No idea based on brochure.”

🧠 Core Design Principles

Simplicity: Minimal, clean, and intuitive flow.

Intelligence: AI-driven structured understanding.

Speed: Async operations with lazy-loading and caching.

Reliability: Strong error handling and logging.

Delight: Smooth animations and professional aesthetics.


🤖 Future Enhancements

Add user login & history of uploaded brochures.

Export structured data as JSON/Excel.

Integrate with Google Maps API for location insights.

Add voice-based Q&A chatbot (Gemini Speech).

Enable auto-deployment to Vercel/Render.

🧩 Contributors

Pankaj Joshi — Full Stack Developer, AI & UI Engineer

📜 License

This project is licensed under the MIT License — you’re free to modify and distribute with attribution.
