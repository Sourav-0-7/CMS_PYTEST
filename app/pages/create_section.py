from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CreateSectionPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def go_to_content_template_page(self):
        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//span[normalize-space()='Content Templates' or "
                 "normalize-space()='Templates']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        button.click()

    def open_first_document(self):
        doc_element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "(//tbody/tr)[1]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", doc_element)
        self.driver.execute_script("arguments[0].click();", doc_element)

    def create_section(self, section_name):
        # Click "Create Section"
        create_section_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Create Section')]"))
        )
        create_section_btn.click()

        # Input section name
        name_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
        )
        name_input.clear()
        name_input.send_keys(section_name)

        # Click Save
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))
        )
        save_button.click()
