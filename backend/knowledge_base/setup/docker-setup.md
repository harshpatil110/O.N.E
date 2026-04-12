---
title: "Docker Setup and Workflows"
category: "setup"
applicable_roles: ["devops", "backend", "fullstack"]
applicable_stacks: ["all"]
applicable_levels: ["intern", "junior", "mid", "senior"]
last_updated: "2026-04-13"
---

# Docker Setup and Workflows

Welcome to the team! Our robust microservices architecture and backing data stores rely heavily on containerization. By standardizing on Docker, we guarantee that the software runs seamlessly regardless of whether it's deployed on your laptop, our staging environments, or production clusters. This guide outlines how to configure Docker securely and effectively.

## Installation Links
You must install Docker Desktop to gain access to the Docker engine and GUI. Download the appropriate version for your operating system:
- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) (Ensure you select Apple Silicon vs. Intel properly).
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) (Verify WSL2 backend is enabled natively).
- **Linux**: [Docker Engine for Linux](https://docs.docker.com/engine/install/) (Follow distribution-specific apt/yum/dnf commands).

## Verification and Minimum Versions
To ensure compatibility with our modern `docker-compose.yml` configurations, verify your installed versions. We require Docker Engine **24+** and Docker Compose **v2+**.

Run the following in your terminal:
```bash
docker --version && docker-compose --version
```
*Note: Depending on your OS, Docker Compose v2 may be executed via `docker compose` (with a space) rather than `docker-compose` (with a hyphen). Both trigger the same underlying V2 plugin on modern installations.*

## Running the Application Stack
Our projects are orchestrated using Compose files. To spin up the entire dependency graph (e.g., APIs, PostgreSQL databases, Redis, ChromaDB), navigate to the root directory containing `docker-compose.yml` and execute:
```bash
docker-compose up --build
```
- The `--build` flag forces Docker to rebuild images. This is mandatory if you have recently altered `requirements.txt`, `pyproject.toml`, or `Dockerfile`.
- Append `-d` (detached mode) if you wish to run the containers in the background, keeping your terminal free for other commands.

## Useful Daily Commands
Mastering these recurring container operations will vastly improve your debugging speed:
- **`docker ps`**: View all currently executing containers, their IDs, mapped ports, and health status.
- **`docker logs -f <container_name>`**: Tail the live logs of a specific container. Replace `<container_name>` with the target service (e.g., `one-backend`).
- **`docker exec -it <container_name> bash`**: Spawn an interactive shell session inside a running container. Highly useful for poking around the internal filesystem or manually querying a database container.
- **`docker system prune`**: Cleans up dangling images and stopped containers to free up hard drive space (run this monthly).

## Stopping and Tearing Down
When you are done developing for the day, or if you need a pristine environment reset, halt your containers properly:
```bash
docker-compose down
```
If you encounter deep state-related bugs and need a complete reset (destroying volumes and database data), append the volumes flag:
```bash
docker-compose down -v
```
**Warning**: Using `-v` permanently deletes local database records stored in Docker volumes. Use with caution.
