from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, WebDriverException
import time

class ContentTemplate:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
        # Updated locators with better compatibility
        self.content_template_tab = (
            By.XPATH,
            "//button[.//span[normalize-space()='Content Templates' or normalize-space()='Templates']]"
        )
        self.create_new_button = (
            By.XPATH,
            "//button[normalize-space()='Create New' or .//span[normalize-space()='Create New']]"
        )
        self.template_name_input = (By.XPATH, "//input[@name='template_name' or contains(@id,'template_name')]")
        self.create_button = (By.XPATH, "/html/body/div[2]/div[3]/div[3]/div/button[2]")
        
        # Dropdown Triggers
        self.registrant_dropdown_trigger = (By.XPATH, "//label[text()='Registrant']/following-sibling::div//div[@role='combobox']")
        self.filing_type_dropdown_trigger = (By.XPATH, "//label[text()='Filing Type']/following-sibling::div//div[@role='combobox']")
        self.style_template_dropdown_trigger = (By.XPATH, "//label[text()='Style Template']/following-sibling::div//div[@role='combobox']")
        
        self.generic_mui_listbox_container = (By.XPATH,
            "//div[contains(@class, 'MuiPopover-paper')]//ul[@role='listbox'] | //ul[contains(@class, 'MuiMenu-list') and @role='listbox'] | //ul[@role='listbox']"
        )
        
    def option_text_locator(self, text):
        return (By.XPATH, f"//li[normalize-space()='{text}']")

    def open_content_template_modal(self):
        try:
            tab = self.wait.until(EC.element_to_be_clickable(self.content_template_tab))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
            tab.click()
        except TimeoutException:
            self.driver.save_screenshot("content_templates_tab_timeout.png")
            raise

        try:
            create_btn = self.wait.until(EC.element_to_be_clickable(self.create_new_button))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", create_btn)
            create_btn.click()
            self.wait.until(EC.visibility_of_element_located(self.template_name_input))
        except TimeoutException:
            self.driver.save_screenshot("create_new_button_timeout.png")
            raise

    def fill_template_form(self, name):
        try:
            template_name_input_elem = self.wait.until(EC.presence_of_element_located(self.template_name_input))
            template_name_input_elem.send_keys(name)
        except TimeoutException:
            self.driver.save_screenshot("template_name_input_timeout.png")
            raise

        self._select_mui_dropdown(self.registrant_dropdown_trigger, "ABC Investments", "Registrant")
        self._select_mui_dropdown(self.filing_type_dropdown_trigger, "N-CSR", "Filing Type")
        
        try:
            self.wait.until(EC.element_to_be_clickable(self.style_template_dropdown_trigger))
            self._select_mui_dropdown(self.style_template_dropdown_trigger, "new", "Style Template")
        except TimeoutException:
            self.driver.save_screenshot("style_template_disabled_timeout.png")
            raise

    def _select_mui_dropdown(self, trigger_locator, option_text, field_name):
        try:
            trigger_element = self.wait.until(EC.element_to_be_clickable(trigger_locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", trigger_element)
            trigger_element.click()
            
            self.wait.until(EC.presence_of_element_located(self.generic_mui_listbox_container))
            self.wait.until(EC.visibility_of_element_located(self.generic_mui_listbox_container))
            
            option_element = self.wait.until(EC.element_to_be_clickable(self.option_text_locator(option_text)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
            option_element.click()
            
        except TimeoutException as e:
            self.driver.save_screenshot(f"{field_name.lower().replace(' ', '_')}_dropdown_timeout.png")
            raise
        except ElementClickInterceptedException:
            self.driver.save_screenshot(f"{field_name.lower().replace(' ', '_')}_dropdown_intercepted.png")
            raise

    def submit(self):
        try:
            create_button = self.wait.until(EC.element_to_be_clickable(self.create_button))
            self.driver.execute_script("arguments[0].click();", create_button)
        except TimeoutException:
            self.driver.save_screenshot("create_button_timeout.png")
            raise
