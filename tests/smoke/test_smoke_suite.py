import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.cms_actions import perform_login

@pytest.mark.smoke
class TestSmokeTests:
    """Smoke test suite for basic functionality validation"""
    
    def test_application_accessibility(self, chrome_driver, test_config):
        """Test if application is accessible"""
        chrome_driver.get(test_config['base_url'])
        assert "login" in chrome_driver.current_url.lower() or "dashboard" in chrome_driver.current_url.lower()
        assert chrome_driver.title is not None
        
    def test_basic_login_smoke(self, chrome_driver, test_config):
        """Smoke test for login functionality"""
        dashboard = perform_login(
            chrome_driver, 
            test_config['base_url'], 
            test_config['email'], 
            test_config['password']
        )
        assert dashboard.is_loaded()
        
    def test_dashboard_load_smoke(self, authenticated_driver):
        """Smoke test for dashboard loading"""
        driver, dashboard = authenticated_driver
        assert dashboard.is_loaded()
        assert "dashboard" in driver.current_url.lower() or driver.current_url != ""
