# AppSec Risk Scoring Dashboard (Org-wide Visibility)

A centralized AppSec visibility platform that ingests findings from multiple security sources (SAST/DAST/SCA/container/cloud/runtime), normalizes them into a single schema, and computes a dynamic per-application risk score (0–100) with trends and MTTR.

## What it includes (MVP)
- **FastAPI backend**: ingestion + metrics endpoints
- **PostgreSQL**: normalized storage for apps/findings/scores
- **Risk scoring engine**: severity/CVSS, exploitability, exposure, sensitivity, aging
- **Historical scoring**: trends over time
- **MTTR**: mean time to remediate from fixed findings
- **Streamlit dashboard**: executive view + engineering drill-down
- **Worker**: periodic score recalculation

## Quickstart (Docker)
1. Create env file:
   ```bash
   cp .env.example .env
   ```

2. Start services:
   ```bash
   docker compose up --build
   ```

3. Seed sample findings (from your host machine):
   ```bash
   export API_BASE_URL=http://localhost:8000
   python sample_data/seed_findings.py
   ```

## Access
- API docs: http://localhost:8000/docs
- Dashboard: http://localhost:8501

## Notes
- This repo ships with sample mock data so you can demo end-to-end without any commercial tool access.
- Replace mock ingestion with real connectors (Snyk/SonarQube/ZAP/Trivy/Wiz/etc.) as a next step.
