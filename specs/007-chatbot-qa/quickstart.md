# Quickstart: Chatbot Q&A from Brochure Data

## Prerequisites
- Backend running (Flask)
- `GEMINI_API_KEY` set in `.env`
- Spec 6 structured JSON available on the frontend

## API Usage
POST http://localhost:5000/chatbot/query
Content-Type: application/json

Example body:
```
{
  "question": "What amenities are available?",
  "context": {
    "project_overview": {
      "project_name": "Emerald Heights",
      "developer_name": "Skyline Builders",
      "location": "Sector 45, Gurgaon"
    },
    "amenities": ["Clubhouse", "Swimming Pool", "Jogging Track", "Gymnasium"],
    "connectivity": { "nearby_schools": ["Delhi Public School"] },
    "floor_plans": [ {"tower_name":"A","bhk_type":"3 BHK","carpet_area":"1600 sq.ft"} ],
    "faqs": [ {"question":"Is it RERA registered?","answer":"Yes"} ]
  }
}
```

Expected response:
```
{ "answer": "Amenities include Clubhouse, Swimming Pool, Jogging Track, and Gymnasium." }
```

## Frontend Integration
- Show floating chat icon only after extraction completes (explicit flag)
- On click: open animated ChatWindow, greet user, accept input, call `/chatbot/query`
- Maintain page-lifetime session history in component state
- Enforce 500-char max for questions (truncate with notice)

## Troubleshooting
- If out-of-scope: expect exact fallback "No idea based on brochure."
- If latency > 600ms: show typing animation
