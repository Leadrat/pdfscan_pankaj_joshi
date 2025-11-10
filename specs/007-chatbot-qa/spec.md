# Feature Specification: Chatbot Q&A from Brochure Data

**Feature Branch**: `007-chatbot-qa`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: Build an intelligent chatbot that answers questions strictly from structured brochure data (PDF + OCR). If a question is outside brochure context, respond: "No idea based on brochure." Chat appears only after data extraction is complete and provides a modern, animated, responsive experience.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Context‑limited answers with fallback (Priority: P1)

As a visitor, I can ask questions about the project and receive clear answers derived only from the brochure’s structured data; if the answer is not present, I’m told politely: "No idea based on brochure."

**Why this priority**: Delivers the core value of trustworthy, brochure‑grounded answers and prevents hallucinations.

**Independent Test**: Provide a question covered by the structured data and receive a correct, concise answer; ask an out‑of‑scope question and receive the fallback phrase.

**Acceptance Scenarios**:

1. **Given** structured data is available, **When** I ask “What amenities are available?”, **Then** the answer lists amenities from the data.
2. **Given** a question not covered by the data, **When** I ask “How far is the airport?”, **Then** the answer is “No idea based on brochure.”

---

### User Story 2 - Chat entry and modern UI (Priority: P2)

As a visitor, I see a floating chat entry point only after brochure data extraction completes; clicking it opens a chat window with smooth animation, greeting, and input.

**Why this priority**: Aligns chat availability with data readiness and provides an engaging experience.

**Independent Test**: Complete extraction → chat icon appears; click → animated window opens with greeting; ask a question → receive answer.

**Acceptance Scenarios**:

1. **Given** extraction is complete, **When** I visit the landing page, **Then** the chat icon is visible with a helpful tooltip.
2. **Given** I click the icon, **When** the chat opens, **Then** I see a greeting and can type a question.

---

### User Story 3 - Session chat history (Priority: P3)

As a visitor, I can see my recent questions and answers in the chat window during my session.

**Why this priority**: Preserves context and improves usability within a single session.

**Independent Test**: Ask multiple questions in one session and see past exchanges maintained in the chat window.

**Acceptance Scenarios**:

1. **Given** an open chat, **When** I ask multiple questions, **Then** the history shows prior messages in order.
2. **Given** I refresh the page (same session scope defined below), **When** I reopen the chat, **Then** the session history policy is respected.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

 - Empty or ambiguous questions
 - Very long questions or repeated queries
 - Missing fields in structured data (must still answer or fallback)
 - Data extraction not complete (chat hidden)
 - Multi‑part questions mixing in/out of scope (answer only in‑scope portion or fallback if none)
 - Mobile and small screens (responsive layout)

## Requirements *(mandatory)*

-->

### Functional Requirements

 - **FR-001**: The system MUST answer using only the provided structured brochure data; no invented content.
 - **FR-002**: The system MUST return the fallback phrase exactly: "No idea based on brochure." when an answer is not present.
 - **FR-003**: The chat entry MUST remain hidden until brochure data extraction is complete.
 - **FR-004**: The chat window MUST open with an animation and display a friendly greeting and input field.
 - **FR-005**: The system MUST maintain in‑session chat history and display it in the chat window.
 - **FR-006**: The system SHOULD respond within typical interactive latency (target ≤ 3 seconds for common queries).
 - **FR-007**: The system MUST keep responses concise, clear, and user‑friendly.
 - **FR-008**: The system MUST accept a user question and the structured data payload as inputs to produce an answer.
 - **FR-009**: The system MUST be resilient to empty/ambiguous questions by asking for clarification or returning the fallback.

 *NEEDS CLARIFICATION (max 3):*

 - **NC-1**: Session scope for history (tab‑lifetime, page‑lifetime, or short persistence)? [NEEDS CLARIFICATION]
 - **NC-2**: Maximum chat message length before truncation? [NEEDS CLARIFICATION]
 - **NC-3**: Visibility trigger for "extraction complete" (explicit flag or inferred)? [NEEDS CLARIFICATION]

### Key Entities *(include if feature involves data)*

- **ChatQuery**: { question, timestamp }
- **ChatAnswer**: { answer, timestamp, grounded: boolean, fallback_used: boolean }
- **ChatSession**: { messages: [ {role, content, ts} ], state: ready|waiting|hidden }
- **BrochureData**: structured JSON with overview, amenities, connectivity, floor plans, FAQs

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

 - **SC-001**: ≥ 95% of in‑scope questions answered correctly from brochure data during evaluation.
 - **SC-002**: Out‑of‑scope questions consistently return the exact fallback phrase.
 - **SC-003**: Typical response time ≤ 3 seconds for common queries in a normal environment.
 - **SC-004**: Chat icon appears only after extraction completion in 100% of tested flows.
 - **SC-005**: Session history preserved during the defined session scope with no loss across ≥ 5 back‑to‑back questions.
