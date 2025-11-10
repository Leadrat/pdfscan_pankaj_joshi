# Feature Specification: Gemini-Driven Property Data Structuring

**Feature Branch**: `006-gemini-structuring`  
**Created**: 2025-11-10  
**Status**: Draft  
**Input**: User description: "Integrate Google Gemini 2.5-Flash model to analyze all extracted textual and visual data from PDFs and images (OCR results, metadata, and structured text). The model should intelligently understand the document context and produce clean, structured JSON data that can be used for property visualization, display, and insights. Context: existing modules cover upload, UI, PDF text extraction, image extraction, OCR; objective is to combine outputs and return consistent schema across properties."

## Clarifications

### Session 2025-11-10

- Q: Conflict resolution priority between PDF text and OCR text? → A: Prefer OCR if it contains explicit numeric patterns or clearer context.
- Q: Input size and response time limits? → A: 1M chars cap; 12s end-to-end timeout.
- Q: Minimum required fields in project_overview? → A: project_name + developer_name + location.
 - Q: Language handling policy before structuring? → A: English-only (discard non-English).
 - Q: Logging scope for LLM prompts/responses? → A: Summaries + key metrics with PII-safe redaction (no raw prompts/responses stored).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Structure a single property's data (Priority: P1)

As a data consumer, I want combined brochure text and OCR outputs to be transformed into a clean, consistent JSON so that I can render a property detail page and analytics with minimal manual cleanup.

**Why this priority**: Delivers the core value of turning messy content into usable structured data; enables immediate downstream use.

**Independent Test**: Provide sample PDF text, OCR text, and image labels for one project; receive schema-valid JSON covering Overview and Amenities without empty top-level sections.

**Acceptance Scenarios**:

1. **Given** valid PDF text and OCR text, **When** I submit them for structuring, **Then** I receive schema-valid JSON with populated project_overview fields where information exists.
2. **Given** duplicate or conflicting lines across sources, **When** data is combined, **Then** duplicates are removed and conflicts resolved deterministically with clear preference rules.

---

### User Story 2 - Include floor plans and image references (Priority: P2)

As a content curator, I want floor plan details (BHK, areas, tower) identified and linked to the most relevant image reference so that users can explore units visually.

**Why this priority**: Enhances usefulness by connecting text to images for floor plans.

**Independent Test**: Provide OCR text indicating “2 BHK 750 sq.ft Tower A” and a corresponding image label; receive a floor_plans array element with these attributes and an image reference.

**Acceptance Scenarios**:

1. **Given** text with BHK and area, **When** structured, **Then** the floor_plans item contains bhk_type and area fields in human-readable form.
2. **Given** multiple images, **When** categories/labels are provided, **Then** the best matching image_reference is attached to each floor plan.

---

### User Story 3 - Connectivity, FAQs, and highlights (Priority: P3)

As a marketing analyst, I want connectivity points and FAQs extracted so that key highlights are surfaced consistently across brochures.

**Why this priority**: Improves completeness and comparability across projects.

**Independent Test**: Provide brochure text with nearby schools and a Q&A section; receive connectivity lists populated and faqs items with question/answer pairs.

**Acceptance Scenarios**:

1. **Given** location content, **When** structured, **Then** nearby_schools and transport_facilities arrays contain normalized entries without duplicates.
2. **Given** a Q&A block, **When** structured, **Then** faqs contains multiple question/answer pairs extracted faithfully from the source.

### Edge Cases

- Incomplete inputs (missing OCR or missing PDF text)
- Conflicting values across sources (e.g., different areas or tower names)
- Non-English or mixed-language lines; watermark and boilerplate removal
- Extremely long documents; repeated headers, footers, and disclaimers
- Malformed or partial JSON returned by the structuring process
- Sparse brochures without amenities or floor plans (schema still required)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept combined inputs consisting of brochure text, OCR text, image metadata/labels, and optional project name hint.
- **FR-002**: The system MUST normalize and de-duplicate textual content prior to structuring, preserving meaningful sections and removing boilerplate.
- **FR-003**: The system MUST produce output that strictly conforms to the defined schema: project_overview, amenities, connectivity, floor_plans, faqs.
- **FR-004**: The system MUST populate fields when evidence exists and use empty strings or empty arrays where data is absent.
- **FR-005**: The system MUST resolve conflicts across sources by preferring OCR-derived values when they include explicit numeric patterns (e.g., areas, counts) or clearer contextual evidence; otherwise keep previously extracted values.
- **FR-006**: The system MUST log inputs (size/summary), outputs (size/summary), and validation results for auditability without storing raw sensitive content unnecessarily.
- **FR-007**: The system MUST validate the output against the schema and reject or correct malformed structures before returning a response.
- **FR-008**: The system SHOULD complete typical requests within an acceptable response time suitable for interactive use.
- **FR-009**: The system SHOULD handle documents across residential and commercial categories with robust defaults.
- **FR-010**: The system MUST handle errors gracefully with a single retry for incomplete outputs and return a safe, well-formed error object if issues persist.
 - **FR-011**: The system MUST enforce input size and latency limits: maximum combined input of 1,000,000 characters and an end-to-end response timeout of 12 seconds.
 - **FR-012**: The system MUST ensure `project_overview` includes at minimum: project_name, developer_name, and location (empty strings allowed if truly unavailable, but acceptance requires best-effort population of these three).
 - **FR-013**: The system MUST filter inputs to English-only prior to normalization and structuring (non-English content discarded).
 - **FR-014**: The system MUST log compact summaries and key metrics with PII-safe redaction and MUST NOT persist raw prompts or raw LLM responses.

 

### Key Entities *(include if feature involves data)*

- **StructuredPropertyData**: Top-level container with project_overview, amenities, connectivity, floor_plans, faqs.
- **ProjectOverview**: project_name, developer_name, location, description, launch_date, possession_date, rera_number, total_towers, total_units, project_type.
- **FloorPlanItem**: tower_name, bhk_type, carpet_area, super_area, price_range, image_reference.
- **Connectivity**: nearby_schools, nearby_hospitals, nearby_malls, transport_facilities (arrays of strings).
- **FAQItem**: question, answer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 90%+ of sampled brochures produce schema-valid JSON with non-empty project_overview and at least one populated section among amenities, connectivity, or floor_plans.
- **SC-002**: Median response time for typical brochure inputs within 3–4 seconds under normal load.
- **SC-003**: Zero malformed JSON responses after validation; all outputs pass schema checks.
- **SC-004**: Duplicate/conflict resolution reduces redundant lines by ≥80% in combined text.
- **SC-005**: Works across at least three brochure types (residential mid-rise, premium residential, commercial) with no spec changes.
