# ╔══════════════════════════════════════════════════════════════════════╗
# ║                 PHASE 04 — KNOWLEDGE INGESTION PIPELINE             ║
# ╚══════════════════════════════════════════════════════════════════════╝

## Overview

This phase establishes the complete Knowledge Ingestion Pipeline for EduGuide.

The objective is to transform raw educational documents into validated, normalized, ontology-compliant knowledge that can be stored inside the Knowledge Graph while simultaneously preparing standardized metadata for the Retrieval and Hybrid RAG pipeline.

This phase represents the bridge between the raw knowledge sources and the intelligent components of the system.

No Retrieval, Recommendation, Embedding, or LLM functionality shall be implemented during this phase.

---

# References

Before implementation, the AI Agent MUST fully understand the following project documents.

Project Context

- docs/00_project_context.md
- docs/01_vision.md

Architecture

- docs/02_architecture.md

Domain

- docs/03.5_domain_model.md

Ontology

- docs/04_ontology.md

Knowledge Graph

- docs/05_graph_design.md

RAG

- docs/06_rag_design.md

Database

- docs/10_database_design.md

Infrastructure

- docs/11_development_infrastructure_design.md

Development Rules

- .ai/agent.md
- .ai/planner.md
- .ai/architect.md
- .ai/researcher.md
- .ai/review.md

---

# Objective

Build a production-ready Knowledge Ingestion Pipeline capable of:

• Registering knowledge sources

• Reading multiple document formats

• Parsing structured educational knowledge

• Validating every document

• Normalizing entities

• Extracting ontology entities

• Extracting ontology relationships

• Preventing duplicated knowledge

• Loading validated knowledge into Neo4j

• Preparing standardized metadata for future Retrieval

• Recording every ingestion operation

---

# Expected Outcome

At the completion of this phase the system shall be capable of:

Raw Document

↓

Reader

↓

Parser

↓

Validator

↓

Normalizer

↓

Entity Extraction

↓

Relationship Extraction

↓

Duplicate Detection

↓

Graph Loader

↓

Neo4j

while simultaneously producing retrieval-ready metadata.

---

# Scope

## Included

✓ Source Registry

✓ Reader Framework

✓ Markdown Reader

✓ JSON Reader

✓ Unified Document Model

✓ Parsing Framework

✓ Validation Framework

✓ Normalization Framework

✓ Entity Extraction

✓ Relationship Extraction

✓ Duplicate Detection

✓ Graph Loader

✓ Metadata Generator

✓ Logging

✓ Error Handling

✓ Unit Testing

✓ Integration Testing

---

## Excluded

✗ Embedding Generation

✗ Chunking

✗ Vector Database

✗ Hybrid Search

✗ Retrieval

✗ Prompt Builder

✗ LLM

✗ Recommendation Engine

✗ Frontend

---

# Development Principles

The implementation MUST follow these principles.

## Modular

Every component shall have one responsibility.

Readers shall never perform validation.

Validators shall never perform extraction.

Loaders shall never parse documents.

---

## Extensible

Adding a new document format should require creating only a new Reader.

No existing pipeline should require modification.

---

## Ontology Driven

Every entity

Every relationship

Every validation rule

must follow

docs/04_ontology.md

No undocumented entity may be introduced.

---

## Source Independent

The ingestion pipeline must not depend on:

Markdown

JSON

PDF

CSV

The internal pipeline shall process only the Unified Document Model.

---

## Production Ready

Every component shall include:

Logging

Validation

Error handling

Type hints

Unit tests

Documentation

---

# Overall Architecture

                    Knowledge Source
                           │
                           ▼
                  Source Registry
                           │
                           ▼
                    Reader Framework
                           │
                           ▼
                 Unified Document Model
                           │
                           ▼
                   Parsing Framework
                           │
                           ▼
                 Validation Framework
                           │
                           ▼
                 Normalization Framework
                           │
                           ▼
                  Entity Extraction
                           │
                           ▼
              Relationship Extraction
                           │
                           ▼
                 Duplicate Detection
                           │
                           ▼
                    Graph Loader
                           │
                           ▼
                        Neo4j

──────────────────────────────────────────

Unified Document

↓

Metadata Generator

↓

Phase 05 Retrieval

---

# Development Workflow

Every subphase MUST follow:

Planning

↓

Architecture Review

