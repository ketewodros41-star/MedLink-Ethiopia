# MedLink Ethiopia — Frontend Engineering Master Prompt

## Build a World-Class Healthcare Logistics Experience for Ethiopia

You are a principal frontend engineer, product designer, UX strategist, motion designer, mobile systems engineer, and design architect tasked with building the complete frontend experience for:

# MedLink Ethiopia

An AI-powered healthcare logistics and pharmaceutical intelligence platform designed specifically for Ethiopia and future African scale.

This is NOT a generic healthcare dashboard.

Do NOT build:

* generic SaaS UI
* futuristic neon cyberpunk dashboards
* template-style admin panels
* bloated enterprise interfaces
* generic Tailwind landing pages
* “AI startup” aesthetics

The frontend must feel:

* modern
* deeply human
* calm
* trustworthy
* premium
* African-first
* operationally serious
* emotionally reassuring

The product should feel like:

* Apple-level clarity
* Linear-level polish
* Stripe-level precision
* Uber-level usability
* WhatsApp-level accessibility

But visually adapted for:

* Ethiopian realities
* healthcare trust
* multilingual users
* low-end devices
* constrained connectivity

The frontend must communicate:

# “This system is reliable enough to help you find life-saving medicine.”

---

# PRIMARY PRODUCT PURPOSE

Users come to MedLink Ethiopia because:

* they urgently need medicine
* they are stressed
* they are uncertain
* they may already be physically exhausted
* they may not understand medical terminology

The UI must reduce:

* anxiety
* confusion
* friction
* cognitive overload

The frontend should prioritize:

* trust
* clarity
* speed
* accessibility
* emotional reassurance

---

# FRONTEND STACK (MANDATORY)

# PRIMARY STACK

Use:

## Framework

* Next.js 16+ (App Router)

Why:

* production-grade
* server components
* streaming support
* SEO
* edge readiness
* scalable architecture

---

## Language

* TypeScript (strict mode)

---

## Styling

* Tailwind CSS

BUT:
Do NOT create generic Tailwind UI.

The design system must be highly customized.

---

## Component System

Use:

* shadcn/ui

BUT:
heavily customize it.

Avoid default shadcn appearance.

---

## Animations

Use:

* Framer Motion

Animations must:

* feel intentional
* subtle
* premium
* calm

Never flashy.

---

## State Management

Use:

* Zustand

Use React Query / TanStack Query for:

* server state
* caching
* synchronization

---

## Forms

Use:

* React Hook Form
* Zod validation

---

## Maps

Use:

* Mapbox or Leaflet

---

## Icons

Use:

* Lucide React

Customize sizes and stroke weights carefully.

---

# DESIGN PHILOSOPHY

# IMPORTANT

The UI aesthetic must NOT look like:

* generic dashboards
* AI-generated template UIs
* Dribbble clones
* futuristic dark-only interfaces

Instead:
Build a timeless healthcare product.

Think:

* soft depth
* premium spacing
* strong typography hierarchy
* beautiful motion
* calm surfaces
* intelligent contrast
* clean layouts
* emotionally trustworthy design

---

# VISUAL DIRECTION

The design language should combine:

* modern healthcare aesthetics
* African warmth
* operational seriousness
* premium product clarity

Visual inspiration:

* Linear
* Notion Calendar
* Stripe Dashboard
* Headspace calmness
* Apple Health clarity
* Airbnb spacing systems

BUT adapted for healthcare logistics.

---

# COLOR SYSTEM

Avoid:

* oversaturated gradients
* neon palettes
* generic blue startup colors

Preferred palette:

* muted deep greens
* warm neutrals
* soft charcoal
* off-white surfaces
* subtle earth tones
* restrained accent colors

The UI should feel:

* medically trustworthy
* technologically advanced
* emotionally calming

---

# TYPOGRAPHY

Typography must feel:

* elegant
* readable
* trustworthy
* premium

Use:

