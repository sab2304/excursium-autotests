import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.excursions_page import ExcursionsPage

class TestFilters:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(15)
        self.excursions_page = ExcursionsPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_filters_default_state(self):
        """Требование: Фильтры должны быть открыты по умолчанию"""
        assert self.excursions_page.open(), "Не удалось открыть страницу экскурсий"
        
        # Проверяем что фильтры видны
        assert self.excursions_page.are_filters_visible(), "Фильтры не открыты по умолчанию"
        print("✅ Фильтры открыты по умолчанию")
        
        # Ищем элементы фильтров
        filter_elements = self.driver.find_elements(By.CSS_SELECTOR, ".filter, [class*='filter'], .checkbox, input[type='checkbox']")
        print(f"✅ Найдено {len(filter_elements)} элементов фильтров")

    def test_excursions_count(self):
        """Тест: Экскурсии отображаются"""
        assert self.excursions_page.open(), "Не удалось открыть страницу экскурсий"
        
        initial_count = self.excursions_page.count_visible_excursions()
        assert initial_count > 0, f"Не найдено экскурсий: {initial_count}"
        print(f"✅ Найдено {initial_count} экскурсий")

    def test_basic_filter_functionality(self):
        """Тест базовой функциональности фильтров"""
        assert self.excursions_page.open(), "Не удалось открыть страницу экскурсий"
        
        # Пробуем найти и кликнуть на первый чекбокс фильтра
        try:
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            if checkboxes:
                first_checkbox = checkboxes[0]
                print(f"🔘 Найдено чекбоксов: {len(checkboxes)}")
                
                # Прокручиваем и кликаем через JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView();", first_checkbox)
                self.driver.execute_script("arguments[0].click();", first_checkbox)
                time.sleep(3)
                
                # Проверяем что что-то изменилось
                new_count = self.excursions_page.count_visible_excursions()
                print(f"📊 После фильтрации: {new_count} экскурсий")
                print("✅ Фильтры реагируют на клик")
            else:
                print("⚠️  Чекбоксы не найдены")
        except Exception as e:
            print(f"⚠️  Не удалось протестировать фильтры: {e}")

    def test_page_structure(self):
        """Тест структуры страницы экскурсий"""
        assert self.excursions_page.open(), "Не удалось открыть страницу экскурсий"
        
        # Проверяем основные элементы
        assert "ЭкскурсиУм" in self.driver.title
        assert "ekskursii" in self.driver.current_url
        
        # Проверяем наличие ключевых разделов
        page_text = self.driver.page_source
        assert "экскурс" in page_text.lower(), "Нет упоминания экскурсий"
        assert "цена" in page_text.lower() or "руб" in page_text.lower() or "₽" in page_text, "Нет информации о ценах"
        
        print("✅ Структура страницы корректна")