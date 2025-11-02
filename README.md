# 5SKYE Digital Twin Platform

A full‑stack platform for intelligent monitoring of telecommunication towers. The system brings together a 3D web UI, Spring Boot APIs, a FastAPI AI service, a telemetry simulator, and an observability stack.

## Monorepo Layout

- `5skye-Frontend-main/` — Next.js 14 + TypeScript UI, Cesium globe, 3D tower viewer, dashboards
- `5skye-backend-main/` — Spring Boot 3 APIs (towers, hardware, maintenance, alerts, auth) + telemetry ingest
- `ai-service/` — FastAPI service integrating Gemini for tower insights and alert generation
- `tower-telemetry-simulator/` — Spring Boot simulator producing realistic tower metrics
- `siteboss-project/` — Utilities and scripts for pulling/transforming SiteBoss XML/JSON data
- `docker-compose.observability.yml` — Prometheus + Grafana stack
- `5SKYE_PROJECT_ARCHITECTURE_DOCUMENTATION.md` — in‑repo architecture write‑up

## System Layers and Ports

- Presentation (frontend): `http://localhost:3000`
- Application:
  - Backend (Spring Boot): `http://localhost:8088`
  - AI service (FastAPI): `http://localhost:8000`
  - Telemetry simulator (Spring Boot): `http://localhost:8080`
- Data: PostgreSQL (prod/dev), H2 (local/dev), file storage for GLB models
- Monitoring: Prometheus `9090`, Grafana `3001`

## Quickstart

Fast path (starts observability, backend, simulator, frontend):

```bash
./start-project.sh
```

Manual run (per service):

- Observability: `docker compose -f docker-compose.observability.yml up -d`
- Backend: `cd 5skye-backend-main && ./mvnw spring-boot:run`
- Simulator: `cd tower-telemetry-simulator && ./mvnw spring-boot:run`
- Frontend: `cd 5skye-Frontend-main && npm install && npm run dev`
- AI service: `cd ai-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn app:app --port 8000`

## Data Flow (high level)

```
Physical Towers / SiteBoss → Backend API → Frontend (3D UI)
                    ↓                     ↑
Simulator → Prometheus → Grafana (embed)  │
                    ↓                     │
                 Backend (ingest snapshots + expose history)
                    ↓
AI Service ↔ Gemini (chat/insights) → Backend Alerts → Frontend notifications
```

## Release Plan (for thesis mapping)

- Release 1 (Sprints 1–2):
  - Sprint 1: Cesium globe, filters, 3D tower viewer, model upload
  - Sprint 2: Tower/Hardware/Maintenance CRUD, validation + cleanup, authentication
- Release 2 (Sprints 3–4):
  - Sprint 3: Telemetry live proxy, historical snapshots, live telemetry UI, Prometheus/Grafana
  - Sprint 4: AI chat + insights, alert deduplication, multi‑language UX

See `docs/THESIS_GUIDE.md` for a chapter‑by‑chapter checklist and screenshot suggestions.

## Environment and Secrets

- Frontend: `NEXT_PUBLIC_BACKEND_URL`, `NEXT_PUBLIC_CESIUM_ACCESS_TOKEN` (optional), SiteBoss envs if used
- Backend: database config (PostgreSQL/H2), file upload paths
- AI service: `GEMINI_API_KEY` (move secrets to `.env` or local environment; do not commit keys)

## Verifications / Health

- Backend: `GET /api/towers`, `GET /api/health/connection-test`
- Simulator: `GET /api/telemetry/live`
- AI service: `GET /` (health)
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (default admin/admin unless changed)

## Notes and Constraints

- Auto‑alerting in the AI service is disabled by default to conserve LLM quota; use the manual endpoint to trigger analysis.
- The monitoring page can embed Grafana; ensure Grafana allows embedding (X‑Frame‑Options, auth).
- Translate strings via the custom translation context (EN/FR/AR).

## License / Attribution

This repository is for academic and internal use. Do not publish API keys or sensitive data.

