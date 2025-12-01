# tests/test_excursions_filters.py
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestExcursionsFilters:
    def test_excursions_page_loads(self, init_driver):
        """Тест загрузки страницы экскурсий"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🏞️ Тестируем загрузку страницы экскурсий")
        
        # Ждем загрузки
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        assert "экскурс" in driver.title.lower()
        print("✅ Страница экскурсий загружена")
    
    def test_filters_section_displayed(self, init_driver):
        """Тест отображения секции фильтров"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🔧 Тестируем отображение фильтров")
        
        time.sleep(3)
        
        # Ищем aside с фильтрами (как показала диагностика)
        try:
            filters_aside = driver.find_element(By.TAG_NAME, "aside")
            assert filters_aside.is_displayed()
            print("✅ Секция фильтров (aside) найдена и отображается")
            
            # Проверяем что в aside есть текст "Фильтр"
            filter_text = filters_aside.find_element(By.XPATH, ".//*[contains(text(), 'Фильтр')]")
            print("✅ Текст 'Фильтр' найден в секции")
            
        except Exception as e:
            print(f"❌ Секция фильтров не найдена: {e}")
            pytest.fail("Секция фильтров не найдена на странице")
    
    def test_filter_buttons_exist(self, init_driver):
        """Тест наличия кнопок фильтров"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🎯 Тестируем кнопки фильтров")
        
        time.sleep(3)
        
        # Кнопки которые должны быть (из диагностики)
        expected_buttons = ["Популярные запросы", "Класс", "Стоимость", "Продолжительность", "Место проведения"]
        
        found_buttons = []
        for button_text in expected_buttons:
            try:
                button = driver.find_element(By.XPATH, f"//button[contains(text(), '{button_text}')]")
                if button.is_displayed():
                    found_buttons.append(button_text)
                    print(f"✅ Кнопка '{button_text}' найдена")
            except:
                print(f"⚠️ Кнопка '{button_text}' не найдена")
        
        # Проверяем что найдены хотя бы некоторые кнопки
        assert len(found_buttons) > 0, "Не найдено ни одной кнопки фильтра"
        print(f"✅ Найдено кнопок фильтров: {len(found_buttons)} из {len(expected_buttons)}")
    
    def test_excursion_cards_displayed(self, init_driver):
        """Тест отображения карточек экскурсий"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🎴 Тестируем отображение карточек экскурсий")
        
        time.sleep(3)
        
        # Ищем карточки экскурсий (как показала диагностика)
        try:
            cards = driver.find_elements(By.CLASS_NAME, "card")
            assert len(cards) > 0, "Карточки не найдены"
            
            # Проверяем что хотя бы некоторые карточки отображаются
            displayed_cards = [card for card in cards if card.is_displayed()]
            assert len(displayed_cards) > 0, "Нет отображаемых карточек"
            
            print(f"✅ Найдено карточек: {len(cards)}")
            print(f"✅ Отображаемых карточек: {len(displayed_cards)}")
            
        except Exception as e:
            print(f"❌ Ошибка при поиске карточек: {e}")
            pytest.fail("Карточки экскурсий не найдены")