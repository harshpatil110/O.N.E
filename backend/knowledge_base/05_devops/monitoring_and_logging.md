# Monitoring & Logging Standards

## Logging Framework
All backend services use Python's `logging` module configured via
`app/core/config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
```

## Log Levels
| Level    | Usage                                         |
|----------|-----------------------------------------------|
| DEBUG    | Detailed diagnostic (local dev only)          |
| INFO     | Normal operations (requests, completions)     |
| WARNING  | Unexpected but non-critical events             |
| ERROR    | Failures requiring attention                  |
| CRITICAL | System-level failures (DB down, OOM)          |

## Structured Logging for Agents
Agent interactions log structured JSON:
```python
logger.info("Agent response", extra={
    "session_id": session.id,
    "tool_called": "rag_search",
    "query": user_message[:100],
    "response_length": len(response),
    "latency_ms": elapsed_ms,
})
```

## Monitoring Endpoints
* `GET /health` — Returns `{"status": "ok"}` with 200.
* `GET /health/deep` — Checks DB, Redis, and ChromaDB connectivity.

---
*Observability: Archit Verma*
