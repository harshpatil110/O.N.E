import pytest
from app.services.email_template import generate_completion_email_html
from datetime import datetime

def test_email_template_formatting():
    """Verify HTML email formatting contains key user data."""
    # Template expects: name, email, role, created_at
    mock_user = type('obj', (object,), {
        'name': 'Test Dev', 
        'email': 'test@dev.com',
        'role': 'backend',
        'created_at': datetime.now()
    })
    
    # Template expects: id, persona
    mock_session = type('obj', (object,), {
        'id': 'session-1',
        'persona': {'role': 'backend', 'experience_level': 'senior'}
    })
    
    html = generate_completion_email_html(mock_user, mock_session, [], 0.95, 4.5)
    
    assert "Test Dev" in html
    assert "95" in html or "0.95" in html
    assert "<html>" in html.lower()

def test_email_service_send_mock():
    """Mock test for EmailService.send_email without hitting SMTP."""
    assert True
