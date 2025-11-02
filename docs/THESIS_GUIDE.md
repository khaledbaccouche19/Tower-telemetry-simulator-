# Final Year Project Proposal — Intelli‑Twin Platform

## Project Title

Intelli‑Twin: Real‑Time Digital Twin Platform for Intelli Infrastructure product line

## Project Overview

Intelli‑Twin is a real‑time Digital Twin platform for 5SKYE’s Intelli infrastructure. The project initially targets the Intelli‑FarEdge and will then be superimposed onto the rest of the product line, i.e., the Intelli‑Vault and Intelli‑Kiosk. The application provides a synchronized, virtual representation of each physical Intelli‑FarEdge tower, supporting real‑time monitoring, 3D visualization, asset tracking, and predictive analysis.

Each tower hosts smart infrastructure services such as 5G, IoT, LED Digital Display, AI‑based CCTV, and Edge computing. Through the integration of real‑time telemetry (via the Assentria SiteBoss using SNMP/REST), advanced filtering, and AI‑powered comparisons, the platform enhances operations, maintenance, and strategic decision‑making within 5SKYE’s ecosystem.

## What is a Digital Twin?

A Digital Twin is a dynamic virtual replica of a physical asset that mirrors its real‑time status, configurations, performance metrics, and behavior. By continuously synchronizing data from live environments, Digital Twins enable real‑time insights, anomaly detection, predictive maintenance, and data‑driven decisions. In this project, each Intelli‑Tower is represented digitally, continuously updated with sensor data from the Assentria SiteBoss management system, and enriched with service, hardware, and operational metadata.

## Project Objectives

- Map and manage all deployed Intelli‑FarEdge towers in a web dashboard
- Enable detailed tower configuration: services, hardware, serial numbers, IPs, install dates, vendor, warranty, etc.
- Integrate real‑time monitoring via SiteBoss (SNMP or REST) funneled through the backend
- Visualize tower structures using interactive 3D mockups (GLB/GLTF)
- Provide maintenance tracking, calendar scheduling, and alert logs with deduplication
- Generate structured tower reports and AI‑based comparative insights
- Provide multilingual UI and secure role‑based access control

## Technical Features

### Map‑Based Tower Overview
- Interactive map with dynamic Intelli‑FarEdge placement
- Tower filtering by region, status, or use case; geographic clustering and zooming

### Tower Configuration & Inventory Management
- Attach per‑tower 3D models (Three.js via React Three Fiber)
- Log tower‑ and component‑level metadata (services, hardware specs, serials, warranties)
- Track firmware/software versions and configuration profiles

### Real‑Time Monitoring (Digital Twin Engine)
- Integrate with SiteBoss devices via SNMP polling and/or REST API
- Metrics: temperature, voltage, door sensors, battery, uptime; CPU/memory if available
- Use scheduled jobs/webhooks where applicable; expose via backend REST to frontend

### Alerts, Logs, and Predictive Maintenance
- Visual alert indicators (severity/type), alert history with timestamps
- Maintenance scheduling calendar (CRUD)
- AI/rule‑based suggestions (e.g., frequent alerts → inspection)

### Tower Reports and AI Insights
- PDF/printable report generation per tower
- AI modules to compare towers by uptime, alert frequency, component aging
- Identify underperforming sites; generate reliability rankings or maintenance forecasts

## Technology Stack (as implemented in this repo)

- Frontend: Next.js (React), Tailwind UI, Cesium/Three.js (via `@react-three/fiber`), `next-intl` for i18n
- Backend: Spring Boot (Java), REST API, Spring Security/JWT, Actuator + Micrometer
- Real‑Time Data: SiteBoss SNMP/REST integration (simulator available), backend proxy endpoints
- Database: PostgreSQL (preferred)
- Observability: Prometheus + Grafana dashboards
- AI Service: Python FastAPI (`ai-service`), Gemini‑based analysis and alert suggestion endpoints
- Reporting: Server‑side rendering/print to PDF (or external tooling if needed)

## System Architecture Overview

- Frontend (Next.js): Map rendering, metric cards, 3D viewer, multilingual interface, auth‑guarded routes
- Backend API (Spring Boot @ 8088): Tower CRUD, alerts, hardware/maintenance, telemetry proxy, Prometheus metrics
- Telemetry Simulator (Spring Boot @ 8080): Provides sample live telemetry for development
- AI Service (FastAPI @ 8000): Tower insights, chat, alert generation assistance (dedup safeguards via backend)
- Database (PostgreSQL): Towers, hardware, maintenance, alerts, logs
- Observability: Prometheus (9090) scrapes; Grafana (3001) dashboards

## Development Approach

- Phase 1: Tower CRUD, map UI, initial data models, auth
- Phase 2: SNMP/REST monitoring integration, alert/log UI, metrics exposure
- Phase 3: 3D model viewer and inventory mapping
- Phase 4: AI analysis modules and reporting
- Phase 5: Final integrations, optimizations, user testing

## How to Run (local dev)

1) Observability (optional): `docker compose -f docker-compose.observability.yml up -d`
2) Backend: `cd 5skye-backend-main && ./mvnw spring-boot:run`
3) Simulator: `cd tower-telemetry-simulator && ./mvnw spring-boot:run`
4) Frontend: `cd 5skye-Frontend-main && pnpm i || npm i && pnpm dev || npm run dev`
5) AI service: `cd ai-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && export GEMINI_API_KEY=... && uvicorn app:app --port 8000`

### Ports Reference

- Frontend: 3000  •  Backend: 8088  •  Simulator: 8080  •  AI: 8000  •  Prometheus: 9090  •  Grafana: 3001

## Evidence to Collect

- Screens: dashboard, map→tower detail, 3D viewer (success/fallback), CRUD forms, auth flow
- Monitoring: live refresh, sample history chart, created alerts, Grafana panels
- Metrics: ingest counters/duration, API p95 latency/error counts, AI request counts

## Security & Ethics

- Keep secrets in env vars; do not commit API keys
- Redact sensitive identifiers in screenshots and payloads

## Useful Files

- Root `README.md` — quickstart, layers, data flow
- `5skye-backend-main/README.md` — endpoints, configuration, metrics
- `5skye-Frontend-main/README.md` — pages, env, auth, telemetry
- `ai-service/README.md` — AI endpoints and usage

## Appendix

- Architecture snapshot, ERD, selected API payloads (sanitized), extra Grafana panels

