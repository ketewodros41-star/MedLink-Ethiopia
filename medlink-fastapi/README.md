# MedLink Ethiopia Backend

Production-oriented backend for an AI-powered healthcare logistics platform designed around a difficult real-world constraint:

**help a patient find verified medicine nearby in under two minutes, even when inventory is fragmented and connectivity is unreliable.**

This project focuses on backend engineering only. The work centers on medicine discovery, pharmacy coordination, prescription OCR, trust scoring, offline synchronization, telecom ingestion, and auditability.

## Why this project matters

In many healthcare environments, medicine availability is not a clean database problem.

- Inventory can be stale or partially updated.
- Pharmacies may operate with weak or intermittent internet.
- Patients search using brand names, generic names, abbreviations, or informal descriptions.
- Sensitive prescription data requires stronger handling than a normal CRUD app.

MedLink is built around those constraints rather than pretending they do not exist.

## What I built

This backend is structured as a modular FastAPI service with domain-driven routing, async persistence, immutable audit events, and operational controls suitable for a serious health-tech foundation.

Core capabilities:

- Medicine search with alias normalization, search-failure intelligence, and Meilisearch integration hooks
- Inventory verification with freshness states, confidence scoring, and pharmacy-aware verification workflows
- Reservation handling with quota controls, expiry logic, and event emission
- Pharmacy trust scoring and counterfeit-risk heuristics
- OCR ingestion with upload validation, structured extraction output, and signed prescription file access
- Offline synchronization queues for delayed client operations
- SMS-style telecom ingestion for low-bandwidth pharmacy participation
- Immutable audit event recording and replay for investigations and analytics reconstruction
- Request tracing, structured logs, throttling, and JSON metrics exposure

## Architecture

The system is intentionally built as a **modular monolith** with clean boundaries so it can scale operationally without premature microservice complexity.

### Domain modules

- `medicine`: search, normalization, alias graph handling
- `inventory`: verification workflows, confidence scoring, freshness logic
- `reservations`: reservation lifecycle and anti-hoarding controls
- `pharmacy`: proximity discovery and ranking
- `trust`: weighted trust scoring from operational and community signals
- `counterfeit`: pharmacy and inventory risk heuristics
- `ocr`: prescription ingestion and structured extraction
- `sync`: offline-first operation intake
- `telecom`: SMS command parsing for pharmacy stock updates
- `community`: crowdsourced stock reporting
- `audit`: immutable event replay
- `analytics`: shortage and demand-oriented views

### Technical design choices

- **FastAPI + async SQLAlchemy** for clean API ergonomics and non-blocking I/O
- **PostgreSQL-oriented relational model** with explicit entities for medicines, aliases, inventory, reservations, sync operations, and audit events
- **Redis hooks** for lightweight event emission and throttling support
- **Meilisearch integration** for fast medicine discovery expansion
- **JWT + role-aware authorization hooks** for patient, pharmacist, and admin boundaries
- **Signed file access** for uploaded prescription artifacts
- **Structured observability** through request IDs, timing headers, logs, and a metrics endpoint

## Data model highlights

The backend is not a flat CRUD layer. It models operational realities explicitly.

- `Medicine` and `MedicineAlias` support canonical names, generic mapping, and synonym resolution.
- `InventoryItem` tracks quantity, verification history, confidence, freshness state, and last verifier.
- `Reservation` models expiry and controlled holding of stock.
- `CommunityStockReport` captures patient-generated availability signals with weighted trust.
- `SyncOperation` preserves delayed client actions from unreliable network conditions.
- `AuditEvent` creates an immutable event trail for replay, debugging, and analytics.

## Inventory verification engine

One of the strongest parts of the backend is the inventory verification model.

Instead of trusting pharmacy stock at face value, the system tracks:

- quantity available
- quantity reserved
- verification count
- last verified timestamp
- last verified actor
- confidence score
- freshness state

Inventory moves through states such as:

- `unverified`
- `estimated`
- `recently_verified`
- `stale`
- `unavailable`

This creates a better operational foundation than a simple `in_stock: true/false` model.

## OCR and prescription handling

Prescription uploads go through a safer ingestion path:

- file type validation
- upload size enforcement
- deterministic image signature checks
- local artifact persistence
- signed retrieval URLs
- structured OCR output with confidence metadata
- review queue signaling when extraction confidence is weak

The current implementation is a strong backend foundation for a future worker-based OCR pipeline.

## Security and operational controls

This project includes practical backend safeguards rather than superficial auth wiring.

- JWT verification with local-secret and JWKS fallback support
- role-aware access control for sensitive routes
- route-level request throttling
- immutable audit events on major workflows
- request ID propagation and response timing headers
- structured request logging
- signed prescription file URLs with expiration

## Observability

The service exposes operational signals that make debugging and monitoring easier:

- `GET /health`
- `GET /metrics`
- structured request logs
- per-route latency summaries
- counters for OCR and medicine search flows
- search-failure tracking for product intelligence

## Selected workflows

### Medicine search

User query:

- normalized
- matched against alias graph and search vectors
- optionally enhanced with Meilisearch
- written to audit history
- tracked for failure intelligence

### Inventory verification

Pharmacist action:

- updates inventory record
- recalculates confidence
- updates freshness state
- writes immutable audit event
- emits Redis stream payload for event-driven expansion

### Reservation lifecycle

Patient request:

- checks quotas
- validates available verified inventory
- reserves stock
- sets expiry
- records audit event
- emits reservation stream event

### Offline sync

Delayed client operations:

- are persisted as sync operations
- assigned status
- auditable for reconciliation
- suitable for eventual consistency workflows

## Local run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m pytest -q tests
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Testing

The backend includes async integration-style coverage for the most important flows:

- medicine alias search
- inventory verification
- reservation creation
- trust and counterfeit analysis
- telecom ingestion
- offline sync intake
- audit replay
- OCR signed upload behavior
- RBAC enforcement

## CI

A GitHub Actions workflow is included to run the backend test suite automatically on pushes and pull requests touching the service.

## Portfolio notes

This project is a good example of how I approach backend engineering when the domain is messy and operationally sensitive:

- I model uncertainty explicitly instead of hiding it behind simplistic fields.
- I separate domain logic from HTTP handlers.
- I build with auditability and replay in mind.
- I harden inputs before talking about “AI features.”
- I treat observability and security as backend responsibilities, not optional polish.

## What I would build next

If this were moving toward full production, the next steps would be:

- PostGIS-backed geospatial search instead of application-side distance calculations
- S3-compatible encrypted storage for prescription artifacts
- dedicated OCR worker processes with richer multilingual support
- stronger FHIR/Medplum write integration
- distributed rate limiting
- richer metrics export and dashboarding
- fraud anomaly detection beyond heuristics
- queue consumers for asynchronous event processing

## Status

This is not a demo CRUD backend. It is a serious backend foundation for a healthcare logistics platform, with strong domain modeling, operational awareness, and room to scale into a more advanced distributed architecture.
