# 11 Deployment & Infrastructure Design

# 1. Purpose

## 1.1 Overview

The Deployment & Infrastructure Layer defines how the EduGuide platform is deployed, configured, and operated in a production environment.

While previous design documents describe the system architecture, data model, AI workflows, and APIs, this document focuses on the runtime environment that hosts these components and enables reliable service delivery.

The deployment architecture ensures that the platform remains secure, scalable, maintainable, and resilient while supporting future growth.

---

## 1.2 Role in System Architecture

The deployment layer provides the infrastructure required to execute all system services.

```text
                    Student
                        │
                        ▼
                  Web Browser
                        │
                        ▼
                    React Frontend
                        │
                        ▼
                 Nginx Reverse Proxy
                        │
                        ▼
                 FastAPI Application
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Planner Agent   PostgreSQL Database   Neo4j Graph
        │                                 │
        ▼                                 ▼
Recommendation Engine              Neo4j Vector Index
        │                                 │
        └───────────────┬─────────────────┘
                        ▼
                   OpenAI API
```

The deployment layer connects all infrastructure components into a single operational platform.

---

# 2. Deployment Objectives

The deployment architecture is designed to achieve the following objectives.

## Reliability

Ensure continuous availability of AI services.

---

## Scalability

Support increasing numbers of users, educational resources, and AI requests.

---

## Maintainability

Allow independent deployment and maintenance of individual services.

---

## Security

Protect user information, AI services, and educational knowledge.

---

## Portability

Enable deployment on local servers, cloud environments, or institutional infrastructure.

---

# 3. Deployment Architecture

EduGuide follows a layered deployment architecture.

```text
Client Layer
        │
        ▼
Presentation Layer
        │
        ▼
Application Layer
        │
        ▼
AI Service Layer
        │
        ▼
Data Layer
```

Each layer is independently deployable and communicates through well-defined interfaces.

---

# 4. Infrastructure Components

The platform consists of several infrastructure services.

| Component | Technology | Responsibility |
|------------|------------|----------------|
| Frontend | React + Vite | User Interface |
| Reverse Proxy | Nginx | Request routing and HTTPS |
| Backend API | FastAPI | Business logic and AI orchestration |
| Knowledge Graph | Neo4j | Educational knowledge storage |
| Operational Database | PostgreSQL | User and conversation data |
| Vector Storage | Neo4j Vector Index | Semantic retrieval |
| LLM Service | OpenAI API | Natural language generation |

Each component performs a specialized function within the overall architecture.

---

# 5. Container Architecture

Each infrastructure component is deployed as an independent container.

```text
Docker Network

├── frontend
├── nginx
├── backend
├── neo4j
└── postgres
```

Containerization provides:

- service isolation;
- simplified deployment;
- portability;
- reproducible environments.

---

# 6. Network Architecture

External users access only the frontend.

```text
Internet
    │
    ▼
Nginx Reverse Proxy
    │
    ▼
FastAPI Backend
    │
 ┌──┴───────────────┐
 ▼                  ▼
Neo4j          PostgreSQL
```

Internal databases are not exposed directly to the public network.

---

# 7. Service Communication

Services communicate through internal APIs.

```text
Frontend

↓

REST API

↓

Planner Agent

↓

Recommendation Agent

↓

Retrieval Agent

↓

Neo4j

↓

OpenAI API
```

This architecture minimizes coupling between services.

---

# 8. Configuration Management

Runtime configuration is externalized through environment variables.

Examples include:

```text
DATABASE_URL

NEO4J_URI

NEO4J_USERNAME

NEO4J_PASSWORD

OPENAI_API_KEY

JWT_SECRET

ENVIRONMENT
```

Configuration files are separated from application source code.

---

# 9. Monitoring and Logging

The platform continuously monitors service health.

Examples include:

- API response time;
- request volume;
- AI latency;
- database availability;
- retrieval performance;
- recommendation execution time;
- application errors.

System logs support troubleshooting and performance optimization.

---

# 10. Security

The deployment architecture implements multiple security mechanisms.

These include:

- HTTPS communication;
- JWT authentication;
- encrypted credentials;
- secure environment variables;
- database authentication;
- role-based authorization;
- request validation;
- API rate limiting.

These measures protect both system resources and user information.

---

# 11. Scalability

The deployment architecture supports horizontal expansion.

Current deployment

```text
React

↓

FastAPI

↓

Neo4j
```

Future deployment

```text
Load Balancer

↓

Multiple FastAPI Instances

↓

Neo4j Cluster

↓

PostgreSQL Replicas
```

The architecture supports increased workloads without significant redesign.

---

# 12. CI/CD Pipeline

Continuous Integration and Continuous Deployment streamline software delivery.

Development workflow

```text
Developer

↓

Git Repository

↓

GitHub Actions

↓

Automated Testing

↓

Docker Image Build

↓

Deployment Server
```

CI/CD improves deployment reliability and reduces manual errors.

---

# 13. Backup and Recovery

Regular backups protect educational knowledge and operational data.

| Component | Backup Strategy |
|------------|-----------------|
| Markdown Repository | Git Version Control |
| PostgreSQL | Scheduled Database Backup |
| Neo4j | Database Dump |
| Vector Storage | Rebuild from Knowledge Repository |
| Configuration | Secure Backup |

Markdown remains the authoritative source of educational knowledge.

---

# 14. Production Environment

A typical production deployment includes:

| Component | Environment |
|------------|-------------|
| Operating System | Ubuntu Server |
| Web Server | Nginx |
| Backend | FastAPI |
| Database | PostgreSQL |
| Knowledge Graph | Neo4j |
| AI Service | OpenAI API |
| Container Platform | Docker |

This environment supports reliable long-term operation.

---

# 15. Future Cloud Deployment

The deployment architecture is cloud-independent.

Possible deployment targets include:

- Amazon Web Services (AWS);
- Microsoft Azure;
- Google Cloud Platform (GCP);
- DigitalOcean;
- institutional private servers.

Since application components are containerized, migration between environments requires minimal modification.

---

# 16. AI Service Dependency Matrix

The following table summarizes runtime dependencies.

| Service | Depends On | Purpose |
|---------|------------|---------|
| Planner Agent | FastAPI | Workflow orchestration |
| Recommendation Agent | Recommendation Engine | Personalized recommendations |
| Retrieval Agent | Neo4j + Vector Storage | Hybrid Graph RAG |
| Response Agent | OpenAI API | Natural language generation |
| FastAPI | PostgreSQL | Operational data management |
| Recommendation Engine | Neo4j | Graph reasoning |
| Hybrid Graph RAG | Neo4j Vector Index | Semantic retrieval |

This matrix illustrates how AI services collaborate during runtime.

---

# 17. Deployment Workflow

The following illustrates the complete deployment process.

```text
Source Code

↓

Git Repository

↓

CI/CD Pipeline

↓

Docker Image

↓

Deployment Server

↓

Docker Network

↓

Running Services

↓

Student Access
```

This workflow supports repeatable and automated deployments.

---

# 18. Summary

The Deployment & Infrastructure Design provides the operational foundation for the EduGuide platform.

By separating frontend, backend, AI services, and databases into independent infrastructure components, the architecture achieves modularity, scalability, security, and maintainability.

Containerization, standardized service communication, centralized configuration, and automated deployment workflows enable reliable production operation while supporting future growth and cloud migration.

This deployment strategy ensures that the AI-powered educational guidance platform can evolve as new educational knowledge, AI capabilities, and user demands increase.