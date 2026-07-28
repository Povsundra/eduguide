# =============================================================================
# EduGuide Frontend Dockerfile
# Multi-stage build: compiles Vite app, serves static files via Nginx
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM node:22-alpine AS builder

WORKDIR /app

# Install dependencies first (leverage Docker cache)
COPY package.json package-lock.json* ./
RUN npm ci || npm install

# Copy source code and build
COPY . .
RUN npm run build

# -----------------------------------------------------------------------------
# Stage 2: Runner (Static Server)
# -----------------------------------------------------------------------------
FROM nginx:alpine AS runner

# Remove default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy built artifacts from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Note: We do NOT provide a custom nginx.conf here.
# This container only serves static files locally on its port 80.
# The MAIN reverse proxy in the `nginx/` folder handles the routing.

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
