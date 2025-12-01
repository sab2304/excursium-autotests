import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from pages.excursions_page import ExcursionsPage

class TestFinalReport:
    """Финальные тесты для отчёта"""
    
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(15)
        self.main_page = MainPage(self.driver)
        self.excursions_page = ExcursionsPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_01_main_page_availability(self):
        """ТЕСТ 1: Главная страница доступна"""
        assert self.main_page.open(), "Главная страница недоступна"
        assert "ЭкскурсиУм" in self.driver.title
        print("✅ ТЕСТ 1 ПРОЙДЕН: Главная страница доступна")

    def test_02_search_functionality(self):
        """ТЕСТ 2: Поиск экскурсий работает"""
        assert self.main_page.open(), "Главная страница недоступна"
        assert self.main_page.search_excursions("музей"), "Поиск не работает"
        print("✅ ТЕСТ 2 ПРОЙДЕН: Поиск экскурсий работает")

    def test_03_excursions_page_availability(self):
        """ТЕСТ 3: Страница экскурсий доступна"""
        assert self.excursions_page.open(), "Страница экскурсий недоступна"
        assert "ekskursii" in self.driver.current_url
        print("✅ ТЕСТ 3 ПРОЙДЕН: Страница экскурсий доступна")

    def test_04_excursions_displayed(self):
        """ТЕСТ 4: Экскурсии отображаются на странице"""
        assert self.excursions_page.open(), "Страница экскурсий недоступна"
        excursions_count = self.excursions_page.count_visible_excursions()
        assert excursions_count > 0, f"Не найдено экскурсий: {excursions_count}"
        print(f"✅ ТЕСТ 4 ПРОЙДЕН: Найдено {excursions_count} экскурсий")

    def test_05_filters_present(self):
        """ТЕСТ 5: Фильтры присутствуют на странице"""
        assert self.excursions_page.open(), "Страница экскурсий недоступна"
        assert self.excursions_page.are_filters_visible(), "Фильтры не видны"
        print("✅ ТЕСТ 5 ПРОЙДЕН: Фильтры присутствуют")

    def test_06_navigation_works(self):
        """ТЕСТ 6: Навигация между страницами работает"""
        assert self.main_page.open(), "Главная страница недоступна"
        assert self.main_page.go_to_excursions(), "Навигация не работает"
        assert "ekskursii" in self.driver.current_url
        print("✅ ТЕСТ 6 ПРОЙДЕН: Навигация работает")

    def test_07_basic_ui_elements(self):
        """ТЕСТ 7: Основные UI элементы присутствуют"""
        self.main_page.open()
        assert self.driver.title, "Заголовок страницы пустой"
        assert len(self.driver.page_source) > 10000, "Страница не загрузила достаточно контента"
        assert "экскурс" in self.driver.page_source.lower(), "На странице нет текста про экскурсии"
        print("✅ ТЕСТ 7 ПРОЙДЕН: Основные UI элементы присутствуют")

    def test_08_search_on_excursions_page(self):
        """ТЕСТ 8: Поиск на странице экскурсий работает"""
        assert self.excursions_page.open(), "Страница экскурсий недоступна"
        assert self.excursions_page.search_on_excursions_page("кремль"), "Поиск на странице экскурсий не работает"
        print("✅ ТЕСТ 8 ПРОЙДЕН: Поиск на странице экскурсий работает")