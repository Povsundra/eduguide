# 09 API Design

# 1. Purpose

## 1.1 Overview

The API Layer provides a standardized communication interface between the EduGuide frontend, backend services, AI agents, Knowledge Graph, Recommendation Engine, and Large Language Model (LLM).

Rather than exposing internal implementation details, the API Layer defines a stable contract through which all system functionalities can be accessed.

The API serves as the communication gateway for:

- web frontend;
- mobile applications;
- administrative tools;
- future third-party integrations.

---

## 1.2 Role in System Architecture

The API Layer sits between client applications and the internal AI services.

```text
                 React Frontend
                        │
                        ▼
                 REST API Layer
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
  Planner Agent   Recommendation     Retrieval
                      Engine             Agent
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                  Knowledge Services
             (Neo4j + Vector Database)
                        │
                        ▼
                     LLM Service
```

The frontend communicates only with the REST API.

Internal services are never accessed directly.

---

# 2. Design Objectives

The API Layer is designed with the following objectives.

## Standardization

Provide a consistent communication protocol across all services.

---

## Decoupling

Separate frontend implementation from backend services.

---

## Scalability

Support future services without changing existing client applications.

---

## Security

Protect internal services from unauthorized access.

---

## Extensibility

Allow new AI capabilities to be added with minimal modifications.

---

# 3. API Architecture

EduGuide adopts a layered RESTful API architecture.

```text
Client Applications
        │
        ▼
REST API
        │
        ▼
Planner Agent
        │
 ┌──────┼────────────┐
 ▼      ▼            ▼
Recommendation   Retrieval   Comparison
        │
        ▼
Knowledge Services
        │
        ▼
LLM
```

The API Layer coordinates requests but does not contain business logic.

---

# 4. API Design Principles

The API follows several architectural principles.

---

## Resource-Oriented Design

Resources are accessed using meaningful endpoints.

Examples:

- Universities
- Programs
- Scholarships
- Careers

---

## Action-Based AI APIs

AI operations are exposed as task-oriented endpoints.

Examples:

- Chat
- Recommendation
- Comparison

---

## Stateless Communication

Each request contains all information required for processing.

---

## Consistent Response Format

Every API returns the same response structure.

---

## Versioning

All APIs include version identifiers.

Example

```text
/api/v1/chat
```

---

# 5. Authentication

The API supports role-based authentication.

| Role | Permission |
|------|------------|
| Student | Chat, Recommendation, Search |
| Administrator | Data Management, Reindexing |

Authentication is implemented using JWT access tokens.

Public APIs may be accessed without authentication depending on deployment requirements.

---

# 6. Request Lifecycle

The following illustrates the execution flow of an API request.

```text
Student

↓

POST /chat

↓

REST API

↓

Planner Agent

↓

Recommendation Agent

↓

Retrieval Agent

↓

Response Agent

↓

REST API

↓

JSON Response

↓

Frontend
```

The API Layer is responsible for coordinating the workflow but not executing recommendation or retrieval algorithms.

---

# 7. API Categories

EduGuide exposes six primary API groups.

| Category | Purpose |
|----------|---------|
| Chat APIs | Conversational AI |
| Recommendation APIs | Personalized recommendations |
| Comparison APIs | Entity comparison |
| Search APIs | Knowledge retrieval |
| Knowledge APIs | Resource information |
| Administration APIs | System maintenance |

---

# 8. Chat APIs

## POST /api/v1/chat

General conversational interface.

### Request

```json
{
    "message":"Tell me about Data Science at ITC."
}
```

### Response

```json
{
    "success":true,
    "data":{
        "response":"..."
    }
}
```

The Planner Agent determines whether retrieval, recommendation, or comparison services are required.

---

# 9. Recommendation APIs

## POST /api/v1/recommend

Generate personalized educational recommendations.

### Request

```json
{
    "gpa":3.8,
    "interests":[
        "Artificial Intelligence"
    ],
    "career_goal":"Data Scientist"
}
```

### Response

```json
{
    "success":true,
    "data":{
        "programs":[...],
        "universities":[...],
        "scholarships":[...]
    }
}
```

