# MedLink Ethiopia — Backend Engineering Master Prompt

## AI-Powered Healthcare Logistics Platform (Backend-Only Build)

You are a principal backend engineer, distributed systems architect, healthcare interoperability engineer, AI systems engineer, DevOps architect, and infrastructure specialist tasked with designing and implementing the backend architecture for:

# MedLink Ethiopia

A production-grade AI-powered healthcare logistics and pharmaceutical intelligence platform optimized for Ethiopia’s real-world infrastructure constraints.

This prompt is ONLY for backend engineering.

Do NOT focus on:

* frontend UI
* design systems
* animations
* marketing pages

Focus on:

* APIs
* infrastructure
* AI pipelines
* event-driven systems
* offline synchronization
* observability
* healthcare interoperability
* reliability
* security
* scalability
* pharmacy coordination

The backend must be production-grade and architected like a serious African health-tech infrastructure company.

---

# PRIMARY MISSION

Build a backend platform that enables Ethiopian users to:

* search medicines
* verify stock availability
* upload prescriptions
* identify generic substitutes
* reserve medicine
* coordinate delivery
* access pharmacies under poor connectivity conditions

The platform must support:

* fragmented pharmacy ecosystems
* offline workflows
* multilingual medicine search
* unreliable inventory updates
* low-bandwidth participation
* auditability
* real-time coordination

---

# PRODUCT CORE

The product is NOT:

* a hospital management system
* an EMR replacement
* a doctor appointment app

The product IS:

# a decentralized pharmaceutical coordination and medicine discovery network.

The platform’s core promise:

# “Find verified medicine nearby in under 2 minutes.”

---

# ARCHITECTURE REQUIREMENTS

# SYSTEM DESIGN PRINCIPLES

The backend must be:

* modular
* event-driven
* observable
* fault tolerant
* horizontally scalable
* offline-aware
* auditable
* AI-ready

Architecture style:

* modular monolith initially
* service extraction later if needed

Avoid premature microservices complexity.

---

# CORE BACKEND STACK

## API Framework

Use:

* FastAPI

Requirements:

* async-first
* OpenAPI generation
* modular routers
* dependency injection
* versioned APIs

---

# DATABASES

## Primary Database

Use:

* PostgreSQL

Requirements:

* strong relational integrity
* event storage
* auditability
* geospatial support
* JSONB support

Use:

* PostGIS extension

---

## Search Engine

Use:

* Meilisearch

Responsibilities:

* medicine discovery
* typo tolerance
* transliteration
* fuzzy matching
* synonym indexing

---

## Cache Layer

Use:

* Redis

Responsibilities:

* session caching
* hot inventory cache
* pharmacy response cache
* distributed locks
* rate limiting
* realtime events

---

# ASYNC + EVENT SYSTEM

Use:

* Redis Streams initially
  OR
* Kafka if scaling later

Build an event-driven architecture.

Important domain events:

* PrescriptionUploaded
* OCRProcessed
* MedicineSearchPerformed
* MedicineVerified
* PharmacyResponded
* InventoryUpdated
* InventoryExpired
* ReservationCreated
* ReservationExpired
* GenericAlternativeSuggested
* DeliveryAssigned
* DeliveryCompleted
* PharmacyTrustUpdated
* CommunityReportSubmitted
* FraudSignalDetected

All important actions must generate immutable events.

---

# AI + OCR PIPELINE

# PRESCRIPTION INTELLIGENCE ENGINE

Build a full OCR processing pipeline.

Use:

* EasyOCR
* OpenCV preprocessing

Pipeline stages:

1. image upload
2. denoise
3. crop
4. contrast enhancement
5. OCR extraction
6. medicine entity extraction
7. dosage extraction
8. confidence scoring
9. fallback review queue

Store:

* extracted text
* bounding boxes
* confidence metrics
* preprocessing metadata
* review status

Support:

* handwritten prescriptions
* blurry photos
* folded prescriptions
* stamps
* multilingual text

---

# MEDICINE ENTITY RESOLUTION ENGINE

Critical feature.

Build an intelligent medicine normalization system.

Requirements:

* brand-to-generic mapping
* synonym resolution
* transliteration matching
* typo correction
* Amharic aliases
* therapeutic equivalence graph

