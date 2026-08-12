# CI/CD Pipeline Configuration

## Overview
Nexus AI Innovations uses **GitHub Actions** for continuous integration and
deployment.

## Pipeline Stages
```
Push to PR → Lint → Test → Build → Deploy (staging) → Manual approval → Deploy (prod)
```

## GitHub Actions Workflow
```yaml
name: O.N.E CI/CD

on:
  push:
    branches: [dev, main]
  pull_request:
    branches: [dev]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install ruff pytest
      - name: Lint
        run: ruff check backend/
      - name: Test
        run: |
          cd backend
          pytest --tb=short -q
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
          JWT_SECRET_KEY: test-secret-key

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: cd frontend && npm ci && npm run build
```

## Secrets Management
All secrets are stored in **GitHub Repository Settings → Secrets**:
* `TEST_DATABASE_URL`
* `PROD_DATABASE_URL`
* `JWT_SECRET_KEY`
* `NVIDIA_API_KEY`

---
*CI/CD Lead: Harshvardhan Patil*
