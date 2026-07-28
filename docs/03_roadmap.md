# 02. System Architecture

## Overview

EduGuide is an **Agentic Retrieval-Augmented Decision Support System** designed to provide personalized higher education guidance for students in Cambodia.

Unlike traditional chatbot systems that rely primarily on Large Language Models (LLMs) for reasoning and recommendation, EduGuide adopts a **hybrid AI architecture** that combines symbolic reasoning, deterministic decision making, knowledge retrieval, and natural language generation.

The architecture separates different AI responsibilities into specialized components to improve:

- Explainability
- Reliability
- Maintainability
- Scalability
- Trustworthiness

Instead of allowing the LLM to determine recommendations directly, EduGuide performs educational reasoning through a Knowledge Graph and rule-based recommendation engine, while the LLM focuses on understanding users and communicating recommendations naturally.

This architecture aligns with the principles of trustworthy AI by ensuring that every recommendation can be traced back to verified educational knowledge.

---

# Architectural Goals

The architecture is designed to achieve the following goals:

- Provide personalized educational recommendations.
- Produce explainable and evidence-based decisions.
- Prevent AI hallucinations.
- Support modular and scalable development.
- Separate reasoning from language generation.
- Allow independent improvement of each AI component.
- Support future educational services beyond university recommendation.

---

# Architectural Principles

## Separation of Responsibilities

Every component has one clearly defined responsibility.

The system separates:

- User interaction
- Business logic
- Recommendation reasoning
- Knowledge retrieval
- Language generation
- Data storage

This improves maintainability and reduces system complexity.

---

## Graph-Driven Decision Making

Educational recommendations are generated through Knowledge Graph reasoning and rule-based filtering.

The Large Language Model is **not responsible** for deciding which university or academic program should be recommended.

---

## Evidence-First AI

Every recommendation should be supported by retrieved evidence from trusted educational documents.

The system never generates unsupported educational advice.

---

## Explainability

Every recommendation should answer two questions:

- Why was this recommendation generated?
- What evidence supports this recommendation?

---

## Modularity

Each intelligent component can evolve independently.

For example:

- Gemini can be replaced without changing Neo4j.
- Neo4j can grow without changing the frontend.
- RAG can improve independently.
- Recommendation algorithms can evolve without modifying the UI.

---

## Scalability

The architecture is designed for future expansion including:

- Parent advisor
- Career advisor
- Graduate recommendation
- Internship recommendation
- Academic planning
- National educational knowledge graph

---

# High-Level System Architecture

```text
                        ┌────────────────────────────┐
                        │        Web Frontend        │
                        │ React + Vite + Tailwind   │
                        └─────────────┬──────────────┘
                                      │
                                      ▼
                        ┌────────────────────────────┐
                        │      FastAPI Backend       │
                        │ API + Business Logic       │
                        └─────────────┬──────────────┘
                                      │
                                      ▼
                ┌────────────────────────────────────────┐
                │       Agent Orchestration Layer        │
                │              LangGraph                 │
                └────────────────────────────────────────┘
                         │          │          │
                         ▼          ▼          ▼
          Student Agent  Recommendation  Retrieval Agent
                                        │
                                        ▼
                               Response Agent

                         │
                         ▼

             Recommendation Decision Engine

          Rule Engine
                +
      Knowledge Graph Reasoning
                +
         Ranking & Scoring Engine

                         │
                         ▼

      ┌────────────┬─────────────┬──────────────┐
      │            │             │              │
      ▼            ▼             ▼              ▼

   Neo4j       Qdrant      PostgreSQL       Gemini
 Knowledge      Vector      User Data         LLM
   Graph      Database
```

---

# System Layers

The system is divided into five logical layers.

## 1. Presentation Layer

Responsible for user interaction.

Technology

- React
- TypeScript
- Vite
- TailwindCSS

Responsibilities

- Student assessment
- Conversational interface
- University comparison
- Recommendation visualization
- Evidence display
- Dashboard
- Mobile responsive UI

---

## 2. Application Layer

