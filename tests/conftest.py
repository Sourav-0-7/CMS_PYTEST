import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        'base_url': os.getenv('CMS_URL', 'http://54.218.101.86:9000/login'),
        'email': os.getenv('CMS_USERNAME', 'admin@qualityedgar.com'),
        'password': os.getenv('CMS_PASSWORD', 'password'),
        'download_dir': os.path.join(os.getcwd(), "downloads"),
        'screenshot_dir': os.path.join(os.getcwd(), "screenshots")
    }

@pytest.fixture(scope="function")
def chrome_driver(test_config, request):
    """Chrome driver fixture with proper setup and teardown"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    
    # Setup screenshot directory
    screenshot_dir = test_config['screenshot_dir']
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Setup download directory for download tests
    if 'download' in request.node.name.lower():
        download_dir = test_config['download_dir']
        os.makedirs(download_dir, exist_ok=True)
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    
    # Add custom screenshot method
    def save_test_screenshot(filename):
        full_path = os.path.join(screenshot_dir, filename)
        driver.save_screenshot(full_path)
        print(f"Screenshot saved: {full_path}")
    
    driver.save_test_screenshot = save_test_screenshot
    
    yield driver
    
    # Cleanup
    if hasattr(driver, 'quit'):
        driver.quit()

@pytest.fixture(scope="function")
def authenticated_driver(chrome_driver, test_config):
    """Driver with authenticated session"""
    from app.cms_actions import perform_login
    
    dashboard = perform_login(
        chrome_driver, 
        test_config['base_url'], 
        test_config['email'], 
        test_config['password']
    )
    
    return chrome_driver, dashboard

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "smoke: Smoke test suite")
    config.addinivalue_line("markers", "login: Login test suite")
    config.addinivalue_line("markers", "functional: Functional test suite")
    config.addinivalue_line("markers", "content_template: Content template tests")
    config.addinivalue_line("markers", "section: Section creation tests")
    config.addinivalue_line("markers", "download: Download functionality tests")
    config.addinivalue_line("markers", "dashboard: Dashboard tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
