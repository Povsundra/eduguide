# EduGuide Platform

EduGuide is an AI-powered educational guidance platform tailored for Cambodia. It leverages Knowledge Graphs, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs) to help students discover universities, academic programs, scholarships, and career pathways.

## Architecture

- **Backend:** FastAPI (Python 3.12)
- **Frontend:** React + Vite + TailwindCSS (TypeScript)
- **Databases:**
  - PostgreSQL (Relational Data, Users, Auth)
  - Neo4j (Knowledge Graph for Careers, Majors, Universities)
  - Redis (Caching, Celery Broker for async AI tasks)
- **Infrastructure:** Docker & Docker Compose

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.
- Python 3.12 (for local development/linting)
- Node.js 20.x (for frontend local development)

## Getting Started (Dockerized Development)

The easiest way to run the entire stack is using Docker Compose.

1. **Environment Variables**
   Copy the example environment file and customize it if necessary:
   ```bash
   cp .env.example .env
   ```
   *Note: The default values in `.env.example` are pre-configured to work perfectly with the Docker Compose setup out of the box.*

2. **Start the Stack**
   ```bash
   docker-compose up -d --build
   ```

3. **Verify the Stack**
   - **Frontend:** http://localhost
   - **Backend API Docs:** http://localhost/api/v1/docs
   - **System Health:** http://localhost/api/v1/health (Should return `"postgres": "ok"` and `"neo4j": "ok"`)
   - **Neo4j Browser:** http://localhost:7474

## Local Development (Without Docker)

If you prefer to run the services directly on your host machine for debugging:

### Backend
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r backend/requirements/dev.txt`
4. Run the server: `cd backend && uvicorn app.main:app --reload`

### Frontend
1. Install dependencies: `cd frontend && npm install`
2. Run the dev server: `npm run dev`

## Code Quality & Linting

EduGuide strictly enforces code quality using `pre-commit` hooks. 
Before submitting a Pull Request, ensure your code passes all linters.

**Install pre-commit hooks:**
```bash
pre-commit install
```

**Run linters manually:**
```bash
pre-commit run --all-files
```
*This will run Black, isort, Ruff, and mypy for Python, and Prettier for the frontend.*