↓

Implementation

↓

Testing

↓

Documentation

↓

Review

↓

Approval

The AI Agent shall NEVER skip a step.

The AI Agent shall NEVER continue to the next subphase without explicit approval.

---

# Project Structure

backend/

app/

ingestion/

├── registry/

├── readers/

├── parsers/

├── validators/

├── normalizers/

├── extractors/

├── loaders/

├── metadata/

├── models/

├── schemas/

├── services/

└── tests/

---

# ════════════════════════════════════════════════
# Subphase 4.1 — Knowledge Source Registry
# ════════════════════════════════════════════════

## Objective

Create a centralized registry responsible for managing every knowledge source supported by EduGuide.

The registry shall allow future expansion without changing the ingestion pipeline.

---

## Responsibilities

Register sources

Store source metadata

Track versions

Track ingestion status

Store configuration

Enable or disable sources

Priority ordering

---

## Supported Sources

Initial

✓ Markdown

✓ JSON

Future

□ PDF

□ CSV

□ Website

□ REST API

---

## Deliverables

Source Registry

Configuration Models

Source Metadata Models

Validation

Unit Tests

Documentation

---

## Acceptance Criteria

✓ New source can be registered

✓ Source configuration validated

✓ Source status tracked

✓ Version information stored

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.2 — Reader Framework
# ════════════════════════════════════════════════

## Objective

Develop a generic reader framework that converts raw files into a unified internal representation.

The ingestion pipeline shall never directly interact with file formats.

---

## Required Readers

BaseReader

MarkdownReader

JsonReader

---

## Responsibilities

Read file

Validate encoding

Validate file type

Read metadata

Handle errors

Return Unified Document

---

## Design Rules

Readers SHALL NOT

Extract entities

Validate ontology

Insert into Neo4j

Readers ONLY read documents.

---

## Deliverables

Base Reader

Markdown Reader

JSON Reader

Reader Tests

Documentation

---

## Acceptance Criteria

✓ Markdown successfully read

✓ JSON successfully read

✓ Encoding detected

✓ Invalid files rejected

✓ Unified Document returned

---

# ════════════════════════════════════════════════
# Subphase 4.3 — Unified Document Model
# ════════════════════════════════════════════════

## Objective

Create one internal document representation shared by every pipeline component.

No downstream component shall know the original document format.

---

## Required Fields

Document ID

Source ID

Document Type

Title

Language

Content

Metadata

Created At

Updated At

Version

Checksum

---

## Design Principles

Immutable

Serializable

Versioned

Extensible

Type Safe

---

## Responsibilities

Represent every document

Carry metadata

Carry parsed content

Support future chunking

Support future retrieval

Support future embeddings

---

## Deliverables

Unified Document Model

Schemas

Validation

Serialization

Unit Tests

Documentation

---

## Acceptance Criteria

✓ Every reader produces the Unified Document

✓ Serialization works

✓ Validation passes

✓ Metadata preserved

✓ Unit tests pass

---

STOP.

Wait for approval before implementing Subphase 4.4.


# ════════════════════════════════════════════════
# Subphase 4.4 — Parsing Framework
# ════════════════════════════════════════════════

## Objective

Develop a modular parsing framework capable of converting a Unified Document into structured educational content.

The parser is responsible for understanding the logical structure of a document, **not** its meaning.

It transforms raw text into structured sections that can later be validated and processed.

---

## Responsibilities

The parser shall:

• Parse document hierarchy

• Detect sections

• Detect headings

• Detect paragraphs

• Detect lists

• Detect tables

• Detect hyperlinks

• Detect metadata blocks

• Preserve document order

• Produce a Structured Document

---

## Design Rules

The parser SHALL NOT

- Validate entities
- Normalize values
- Create graph nodes
- Create relationships
- Communicate with Neo4j

The parser ONLY understands document structure.

---

## Expected Pipeline

Unified Document

↓

Markdown Parser

↓

Structured Sections

↓

Structured Document

---

## Output Structure

Example

Document

├── Metadata

├── Section

│ ├── Heading

│ ├── Paragraph

│ ├── List

│ ├── Table

│ └── Links

└── Footer

---

## Deliverables

✓ Parser Framework

✓ Markdown Parser

✓ JSON Parser

✓ Structured Document Model

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Headings parsed correctly

✓ Lists parsed correctly

