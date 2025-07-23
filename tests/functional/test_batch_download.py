import pytest
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.pages.documents_page import DocumentsPage

@pytest.mark.functional
@pytest.mark.download
@pytest.mark.slow
class TestBatchDownload:
    """Batch download functionality tests"""
    
    def test_batch_download_all(self, authenticated_driver, test_config):
        """Test batch download functionality"""
        driver, dashboard = authenticated_driver
        download_dir = test_config['download_dir']
        
        try:
            documents_page = DocumentsPage(driver)
            documents_page.batch_download_all()
            
            # Check for downloaded files
            max_wait = 60
            downloaded_files = []
            
            for i in range(max_wait // 5):
                time.sleep(5)
                if os.path.exists(download_dir):
                    downloaded_files = [
                        f for f in os.listdir(download_dir) 
                        if os.path.isfile(os.path.join(download_dir, f))
                    ]
                    if downloaded_files:
                        break
            
            assert len(downloaded_files) > 0, "No files were downloaded"
            
        except Exception as e:
            driver.save_test_screenshot("batch_download_failure.png")
            pytest.fail(f"Batch download test failed: {str(e)}")
    
    def test_document_selection(self, authenticated_driver):
        """Test document selection functionality"""
        driver, dashboard = authenticated_driver
        
        documents_page = DocumentsPage(driver)
        documents_page.click_batch_download_button()
        
        # Test selecting all documents
        documents_page.select_all_documents()