Responsible for application logic.

Technology

- FastAPI

Responsibilities

- API endpoints
- Authentication
- Session management
- Business logic
- Agent orchestration
- Database communication

---

## 3. Intelligence Layer

The intelligence layer contains all AI decision-making components.

It consists of:

- Agent Layer
- Recommendation Engine
- Retrieval System

This is the core contribution of the research.

---

## 4. Knowledge Layer

Responsible for storing structured and unstructured educational knowledge.

Includes

- Neo4j
- Qdrant
- PostgreSQL

---

## 5. AI Service Layer

Responsible for language understanding and natural language generation.

Technology

- Gemini

---

# Agent Architecture

EduGuide adopts an Agentic AI architecture.

Instead of one general-purpose AI agent, the system consists of specialized agents with clearly defined responsibilities.

---

## Student Understanding Agent

Purpose

Understand the student's request.

Responsibilities

- Detect user intent.
- Extract educational preferences.
- Identify academic interests.
- Extract structured student profile.
- Identify missing information.

Output

Structured Student Profile

Example

```json
{
  "interests": [
    "Artificial Intelligence",
    "Programming"
  ],
  "favorite_subjects": [
    "Mathematics"
  ],
  "budget": "Medium",
  "preferred_location": "Phnom Penh"
}
```

---

## Recommendation Agent

Purpose

Generate personalized recommendations.

Responsibilities

- Apply rule-based filtering.
- Query Knowledge Graph.
- Compute recommendation scores.
- Rank academic programs.
- Produce Top-K recommendations.

This agent never uses the LLM for ranking.

---

## Retrieval Agent

Purpose

Retrieve supporting evidence.

Responsibilities

- Search Qdrant.
- Retrieve relevant document chunks.
- Collect supporting evidence.
- Prepare context for LLM.

---

## Response Agent

Purpose

Generate grounded responses.

Responsibilities

- Receive recommendations.
- Receive retrieved evidence.
- Generate conversational explanations.
- Explain recommendations.
- State system limitations.
- Never fabricate missing information.

---

# Recommendation Pipeline

The recommendation workflow follows a deterministic pipeline.

```text
Student Question
        │
        ▼
Student Understanding Agent
        │
        ▼
Structured Student Profile
        │
        ▼
Rule-Based Filtering
        │
        ▼
Knowledge Graph Reasoning
        │
        ▼
Candidate Programs
        │
        ▼
Recommendation Ranking
        │
        ▼
Top-K Recommendations
        │
        ▼
Retrieve Supporting Documents
        │
        ▼
Evidence Context
        │
        ▼
Gemini
        │
        ▼
Grounded Response
```

---

# Rule-Based Filtering

Rule-based filtering applies hard constraints before graph reasoning.

Examples

- Degree level
- GPA requirements
- Budget
- Tuition affordability
- Province preference
- Public or private university
- Scholarship preference
- Language preference

Rule filtering reduces the search space before recommendation scoring.

---

# Knowledge Graph Reasoning

Neo4j is responsible for symbolic reasoning.

Responsibilities

- Store entities.
- Store relationships.
- Graph traversal.
- Similarity reasoning.
- Relationship discovery.
- Candidate recommendation generation.

The graph does **not** generate natural language.

---

# Recommendation Engine

The recommendation engine combines:

Rule Score

+

Knowledge Graph Score

↓

Final Recommendation Score

Possible scoring dimensions

- Interest similarity
- Skill similarity
- Career alignment
- Subject alignment
- University preference
- Scholarship availability
- Curriculum relevance

Final ranking is computed inside the backend.

---

# Retrieval-Augmented Generation (RAG)

The Retrieval Agent searches only the curated EduGuide knowledge base.

The vector database stores document chunks from verified educational resources.

Examples

- Curriculum documents
- Scholarship announcements
- Admission guides
- Tuition information
- University regulations
- Government publications

The retrieved documents provide evidence for the generated response.

---

# Knowledge Boundary Policy

EduGuide retrieves information only from its curated knowledge base.