✓ Tables parsed correctly

✓ Metadata extracted

✓ Section order preserved

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.5 — Validation Framework
# ════════════════════════════════════════════════

## Objective

Create a centralized validation framework responsible for ensuring that every document complies with the EduGuide ontology and data quality standards.

Invalid knowledge must never continue through the ingestion pipeline.

---

## Responsibilities

Validate:

• Required fields

• Empty values

• Invalid data types

• Broken hierarchy

• Missing metadata

• Invalid ontology references

• Duplicate identifiers

• Unsupported entities

• Invalid relationships

---

## Validation Categories

### Document Validation

- Document exists
- Metadata exists
- Required fields exist
- Language supported

---

### Structural Validation

- Sections ordered correctly
- Heading hierarchy valid
- Tables valid
- Lists valid

---

### Entity Validation

- Entity type exists
- Entity name exists
- Entity identifier valid
- Required attributes complete

---

### Relationship Validation

Relationship exists in ontology

Entity types match ontology

Relationship direction valid

---

## Validation Result

Every validation shall return:

PASS

WARNING

FAIL

---

## Error Reporting

Every validation failure must contain:

Validation Rule

Error Message

Affected Document

Affected Section

Severity

Suggested Resolution

---

## Deliverables

✓ Validation Engine

✓ Validation Rules

✓ Validation Report

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Invalid documents rejected

✓ Errors reported correctly

✓ Validation rules reusable

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.6 — Normalization Framework
# ════════════════════════════════════════════════

## Objective

Normalize educational knowledge into one canonical representation.

Normalization guarantees consistency across the Knowledge Graph and Retrieval system.

---

## Responsibilities

Normalize

University names

Faculty names

Major names

Curriculum names

Scholarship names

Career names

Country names

Language

URLs

Dates

Whitespace

Identifiers

Aliases

---

## Design Principles

Normalization must be

Deterministic

Repeatable

Configurable

Ontology-driven

---

## Example

Before

ITC

Institute of Technology Cambodia

Institute of Technology of Cambodia

↓

After

Institute of Technology of Cambodia

---

## Deliverables

✓ Normalization Framework

✓ Canonical Mapping

✓ Alias Mapping

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Duplicate aliases resolved

✓ Canonical names generated

✓ URLs normalized

✓ Dates standardized

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.7 — Entity Extraction
# ════════════════════════════════════════════════

## Objective

Extract ontology-compliant entities from normalized educational documents.

This layer creates domain objects only.

It does NOT create graph nodes.

---

## Supported Entities

University

Faculty

Department

Major

Curriculum

Course

Subject

Career

Scholarship

Admission

Requirement

Event

News

FAQ

Organization

Province

City

---

## Responsibilities

Identify entities

Determine entity type

Extract attributes

Generate canonical identifier

Preserve source reference

Generate entity object

---

## Entity Object

Every entity shall include

Entity ID

Entity Type

Name

Description

Attributes

Metadata

Source

Confidence

---

## Design Rules

Entity Extraction SHALL NOT

Insert Neo4j nodes

Generate embeddings

Create chunks

Perform retrieval

---

## Deliverables

✓ Entity Extractor

✓ Entity Models

✓ Entity Validation

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Entities extracted correctly

✓ Entity types valid

✓ Metadata preserved

✓ Canonical IDs generated

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.8 — Relationship Extraction
# ════════════════════════════════════════════════

## Objective

Generate ontology-compliant relationships between extracted entities.

Every relationship must strictly follow docs/04_ontology.md.

---

## Supported Relationships

Examples

University

HAS_FACULTY

Faculty

Faculty

OFFERS

Major

Major

HAS_CURRICULUM

Curriculum

Major

LEADS_TO

Career

Scholarship

AVAILABLE_AT

University

Admission

REQUIRES

Requirement

Subject

PREREQUISITE_OF

Subject

---

## Responsibilities

Identify relationships

Validate ontology

Determine direction

Generate relationship object

Preserve source reference

---

## Relationship Object

Relationship ID

Source Entity

Target Entity

Relationship Type

Metadata

Confidence

Source Reference

---

## Design Rules

Relationship Extraction SHALL NOT

Create Neo4j relationships

Modify ontology

Create new relationship types

---

## Deliverables

✓ Relationship Extractor

✓ Relationship Models