Example:
Paracetamol
PCM
Panadol
Acetaminophen

All should resolve correctly.

Build:

* canonical medicine registry
* medicine alias graph
* local Ethiopian naming dictionary

---

# INVENTORY VERIFICATION ENGINE

This is the heart of the system.

The system must NEVER blindly trust pharmacy inventory.

Build:

* inventory confidence scoring
* freshness windows
* live verification flow
* stale inventory detection
* pharmacy verification actions

Inventory states:

* unverified
* estimated
* recently verified
* stale
* unavailable

Track:

* verification timestamps
* pharmacist actions
* historical accuracy
* fulfillment reliability

---

# PHARMACY TRUST ENGINE

Build a dynamic trust scoring system.

Each pharmacy should receive scores for:

* response speed
* stock reliability
* reservation fulfillment
* counterfeit risk
* community feedback
* delivery success

Build:

* weighted scoring models
* anomaly detection
* suspicious behavior detection

Potential fraud patterns:

* fake stock confirmations
* excessive cancellations
* inconsistent inventory updates
* unusual medicine patterns

---

# COMMUNITY STOCK-WATCH ENGINE

Users can:

* report medicine sightings
* validate stock
* upload proof
* confirm availability

Build:

* reputation scoring
* anti-spam protection
* fraud heuristics
* duplicate detection
* verification weighting

Inspired by:

* Waze crowdsourced reporting

---

# OFFLINE SYNCHRONIZATION ENGINE

Critical requirement.

Many pharmacies operate under poor internet conditions.

Build:

* sync queue system
* retry logic
* conflict resolution
* eventual consistency workflows

Support:

* delayed inventory updates
* partial synchronization
* offline transaction batching

---

# SMS + USSD INVENTORY ENGINE

Build low-tech pharmacy participation infrastructure.

Pharmacies should update stock via:

* SMS
* USSD
* Telegram bot

Example SMS:
STOCK AMOX500 12

System parses and updates inventory.

Requirements:

* command parser
* validation layer
* fraud prevention
* confirmation replies

Build:

* lightweight ingestion gateway
* telecom abstraction layer

---

# MEDICINE RESERVATION ENGINE

Users reserve medicine before traveling.

Requirements:

* expiration timers
* anti-hoarding protections
* pharmacy approval workflow
* pickup verification
* reservation quotas

Handle:

* race conditions
* duplicate reservations
* stale inventory conflicts

---

# DELIVERY COORDINATION ENGINE

Optional initially but architecturally prepared.

Features:

* delivery assignment
* route optimization
* bundled delivery planning
* driver tracking
* status events

Future integrations:

* ride-hailing APIs
* local courier systems

---

# GEOLOCATION + PROXIMITY ENGINE

Build pharmacy geospatial search.

Requirements:

* nearest pharmacy ranking
* travel distance estimation
* regional filtering
* delivery radius support

Use:

* PostGIS

---

# MEDICINE SHORTAGE INTELLIGENCE ENGINE

Build regional analytics.

Track:

* medicine shortages
* demand spikes
* regional trends
* outbreak indicators
* inventory collapse patterns

Future stakeholders:

* NGOs
* distributors
* health agencies

---

# COUNTERFEIT RISK DETECTION ENGINE

Advanced feature.

Build risk heuristics for:

* suspicious inventory behavior
* abnormal medicine pricing
* irregular pharmacy activity
* inconsistent supply patterns

Future AI possibilities:

* packaging image analysis
* batch verification
* counterfeit probability scoring

---

# MULTILINGUAL SUPPORT

Backend must support:

* English
* Amharic

Future:

* Afaan Oromo
* Tigrinya

Requirements:

* transliteration normalization
* multilingual indexing
* multilingual OCR metadata
* locale-aware search

---

# HEALTHCARE INTEROPERABILITY

Use:

* Medplum
* HL7 FHIR resources

Use Medplum ONLY as:

* healthcare data layer
* auth provider
* patient resource management
* medication resource management

Do NOT tightly couple business logic to Medplum internals.

Build independent domain services.

---

# AUTHENTICATION + AUTHORIZATION

Implement:

* JWT auth
* RBAC
* pharmacy roles
* pharmacist verification
* admin roles
* patient roles

Potential future:

* Ethiopian digital identity integrations

---