The endpoint invokes the Recommendation Agent.

---

# 10. Comparison APIs

## POST /api/v1/compare

Compare educational entities.

Supported entities include:

- universities;
- programs;
- scholarships.

### Request

```json
{
    "entities":[
        "ITC",
        "CADT"
    ]
}
```

### Response

```json
{
    "success":true,
    "data":{
        "comparison":{...}
    }
}
```

---

# 11. Search APIs

## GET /api/v1/search

Search educational resources.

Example

```text
GET /api/v1/search?q=data science
```

Returns matching educational entities.

---

# 12. Knowledge APIs

Knowledge APIs retrieve detailed information about educational resources.

Examples

```text
GET /api/v1/universities/{id}

GET /api/v1/programs/{id}

GET /api/v1/scholarships/{id}

GET /api/v1/careers/{id}
```

These APIs support detailed information pages in the frontend.

---

# 13. Conversation APIs

Conversation APIs manage user sessions.

Examples

```text
POST /api/v1/conversations

GET /api/v1/conversations/{id}

DELETE /api/v1/conversations/{id}
```

These endpoints preserve conversation history.

---

# 14. Administration APIs

Administrative APIs maintain the knowledge repository.

Examples

```text
POST /api/v1/admin/reindex

POST /api/v1/admin/rebuild-graph

POST /api/v1/admin/rebuild-embeddings

POST /api/v1/admin/import-markdown
```

These APIs are restricted to administrators.

---

# 15. Standard Response Format

Every API returns a consistent response structure.

Successful response

```json
{
    "success":true,
    "data":{},
    "message":"Request completed successfully.",
    "metadata":{}
}
```

Error response

```json
{
    "success":false,
    "error":{
        "code":"RESOURCE_NOT_FOUND",
        "message":"Requested university does not exist."
    }
}
```

A standardized format simplifies frontend integration.

---

# 16. Error Handling

The API returns standardized HTTP status codes.

| Status Code | Meaning |
|-------------|----------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

Error messages include descriptive information to facilitate debugging.

---

# 17. Security

The API implements multiple security mechanisms.

These include:

- JWT authentication;
- HTTPS communication;
- request validation using Pydantic;
- input sanitization;
- CORS configuration;
- API rate limiting;
- prompt injection protection;
- secure API key management.

These measures protect both user data and AI services.

---

# 18. API Versioning

API versioning ensures backward compatibility.

Example

```text
/api/v1/chat

/api/v2/chat
```

Future enhancements can be introduced without breaking existing client applications.

---

# 19. Performance Optimization

The API incorporates several optimization strategies.

These include:

- asynchronous request processing;
- connection pooling;
- pagination;
- response caching;
- streaming responses for chat;
- background embedding generation;
- lazy loading of large resources.

These optimizations improve scalability and responsiveness.

---

# 20. API-to-Agent Mapping

The following table illustrates how API endpoints interact with the Agent Layer.

| API | Planner | Recommendation | Retrieval | Comparison | Response |
|-----|----------|----------------|------------|------------|----------|
| POST /chat | ✓ | Optional | ✓ | Optional | ✓ |
| POST /recommend | ✓ | ✓ | Optional | ✗ | ✓ |
| POST /compare | ✓ | ✗ | ✓ | ✓ | ✓ |
| GET /search | ✗ | ✗ | ✓ | ✗ | ✗ |
| GET /universities/{id} | ✗ | ✗ | ✓ | ✗ | ✗ |

This mapping demonstrates the separation between the external API interface and the internal AI orchestration layer.

---

# 21. Summary

The API Layer provides a standardized and secure communication interface for the EduGuide platform.

By separating client applications from internal AI services, the API enables modular development, simplifies frontend integration, and supports future system expansion.

The design includes standardized request and response formats, resource-oriented endpoints, AI-specific task APIs, authentication, error handling, versioning, and performance optimization.

Through its integration with the Planner Agent, Recommendation Engine, and Hybrid Graph RAG subsystem, the API Layer serves as the central communication gateway of the EduGuide architecture.