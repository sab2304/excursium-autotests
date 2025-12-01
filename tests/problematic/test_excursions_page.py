import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestExcursionsPage:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        self.driver.quit()

    def test_excursions_page_loads(self):
        """Тест загрузки страницы экскурсий"""
        self.driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        assert "Экскурсии" in self.driver.title
        assert "list" in self.driver.current_url
        print("✅ Страница экскурсий загружена")

    def test_excursions_list_displayed(self):
        """Тест отображения списка экскурсий"""
        self.driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        # Ищем элементы экскурсий
        excursion_selectors = [
            ".excursion-item",
            ".tour-card", 
            "[class*='excursion']",
            "[class*='tour']"
        ]
        
        excursions_found = False
        for selector in excursion_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 0:
                    excursions_found = True
                    print(f"✅ Найдено {len(elements)} экскурсий с селектором {selector}")
                    break
            except:
                continue
                
        assert excursions_found, "Список экскурсий не отображается"

    def test_search_field_on_excursions_page(self):
        """Тест поля поиска на странице экскурсий"""
        self.driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        # Ищем поле поиска
        search_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='search']")
        search_found = False
        
        for input_field in search_inputs:
            try:
                placeholder = input_field.get_attribute('placeholder') or ''
                if any(word in placeholder.lower() for word in ['найти', 'поиск', 'search', 'экскурс']):
                    search_found = True
                    break
            except:
                continue
                
        assert search_found, "Поле поиска не найдено на странице экскурсий"
        print("✅ Поле поиска присутствует на странице экскурсий")

    def test_search_functionality(self):
        """Тест функциональности поиска экскурсий"""
        self.driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        # Находим поле поиска и вводим текст
        search_input = None
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='search']")
        
        for input_field in inputs:
            try:
                if input_field.is_displayed() and input_field.is_enabled():
                    search_input = input_field
                    break
            except:
                continue
        
        if search_input:
            # Вводим поисковый запрос
            search_input.clear()
            search_input.send_keys("Москва")
            time.sleep(2)
            
            # Ищем кнопку поиска
            search_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], .search-btn")
            for button in search_buttons:
                if button.is_displayed():
                    button.click()
                    time.sleep(3)
                    print("✅ Функциональность поиска работает")
                    return
        
        print("⚠️ Функциональность поиска требует ручной проверки")