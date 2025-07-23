import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.pages.content_template_page import ContentTemplate

@pytest.mark.functional
@pytest.mark.content_template
class TestContentTemplate:
    """Content template functionality tests"""
    
    def test_create_content_template(self, authenticated_driver):
        """Test creating a new content template"""
        driver, dashboard = authenticated_driver
        
        try:
            content_page = ContentTemplate(driver)
            content_page.open_content_template_modal()
            content_page.fill_template_form(name="AutoTemplate_Test")
            content_page.submit()
            
        except Exception as e:
            driver.save_test_screenshot("content_template_error.png")
            pytest.fail(f"Content template creation failed: {str(e)}")
    
    def test_content_template_modal_elements(self, authenticated_driver):
        """Test content template modal has required elements"""
        driver, dashboard = authenticated_driver
        
        content_page = ContentTemplate(driver)
        content_page.open_content_template_modal()
        
        # Verify modal elements are present
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(driver, 10)
        
        # Check template name input
        name_input = wait.until(EC.presence_of_element_located(content_page.template_name_input))
        assert name_input.is_displayed()
