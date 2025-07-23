from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        # Fixed locator - removed 's' from 'buttons'
        self.account_button = (By.XPATH, "//*[@id='header']/div[2]/div/button")

    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.account_button)
            )
            return True
        except TimeoutException:
            return False
