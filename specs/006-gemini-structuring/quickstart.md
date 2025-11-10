# Quickstart: Gemini-Driven Property Data Structuring

## Prerequisites
- Backend: Flask app running (see backend/app.py)
- Env var: `GEMINI_API_KEY` set in `.env`
- Dependencies installed: `pip install -r backend/requirements.txt`

## Input Assembly (example)
```
POST /structure-data
Content-Type: application/json
{
  "pdf_text": "<raw PDF text>",
  "ocr_text": "<merged OCR text>",
  "image_metadata": { "floor_plan_1": { "category": "Floor Plan" } },
  "project_name": "Optional hint"
}
```

## Expected Output Skeleton
```
{
  "project_overview": { ... },
  "amenities": [ ... ],
  "connectivity": { ... },
  "floor_plans": [ ... ],
  "faqs": [ ... ]
}
```

## Validation
- Enforce English-only text before send
- Cap combined input length ≤ 1,000,000 chars
- Expect response within 12s
- Validate JSON against OpenAPI schema (contracts/openapi.yaml)

## Logs
- Log summaries + metrics only (no raw LLM content)

## Testing Steps
1. Start backend: `python backend/app.py`
2. Prepare sample payloads from previously extracted text and OCR results
3. Call `POST /structure-data`
4. Verify response structure and minimal overview fields (name, developer, location)
