from selenium.webdriver.common.by import By
from .base_page import BasePage

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = "https://excursium.com/"
    
    def open(self):
        self.driver.get(self.base_url)
        self.wait_for_page_load()
        return self
    
    def get_navigation_links(self):
        try:
            nav_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav, .navbar, .menu")
            all_links = []
            for nav in nav_elements:
                links = nav.find_elements(By.TAG_NAME, "a")
                for link in links:
                    if link.text.strip():
                        all_links.append((link.text.strip(), link.get_attribute('href')))
            return all_links
        except:
            return []