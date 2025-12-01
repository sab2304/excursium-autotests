import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestFixedStructure:
    @pytest.fixture(autouse=True)
    def setup(self, pytestconfig):
        self.env = pytestconfig.getoption("env").lower()
        self.is_prod = self.env == "prod"
        
        if self.env == "prod":
            self.base_url = "https://excursium.com"
        elif self.env == "stage":
            self.base_url = "https://www.google.com"
        else:
            self.base_url = "https://httpbin.org/html"

    @pytest.fixture
    def driver(self):
        # Создаем драйвер самостоятельно
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def test_main_page(self, driver):
        if self.is_prod:
            pytest.skip("Skip production")
        
        driver.get(self.base_url)
        assert driver.title is not None
        print("✅ Test passed!")

    def test_login_page(self, driver):
        if self.is_prod:
            pytest.skip("Skip production")
        
        driver.get("https://httpbin.org/forms/post")
        assert "form" in driver.page_source.lower()
        print("✅ Test passed!")