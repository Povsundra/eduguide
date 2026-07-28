# EduGuide Cambodia

An Agentic Retrieval-Augmented Decision Support System for Personalized Higher Education Guidance in Cambodia.

## Overview
EduGuide Cambodia is an AI-powered educational decision support system that helps Cambodian students discover suitable majors, compare universities, understand career pathways, and access trusted educational information through Retrieval-Augmented Generation (RAG).

## Architecture
The system combines three core AI technologies:
- **Knowledge Graph (Neo4j):** Structured reasoning and recommendation.
- **RAG (Qdrant + Hybrid Search):** Retrieving trusted educational information.
- **LLM:** Conversational interaction and natural-language explanations.

## Directory Structure
- `knowledge/`: Raw educational data (entities, ontology, graph scripts, prompts).
- `docs/`: Project memory and design documents (architecture, roadmap, ontology, etc.).
- `.ai/`: Permanent AI system prompts and roles.
- `tasks/`: Atomic sprint tasks and templates.
- `backend/`: FastAPI application code.
- `frontend/`: React/Next.js application code.

*Note: This is a draft README. Full project documentation is maintained within the `docs/` directory.*
