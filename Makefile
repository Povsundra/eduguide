# =============================================================================
# EduGuide Makefile
# Helper commands for local development using Docker Compose
# =============================================================================

.PHONY: up down build logs clean

# Start the application in the background
up:
	docker-compose up -d

# Stop the application
down:
	docker-compose down

# Rebuild the Docker images
build:
	docker-compose build

# Rebuild and start
up-build:
	docker-compose up -d --build

# View logs from all containers
logs:
	docker-compose logs -f

# View logs for a specific service (e.g. make log-backend)
log-%:
	docker-compose logs -f $*

# Stop and remove volumes (clean database, etc.)
clean:
	docker-compose down -v
