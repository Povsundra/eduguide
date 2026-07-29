# EduGuide Backend - Database Architecture

This document describes the Database Foundation for the EduGuide backend application, powered by PostgreSQL, asynchronous SQLAlchemy 2.0, and Alembic migrations.

## Database Architecture

- **PostgreSQL:** Primary relational datastore for entity management.
- **SQLAlchemy 2.0:** Asynchronous ORM utilizing `asyncpg` for high-performance non-blocking data access.
- **Connection Pool:** Hosted in `app/db/session.py`.
  - Configured securely with `pool_size=5`, `max_overflow=10`, `pool_pre_ping=True` (automated drop-connection checks), and `pool_recycle=3600` (idle refresh).
- **Generic Repository:** Hosted in `app/crud/base.py`. Provides standard async CRUD operations (`get`, `get_multi`, `create`, `update`, `remove`) enforcing strict typing using Pydantic schemas.

## Environment Variables

To run the database or migrations, the following variable must be set in your `backend/.env` file:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/eduguide
```
*(Note: Using `db` as the host assumes you are running via Docker. If you run migrations from your host OS, this should be `localhost`).*

## Local Development & Alembic Usage

Migrations are handled by Alembic. 
Because the application runs in a Docker network, it is **highly recommended** to run all migrations via `docker exec` against the running `eduguide-backend-1` container. This avoids networking issues between the host OS and the database.

### 1. Generating a new migration
When you update a model or create a new one, autogenerate the migration:
```bash
docker exec eduguide-backend-1 alembic revision --autogenerate -m "Description of changes"
```

### 2. Applying migrations
To apply all pending migrations to the database:
```bash
docker exec eduguide-backend-1 alembic upgrade head
```

### 3. Reverting a migration
If you need to rollback the last applied migration:
```bash
docker exec eduguide-backend-1 alembic downgrade -1
```

## Testing Infrastructure

- The test suite strictly uses an independent, perfectly-isolated **in-memory SQLite database** (`sqlite+aiosqlite:///:memory:`). 
- All database state is automatically created and dropped natively per test using the `db_session` fixture inside `tests/conftest.py`. No mocking is required, and your local PostgreSQL instance is never polluted with test data.
