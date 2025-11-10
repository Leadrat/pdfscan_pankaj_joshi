# Quickstart: Dynamic Landing Page (Auto‑Generated)

## Prerequisites
- Frontend running (Vite React + TailwindCSS + Framer Motion)
- Structured JSON available from Spec 6 (Overview, Amenities, Connectivity, Floor Plans, FAQs)

## Usage
1. Provide `LandingPageProps` JSON to the parent component `DynamicLandingPage`.
2. The component renders sections dynamically; empty sections are hidden.

Example integration:
```jsx
import DynamicLandingPage from './components/dynamic/DynamicLandingPage';
import data from './mock/project.json';

export default function Page() {
  return <DynamicLandingPage data={data} />;
}
```

## Data Shapes (Minimal)
- overview: { project_name, developer_name, location, possession_date, project_type, hero_image? }
- amenities: ["Clubhouse", "Gymnasium", ...]
- connectivity: either { schools:[], hospitals:[], transport:[] } OR ["Delhi Public School - 2 km", ...]
- floor_plans: [{ tower_name, bhk_type, area, image }]
- faqs: [{ question, answer }]

## Behavior
- Animations: fade/slide on reveal, parallax on hero background, hover scale on cards
- Zoom: click floor plan “View” to open Lightbox; close with overlay or ESC
- Smooth scroll between sections via anchor links

## Troubleshooting
- If images fail to load → fallback placeholder used
- If a section is missing → it is hidden automatically
- Verify JSON keys/spellings; unknown keys are ignored
