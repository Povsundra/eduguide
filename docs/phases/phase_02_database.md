# Phase 02 — Database Foundation

## Objective

Establish the complete database foundation for the EduGuide platform.

This phase prepares all persistence layers for future development by configuring relational database infrastructure, database migration management, ORM models, repository architecture, and connection management.

This phase does **not** implement business entities, Knowledge Graph schema, vector indexing, RAG, Recommendation Engine, AI Agents, authentication, or application business logic.

The outcome is a production-ready database layer that future phases can safely build upon.

---

# Required Reading (before any planning or coding)

- `.ai/agent.md`
- `.ai/planner.md`
- `docs/00_project_context.md`
- `docs/01_vision.md`
- `docs/02_architecture.md`
- `docs/03_roadmap.md`

Do not write a plan or any code until these documents are fully understood.

If documentation conflicts with this phase specification, stop and report the conflict.

Do not make assumptions.

---

# Decision Authority

Unless explicitly instructed:

Do not

- change database technologies
- replace SQLAlchemy
- replace Alembic
- replace PostgreSQL
- redesign repository architecture
- redesign dependency injection
- redesign configuration management

If improvements are identified,

Explain them.

Wait for approval.

Do not implement them automatically.

---

# Working Protocol

This phase is divided into sub-phases.

Each sub-phase follows the workflow below.

## Step 1

Plan

Output only:

- Files to create
- Files to modify
- Key decisions
- Assumptions

Do not write code.

---

## Step 2

Approval

Wait until I explicitly approve.

Do not continue automatically.

---

## Step 3

Build

Implement only the approved work.

If implementation requires changes to the approved plan,

Stop.

Explain.

Request approval.

---

## Step 4

Test & Report

Validate the implementation.

Provide the report.

Stop.

Wait for approval before continuing.

---

Never combine multiple sub-phases into one implementation.

---

# Report Format

Use this format after every sub-phase.

```text
## Summary

## Files Created

## Files Modified

## Validation

## Known Issues

## Remaining Work
```

---

# Sub-Phase Breakdown

---

## 2.1 Database Configuration

Scope

Create centralized database configuration.

Requirements

- SQLAlchemy configuration
- Database session management
- Async-ready architecture
- Configuration via environment variables
- Dependency Injection support

Acceptance Criteria

- Database configuration loads successfully
- Environment variables validated
- Session creation works

---

## 2.2 Alembic Configuration

Scope

Initialize migration framework.

Requirements

- Alembic configured
- Migration environment created
- Version directory configured
- Naming convention configured

Explicitly out of scope

- Business migrations
- Application tables

Acceptance Criteria

- Alembic initializes successfully
- Empty migration can be generated
- Upgrade and downgrade commands execute successfully

---

## 2.3 Base ORM Architecture

Scope

Create reusable ORM foundation.

Requirements

Create

- Base model
- Timestamp mixin
- UUID primary key mixin
- Soft delete mixin (if defined in architecture)
- Common metadata

Do not create application entities.

Acceptance Criteria

- Base classes reusable
- Metadata generated successfully

---

## 2.4 Repository Architecture

Scope

Create repository layer.

Requirements

- Generic repository
- CRUD base interface
- Repository abstraction
- Dependency injection integration

Do not implement repositories for business entities.

Acceptance Criteria

- Repository layer compiles
- Dependency injection works

---

## 2.5 Database Utilities

Scope

Create shared database utilities.

Requirements

- Transaction manager
- Session provider
- Connection utilities
- Health check utilities

Acceptance Criteria

- Utilities tested
- Connections properly closed

---

## 2.6 PostgreSQL Validation

Scope

Validate PostgreSQL infrastructure.

Requirements

- Connection pooling
- Connection retry
- Health validation

Do not create application tables.

Acceptance Criteria

- Database connection succeeds
- Pool configuration verified

---

## 2.7 Testing Infrastructure

Scope

Prepare testing utilities.

Requirements

- Test database configuration
- Fixtures
- Database rollback strategy
- Temporary database session

Acceptance Criteria

- Test session created successfully
- Rollback verified

---

## 2.8 Documentation

Scope

Document database architecture.

Requirements

Update

README

Include

- Database architecture
- Migration workflow
- Alembic usage
- Environment variables
- Local development

Acceptance Criteria

A new developer can initialize the database using documentation alone.

---

# Deliverables

The completed phase must provide

- Database configuration
- Alembic
- ORM base classes
- Repository architecture
- Session management
- Transaction manager
- Health utilities
- Testing utilities
- Updated documentation

---

# Pre-Push Checklist

Before this phase is considered complete:

- [ ] Database configuration validated
- [ ] Alembic initializes successfully
- [ ] Empty migration executes successfully
- [ ] Session management verified
- [ ] Connection pool verified
- [ ] Health check passes
- [ ] Repository layer compiles
- [ ] Test infrastructure operational
- [ ] Documentation updated

If any item fails,

Do not mark the phase complete.

---

# Out of Scope

This phase must NOT implement

- User entity
- University entity
- Major entity
- Scholarship entity
- Curriculum entity
- Career entity
- Graph database
- Neo4j nodes
- Relationships
- Knowledge ingestion
- Vector database
- Embeddings
- RAG
- Recommendation
- AI Agent
- Business services
- REST APIs

Those belong to later phases.

---

# Definition of Success

This phase is complete only when

- Every acceptance criterion passes
- Database infrastructure is production-ready
- Future entities can be added without redesign
- Migration workflow is stable
- Repository architecture is reusable
- Documentation is complete

---

# Final Phase Report

After sub-phase 2.8 is approved,

Provide a consolidated report including

## Summary

## Files Created

## Files Modified

## Validation

## Known Issues

## Remaining Work

## Completed Pre-Push Checklist

Do not begin Phase 03 automatically.

Wait for explicit approval.