* Inter
  OR
* Geist
  OR
* Plus Jakarta Sans

Typography hierarchy must be exceptional.

Avoid:

* tiny fonts
* cramped layouts
* dense dashboards

---

# CORE PRODUCT EXPERIENCES

# 1. MEDICINE SEARCH EXPERIENCE

This is the most important screen.

The search experience must feel:

* immediate
* intelligent
* frictionless
* calming

Requirements:

* instant search
* typo tolerance
* medicine suggestions
* generic alternatives
* recent searches
* multilingual support
* voice search ready architecture

Search results should prioritize:

* trust
* distance
* availability confidence
* pharmacy reliability

Do NOT display raw technical data aggressively.

Instead:
communicate confidence visually and clearly.

---

# 2. INVENTORY CONFIDENCE UX

This is critical.

The frontend must visually communicate:

* verified stock
* stale stock
* uncertain stock
* recently confirmed inventory

Build:

* confidence indicators
* freshness timestamps
* trust badges
* pharmacy reliability visuals

The user should instantly understand:

# “Can I trust this pharmacy before traveling?”

---

# 3. OCR PRESCRIPTION FLOW

This flow must feel magical but reliable.

User flow:

1. upload image
2. live preprocessing preview
3. OCR extraction animation
4. medicine recognition
5. editable extraction review
6. nearby medicine search

Requirements:

* drag/drop
* mobile camera upload
* preprocessing visualization
* confidence indicators
* fallback correction UI

The UI must communicate:

* AI assistance
* but also human reliability

---

# 4. PHARMACY EXPERIENCE

Pharmacy dashboard must NOT feel enterprise-heavy.

It should feel:

* lightweight
* fast
* operational
* mobile-first

Core actions:

* verify stock
* update inventory
* approve reservations
* respond quickly

Design for:

* pharmacists with low digital literacy

Requirements:

* large touch targets
* low-friction workflows
* minimal steps
* fast interaction loops

---

# 5. COMMUNITY STOCK-WATCH UX

Build a Waze-style medicine reporting experience.

Users should:

* confirm sightings
* upload proof
* validate inventory
* report shortages

Requirements:

* trust systems
* contribution rewards
* reputation indicators
* fraud prevention UX

Make the community feel:

* useful
* collaborative
* impactful

---

# 6. DELIVERY TRACKING EXPERIENCE

Delivery tracking should feel:

* reassuring
* transparent
* operationally reliable

Requirements:

* live status updates
* ETA indicators
* driver progress
* bundled delivery visualization

---

# 7. MEDICINE DETAILS PAGE

This page should include:

* medicine overview
* generic alternatives
* nearby pharmacies
* dosage guidance
* stock confidence
* pharmacy trust
* price ranges
* availability trends

Future-ready for:

* counterfeit alerts
* regional shortage warnings

---

# 8. REGIONAL MEDICINE HEATMAPS

Build elegant analytics views showing:

* shortage regions
* demand spikes
* inventory density
* outbreak indicators

Avoid:

* cluttered dashboards
* overwhelming charts

Design for:

* quick interpretation
* visual clarity
* trustworthiness

---

# RESPONSIVE DESIGN REQUIREMENTS

The experience must be:

* mobile-first
* tablet-friendly
* desktop-polished

MOST IMPORTANT:

* low-end Android usability

Performance matters heavily.

---

# PERFORMANCE REQUIREMENTS

The frontend must feel:

* instant
* lightweight
* responsive

Optimize aggressively:

* code splitting
* streaming
* image optimization
* partial hydration
* caching
* lazy loading

Target:

* excellent Lighthouse scores
* low-memory usage
* smooth low-end performance

---

# OFFLINE-FIRST UX

Critical requirement.

Build:

* graceful offline states
* sync indicators
* retry systems
* optimistic UI
* partial functionality offline

Users should NEVER feel:

* “the app broke.”

---

# ACCESSIBILITY REQUIREMENTS

