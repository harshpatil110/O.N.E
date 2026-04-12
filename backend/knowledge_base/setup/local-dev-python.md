---
title: "Local Development Setup - Python"
category: "setup"
applicable_roles: ["backend", "fullstack", "data"]
applicable_stacks: ["python"]
applicable_levels: ["intern", "junior", "mid", "senior"]
last_updated: "2026-04-13"
---

# Local Development Setup - Python

Welcome to the backend engineering team! This document outlines the mandatory steps to configure your local development environment for Python-based services. Adhering to these guidelines ensures consistency across the team and minimizes "it works on my machine" scenarios. 

## Prerequisites
Before beginning, ensure your system meets the following baseline requirements:
- **Python 3.11+**: We standardize on Python 3.11. Validate your installation using `python3 --version`. If multiple versions are installed, consider using `pyenv` to manage your active version.
- **pip**: Ensure `pip` is updated to the latest version (`python3 -m pip install --upgrade pip`).

## Installing Poetry
We rely on [Poetry](https://python-poetry.org/) for robust dependency management and packaging, ditching `requirements.txt` for deterministic `pyproject.toml` configuration. 

Install Poetry globally using pip:
```bash
pip install poetry
```
Verify the installation by running `poetry --version`.

## Project Initialization
If you are initiating a net-new service, use Poetry's scaffolding tool:
```bash
poetry new project-name
cd project-name
```
For existing projects, simply clone the repository from GitHub and navigate into the root directory.

## Managing Dependencies
Once inside the project directory, resolve and install all required dependencies defined in `pyproject.toml` or `poetry.lock`:
```bash
poetry install
```
This command automatically creates an isolated virtual environment and installs identical versions of all packages.

## Activating the Virtual Environment
To run commands within the context of your project's isolated environment, activate the Poetry shell:
```bash
poetry shell
```
*Note:* You must run this command every time you open a new terminal session before executing application code.

## Environment Variables Configuration
Our applications rely on `pydantic-settings` to securely load configuration from environment variables. 
1. Locate the `.env.example` file in the root directory.
2. Duplicate it to create your local `.env` file: `cp .env.example .env`. 
3. Request local secrets (e.g., API keys, Local DB connection strings) from your engineering manager or refer to our 1Password vault. **Never commit `.env` to version control.**

## Running the Application
Our standard API framework is FastAPI. With your environment active and `.env` configured, launch the ASGI development server:
```bash
uvicorn app.main:app --reload
```
The `--reload` flag enables hot-reloading for rapid development. Access the local API at `http://localhost:8000` and Swagger docs at `http://localhost:8000/docs`.

## Common Troubleshooting
- **ModuleNotFoundError**: Ensure your `poetry shell` is active. If you recently pulled changes, run `poetry install` to fetch newly added packages.
- **Python Version Mismatch**: Poetry might pick up an older system Python. Force it to use 3.11 via `poetry env use python3.11`.
- **Database Connection Errors**: Verify your `.env` variables. Ensure your local PostgreSQL Docker container (if applicable) is actually running via `docker ps`.
- **Port 8000 in use**: Ensure no other background terminals are running Uvicorn. Kill the zombie process using `kill -9 $(lsof -t -i:8000)` on Unix/Mac. 

For persistent issues, reach out in the `#engineering-backend` Slack channel.
