import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.cms_actions import perform_login
from app.pages.login_page import LoginPage

@pytest.mark.login
class TestLoginSuite:
    """Login test suite"""
    
    def test_successful_login(self, chrome_driver, test_config):
        """Test successful login with valid credentials"""
        try:
            dashboard = perform_login(
                chrome_driver, 
                test_config['base_url'], 
                test_config['email'], 
                test_config['password']
            )
            assert dashboard.is_loaded(), "Dashboard should load after successful login"
            
        except Exception as e:
            chrome_driver.save_test_screenshot("login_failure.png")
            pytest.fail(f"Login test failed: {str(e)}")
    
    def test_login_page_elements(self, chrome_driver, test_config):
        """Test login page elements are present"""
        chrome_driver.get(test_config['base_url'])
        login_page = LoginPage(chrome_driver)
        
        # Check if login elements exist
        email_field = chrome_driver.find_element(*login_page.email_field)
        password_field = chrome_driver.find_element(*login_page.password_field)
        sign_in_button = chrome_driver.find_element(*login_page.sign_in_button)
        
        assert email_field.is_displayed()
        assert password_field.is_displayed()
        assert sign_in_button.is_displayed()
    
    @pytest.mark.parametrize("invalid_email,invalid_password", [
        ("wrong@email.com", "wrongpassword"),
        ("", "password"),
        ("admin@qualityedgar.com", ""),
    ])
    def test_invalid_login_attempts(self, chrome_driver, test_config, invalid_email, invalid_password):
        """Test login with invalid credentials"""
        chrome_driver.get(test_config['base_url'])
        login_page = LoginPage(chrome_driver)
        
        with pytest.raises(Exception):
            login_page.login(invalid_email, invalid_password)
