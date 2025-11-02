# AI Analytics Service (FastAPI + Gemini)

FastAPI microservice that aggregates tower context (telemetry, SiteBoss, hardware, maintenance) and generates insights/alerts using Google Gemini.

## Setup

```bash
cd ai-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # or: pip install fastapi uvicorn pydantic google-generativeai requests
export GEMINI_API_KEY=YOUR_KEY_HERE
uvicorn app:app --host 127.0.0.1 --port 8000
```

Health check: `GET http://127.0.0.1:8000/`

## Endpoints (selection)

- `POST /chat` — Chat with system/tower context
- `GET /tower/{id}/insights` — Generate a concise analysis for a specific tower
- `POST /generate-all-alerts` — Manually trigger analysis and alert creation for all towers
- `POST /auto-alerts/toggle` — Toggle background auto‑alert loop (disabled by default to save quota)
- `GET /` — Health check (status + auto‑alert flag)

## Data Sources

- Backend (`8088`): towers, hardware, maintenance, alerts
- Telemetry simulator (`8080`): `/api/telemetry/live`
- SiteBoss data via backend integration

## Deduplication

Before creating an alert, the service fetches unresolved alerts for the tower and prevents duplicates by comparing titles/messages.

## Quotas & Safety

- Keep `auto_alerting_enabled = False` (default) during development to avoid exhausting Gemini quota
- Prefer `/generate-all-alerts` for demos and screenshots

## Thesis Tips

- Capture: `/chat` responses (tower/system), manual alert generation, health endpoint, and a snippet of generated alerts viewed from the backend
- Mention how secrets are provided via environment variables; do not commit real keys
