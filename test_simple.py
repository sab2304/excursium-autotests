import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestSimple:
    def setup_method(self):
        # Ручная настройка драйвера без плагинов
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)

    def teardown_method(self):
        self.driver.quit()

    def test_google(self):
        self.driver.get("https://www.google.com")
        assert "Google" in self.driver.title
        print("✅ Google test passed!")

    def test_example(self):
        self.driver.get("https://example.com")
        assert "Example" in self.driver.title
        print("✅ Example test passed!")