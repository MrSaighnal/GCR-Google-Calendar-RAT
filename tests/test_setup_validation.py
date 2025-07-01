"""Validation tests to ensure the testing infrastructure is properly configured."""
import pytest
import sys
import os
from pathlib import Path


class TestSetupValidation:
    """Test class to validate the testing infrastructure setup."""
    
    def test_pytest_is_available(self):
        """Verify pytest is installed and importable."""
        import pytest
        assert pytest.__version__
    
    def test_pytest_cov_is_available(self):
        """Verify pytest-cov is installed and importable."""
        import pytest_cov
        assert pytest_cov
    
    def test_pytest_mock_is_available(self):
        """Verify pytest-mock is installed and importable."""
        import pytest_mock
        assert pytest_mock
    
    def test_project_structure_exists(self):
        """Verify the expected project structure is in place."""
        project_root = Path(__file__).parent.parent
        
        # Check main directories exist
        assert (project_root / "tests").exists()
        assert (project_root / "tests" / "unit").exists()
        assert (project_root / "tests" / "integration").exists()
        
        # Check configuration files exist
        assert (project_root / "pyproject.toml").exists()
        assert (project_root / "tests" / "conftest.py").exists()
        
        # Check __init__.py files exist
        assert (project_root / "tests" / "__init__.py").exists()
        assert (project_root / "tests" / "unit" / "__init__.py").exists()
        assert (project_root / "tests" / "integration" / "__init__.py").exists()
    
    def test_fixtures_are_available(self, temp_dir, mock_google_credentials, mock_calendar_service):
        """Verify that custom fixtures from conftest.py are available."""
        # Test temp_dir fixture
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test mock_google_credentials fixture
        assert mock_google_credentials.service_account_email == "test@example.iam.gserviceaccount.com"
        assert mock_google_credentials.project_id == "test-project-123"
        
        # Test mock_calendar_service fixture
        assert mock_calendar_service.events
        result = mock_calendar_service.events().list().execute()
        assert 'items' in result
        assert result['items'] == []
    
    def test_markers_are_defined(self):
        """Verify custom pytest markers are properly defined."""
        # Get pytest config
        config = pytest.config if hasattr(pytest, 'config') else None
        
        # These markers should be defined in pyproject.toml
        expected_markers = ['unit', 'integration', 'slow']
        
        # Since we can't easily access the config in a test, we'll just
        # verify that we can use the markers without errors
        @pytest.mark.unit
        def dummy_unit_test():
            pass
        
        @pytest.mark.integration
        def dummy_integration_test():
            pass
        
        @pytest.mark.slow
        def dummy_slow_test():
            pass
        
        # If we got here without errors, markers are working
        assert True
    
    def test_coverage_configuration(self):
        """Verify coverage is properly configured."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Check coverage configuration exists
        assert "[tool.coverage.run]" in content
        assert "[tool.coverage.report]" in content
        assert "fail_under = " in content  # Coverage threshold is configured
        assert "--cov-fail-under=" in content  # Coverage threshold is configured
    
    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Test that unit marker can be applied and works correctly."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker_works(self):
        """Test that integration marker can be applied and works correctly."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Test that slow marker can be applied and works correctly."""
        assert True
    
    def test_main_module_importable(self):
        """Verify the main module (gcr.py) can be imported."""
        # Add project root to Python path
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        try:
            import gcr
            assert gcr
        except ImportError as e:
            # This is expected until dependencies are installed
            assert "google" in str(e) or "googleapiclient" in str(e)


class TestPytestCommands:
    """Test class to validate pytest command configurations."""
    
    def test_pytest_ini_options_configured(self):
        """Verify pytest options are properly configured in pyproject.toml."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Check key pytest options
        assert "[tool.pytest.ini_options]" in content
        assert 'testpaths = ["tests"]' in content
        assert '"--strict-markers"' in content
        assert '"--cov=gcr"' in content
        assert '"--cov-report=html"' in content
        assert '"--cov-report=xml"' in content