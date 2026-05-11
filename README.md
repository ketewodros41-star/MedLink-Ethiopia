# MedLink Ethiopia

MedLink Ethiopia is an AI-powered healthcare logistics platform built to help patients find verified medicine quickly, even when inventory is fragmented, pharmacy data is stale, or connectivity is unreliable.

This workspace is organized as a multi-app repository with a clean separation between the product surface and the service layer:

- [frontend/](frontend) contains the Next.js user interface.
- [medlink-fastapi/](medlink-fastapi) contains the FastAPI backend.
- [medplum-main/](medplum-main) is a separate MedPlum codebase kept alongside the main product.

The root README is written as portfolio documentation for the full system. Backend-specific implementation notes live in [medlink-fastapi/README.md](medlink-fastapi/README.md), and the frontend starter notes live in [frontend/README.md](frontend/README.md).

## What MedLink Solves

Healthcare logistics is often treated like a simple inventory problem. In reality, it is usually a trust, latency, and communication problem.

MedLink is designed around those constraints:

- Patients may search by brand name, generic name, or informal description.
- Pharmacy stock can be incomplete, delayed, or manually reported.
- Network access may be weak or intermittent.
- Prescription handling requires stronger validation than a normal CRUD workflow.
- Verification, auditability, and traceability matter as much as speed.

The project is built to support a realistic workflow: search for medicine, locate nearby pharmacies, validate stock, reserve inventory, and preserve the full audit trail.

## Portfolio Highlights

- Full-stack healthcare platform with a modern Next.js front end and a FastAPI backend.
- Medicine search, pharmacy discovery, and reservation workflows designed for real-world supply constraints.
- OCR-based prescription ingestion with secure file handling and review signaling.
- Trust scoring and counterfeit-risk heuristics for pharmacy and inventory signals.
- Offline synchronization support for delayed client actions.
- Telecom/SMS-style ingestion paths for low-bandwidth updates.
- Immutable audit events and operational observability for traceability.

## System Overview

The product is intentionally split into three parts.

### Frontend

The frontend is a Next.js application that provides the user-facing experience for:

- medicine search
- pharmacy browsing
- reservations
- community reporting
- prescription upload flows
- authentication and user session handling

### Backend

The backend is a modular FastAPI service that handles:

- medicine normalization and alias resolution
- inventory verification and freshness tracking
- reservation lifecycles
- trust scoring and counterfeit checks
- OCR ingestion and upload validation
- offline sync processing
- telecom message intake
- structured audit logging

### Shared Workspace

The root folder is now documentation and coordination only. That keeps the repository clean and prevents the backend from appearing twice at the top level.

## Technical Stack

### Frontend stack

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- Framer Motion
- Lucide React
- React Hook Form
- Zod
- Zustand
- Leaflet and React Leaflet

### Backend stack

- FastAPI
- Uvicorn
- SQLAlchemy 2
- Alembic
- asyncpg and aiosqlite
- Pydantic v2
- Redis
- Meilisearch
- EasyOCR
- OpenCV
- PyJWT
- Structlog
- OpenTelemetry

## Key Capabilities

### Medicine discovery

- Canonical medicine lookup with alias support.
- Search behavior that can handle abbreviations and partial names.
- Hooks for search intelligence and ranking improvements.

### Inventory verification

- Tracks verified, stale, estimated, and unavailable states.
- Keeps confidence and freshness visible instead of hiding uncertainty.
- Supports pharmacy-aware validation workflows.

### Reservation flow

- Helps prevent hoarding and duplicate holds.
- Supports expiry-based reservation logic.
- Records reservation actions for audit and replay.

### OCR prescription handling

- Validates uploads before processing.
- Stores artifacts locally with signed retrieval support.
- Produces structured OCR output that can be reviewed when confidence is low.

### Trust and risk analysis

- Scores pharmacy and inventory activity using operational and community signals.
- Supports counterfeit-risk heuristics.
- Creates a foundation for safer medicine discovery.

### Offline and telecom workflows

- Persists delayed client actions for unreliable networks.
- Supports SMS-style intake for pharmacy stock updates.
- Keeps asynchronous workflows auditable.

### Observability and security

- JWT and role-aware authorization hooks.
- Request tracing and structured logs.
- Metrics and latency visibility.
- Immutable audit events for major workflows.

## Repository Layout

- [frontend/](frontend) - Next.js app for the product UI.
- [medlink-fastapi/](medlink-fastapi) - FastAPI backend and backend documentation.
- [medplum-main/](medplum-main) - Separate MedPlum codebase kept in the workspace.
- [docker-compose.yml](docker-compose.yml) - Local infrastructure and service orchestration.
- [instruction.md](instruction.md) - Workspace guidance and product instructions.
- [frontendinstruct.md](frontendinstruct.md) - Frontend-specific instructions.

## Local Setup

Run the apps from their own folders so the workspace stays clean and the dependencies stay isolated.

### Backend

```powershell
Set-Location medlink-fastapi
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m pytest -q tests
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Frontend

```powershell
Set-Location frontend
npm install
npm run dev
```

### Full workspace with Docker

```powershell
docker compose up --build
```

## Environment Notes

- The backend expects database and service dependencies that are wired through the backend project and the compose file.
- The frontend reads its API base URL from the client configuration in [frontend/src/lib/api.ts](frontend/src/lib/api.ts).
- The backend has its own detailed setup notes in [medlink-fastapi/README.md](medlink-fastapi/README.md).

## Why This Structure Matters

This repository now reflects a clearer production-style layout:

- One frontend app.
- One backend app.
- Shared root documentation.
- No duplicate backend source at the top level.

That makes the project easier to understand, easier to run locally, and stronger for portfolio review.

## Portfolio Summary

This project shows work across product design, API design, data modeling, search, observability, and security.

It is especially relevant if you want to present yourself as a builder who can handle messy real-world systems rather than just clean demo CRUD applications.
