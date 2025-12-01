import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from pages.excursions_page import ExcursionsPage

class TestFunctional:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(15)
        self.main_page = MainPage(self.driver)
        self.excursions_page = ExcursionsPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_main_page_functionality(self):
        """Тест функциональности главной страницы"""
        # 1. Открываем главную
        assert self.main_page.open(), "Не удалось открыть главную страницу"
        assert "ЭкскурсиУм" in self.driver.title
        print("✅ Главная страница загружена")
        
        # 2. Проверяем поле поиска
        assert self.main_page.is_element_present(*self.main_page.SEARCH_INPUT), "Поле поиска не найдено"
        print("✅ Поле поиска присутствует")
        
        # 3. Тестируем поиск
        assert self.main_page.search_excursions("музей"), "Поиск не сработал"
        assert "музей" in self.driver.page_source.lower() or "search" in self.driver.current_url
        print("✅ Поиск работает")

    def test_excursions_page_functionality(self):
        """Тест функциональности страницы экскурсий"""
        # 1. Прямой переход на экскурсии
        assert self.excursions_page.open(), "Не удалось открыть страницу экскурсий"
        assert "ekskursii" in self.driver.current_url
        print("✅ Страница экскурсий загружена")
        
        # 2. Проверяем что есть экскурсии
        excursions_count = self.excursions_page.count_visible_excursions()
        assert excursions_count > 0, f"Не найдено экскурсий, найдено: {excursions_count}"
        print(f"✅ Найдено {excursions_count} экскурсий")
        
        # 3. Проверяем фильтры
        assert self.excursions_page.are_filters_visible(), "Фильтры не видны"
        print("✅ Фильтры присутствуют")

    def test_navigation_between_pages(self):
        """Тест навигации между страницами"""
        # 1. Главная → Экскурсии (пробуем найти ссылку)
        assert self.main_page.open(), "Не удалось открыть главную"
        
        if self.main_page.go_to_excursions():
            assert "ekskursii" in self.driver.current_url
            print("✅ Навигация с главной на экскурсии работает через ссылку")
        else:
            # Если ссылка не найдена, используем прямой URL
            print("⚠️  Ссылка не найдена, используем прямой переход")
            assert self.main_page.go_to_excursions_direct(), "Не удалось перейти на экскурсии"
            assert "ekskursii" in self.driver.current_url
            print("✅ Прямой переход на экскурсии работает")
        
        # 2. Экскурсии → Поиск
        assert self.excursions_page.search_on_excursions_page("кремль"), "Поиск на странице экскурсий не работает"
        assert "кремль" in self.driver.page_source.lower()
        print("✅ Поиск на странице экскурсий работает")

    def test_basic_ui_elements(self):
        """Тест основных UI элементов"""
        self.main_page.open()
        
        # Проверяем основные элементы
        assert self.driver.title, "Заголовок страницы пустой"
        assert len(self.driver.page_source) > 10000, "Страница не загрузила достаточно контента"
        assert "экскурс" in self.driver.page_source.lower(), "На странице нет текста про экскурсии"
        
        print("✅ Основные UI элементы присутствуют")