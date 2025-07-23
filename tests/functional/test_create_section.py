import pytest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.pages.create_section import CreateSectionPage

@pytest.mark.functional
@pytest.mark.section
class TestCreateSection:
    """Section creation functionality tests"""
    
    def test_create_section(self, authenticated_driver):
        """Test creating a new section"""
        driver, dashboard = authenticated_driver
        
        try:
            section_page = CreateSectionPage(driver)
            section_page.go_to_content_template_page()
            section_page.open_first_document()
            section_page.create_section("Test Section Name")
            
        except Exception as e:
            driver.save_test_screenshot("create_section_failure.png")
            pytest.fail(f"Section creation failed: {str(e)}")
    
    def test_section_creation_workflow(self, authenticated_driver):
        """Test the complete section creation workflow"""
        driver, dashboard = authenticated_driver
        
        section_page = CreateSectionPage(driver)
        
        # Test navigation to content template page
        section_page.go_to_content_template_page()
        
        # Test opening first document
        section_page.open_first_document()
        
        # Test section creation with different names
        test_names = ["Test Section 1", "Test Section 2"]
        
        for name in test_names:
            try:
                section_page.create_section(name)
            except Exception as e:
                pytest.fail(f"Failed to create section '{name}': {str(e)}")
