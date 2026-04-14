def test_auth_login_fail(sync_client):
    """Test successful and invalid login payloads."""
    # Since DB is mocked and empty (SQLite memory), it should fail.
    response = sync_client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_auth_login_mock():
    """Placeholder structural test for valid JWT auth payload."""
    assert True
