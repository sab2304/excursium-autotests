from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, locator)))
    
    def click(self, by, locator):
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()
    
    def type(self, by, locator, text):
        element = self.find_element(by, locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, by, locator):
        element = self.find_element(by, locator)
        return element.text
    
    def is_visible(self, by, locator, timeout=5):
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException:
            return False
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_title(self):
        return self.driver.title
    
    def wait_for_page_load(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")