# Python Coding Standards — Nexus AI Innovations

## General Rules
* Follow **PEP 8** strictly. Use `ruff` as the primary linter.
* Maximum line length: **88 characters** (Black formatter default).
* Use **type hints** for all function signatures.

## Formatting
```bash
# Auto-format before committing
ruff format .
ruff check --fix .
```

## Naming Conventions
| Element       | Convention          | Example                    |
|---------------|---------------------|----------------------------|
| Variables     | snake_case          | `user_count`               |
| Functions     | snake_case          | `get_active_users()`       |
| Classes       | PascalCase          | `OnboardingSession`        |
| Constants     | UPPER_SNAKE_CASE    | `MAX_RETRY_COUNT`          |
| Modules       | snake_case          | `auth_deps.py`             |

## Docstrings
Use Google-style docstrings:
```python
def create_user(email: str, role: str) -> User:
    """Create a new user in the database.

    Args:
        email: The user's email address.
        role: The user's role (e.g., 'admin', 'engineer').

    Returns:
        The newly created User ORM instance.

    Raises:
        ValueError: If the email already exists.
    """
```

## Import Order
1. Standard library
2. Third-party packages
3. Local application imports

Enforced by `ruff` rule `I` (isort-compatible).

## Error Handling
* Always use specific exception types, never bare `except:`.
* Log exceptions with `logger.error(msg, exc_info=True)`.
* Use FastAPI's `HTTPException` for API error responses.

---
*Standards maintained by Harshvardhan Patil*