If requested information is unavailable:

- Never hallucinate.
- Inform the user that the information is unavailable.
- Explain what verified information is available.
- Suggest related questions.
- Never fabricate evidence.

---

# Large Language Model Responsibilities

Gemini is responsible for:

- Natural language understanding
- Student profile extraction
- Conversation management
- Evidence summarization
- Response generation

Gemini is **not responsible** for:

- Recommendation ranking
- Educational reasoning
- University comparison logic
- Graph traversal
- Scholarship eligibility decisions

---

# Data Storage Architecture

## Neo4j

Purpose

Structured educational knowledge.

Stores

- Universities
- Faculties
- Programs
- Subjects
- Skills
- Careers
- Scholarships
- Relationships

---

## Qdrant

Purpose

Semantic document retrieval.

Stores

- Embedded document chunks
- Educational documents
- University documents
- Scholarship information
- Curriculum details
- Government publications

---

## PostgreSQL

Purpose

Operational application data.

Stores

- User accounts
- Student profiles
- Conversation history
- User preferences
- Saved recommendations
- Session information

---

# Source of Truth

| Knowledge Domain | Source of Truth |
|-----------------|-----------------|
| Universities | Neo4j |
| Programs | Neo4j |
| Skills | Neo4j |
| Careers | Neo4j |
| Curriculum | Neo4j + Documents |
| Scholarships | Neo4j + Documents |
| Admission Requirements | Neo4j + Documents |
| Tuition | Neo4j + Documents |
| Student Profiles | PostgreSQL |
| Conversations | PostgreSQL |
| Retrieved Evidence | Qdrant |
| Recommendation Scores | Runtime |
| LLM Responses | Runtime |

---

# Data Flow

```text
User

↓

Frontend

↓

FastAPI

↓

Student Understanding Agent

↓

Recommendation Agent

↓

Neo4j

↓

Candidate Recommendations

↓

Retrieval Agent

↓

Qdrant

↓

Evidence

↓

Gemini

↓

Grounded Response

↓

Frontend
```

---

# Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | React, TypeScript, Vite, TailwindCSS |
| Backend | FastAPI |
| Agent Framework | LangGraph |
| Knowledge Graph | Neo4j |
| Vector Database | Qdrant |
| Relational Database | PostgreSQL |
| LLM | Gemini |
| Embedding Model | Gemini Embedding or compatible embedding model |
| Authentication | JWT |
| Deployment | Docker & Docker Compose |

---

# Deployment Architecture

The platform is deployed as a containerized web application.

Main services include:

- Frontend Container
- Backend Container
- Neo4j Container
- Qdrant Container
- PostgreSQL Container
- Nginx Reverse Proxy

This architecture enables scalable deployment and simplifies future cloud migration.

---

# Security Considerations

The architecture follows several security principles:

- JWT-based authentication.
- Secure API communication using HTTPS.
- Environment variables for sensitive credentials.
- Input validation using FastAPI and Pydantic.
- Parameterized database queries.
- Role-based access control for administrative functions.

---

# Scalability Considerations

EduGuide is designed to support future expansion without significant architectural changes.

Potential future enhancements include:

- Parent advisory services.
- Career recommendation modules.
- Internship matching.
- Graduate program recommendation.
- National educational analytics.
- Multi-language support.
- Additional LLM providers.
- Enhanced graph reasoning algorithms.
- Personalized learning pathways.

---

# Architectural Decisions

The following architectural decisions define EduGuide's core design philosophy:

- Educational reasoning is performed through Knowledge Graph reasoning and rule-based decision making.
- Large Language Models are responsible only for language understanding and response generation.
- Every recommendation must be supported by retrieved evidence.
- The system never fabricates educational information.
- Structured knowledge and unstructured documents are stored separately.
- AI components are modular and independently replaceable.
- Recommendations must remain transparent, explainable, and reproducible.

These principles ensure that EduGuide remains a trustworthy, maintainable, and extensible educational decision support system capable of supporting future educational services across Cambodia.