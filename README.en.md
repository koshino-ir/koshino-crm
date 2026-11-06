<div align="center">

# Koshino CRM

**A modern, multi-tenant CRM for software agencies and service businesses**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![PWA](https://img.shields.io/badge/PWA-installable-5A0FC8?logo=pwa&logoColor=white)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.en.md) · [فارسی](README.fa.md) · [العربية](README.ar.md)

</div>

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Architecture](#architecture)
5. [Database Schema](#database-schema)
6. [API Reference](#api-reference)
7. [Quick Start](#quick-start)
8. [Environment Variables](#environment-variables)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Security](#security)
12. [Screenshots](#screenshots)
13. [Roadmap](#roadmap)
14. [License](#license)

---

## Overview

**Koshino CRM** is a full-stack Customer Relationship Management platform built for teams that sell, deliver, and bill — specifically software agencies, consultancies, and service businesses. It covers the complete customer lifecycle: from lead capture through deal closure, project delivery, and invoicing.

The application is **multi-tenant** (one installation serves many organizations with strict data isolation), **multi-language** (Persian, English, Arabic with native RTL), and **installable as a PWA** on desktop and mobile.

This project is a production-grade reference implementation demonstrating clean architecture, SOLID principles, comprehensive testing, and modern frontend engineering.

---

## Features

### Sales & Pipeline Management
- **Kanban pipeline** with drag-and-drop between stages
- **Auto-status transitions** — moving a deal to a "won" stage updates its status automatically
- **Per-stage totals** — revenue aggregated per column in real time
- **Multiple pipelines** per organization, each with custom stages
- **Auto-provisioned default pipeline** for new organizations (Qualified → Proposal → Negotiation → Won / Lost)

### CRM Core
- **Companies** — clients and prospects, with industry, contact info, and notes
- **Contacts** — people at companies, with primary flag and position
- **Leads** — inbound prospects before qualification
- **Deals** — opportunities with amount, currency, probability, and expected close date
- **Projects** — deliverables after a deal closes, with status and budget
- **Invoices** — auto-numbered per organization, with tax calculation and paid-tracking

### Lead Conversion
- One-click convert a lead to a deal
- Auto-creates a company if the lead has none
- Marks lead as `qualified` and links the two records

### Activities & Tasks
- **Activity log** — calls, emails, meetings, and notes, linked polymorphically to deals, leads, contacts, or companies
- **Tasks** — priority (low/medium/high/urgent), due dates, assigned owner, complete/reopen toggle
- **Overdue highlighting** — past-due tasks surface visually

### Dashboard
- **Live KPIs** — open deals count & value, won deals, companies, leads, open tasks, overdue tasks
- **Sales funnel** — deal count and value per stage
- **Revenue chart** — 6-month rolling sum of won deals (SVG-based, no chart library dependency)
- **Recent activities feed** — 10 latest interactions

### Multi-Tenancy
- Row-level isolation via `organization_id` on every domain model
- `X-Organization-Id` header determines active context
- Automatic fallback to the user's first active membership
- Membership roles: `owner`, `admin`, `member`
- Per-org invitation flow with expiring tokens

### Authentication & Authorization
- **JWT in HttpOnly cookies** (secure against XSS)
- **CSRF protection** via double-submit cookie
- **Google OAuth 2.0** sign-in
- **Role-based permissions** enforced at view level
- **Password validation** via Django's validators
- **Argon2** password hashing
- **Rate limiting** on auth and invitation endpoints

### Internationalization
- Full **Persian / English / Arabic** UI
- **Automatic RTL** layout switching
- Logical CSS properties (`ms-`, `me-`, `ps-`, `pe-`) throughout
- Per-user language preference persisted
- Localized dates, numbers, and placeholders

### PWA
- Installable on Android, iOS, and desktop
- **Service worker** caching strategy:
  - Network-first for API
  - Cache-first for fonts, images, static assets
- **Offline fallback page** with retry
- Custom **install prompt** and **update prompt** (opt-in reload)
- **Offline banner** on network loss

### Audit & Security
- **Audit log** on create/update of Deals and Companies
- **Secure file uploads** — extension allowlist, 10 MB max, MIME validation
- **Authenticated downloads** — attachments never exposed via static MEDIA_URL
- **Soft delete** with `deleted_at` and restore capability
- **Argon2** password hashing
- **Security headers** in production (HSTS, CSP-ready, X-Frame-Options)

---

## Tech Stack

### Backend
| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Framework | Django 5.1 + Django REST Framework 3.15 |
| Database | PostgreSQL 16 |
| Cache/Broker | Redis 7 |
| Async | Celery 5.4 |
| Auth | `djangorestframework-simplejwt` (HttpOnly cookies) |
| OAuth | Google OAuth 2.0 |
| Docs | `drf-spectacular` (OpenAPI 3.1) |
| Testing | pytest + pytest-django + factory_boy |

### Frontend
| Layer | Technology |
|-------|-----------|
| Framework | Vue 3.5 (Composition API + `<script setup>`) |
| Language | TypeScript 5.6 (strict mode) |
| Build | Vite 6 |
| Styling | Tailwind CSS v4 (CSS-first tokens) |
| State | Pinia + TanStack Query |
| Routing | Vue Router 4 |
| i18n | vue-i18n 10 |
| Drag & drop | vue-draggable-plus |
| PWA | vite-plugin-pwa + Workbox |
| Icons | lucide-vue-next |

### Infrastructure
| Layer | Technology |
|-------|-----------|
| Dev orchestration | Docker Compose (`docker-compose.infra.yml`) |
| Prod orchestration | Docker Compose (`docker-compose.prod.yml`) |
| Frontend serving | Nginx 1.27 (security headers, gzip, immutable asset cache) |
| Backend serving | Gunicorn (4 workers) |
| TLS | Certbot / Let's Encrypt |
| CI/CD | GitHub Actions |

---

## Architecture

### Directory Structure

```
koshino-crm/
├── backend/
│   ├── config/                 Django project configuration
│   │   ├── settings/
│   │   │   ├── base.py         shared settings
│   │   │   ├── dev.py          local development
│   │   │   ├── test.py         isolated test env (locmem cache, MD5 hashing)
│   │   │   └── prod.py         hardened production
│   │   ├── urls.py             root URL conf
│   │   ├── asgi.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   ├── apps/
│   │   ├── common/             BaseModel, exceptions, pagination, mixins, permissions
│   │   ├── accounts/           User, Organization, Membership, Invitation, JWT, OAuth
│   │   ├── crm/                Company, Contact, Pipeline, Stage, Lead, Deal
│   │   ├── activities/         Activity, Task
│   │   ├── audit/              AuditLog with signal-based auto-logging
│   │   ├── dashboard/          Aggregation selectors and views
│   │   ├── projects/           Project, Invoice
│   │   ├── attachments/        Secure file uploads
│   │   └── core/               Health check and shared utilities
│   ├── tests/
│   │   ├── conftest.py         Shared fixtures
│   │   ├── accounts/           Auth, org, invitation tests
│   │   ├── crm/                Deal, lead, kanban tests
│   │   ├── activities/         Activity and task tests
│   │   ├── projects/           Project and invoice tests
│   │   ├── attachments/        Upload security tests
│   │   └── dashboard/          Aggregation tests
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── core/
│   │   │   ├── api/            Axios client, interceptors, endpoint modules
│   │   │   ├── stores/         Pinia stores (auth, organization, ui)
│   │   │   ├── router/         Route definitions and guards
│   │   │   ├── i18n/           Locale files and configuration
│   │   │   ├── pwa/            Service worker registration
│   │   │   ├── seo/            Meta tag management
│   │   │   ├── config.ts
│   │   │   └── utils/
│   │   ├── modules/
│   │   │   ├── auth/           Login, register, callback pages
│   │   │   ├── landing/        Marketing landing page
│   │   │   ├── dashboard/      KPI cards, funnel, revenue chart
│   │   │   ├── deals/          Kanban board, detail page
│   │   │   ├── companies/      CRUD with search
│   │   │   ├── contacts/       CRUD linked to companies
│   │   │   ├── leads/          CRUD with convert dialog
│   │   │   ├── tasks/          CRUD with status filtering
│   │   │   ├── activities/     Timeline view
│   │   │   ├── projects/       CRUD with client picker
│   │   │   ├── invoices/       CRUD with mark-paid action
│   │   │   └── settings/       Organization, members, preferences
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── ui/         Button, Input, Select, Card, Avatar, Spinner, Skeleton, Textarea
│   │   │   │   ├── layout/     Sidebar, Topbar, UserMenu, LangSwitcher, ThemeToggle, PwaPrompts
│   │   │   │   ├── DataTable.vue
│   │   │   │   ├── Pagination.vue
│   │   │   │   ├── ConfirmDialog.vue
│   │   │   │   └── FormModal.vue
│   │   │   ├── layouts/        AppLayout, AuthLayout
│   │   │   └── composables/
│   │   ├── assets/
│   │   │   └── styles/main.css Design tokens
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/                 PWA manifest, service worker, offline page
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
├── docker/
│   ├── backend.Dockerfile      Multi-stage
│   ├── frontend.Dockerfile     Multi-stage
│   ├── nginx.conf
│   └── nginx.prod.conf
├── docker-compose.yml          Production full stack
├── docker-compose.infra.yml    Local dev (db + redis only)
├── docker-compose.prod.yml     Production build
├── .env.example
├── .env.prod.example
└── README.md                   ← You are here
```

### Layered Backend

The backend follows a strict **layered architecture**:

1. **Views** (thin) — parse request, delegate to service or selector, envelope response
2. **Serializers** — validate input, resolve foreign keys against the current org
3. **Services** (`services/*.py`) — business logic, transactional operations
4. **Selectors** (`selectors.py`) — N+1-safe complex queries
5. **Models** — data integrity constraints, indexes, `BaseModel` inheritance

**Example — Deal creation flow:**

```
POST /api/v1/deals/
   ↓
DealListCreateView (OrgScopedViewMixin + EnvelopeModelViewMixin)
   ↓
DealSerializer.validate_* → resolves company_id, pipeline_id, stage_id against org
   ↓
deal_service.create_deal (atomic)
   ↓   computes order (max+1 within stage)
   ↓   defaults stage to first in pipeline
Deal.objects.create
   ↓
AuditLog (via signal)
   ↓
Response envelope { success, data, message, errors, meta }
```

### API Envelope

Every endpoint returns:

```json
{
  "success": true,
  "data": { ... },
  "message": "OK",
  "errors": null,
  "meta": { "count": 42, "page": 1, "page_size": 20, "total_pages": 3 }
}
```

This is enforced by:
- `apps/common/responses.py` (APIResponse class)
- `apps/common/exceptions.py` (custom_exception_handler)
- `apps/common/pagination.py` (EnvelopePagination)

---

## Database Schema

### Core tables

| Table | Purpose | Key columns |
|-------|---------|-------------|
| `accounts_user` | Custom user (email login) | `email` (unique), `google_id`, `language` |
| `accounts_organization` | Tenant | `slug` (unique), `default_currency`, `default_language` |
| `accounts_membership` | User ↔ Org link | `role`, `is_active` |
| `accounts_invitation` | Pending invites | `token`, `expires_at` |
| `crm_company` | Client organization | `name`, `industry`, `owner` |
| `crm_contact` | Person at company | `first_name`, `email`, `company` FK |
| `crm_pipeline` | Sales pipeline | `name`, `is_default` |
| `crm_stage` | Pipeline stage | `order`, `color`, `is_won`, `is_lost` |
| `crm_lead` | Pre-qualified prospect | `status`, `source`, `owner` |
| `crm_deal` | Opportunity | `amount`, `stage` FK, `order`, `status` |
| `activities_activity` | Logged interaction | `type`, `occurred_at` + polymorphic FK |
| `activities_task` | To-do | `priority`, `due_date`, `status` |
| `projects_project` | Deliverable | `status`, `budget`, `client_company` |
| `projects_invoice` | Billing document | `number` (per-org unique), `total`, `paid_at` |
| `audit_audit_log` | Change tracking | `action`, `entity_type`, `entity_id`, `changes` JSONB |
| `attachments_attachment` | File | `file`, `mime_type`, `size`, polymorphic FK |

### Design decisions

- **UUID primary keys** — collision-resistant, safe to expose in URLs
- **`organization_id` on every domain table** — enables row-level multi-tenancy without schema-per-tenant complexity
- **Soft delete** (`deleted_at`) with `ActiveManager` — restore capability and audit trail
- **Composite indexes** on high-cardinality filter patterns:
  - `(organization_id, status, owner_id)` on Deal
  - `(organization_id, pipeline_id, stage_id)` on Deal
  - `(organization_id, assigned_to_id, status, due_date)` on Task
- **Conditional unique constraint** on invoice number per org (respecting soft delete)
- **`order` integer** on Stage and Deal — enables drag-and-drop ordering without extra tables

---

## API Reference

Full interactive documentation is available at **`/api/docs/`** (Swagger UI) once the backend is running.

### Conventions

| Aspect | Rule |
|--------|------|
| Base URL | `/api/v1/` |
| Auth | JWT in HttpOnly cookies |
| CSRF | `X-CSRFToken` header required for POST/PUT/PATCH/DELETE |
| Multi-tenancy | `X-Organization-Id` header (optional; falls back to first membership) |
| Pagination | `?page=1&page_size=20` (max 100) |
| Filtering | Query params per endpoint (see below) |
| Sorting | `?ordering=-created_at` where supported |
| Response | Envelope `{ success, data, message, errors, meta }` |

### Endpoint summary

**Auth**
- `POST /auth/register/` — create user + organization
- `POST /auth/login/` — set cookies
- `POST /auth/logout/` — clear cookies
- `POST /auth/token/refresh/` — rotate access token
- `GET|PATCH /auth/me/` — profile
- `POST /auth/password/change/`
- `GET /auth/csrf/` — get CSRF token
- `GET /auth/google/` — returns OAuth consent URL
- `GET /auth/google/callback/` — OAuth callback (sets cookies, redirects)
- `POST /auth/invitations/accept/`

**Organizations**
- `GET|POST /organizations/`
- `GET|PATCH|DELETE /organizations/{id}/`
- `GET /organizations/{id}/members/`
- `PATCH|DELETE /organizations/{id}/members/{mid}/`
- `POST /organizations/{id}/invitations/`

**CRM**
- `GET|POST /companies/` — filter: `search`, `industry`, `owner`
- `GET|PATCH|DELETE /companies/{id}/`
- `GET|POST /contacts/` — filter: `search`, `company`, `owner`
- `GET|PATCH|DELETE /contacts/{id}/`
- `GET|POST /pipelines/`
- `GET|PATCH|DELETE /pipelines/{id}/`
- `POST /pipelines/ensure-default/` — idempotent
- `GET|POST /pipelines/{id}/stages/`
- `PATCH|DELETE /stages/{id}/`
- `GET|POST /leads/` — filter: `search`, `status`, `source`, `owner`
- `GET|PATCH|DELETE /leads/{id}/`
- `POST /leads/{id}/convert/` — creates deal, requires `pipeline_id`
- `GET|POST /deals/` — filter: `search`, `pipeline`, `stage`, `status`, `owner`
- `GET|PATCH|DELETE /deals/{id}/`
- `GET /deals/kanban/?pipeline={id}` — board structure ready for UI
- `PATCH /deals/{id}/move/` — `{ stage_id, order? }` for drag-and-drop

**Activities**
- `GET|POST /activities/` — filter: `search`, `type`, `deal`, `lead`, `company`, `date_from`, `date_to`
- `GET|PATCH|DELETE /activities/{id}/`
- `GET|POST /tasks/` — filter: `search`, `status`, `priority`, `assigned_to`, `deal`, `due_before`
- `GET|PATCH|DELETE /tasks/{id}/`
- `POST /tasks/{id}/complete/`
- `POST /tasks/{id}/reopen/`

**Projects & Invoices**
- `GET|POST /projects/` — filter: `search`, `status`, `client`, `owner`
- `GET|PATCH|DELETE /projects/{id}/`
- `GET|POST /invoices/` — filter: `search`, `status`, `project`
- `GET|PATCH|DELETE /invoices/{id}/`
- `POST /invoices/{id}/mark-paid/`

**Dashboard**
- `GET /dashboard/stats/` — KPI object
- `GET /dashboard/funnel/` — array of stages with counts and totals
- `GET /dashboard/revenue/?months=6` — monthly sums
- `GET /dashboard/recent-activities/` — latest 10

**Search & Audit**
- `GET /search/?q={query}` — global search across companies, contacts, deals, leads
- `GET /audit-logs/` — filter: `entity_type`, `entity_id` (owner/admin only)

**Attachments**
- `GET|POST /attachments/` — multipart upload, filter by `deal`, `company`, `project`
- `GET|DELETE /attachments/{id}/`
- `GET /attachments/{id}/download/` — authenticated stream

---

## Quick Start

### Prerequisites

- **Python 3.12+**
- **Node 20+**
- **Docker** (for Postgres + Redis only in dev)
- **Git**

### Local development (recommended)

```bash
git clone https://github.com/koshino-ir/koshino-crm.git
cd koshino-crm

# 1. Environment
cp .env.example .env

# 2. Infrastructure (Postgres on :55432, Redis on :56379)
docker compose -f docker-compose.infra.yml up -d

# 3. Backend
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python manage.py migrate
python manage.py runserver
# → http://localhost:8000  (health: /api/v1/health/, docs: /api/docs/)

# 4. Frontend (new terminal)
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

Then open **http://localhost:5173**, register a workspace, and explore.

### Full Docker (production-like)

```bash
cp .env.prod.example .env.prod
# Edit .env.prod — generate secure DJANGO_SECRET_KEY, DB password, Redis password

# Generate a secret key
python -c "import secrets; print(secrets.token_urlsafe(50))"

docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
# → http://localhost
```

---

## Environment Variables

### Development (`.env`)

```env
# Django
DJANGO_SECRET_KEY=dev-insecure-change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=koshino_crm
POSTGRES_USER=koshino
POSTGRES_PASSWORD=dev-password
DATABASE_URL=postgres://koshino:dev-password@localhost:55432/koshino_crm

# Redis
REDIS_PASSWORD=dev-redis-password
REDIS_URL=redis://:dev-redis-password@localhost:56379/0

# CORS / CSRF
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost:8000

# Google OAuth (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback/
FRONTEND_URL=http://localhost:5173
```

### Production (`.env.prod`)

See `.env.prod.example` in the repository.

---

## Testing

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Test coverage:
- Auth flows (register, login, logout, token refresh, password change)
- Multi-tenant isolation (cross-org access rejected)
- Deal creation, kanban grouping, stage movement
- Lead conversion (creates deal, marks qualified, cannot convert twice)
- Invoice numbering (unique per org), mark-paid, date validation
- Attachment upload security (extension allowlist, size limit, single-target rule)
- Attachment download authorization
- Audit log creation on Deal/Company save
- Dashboard aggregations (KPI, funnel, revenue)
- Global search across entities

Test environment uses:
- `config.settings.test` (locmem cache, MD5 hashing for speed)
- In-memory throttle limits (no cross-run pollution)
- Temp directory for media files (no permission issues)

---

## Deployment

### Production architecture

```
                   ┌─────────────────────────┐
       :80/:443 ──▶│ Nginx (frontend + proxy) │
                   └───────────┬─────────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
         ┌──────────────────┐   ┌────────────────────┐
         │  Vue SPA (dist)  │   │  /api → Gunicorn   │
         └──────────────────┘   └─────────┬──────────┘
                                          │
                          ┌───────────────┼───────────────┐
                          ▼               ▼               ▼
                    ┌──────────┐   ┌──────────┐   ┌──────────┐
                    │ Postgres │   │  Redis   │   │  Celery  │
                    └──────────┘   └──────────┘   └──────────┘
```

### Steps on a fresh VPS

1. **Provision server** — Ubuntu 22.04+ or Debian 12, 2 vCPU / 4 GB RAM minimum
2. **Install Docker & Compose**
3. **Firewall** — allow only 22, 80, 443
4. **DNS** — point A record to server IP
5. **Deploy** — copy repo, create `.env.prod`, run `docker compose -f docker-compose.prod.yml up -d --build`
6. **TLS** — Certbot + Nginx SSL config (see `docs/deployment.md`)
7. **Backups** — daily `pg_dump` + retention policy

### Scaling notes

- **Gunicorn workers** — `(2 × cores) + 1` is a good default; tune per workload
- **Celery** — split into queues (`default`, `email`, `reports`) for isolation
- **Postgres** — connection pooling via PgBouncer above ~50 workers
- **Redis** — separate instances for cache vs. broker at scale
- **Static files** — CDN in front of `/assets/*`

---

## Security

The application implements defense in depth:

| Layer | Control |
|-------|---------|
| **Transport** | HTTPS enforced (HSTS with `includeSubDomains`, `preload`) |
| **Session** | JWT in HttpOnly + Secure + SameSite=Lax cookies |
| **CSRF** | Double-submit token + `X-CSRFToken` header on mutations |
| **Auth** | Argon2 hashing, password validators, rate limiting |
| **API** | Per-org object-level checks on every view |
| **Data** | UUID PKs (no enumeration), soft delete (audit trail) |
| **Files** | Extension + MIME + size allowlist, authenticated download, no direct MEDIA_URL |
| **Headers** | `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` |
| **Logging** | Audit log on sensitive entities, structured production logs |
| **Dependency** | `ruff` + `mypy` in CI, `pip-audit` recommended |

---

## Screenshots


| | |
|---|---|
| **Deals Kanban** | **Dashboard** |
| ![Kanban](docs/screenshots/en/deals-kanban.png) | ![Dashboard](docs/screenshots/en/dashboard.png) |
| **Companies** | **Login** |
| ![Companies](docs/screenshots/en/companies.png) | ![Login](docs/screenshots/en/login.png) |

---

## Roadmap

### Shipped
- [x] MVP: CRM with full pipeline, deals, companies, contacts, leads
- [x] Tasks and activities
- [x] Projects and invoicing
- [x] Dashboard with charts
- [x] Multi-tenant isolation
- [x] JWT auth in HttpOnly cookies + Google OAuth
- [x] Three-language UI with native RTL
- [x] PWA (installable, offline, service worker)
- [x] Audit log
- [x] Docker production + Nginx + security headers

### Planned
- [ ] Email notifications (invitations, reminders)
- [ ] CSV/Excel export for deals, invoices, contacts
- [ ] File attachment UI in Deal detail page
- [ ] Webhook integrations (Slack, Zapier)
- [ ] Team activity reports (per-member)
- [ ] Deal probability auto-adjustment based on stage history
- [ ] Bulk operations (mass assign, mass update)
- [ ] Custom fields per organization

---

## License

MIT License — see [LICENSE](LICENSE).

---

## Author

**Koshino** — [github.com/koshino-ir](https://github.com/koshino-ir)

Questions, feedback, or a project in mind?  
📧 `info@koshino.ir`

---

<div align="center">

**Built with ❤️ for teams that sell and deliver.**

⭐ Star this repo if you find it useful.

</div>
