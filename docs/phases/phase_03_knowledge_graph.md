# Phase 03 — Knowledge Graph Foundation

## Objective

Establish the complete Knowledge Graph foundation for the EduGuide platform.

This phase designs and implements the graph database infrastructure, graph access layer, ontology implementation, graph constraints, indexing strategy, and reusable graph services.

This phase does **not** ingest university data, create embeddings, implement retrieval, RAG, recommendation, or application business logic.

The outcome is a production-ready Knowledge Graph platform that future phases can populate with educational knowledge.

---

# Required Reading (before any planning or coding)

- `.ai/agent.md`
- `.ai/planner.md`
- `docs/00_project_context.md`
- `docs/01_vision.md`
- `docs/02_architecture.md`
- `docs/03_roadmap.md`
- `docs/04_ontology.md`
- `docs/05_graph_design.md`

Do not write a plan or any code until these documents are fully understood.

If documentation conflicts with this phase specification, stop and report the conflict.

Never make assumptions.

---

# Decision Authority

Unless explicitly instructed:

Do not

- modify the ontology
- redesign graph schema
- rename node labels
- rename relationship types
- change Neo4j version
- replace Neo4j with another graph database
- redesign graph architecture

If improvements are identified:

- Explain the proposal.
- Justify the benefits.
- Wait for approval.

Do not implement automatically.

---

# Working Protocol

This phase is divided into sub-phases.

Each sub-phase follows the same workflow.

### Step 1 — Plan

Before writing code, output only:

- Files to create
- Files to modify
- Key implementation decisions
- Assumptions
- Risks

Do not write code.

---

### Step 2 — Approval

Wait until explicit approval is received.

Never continue automatically.

---

### Step 3 — Build

Implement only the approved work.

If implementation requires changing the approved plan:

Stop.

Explain why.

Wait for approval.

---

### Step 4 — Test & Report

Run all validation required by that sub-phase.

Provide the report.

Wait before continuing.

---

Never combine multiple sub-phases.

One approval = one sub-phase.

---

# Report Format

Use this report after every sub-phase.

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

## 3.1 Neo4j Configuration

Scope

Create the production-ready Neo4j integration layer.

Requirements

- Neo4j driver configuration
- Connection management
- Session management
- Dependency Injection support
- Environment variable configuration

Acceptance Criteria

- Driver connects successfully
- Sessions open correctly
- Sessions close correctly
- Health check passes

---

## 3.2 Graph Architecture

Scope

Implement reusable graph infrastructure.

Requirements

Create

- Graph service
- Graph repository base
- Query execution utilities
- Transaction manager

Do not implement domain queries.

Acceptance Criteria

- Graph services reusable
- Transactions work
- Query execution verified

---

## 3.3 Ontology Implementation

Scope

Implement the ontology exactly as documented.

Requirements

Create graph definitions for

- Node Labels
- Relationship Types
- Property definitions

Do not insert any data.

Acceptance Criteria

- Ontology matches documentation
- No undocumented labels exist
- No undocumented relationships exist

---

## 3.4 Constraints & Indexes

Scope

Create graph constraints and indexes.

Requirements

Implement

- Unique constraints
- Required indexes
- Lookup indexes

Do not optimize beyond documented requirements.

Acceptance Criteria

- Constraints created successfully
- Indexes created successfully
- Verification queries succeed

---

## 3.5 Graph Repository Layer

Scope

Create reusable graph repositories.

Requirements

Create

- BaseGraphRepository
- Query helpers
- Read operations
- Write operations

Do not create repositories for specific entities.

Acceptance Criteria

- Repository compiles
- CRUD operations verified

---

## 3.6 Graph Validation

Scope

Create graph validation utilities.

Requirements

Implement

- Connectivity validation
- Constraint validation
- Index validation
- Schema validation

Acceptance Criteria

- Validation reports pass
- Graph schema verified

---

## 3.7 Testing Infrastructure

Scope

Prepare testing support.

Requirements

Create

- Test fixtures
- Neo4j test session
- Graph cleanup utilities
- Test configuration

Acceptance Criteria

- Tests connect successfully
- Cleanup verified

---

## 3.8 Documentation

Scope

Update project documentation.

Include

- Graph architecture
- Neo4j setup
- Constraint creation
- Index creation
- Graph repository usage

Acceptance Criteria

A new developer can initialize the graph environment using documentation alone.

---

# Deliverables

The completed phase must provide

- Neo4j configuration
- Graph infrastructure
- Ontology implementation
- Constraints
- Indexes
- Graph repository layer
- Validation utilities
- Testing utilities
- Updated documentation

---

# Pre-Push Checklist

Before this phase is complete, confirm:

- [ ] Neo4j connects successfully
- [ ] Graph sessions work correctly
- [ ] Constraints created
- [ ] Indexes created
- [ ] Schema matches ontology
- [ ] Repository layer verified
- [ ] Validation passes
- [ ] Tests pass
- [ ] Documentation updated

If any item fails,

Do not mark this phase complete.

---

# Out of Scope

Do NOT implement

- University nodes
- Major nodes
- Scholarship nodes
- Curriculum nodes
- Career nodes
- Company nodes
- User profiles
- Data ingestion
- CSV import
- Web scraping
- ETL pipelines
- Embeddings
- Vector database
- Hybrid Retrieval
- RAG
- Recommendation Engine
- AI Agent
- REST APIs
- Business services

Those belong to later phases.

---

# Definition of Success

This phase is complete only when

- Every Acceptance Criteria passes.
- The Knowledge Graph infrastructure is production-ready.
- The ontology is faithfully implemented.
- Graph validation succeeds.
- Future data ingestion can begin without redesign.

---

# Final Phase Report

After sub-phase 3.8 is approved, provide one consolidated report.

## Summary

## Files Created

## Files Modified

## Validation

## Known Issues

## Remaining Work

## Completed Pre-Push Checklist

Do not begin Phase 04 automatically.

Wait for explicit approval.