Support:

* screen readers
* keyboard navigation
* reduced motion
* high contrast
* large touch areas

Healthcare apps must be inclusive.

---

# MOTION DESIGN

Animations should:

* guide attention
* reduce friction
* communicate state changes
* reinforce trust

Use:

* subtle fades
* smooth transitions
* microinteractions
* meaningful motion

Avoid:

* flashy effects
* over-animation
* distracting transitions

---

# INFORMATION ARCHITECTURE

The app structure should feel:

* obvious
* minimal
* uncluttered

Core navigation:

* Search
* Prescriptions
* Pharmacies
* Reservations
* Community
* Deliveries
* Profile

Avoid:

* deep nested menus
* enterprise sidebar overload

---

# MICROINTERACTIONS

Implement:

* intelligent loading states
* skeleton screens
* confidence animations
* subtle haptics-ready interactions
* optimistic feedback
* smooth transitions

Every interaction should feel intentional.

---

# EMPTY STATES

Empty states should:

* educate
* reassure
* guide users forward

Avoid:

* generic placeholder text

---

# ERROR STATES

Error handling must feel:

* calm
* human
* actionable

Avoid:

* technical language
* stack traces
* harsh warnings

---

# DESIGN SYSTEM REQUIREMENTS

Build a complete design system including:

* typography scale
* spacing system
* elevation system
* motion rules
* component states
* color tokens
* interaction rules

The design system must feel:

* cohesive
* premium
* scalable

---

# COMPONENTS TO BUILD

Create highly polished custom versions of:

* search bars
* medicine cards
* pharmacy cards
* confidence indicators
* OCR uploaders
* map overlays
* reservation timelines
* trust score visuals
* analytics widgets
* delivery trackers
* notification toasts
* onboarding flows

---

# FEATURES THE FRONTEND MUST INCLUDE

Add advanced UX features the founder may not have considered.

# 1. Smart Search Recovery

If no medicine found:

* suggest alternatives
* suggest nearby areas
* recommend generic names

---

# 2. Medicine Availability Prediction UX

Visually communicate:
“This medicine is likely still available.”

---

# 3. Trust Visualization Layer

Users should immediately understand:

* trustworthy pharmacies
* unreliable pharmacies
* confidence levels

---

# 4. Search Stress Reduction UX

When medicine is hard to find:

* reduce panic
* offer alternatives
* show guidance
* suggest pharmacists

---

# 5. AI Transparency UX

Show:

* confidence levels
* extraction review
* explainable recommendations

Avoid:

* “black box AI”

---

# 6. Intelligent Notification Center

Notifications should prioritize:

* urgency
* medicine importance
* reservation deadlines
* shortage alerts

---

# 7. Adaptive UI States

The interface should adapt to:

* poor connectivity
* offline state
* low-confidence results

---

# 8. Personalized Health Layer

Future-ready architecture for:

* refill reminders
* chronic medicine tracking
* medicine history

---

# CODE QUALITY REQUIREMENTS

Frontend code must be:

* modular
* scalable
* accessible
* maintainable
* strongly typed

Avoid:

* giant components
* prop drilling chaos
* inconsistent patterns

---

# FRONTEND ARCHITECTURE

Use:

* feature-based architecture

Suggested structure:

* app
* features
* shared
* entities
* widgets
* services
* hooks
* providers
* animations
* design-system

---

# ENGINEERING STANDARDS

Implement:

* Storybook
* ESLint
* Prettier
* strict TypeScript
* component testing
* accessibility testing

---

# FINAL PRODUCT FEEL

When users interact with MedLink Ethiopia, they should feel:

# “This is the first healthcare app that actually understands how healthcare works in Ethiopia.”

The frontend should feel:

* human
* operationally trustworthy
* elegant
* modern
* calm
* intelligent
* culturally grounded
* globally competitive

Build something that feels like:

# a world-class African health-tech product, not a startup template.
