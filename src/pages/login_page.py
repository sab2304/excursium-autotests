from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def open(self, base_url="https://excursium.com/"):
        login_url = f"{base_url}Account/Login"
        self.driver.get(login_url)
        self.wait_for_page_load()
        return self
    
    def enter_email(self, email):
        selectors = ["input[type='email']", "input[name*='email']", "#Email"]
        for selector in selectors:
            try:
                self.type(By.CSS_SELECTOR, selector, email)
                return self
            except:
                continue
        raise Exception("Не удалось найти поле для ввода email")
    
    def enter_password(self, password):
        selectors = ["input[type='password']", "input[name*='password']", "#Password"]
        for selector in selectors:
            try:
                self.type(By.CSS_SELECTOR, selector, password)
                return self
            except:
                continue
        raise Exception("Не удалось найти поле для ввода пароля")