✓ Ontology Validation

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Relationships extracted correctly

✓ Ontology respected

✓ Relationship direction correct

✓ Metadata preserved

✓ Unit tests pass

---

STOP.

Wait for approval before implementing Subphase 4.9.

# ════════════════════════════════════════════════
# Subphase 4.9 — Duplicate Detection Framework
# ════════════════════════════════════════════════

## Objective

Develop a duplicate detection framework responsible for identifying duplicate entities and relationships before they are persisted into the Knowledge Graph.

Duplicate detection ensures data consistency, prevents graph pollution, and enables safe incremental updates.

---

## Responsibilities

The framework shall:

• Detect duplicate entities

• Detect duplicate relationships

• Detect duplicate documents

• Detect duplicate source identifiers

• Detect duplicate aliases

• Support configurable matching strategies

• Generate duplicate reports

---

## Matching Strategy

The framework should support multiple matching methods.

### Exact Match

Compare:

- Entity ID
- Relationship ID
- Source ID
- Canonical Name

---

### Alias Match

Compare:

- Alternative Names
- Abbreviations
- Common Names

Example

ITC

Institute of Technology of Cambodia

Institute of Technology Cambodia

↓

One canonical entity

---

### Metadata Match

Compare

- Source
- Version
- Checksum
- Created Date
- Updated Date

---

### Future Extension

Reserved for:

- Semantic Similarity
- Embedding Similarity
- Fuzzy Matching

These SHALL NOT be implemented in this phase.

---

## Duplicate Resolution Policy

If duplicate detected

↓

Keep canonical entity

↓

Update metadata if necessary

↓

Skip duplicate insertion

↓

Log duplicate event

---

## Deliverables

✓ Duplicate Detection Engine

✓ Duplicate Rules

✓ Duplicate Report

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Duplicate entities detected

✓ Duplicate relationships detected

✓ Duplicate documents detected

✓ No duplicated graph objects inserted

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.10 — Graph Loader
# ════════════════════════════════════════════════

## Objective

Develop a Graph Loader responsible for persisting validated ontology objects into Neo4j.

The Graph Loader is the ONLY component allowed to communicate with Neo4j.

---

## Responsibilities

Create Nodes

Create Relationships

Update Existing Nodes

Prevent Duplicate Insertions

Transaction Management

Rollback

Error Recovery

Batch Loading

Logging

---

## Design Principles

Graph Loader SHALL

Use Repository Layer

Use Transactions

Support Batch Operations

Be Idempotent

Be Re-runnable

---

## Transaction Workflow

Validated Objects

↓

Begin Transaction

↓

Insert Nodes

↓

Insert Relationships

↓

Commit

↓

Success

OR

↓

Rollback

↓

Error Report

---

## Repository Rules

Neo4j communication must occur ONLY through:

Graph Repository

The Graph Loader SHALL NOT execute Cypher queries directly.

---

## Deliverables

✓ Graph Loader

✓ Repository Integration

✓ Transaction Manager

✓ Rollback Support

✓ Unit Tests

✓ Integration Tests

✓ Documentation

---

## Acceptance Criteria

✓ Nodes inserted correctly

✓ Relationships inserted correctly

✓ Duplicate prevention works

✓ Rollback works

✓ Integration tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.11 — Metadata Generation
# ════════════════════════════════════════════════

## Objective

Generate standardized metadata required for Retrieval, Hybrid Search, Recommendation, and future AI Agents.

Metadata provides traceability between graph entities and source documents.

---

## Responsibilities

Generate metadata for:

Document

Entity

Relationship

Source

Version

Language

Tags

Category

Processing History

---

## Required Metadata

Document ID

Source ID

Entity ID

Relationship ID

Language

Version

Created At

Updated At

Tags

Checksum

Processing Timestamp

Pipeline Version

---

## Design Principles

Metadata must be

Immutable

Versioned

Serializable

Queryable

Extensible

---

## Future Compatibility

Metadata should support:

Chunking

Embeddings

Hybrid Retrieval

Citation Generation

Agent Memory

Knowledge Provenance

without structural changes.

---

## Deliverables

✓ Metadata Generator

✓ Metadata Models

✓ Metadata Validation

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Metadata generated

✓ Required fields complete

✓ Metadata versioned

✓ Traceability maintained

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Subphase 4.12 — Logging & Monitoring
# ════════════════════════════════════════════════

