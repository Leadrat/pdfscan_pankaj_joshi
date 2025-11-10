# Data Model: Dynamic Landing Page (Auto‑Generated)

## Entities

### LandingPageProps
- overview: HeroOverview
- amenities: AmenityItem[]
- connectivity: ConnectivityItem[] | { schools?: string[]; hospitals?: string[]; transport?: string[] }
- floor_plans: FloorPlanCard[]
- faqs: FAQItem[]

### HeroOverview
- project_name: string
- developer_name: string
- location: string
- possession_date: string
- project_type: string
- hero_image?: string

### AmenityItem
- name: string
- icon?: string

### ConnectivityItem
- type: string  # e.g., "School", "Hospital", "Metro"
- label: string # e.g., "Delhi Public School"
- distance: string # e.g., "2 km"

### FloorPlanCard
- tower_name: string
- bhk_type: string
- area: string
- image: string

### FAQItem
- question: string
- answer: string

## Validation Rules
- Hide sections when arrays are empty or undefined.
- Normalize connectivity to ConnectivityItem[] for rendering (parse "Name - Distance").
- Fallback image used when floor plan image missing.

## Relationships & Identity
- One LandingPageProps object per brochure/project rendering.
- FloorPlanCard.image must be a safe, accessible URL/path.
