# Alembic Database Migration Guide

## Overview
Nexus AI Innovations uses **Alembic** for managing PostgreSQL schema migrations
against our Supabase database.

## Setup
```bash
cd backend
alembic init alembic  # Only needed once
```

## Creating a Migration
```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "add_progress_percentage_to_sessions"

# Or create an empty migration for manual edits
alembic revision -m "seed_initial_roles"
```

## Running Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View current revision
alembic current

# View migration history
alembic history --verbose
```

## Best Practices
* **One migration per PR.** Never bundle unrelated schema changes.
* Always test migrations on a local database before running against
  the Supabase production instance.
* Include both `upgrade()` and `downgrade()` functions.
* Use `op.execute()` for data migrations, not ORM models.

## Environment Configuration
Set `sqlalchemy.url` in `alembic.ini`:
```ini
sqlalchemy.url = postgresql://postgres:<pass>@db.<ref>.supabase.co:5432/postgres
```
Or override via environment variable:
```python
# env.py
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])
```

---
*Database Admin: Parth Shah*