## Objective

Implement centralized logging and monitoring for the Knowledge Ingestion Pipeline.

Every processing step must be observable, traceable, and diagnosable.

---

## Responsibilities

Record

Pipeline Start

Pipeline End

Reader Events

Parser Events

Validation Events

Normalization Events

Extraction Events

Duplicate Events

Graph Loading Events

Errors

Warnings

Performance Metrics

---

## Log Levels

INFO

WARNING

ERROR

CRITICAL

DEBUG (Development Only)

---

## Required Metrics

Documents Processed

Documents Failed

Entities Created

Relationships Created

Duplicates Found

Validation Errors

Execution Time

Average Processing Time

---

## Error Handling

Every exception must include:

Timestamp

Pipeline Stage

Document

Component

Exception

Stack Trace

Suggested Resolution

---

## Deliverables

✓ Logging System

✓ Monitoring Utilities

✓ Metrics Collection

✓ Error Reports

✓ Unit Tests

✓ Documentation

---

## Acceptance Criteria

✓ Every stage logged

✓ Metrics collected

✓ Errors traceable

✓ Pipeline observable

✓ Unit tests pass

---

# ════════════════════════════════════════════════
# Testing Requirements
# ════════════════════════════════════════════════

The AI Agent MUST implement automated tests.

Required test categories:

## Unit Tests

✓ Registry

✓ Readers

✓ Parser

✓ Validator

✓ Normalizer

✓ Entity Extractor

✓ Relationship Extractor

✓ Duplicate Detection

✓ Graph Loader

✓ Metadata

---

## Integration Tests

Validate the complete ingestion pipeline.

Example:

Markdown

↓

Reader

↓

Parser

↓

Validator

↓

Normalizer

↓

Entity Extraction

↓

Relationship Extraction

↓

Duplicate Detection

↓

Graph Loader

↓

Neo4j

---

## Performance Tests

Measure:

Documents per second

Average ingestion time

Memory usage

Graph loading performance

---

# Review Gate

The phase SHALL NOT be approved if:

Any test fails

Architecture is violated

Ontology is violated

Graph consistency fails

Logging is incomplete

Documentation is incomplete

# ════════════════════════════════════════════════
# Deliverables
# ════════════════════════════════════════════════

Upon successful completion of Phase 04, the project SHALL include:

## Source Management

✓ Knowledge Source Registry

✓ Source Configuration

✓ Source Metadata Models

✓ Version Management

---

## Reader Framework

✓ Base Reader

✓ Markdown Reader

✓ JSON Reader

✓ Reader Factory

---

## Document Models

✓ Unified Document Model

✓ Structured Document Model

✓ Metadata Models

---

## Processing Framework

✓ Parser Framework

✓ Validation Framework

✓ Normalization Framework

✓ Entity Extraction Framework

✓ Relationship Extraction Framework

✓ Duplicate Detection Framework

✓ Graph Loader

✓ Metadata Generator

✓ Logging Framework

---

## Database Integration

✓ Neo4j Repository Integration

✓ Transaction Management

✓ Rollback Support

✓ Batch Loading

---

## Quality

✓ Unit Tests

✓ Integration Tests

✓ Performance Tests

✓ Documentation

✓ Logging

✓ Error Handling

---

# ════════════════════════════════════════════════
# Pre-Push Checklist
# ════════════════════════════════════════════════

Before requesting approval, the AI Agent MUST verify:

Project Structure

□ Folder structure follows architecture

□ No unnecessary files

□ Naming conventions consistent

□ Dependency rules respected

Implementation

□ Source Registry completed

□ Reader Framework completed

□ Unified Document Model completed

□ Parser completed

□ Validator completed

□ Normalizer completed

□ Entity Extraction completed

□ Relationship Extraction completed

□ Duplicate Detection completed

□ Graph Loader completed

□ Metadata Generator completed

□ Logging completed

Architecture

□ Layered architecture respected

□ Repository pattern followed

□ No direct Neo4j access outside repositories

□ Ontology respected

□ No architecture drift

Quality

□ No duplicated code

□ Type hints complete

□ Proper exception handling

□ Logging implemented

□ Documentation updated

Testing

□ Unit tests pass

□ Integration tests pass

□ Pipeline successfully ingests sample knowledge

□ Neo4j data verified

---

