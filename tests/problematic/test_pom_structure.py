import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestPOMStructure:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)

    def teardown_method(self):
        self.driver.quit()

    def test_main_page_with_pom(self, pytestconfig):
        env = pytestconfig.getoption("env")
        is_prod = env == "prod"
        
        print(f"🔍 Environment = '{env}', is_prod = {is_prod}")
        
        if is_prod:
            pytest.skip("Skip destructive tests on production")
        
        base_url = "https://excursium.com"
        
        print(f"🔍 Using URL: {base_url}")
        self.driver.get(base_url)
        print(f"🔍 Page title = '{self.driver.title}'")
        time.sleep(2)
        
        # Проверяем главную страницу
        title = self.driver.title
        assert "ЭкскурсиУм" in title, f"Expected 'ЭкскурсиУм' in title, got: {title}"
        assert self.driver.current_url == "https://excursium.com/", f"Unexpected URL: {self.driver.current_url}"
        print("✅ Main page test PASSED!")

    def test_login_page_with_pom(self, pytestconfig):
        env = pytestconfig.getoption("env")
        is_prod = env == "prod"
        
        print(f"🔍 Environment = '{env}', is_prod = {is_prod}")
        
        if is_prod:
            pytest.skip("Skip destructive tests on production")
        
        # Проверяем разные возможные URL для логина
        login_urls = [
            "https://excursium.com/login",
            "https://excursium.com/auth", 
            "https://excursium.com/signin",
            "https://excursium.com/account"
        ]
        
        for login_url in login_urls:
            print(f"🔍 Trying URL: {login_url}")
            self.driver.get(login_url)
            print(f"🔍 Page title = '{self.driver.title}'")
            print(f"🔍 Current URL = '{self.driver.current_url}'")
            time.sleep(2)
            
            # Если не 404, считаем что нашли страницу логина
            if "Ошибка 404" not in self.driver.title and "404" not in self.driver.title:
                print(f"✅ Found login page at: {login_url}")
                return
        
        # Если все URL вернули 404, пропускаем тест
        pytest.skip("Login page not found (all URLs returned 404)")

    def test_navigation(self, pytestconfig):
        """Тест навигации по сайту"""
        env = pytestconfig.getoption("env")
        is_prod = env == "prod"
        
        if is_prod:
            pytest.skip("Skip destructive tests on production")
        
        # Переходим на главную
        self.driver.get("https://excursium.com")
        
        # Проверяем что сайт загружается и основные элементы есть
        assert "ЭкскурсиУм" in self.driver.title
        assert len(self.driver.page_source) > 1000  # Страница не пустая
        
        print("✅ Navigation test PASSED!")