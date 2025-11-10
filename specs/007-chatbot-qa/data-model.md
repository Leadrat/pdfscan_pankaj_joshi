# Data Model: Chatbot Q&A from Brochure Data

## Entities

### BrochureData
- project_overview: object
- amenities: string[]
- connectivity: object
- floor_plans: object[]
- faqs: object[]

### ChatQuery
- question: string (≤ 500 chars)
- timestamp: ISO string

### ChatAnswer
- answer: string
- timestamp: ISO string
- grounded: boolean (true if derived from context)
- fallback_used: boolean (true if fallback phrase returned)

### ChatSession
- messages: Array<{ role: "user"|"assistant", content: string, ts: ISO string }>
- state: "hidden" | "ready" | "waiting"

## Validation Rules
- Answers must be derived solely from BrochureData; otherwise fallback phrase.
- Enforce question length ≤ 500; truncate if longer with a notice.
- Session scope: page-lifetime; reset on full reload.

## Relationships & Identity
- One ChatSession per page instance.
- Each ChatQuery has exactly one ChatAnswer.
