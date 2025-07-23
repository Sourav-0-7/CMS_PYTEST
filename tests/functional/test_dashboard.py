import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.mark.functional
@pytest.mark.dashboard
class TestDashboard:
    """Dashboard functionality tests"""
    
    def test_dashboard_loading(self, authenticated_driver):
        """Test dashboard loads correctly after login"""
        driver, dashboard = authenticated_driver
        
        assert dashboard.is_loaded(), "Dashboard should be loaded"
        
    def test_dashboard_navigation_elements(self, authenticated_driver):
        """Test dashboard navigation elements are present"""
        driver, dashboard = authenticated_driver
        
        # Check for key dashboard elements
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 10)
        
        # Check for header
        header = wait.until(EC.presence_of_element_located((By.ID, "header")))
        assert header.is_displayed()