# ════════════════════════════════════════════════
# Acceptance Criteria
# ════════════════════════════════════════════════

Phase 04 is complete ONLY if all criteria below are satisfied.

Knowledge Sources

✓ Markdown source supported

✓ JSON source supported

Readers

✓ Documents successfully read

✓ Invalid documents rejected

Parser

✓ Structured document generated

✓ Document hierarchy preserved

Validation

✓ Invalid knowledge rejected

✓ Validation report generated

Normalization

✓ Canonical names generated

✓ Aliases resolved

Extraction

✓ Entities extracted correctly

✓ Relationships extracted correctly

Ontology

✓ Every entity conforms to ontology

✓ Every relationship conforms to ontology

Duplicate Detection

✓ Duplicate entities prevented

✓ Duplicate relationships prevented

Graph Loading

✓ Nodes inserted successfully

✓ Relationships inserted successfully

✓ Rollback tested

Metadata

✓ Metadata generated

✓ Traceability maintained

Logging

✓ Every pipeline stage logged

✓ Performance metrics collected

Testing

✓ All unit tests pass

✓ All integration tests pass

✓ No critical defects

Documentation

✓ Documentation updated

✓ Final report completed

---

# ════════════════════════════════════════════════
# Definition of Done
# ════════════════════════════════════════════════

Phase 04 shall only be considered complete when:

✓ Every required deliverable exists

✓ Acceptance Criteria are satisfied

✓ Tests pass

✓ Documentation updated

✓ Architecture remains unchanged

✓ Code review completed

✓ User approval received

Without explicit approval the AI Agent SHALL NOT begin Phase 05.

---

# ════════════════════════════════════════════════
# Out of Scope
# ════════════════════════════════════════════════

The following MUST NOT be implemented.

Retrieval

Embedding Generation

Vector Database

Chunking

Hybrid Search

Prompt Construction

LLM Integration

Recommendation Engine

Frontend

Authentication

API Endpoints

Caching

AI Agents

These belong to later phases.

---

# ════════════════════════════════════════════════
# Final Implementation Report
# ════════════════════════════════════════════════

Upon completion, the AI Agent SHALL provide a report using the following structure.

# Phase 04 Completion Report

## Overview

Provide a summary of the completed implementation.

---

## Completed Components

List every implemented component.

Example

✓ Source Registry

✓ Reader Framework

✓ Markdown Reader

✓ JSON Reader

✓ Parser

✓ Validator

✓ Normalizer

✓ Entity Extraction

✓ Relationship Extraction

✓ Duplicate Detection

✓ Graph Loader

✓ Metadata Generator

✓ Logging

---

## Architecture Compliance

Confirm that the implementation follows:

- Project Architecture
- Ontology
- Graph Design
- Database Design

Describe any deviations.

---

## Validation Results

Report:

Number of documents processed

Entities extracted

Relationships extracted

Duplicates detected

Validation failures

Warnings

---

## Testing Results

Provide:

Unit Test Summary

Integration Test Summary

Performance Test Summary

Coverage (if available)

---

## Known Limitations

List any known limitations that remain intentionally unresolved.

---

## Files Created

List all new files and folders.

---

## Files Modified

List every modified file.

---

## Notes

Additional implementation notes.

---

## Recommendation

One of:

READY FOR APPROVAL

or

CHANGES REQUIRED

---

# ════════════════════════════════════════════════
# Stop Conditions
# ════════════════════════════════════════════════

The AI Agent MUST immediately stop implementation if:

• Required documentation is missing

• Architecture conflicts are discovered

• Ontology changes are required

• Phase scope becomes unclear

• A decision requires user approval

The AI Agent SHALL report the issue and wait for instructions.

---

# ════════════════════════════════════════════════
# Definition of Success
# ════════════════════════════════════════════════

Phase 04 is successful when EduGuide can reliably transform raw educational documents into validated, normalized, ontology-compliant knowledge, persist that knowledge into Neo4j, and produce standardized metadata ready for Retrieval.

The implementation must be:

✓ Modular

✓ Extensible

✓ Testable

✓ Maintainable

✓ Production-ready

No Retrieval, RAG, Recommendation, or LLM functionality shall exist after this phase.

Phase 04 serves as the complete knowledge ingestion foundation upon which all future Retrieval, Hybrid RAG, and Recommendation capabilities will be built.