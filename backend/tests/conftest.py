import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock
from app.main import app
from app.core.database import get_db
from app.core.auth_deps import get_current_user
from datetime import datetime

# Mock objects
class MockUser:
    id = 1
    email = "test@example.com"
    role = "hr_admin"
    name = "Test User"
    created_at = datetime.now()
    # A valid-looking bcrypt hash to avoid "Invalid salt" errors
    hashed_password = "$2b$12$KIXH.l.ZpXz8E.Z9Zz9Z9.Z9Zz9Z9.Z9Zz9Z9.Z9Zz9Z9.Z9Zz9Z9" 

class MockSession:
    id = "golden-test-session"
    user_id = 1
    persona = {"role": "backend", "experience_level": "senior", "tech_stack": ["python"]}
    status = "in_progress"

def override_get_db():
    mock_db = MagicMock()
    mock_query = MagicMock()
    
    # Setup a chain
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    
    # By default, let's return a valid-ish object to prevent AttributeErrors
    # But for auth tests, we might want it to return None.
    # We'll use a side_effect or just return a mock that has all needed fields.
    
    mock_result = MagicMock()
    mock_result.id = 1
    mock_result.user_id = 1
    mock_result.email = "test@example.com"
    mock_result.role = "hr_admin"
    mock_result.name = "Test User"
    mock_result.created_at = datetime.now()
    mock_result.hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGGa31S"
    mock_result.persona = {"role": "backend"}
    mock_result.status = "in_progress"
    mock_result.current_fsm_state = "WELCOME"
    
    mock_query.first.return_value = mock_result
    mock_query.all.return_value = []
    
    yield mock_db

def override_get_current_user():
    return MockUser()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="session")
def sync_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
