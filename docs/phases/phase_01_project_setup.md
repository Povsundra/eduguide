# Phase 01 — Project Foundation & Development Environment

## Objective

Establish the complete production-ready development foundation for the EduGuide platform: project structure, development environment, infrastructure, containerization, code quality tooling, CI, and skeleton backend/frontend applications.

This phase does **not** implement business logic, Knowledge Graph schema, RAG, Recommendation Engine, AI Agents, or application features. Those belong to later phases.

The outcome is a clean, reproducible development environment that every later phase builds on.

---

## Required Reading (before any planning or coding)

- `.ai/agent.md`
- `.ai/planner.md`
- `docs/00_project_context.md`
- `docs/01_vision.md`
- `docs/02_architecture.md`
- `docs/03_roadmap.md`

Do not write a plan or any code until these are read and understood. If anything in this phase spec conflicts with those documents, stop and flag the conflict instead of guessing which one wins.

---

## Working Protocol (applies to every sub-phase below)

This phase is broken into sub-phases (1.1, 1.2, …). Each sub-phase follows the same four-step loop, and **you do not advance to the next sub-phase without my explicit approval.**

1. **Plan** — Before writing any code, output a short plan for this sub-phase only: files to be created/modified, key decisions, and any assumptions. No implementation yet.
2. **Approve** — Stop and wait. I will respond "approved" or give corrections. Do not proceed on silence or assumption.
3. **Build** — Implement exactly what was approved. If you discover during implementation that the approved plan needs to change, stop and re-propose rather than silently deviating.
4. **Test & Report** — Run the validation listed in that sub-phase's Acceptance Criteria, then give a short report (see Report Format below). Wait for my approval before moving to the next sub-phase.

**Never batch multiple sub-phases into one plan or one build step.** One sub-phase = one plan = one approval = one build = one test = one report.

**Report Format** (use this for every sub-phase, and again for the full phase at the end):

```
## Summary
## Files Created
## Files Modified
## Validation (what was actually run, and the result)
## Known Issues
## Remaining Work (only if part of this sub-phase was deferred)
```

---

## Sub-Phase Breakdown

### 1.1 — Repository Structure

Scope: create the top-level directory layout only. No dependency files with real content yet, no code logic.

```text
eduguide/
├── .ai/
├── docs/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── nginx/
├── docker/
├── scripts/
├── .env.example
├── docker-compose.yml
├── Makefile
├── README.md
└── .gitignore
```

Acceptance Criteria:
- Directory tree matches the above
- `.gitignore` covers Python, Node, Docker, IDE, and env files
- No implementation code yet

---

### 1.2 — Backend Foundation (FastAPI skeleton)

Stack: Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.x, Alembic, Pydantic v2.

Scope:
- Modular app structure (config, logging, API versioning, dependency-injection-ready)
- `GET /` → `{"service": "EduGuide API", "status": "running"}`
- `GET /health` (stub only — real DB checks happen in 1.5)
- Lifespan events, CORS config, environment loading via Pydantic settings

Explicitly out of scope: auth, business routes, DB models.

Acceptance Criteria:
- `uvicorn app.main:app` starts without errors locally
- `GET /` and `GET /health` return expected JSON

---

### 1.3 — Frontend Foundation (React skeleton)

Stack: React, TypeScript, Vite, TailwindCSS, React Router, Zustand, Axios, ESLint, Prettier.

Scope:
- Home page, Not Found page
- Routing configured
- No UI design polish — structural skeleton only

Acceptance Criteria:
- `npm run dev` starts without errors
- Home route renders

---

### 1.4 — Docker & Docker Compose

Scope:
- Dockerfile for backend, Dockerfile for frontend
- `docker-compose.yml` wiring backend, frontend, PostgreSQL, Neo4j, Redis
- `docker compose up` works with zero manual steps

Acceptance Criteria:
- Full stack builds and starts via `docker compose up`
- All containers reach a healthy/running state

---

### 1.5 — Database Connections (PostgreSQL, Neo4j, Redis)

Scope:
- SQLAlchemy engine + Alembic initialized (no application tables yet)
- Neo4j driver configured with a connection test
- Redis connection test
- Wire real checks into `GET /health`

Explicitly out of scope: schema design, graph ontology, caching logic.

Acceptance Criteria:
- `GET /health` reports true connectivity to all three services, not stubs
- Alembic can run (even with zero migrations)

---

### 1.6 — Code Quality Tooling

Scope: Ruff, Black, isort, mypy configured for backend; ESLint/Prettier confirmed for frontend; pre-commit hooks wired to run these automatically.

Acceptance Criteria:
- `pre-commit run --all-files` passes clean
- mypy passes with no errors on the skeleton code

---

### 1.7 — CI Pipeline

Scope: GitHub Actions workflow that installs backend + frontend deps, runs formatting, linting, and tests on every push/PR.

Acceptance Criteria:
- Workflow file present and syntactically valid
- **You must show me the CI run passing green (or the local equivalent output) before I push anything to the repo.** This is a hard gate — do not tell me the phase is done until this is confirmed.

---

### 1.8 — Documentation

Scope: `README.md` (overview, requirements, installation, Docker usage, env setup, running locally vs. via Docker) and a complete `.env.example`.

Acceptance Criteria:
- A new developer could follow the README alone and get the stack running

---

## Pre-Push Checklist (final gate for the whole phase)

Before anything is pushed to the repo, confirm all of the following explicitly in your final report — do not just assert "done":

- [ ] `docker compose up` succeeds from a clean clone
- [ ] `GET /health` shows real (not stubbed) connectivity for Postgres, Neo4j, Redis
- [ ] Ruff / Black / isort / mypy all pass
- [ ] Frontend lints clean and dev server starts
- [ ] CI workflow passes (paste or describe the actual run result)
- [ ] README and `.env.example` are complete and accurate

If any box is unchecked, the phase is not complete — report it as remaining work instead of marking the phase done.

---

## Out of Scope for All of Phase 1

Authentication, Users, Knowledge Graph schema, RAG, Recommendation Engine, AI Agents, File Upload, Search, Dashboard, any business logic. These start in later phases.

---

## Final Phase Report

After sub-phase 1.8 is approved, produce one consolidated report using the Report Format above, covering the entire phase, plus the completed Pre-Push Checklist.

**Do not begin Phase 02 automatically. Wait for explicit approval.**