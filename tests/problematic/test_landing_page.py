import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLandingPage:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        self.driver.quit()

    def test_landing_page_loads(self):
        """Тест загрузки лендинг страницы"""
        self.driver.get("https://excursium.com")
        
        # Проверяем основные элементы
        assert "ЭкскурсиУм" in self.driver.title
        assert self.driver.find_element(By.TAG_NAME, "body").is_displayed()
        print("✅ Лендинг страница загружена")

    def test_search_field_present(self):
        """Тест наличия поля поиска на лендинге"""
        self.driver.get("https://excursium.com")
        
        # Ищем поле поиска (может быть input или button)
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='экскурс']", 
            ".search-field",
            "[class*='search']"
        ]
        
        search_found = False
        for selector in search_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    search_found = True
                    break
            except:
                continue
                
        assert search_found, "Поле поиска не найдено на лендинге"
        print("✅ Поле поиска присутствует на лендинге")

    def test_empty_search_redirect(self):
        """Тест редиректа при пустом поиске"""
        self.driver.get("https://excursium.com")
        
        # Пробуем найти и нажать кнопку поиска
        search_buttons = [
            "button[type='submit']",
            ".search-btn", 
            "button:contains('Найти')",
            "input[type='submit']"
        ]
        
        for selector in search_buttons:
            try:
                button = self.driver.find_element(By.CSS_SELECTOR, selector)
                button.click()
                time.sleep(3)
                
                # Проверяем редирект на страницу экскурсий
                if "ekskursii" in self.driver.current_url or "list" in self.driver.current_url:
                    print("✅ Редирект на страницу экскурсий при пустом поиске")
                    return
            except:
                continue
        
        # Если кнопка не найдена, проверяем есть ли редирект по умолчанию
        if "ekskursii" in self.driver.current_url:
            print("✅ Автоматический редирект на страницу экскурсий")
        else:
            pytest.fail("Редирект на страницу экскурсий не произошел")

    def test_navigation_links(self):
        """Тест навигационных ссылок"""
        self.driver.get("https://excursium.com")
        
        # Проверяем основные навигационные ссылки
        nav_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
        assert len(nav_links) > 0, "Навигационные ссылки не найдены"
        
        working_links = 0
        for link in nav_links[:5]:  # Проверяем первые 5 ссылок
            try:
                href = link.get_attribute('href')
                if href and 'excursium.com' in href:
                    working_links += 1
            except:
                continue
                
        assert working_links > 0, "Нет рабочих навигационных ссылок"
        print(f"✅ Найдено {working_links} рабочих навигационных ссылок")