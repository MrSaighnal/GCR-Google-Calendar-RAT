"""Shared pytest fixtures and configuration for all tests."""
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_google_credentials():
    """Mock Google service account credentials."""
    mock_creds = Mock()
    mock_creds.service_account_email = "test@example.iam.gserviceaccount.com"
    mock_creds.project_id = "test-project-123"
    return mock_creds


@pytest.fixture
def mock_calendar_service():
    """Mock Google Calendar service object."""
    mock_service = MagicMock()
    
    # Mock events().list() response
    mock_events_list = MagicMock()
    mock_events_list.execute.return_value = {
        'items': [],
        'nextPageToken': None
    }
    mock_service.events.return_value.list.return_value = mock_events_list
    
    # Mock events().insert() response
    mock_events_insert = MagicMock()
    mock_events_insert.execute.return_value = {
        'id': 'test-event-id',
        'status': 'confirmed'
    }
    mock_service.events.return_value.insert.return_value = mock_events_insert
    
    # Mock events().delete() response
    mock_events_delete = MagicMock()
    mock_events_delete.execute.return_value = None
    mock_service.events.return_value.delete.return_value = mock_events_delete
    
    return mock_service


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for command execution tests."""
    mock_result = Mock()
    mock_result.stdout = b"Test command output"
    mock_result.stderr = b""
    mock_result.returncode = 0
    return mock_result


@pytest.fixture
def sample_service_account_key(temp_dir):
    """Create a sample service account key file."""
    key_data = {
        "type": "service_account",
        "project_id": "test-project-123",
        "private_key_id": "key123",
        "private_key": "-----BEGIN PRIVATE KEY-----\ntest-key\n-----END PRIVATE KEY-----",
        "client_email": "test@example.iam.gserviceaccount.com",
        "client_id": "123456789",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test%40example.iam.gserviceaccount.com"
    }
    
    import json
    key_path = temp_dir / "service_account_key.json"
    with open(key_path, 'w') as f:
        json.dump(key_data, f)
    
    return str(key_path)


@pytest.fixture
def mock_environment_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    test_env = {
        'CALENDAR_ID': 'test-calendar-id@group.calendar.google.com',
        'SERVICE_ACCOUNT_KEY_PATH': '/path/to/test/key.json'
    }
    for key, value in test_env.items():
        monkeypatch.setenv(key, value)
    return test_env


@pytest.fixture
def capture_stdout(monkeypatch):
    """Capture stdout for testing print outputs."""
    import io
    import sys
    
    captured = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured)
    
    def get_output():
        return captured.getvalue()
    
    return get_output


@pytest.fixture(autouse=True)
def reset_test_state():
    """Reset any global state between tests."""
    # Add any global state cleanup here if needed
    yield
    # Post-test cleanup


@pytest.fixture
def mock_time(monkeypatch):
    """Mock time.sleep to speed up tests."""
    def mock_sleep(seconds):
        pass
    
    monkeypatch.setattr('time.sleep', mock_sleep)


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom configuration if needed
    pass


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to tests in unit directory
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        # Add integration marker to tests in integration directory
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)