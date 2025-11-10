# Data Model: Gemini-Driven Property Data Structuring

## Entities

### StructuredPropertyData
- project_overview: ProjectOverview
- amenities: string[]
- connectivity: Connectivity
- floor_plans: FloorPlanItem[]
- faqs: FAQItem[]

### ProjectOverview
- project_name: string
- developer_name: string
- location: string
- description: string
- launch_date: string
- possession_date: string
- rera_number: string
- total_towers: string
- total_units: string
- project_type: string

### Connectivity
- nearby_schools: string[]
- nearby_hospitals: string[]
- nearby_malls: string[]
- transport_facilities: string[]

### FloorPlanItem
- tower_name: string
- bhk_type: string
- carpet_area: string
- super_area: string
- price_range: string
- image_reference: string

### FAQItem
- question: string
- answer: string

## Validation Rules
- Required minimums (acceptance): project_overview must include project_name, developer_name, location (may be empty if truly unavailable; best-effort population required).
- Arrays default to [] if no data present.
- Strings default to "" if no data present.
- Language policy: English-only inputs before structuring.
- Limits: Combined input ≤ 1,000,000 characters; end-to-end timeout ≤ 12s.

## Relationships & Identity
- A StructuredPropertyData document corresponds to one brochure/project extraction request.
- project_overview.project_name + developer_name + location together act as a natural identity triplet for downstream deduplication.
