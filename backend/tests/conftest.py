import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import asyncio
from unittest.mock import MagicMock

from app.main import app
from app.core.database import get_db

def override_get_db():
    mock_db = MagicMock()
    
    # Setup mock query chain so db.query(User).filter(...).first() returns None
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_query.filter.return_value = mock_filter
    mock_filter.first.return_value = None
    
    mock_db.query.return_value = mock_query

    yield mock_db

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def sync_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
