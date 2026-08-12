# Docker Compose — Local Development Stack

## Overview
The following `docker-compose.yml` spins up the entire Nexus AI Innovations
development stack locally.

## docker-compose.yml
```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend:/app
    depends_on:
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  redis_data:
  chroma_data:
```

## Usage
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f backend

# Rebuild after dependency changes
docker compose build --no-cache backend

# Tear down
docker compose down -v
```

---
*DevOps: Harshvardhan Patil*