# SECURITY REQUIREMENTS

Treat all prescription data as sensitive medical information.

Implement:

* encrypted file storage
* audit logs
* immutable event history
* abuse detection
* API throttling
* secure upload validation
* malware scanning
* signed URLs

---

# OBSERVABILITY

Integrate:

* OpenTelemetry
* Langfuse
* Prometheus
* Grafana

Track:

* OCR latency
* search latency
* inventory freshness
* reservation success rate
* pharmacy response time
* failed medicine searches
* synchronization failures

All services must emit:

* traces
* structured logs
* metrics

---

# FILE STORAGE

Use:

* S3-compatible object storage

Store:

* prescriptions
* proof images
* OCR artifacts
* pharmacy verification photos

Requirements:

* encrypted storage
* signed upload URLs
* lifecycle policies

---

# API DESIGN

Build clean domain-driven APIs.

Core API domains:

* auth
* pharmacies
* medicines
* inventory
* prescriptions
* OCR
* reservations
* deliveries
* analytics
* trust
* notifications
* community reports

Requirements:

* pagination
* filtering
* sorting
* rate limiting
* idempotency support

---

# NOTIFICATION ENGINE

Support:

* SMS
* push notifications
* email
* Telegram

Events:

* reservation approved
* medicine verified
* stock expiring
* delivery updates
* pharmacy response

---

# FEATURES YOU MUST ADD (IMPORTANT)

Add advanced backend features the founder may not have considered.

# 1. Demand Forecasting Engine

Predict medicine shortages before they happen.

Use:

* historical searches
* reservation trends
* regional demand patterns

---

# 2. Medicine Popularity Heatmaps

Track:

* trending medicines
* outbreak indicators
* unusual regional spikes

---

# 3. Search Failure Intelligence

Track medicines users repeatedly fail to find.

This becomes:

* distributor intelligence
* shortage analytics

---

# 4. Smart Pharmacy Ranking

Rank pharmacies dynamically using:

* trust
* distance
* stock freshness
* delivery speed
* fulfillment history

---

# 5. Abuse Prevention Engine

Detect:

* fake reservations
* scalping behavior
* pharmacy manipulation
* spam inventory updates

---

# 6. Inventory Freshness Predictor

Predict likelihood that stock is still available based on:

* update frequency
* pharmacy reliability
* medicine turnover rate

---

# 7. Real-Time Emergency Broadcasts

Allow health authorities to push:

* outbreak alerts
* shortage warnings
* recall notices

---

# 8. Pharmacist Verification Workflow

Build credential verification infrastructure.

Pharmacists should:

* submit licenses
* undergo approval workflows
* maintain verified status

---

# 9. Audit Replay Engine

Allow replaying historical events for:

* debugging
* fraud investigation
* analytics reconstruction

---

# 10. AI Search Query Understanding

Users may search:
“I need the blue asthma medicine”
or
“migraine injection”

Build semantic search assistance.

---

# DEVOPS + INFRASTRUCTURE

Use:

* Docker
* docker-compose initially

Prepare for:

* Kubernetes later

CI/CD:

* GitHub Actions

Environment strategy:

* local
* staging
* production

---

# PROJECT STRUCTURE

Design a clean scalable backend structure.

Suggested modules:

* auth
* pharmacy
* medicine
* OCR
* search
* reservations
* inventory
* analytics
* notifications
* events
* trust
* fraud
* synchronization

Avoid:

* giant monolithic files
* tightly coupled services
* framework chaos

---

# DATABASE DESIGN

Design:

* normalized schemas
* audit tables
* event tables
* geospatial indexes
* medicine graph structures
* trust score history
* synchronization queues

---

# TESTING REQUIREMENTS

Implement:

* unit tests
* integration tests
* contract tests
* event replay tests
* API tests
* OCR pipeline tests

Use:

* pytest

---

# ENGINEERING PHILOSOPHY

Build for:

* Ethiopia first
* Africa scalability second

Avoid:

* Silicon Valley assumptions
* over-engineering
* unnecessary microservices
* fragile AI systems

Prioritize:

* reliability
* trust
* operational simplicity
* low-bandwidth resilience
* auditability
* scalability
* practical usability

The backend should feel like:

# a modern healthcare infrastructure platform purpose-built for African realities.
