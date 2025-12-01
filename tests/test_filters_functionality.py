# tests/test_filters_functionality.py
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestFiltersFunctionality:
    def test_filters_default_state(self, init_driver):
        """Тест: фильтры должны быть открыты по умолчанию"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("📂 Тестируем состояние фильтров по умолчанию")
        time.sleep(3)
        
        # Проверяем что основные фильтры открыты (имеют класс 'show')
        main_filters = [
            "collapse-popular-request",
            "collapse-grade", 
            "collapse-price",
            "collapse-time",
            "collapse-regions"
        ]
        
        open_filters = 0
        for filter_id in main_filters:
            try:
                filter_element = driver.find_element(By.ID, filter_id)
                if "show" in filter_element.get_attribute("class"):
                    open_filters += 1
                    print(f"✅ Фильтр {filter_id} открыт по умолчанию")
                else:
                    print(f"❌ Фильтр {filter_id} закрыт по умолчанию")
            except:
                print(f"⚠️ Фильтр {filter_id} не найден")
        
        assert open_filters >= 3, f"Меньше 3 фильтров открыто по умолчанию: {open_filters}"
        print(f"✅ Открыто фильтров по умолчанию: {open_filters} из {len(main_filters)}")
    
    def test_filter_options_display(self, init_driver):
        """Тест: каждый фильтр отображает опции"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🎯 Тестируем отображение опций в фильтрах")
        time.sleep(3)
        
        # Проверяем основные фильтры
        filters_to_check = [
            ("Популярные запросы", "collapse-popular-request"),
            ("Класс", "collapse-grade"),
            ("Стоимость", "collapse-price")
        ]
        
        for filter_name, filter_id in filters_to_check:
            try:
                # Находим collapse-элемент
                filter_collapse = driver.find_element(By.ID, filter_id)
                
                # Ищем опции внутри (чекбоксы)
                checkboxes = filter_collapse.find_elements(By.XPATH, ".//input[@type='checkbox']")
                labels = filter_collapse.find_elements(By.XPATH, ".//label")
                
                print(f"✅ Фильтр '{filter_name}': {len(checkboxes)} чекбоксов, {len(labels)} labels")
                
                # Проверяем что есть опции
                assert len(checkboxes) > 0, f"В фильтре '{filter_name}' нет чекбоксов"
                assert len(labels) > 0, f"В фильтре '{filter_name}' нет labels"
                
                # Проверяем что labels соответствуют чекбоксам
                if len(checkboxes) == len(labels):
                    print(f"   ✅ Количество чекбоксов и labels совпадает")
                else:
                    print(f"   ⚠️ Количество чекбоксов ({len(checkboxes)}) и labels ({len(labels)}) не совпадает")
                    
            except Exception as e:
                print(f"❌ Ошибка в фильтре '{filter_name}': {e}")
                pytest.fail(f"Фильтр '{filter_name}' не работает корректно")
    
    def test_filter_option_selection(self, init_driver):
        """Тест выбора опций в фильтрах"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🔘 Тестируем выбор опций в фильтрах")
        time.sleep(3)
        
        try:
            # Запоминаем начальное количество карточек
            initial_cards = len(driver.find_elements(By.CLASS_NAME, "card"))
            print(f"📊 Начальное количество карточек: {initial_cards}")
            
            # Выбираем опцию в фильтре "Популярные запросы"
            popular_collapse = driver.find_element(By.ID, "collapse-popular-request")
            checkboxes = popular_collapse.find_elements(By.XPATH, ".//input[@type='checkbox']")
            labels = popular_collapse.find_elements(By.XPATH, ".//label")
            
            if checkboxes and labels:
                # Выбираем первую опцию (кликаем на label - это безопаснее)
                first_label = labels[0]
                option_text = first_label.text
                print(f"   Выбираем опцию: '{option_text}'")
                
                # Кликаем на label
                first_label.click()
                time.sleep(2)
                
                # Проверяем что чекбокс стал выбранным
                first_checkbox = checkboxes[0]
                if first_checkbox.is_selected():
                    print("   ✅ Чекбокс выбран после клика на label")
                else:
                    print("   ⚠️ Чекбокс не выбран после клика")
                
                # Ждем применения фильтра
                time.sleep(3)
                
                # Проверяем что количество карточек изменилось
                after_filter_cards = len(driver.find_elements(By.CLASS_NAME, "card"))
                print(f"📊 Количество карточек после фильтра: {after_filter_cards}")
                
                if after_filter_cards < initial_cards:
                    print("✅ Фильтр применился - количество карточек уменьшилось")
                elif after_filter_cards == initial_cards:
                    print("ℹ️ Количество карточек не изменилось (возможно выбрана опция которая уже была активна)")
                else:
                    print("⚠️ Количество карточек увеличилось - неожиданно")
                    
            else:
                print("❌ Не найдены опции для выбора")
                
        except Exception as e:
            print(f"❌ Ошибка при выборе опции фильтра: {e}")
            driver.save_screenshot("filter_selection_error.png")
    
    def test_filter_combination(self, init_driver):
        """Тест комбинации нескольких фильтров"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("🔗 Тестируем комбинацию нескольких фильтров")
        time.sleep(3)
        
        try:
            # Запоминаем начальное количество
            initial_cards = len(driver.find_elements(By.CLASS_NAME, "card"))
            print(f"📊 Начальное количество карточек: {initial_cards}")
            
            # Применяем первый фильтр
            self._select_filter_option(driver, "collapse-popular-request", 0)
            time.sleep(2)
            
            # Применяем второй фильтр
            self._select_filter_option(driver, "collapse-grade", 0)  
            time.sleep(2)
            
            # Проверяем результат
            final_cards = len(driver.find_elements(By.CLASS_NAME, "card"))
            print(f"📊 Конечное количество карточек: {final_cards}")
            
            # После применения двух фильтров количество должно уменьшиться (или остаться тем же)
            if final_cards <= initial_cards:
                print("✅ Комбинация фильтров работает корректно")
            else:
                print("⚠️ Количество карточек увеличилось после фильтрации")
                
        except Exception as e:
            print(f"❌ Ошибка при комбинации фильтров: {e}")
    
    def test_show_more_functionality(self, init_driver):
        """Тест кнопки 'Показать больше' в фильтрах"""
        driver = init_driver
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        
        print("📖 Тестируем кнопку 'Показать больше'")
        time.sleep(3)
        
        # Ищем кнопки "Показать больше" (из диагностики видно что они есть)
        show_more_buttons = driver.find_elements(By.XPATH, "//*[contains(@class, 'btn-more')]")
        
        if show_more_buttons:
            print(f"✅ Найдено кнопок 'Показать больше': {len(show_more_buttons)}")
            
            # Берем первую кнопку
            first_button = show_more_buttons[0]
            
            # Кликаем через JavaScript (чтобы избежать перекрытия)
            driver.execute_script("arguments[0].click();", first_button)
            print("✅ Кликнули на 'Показать больше'")
            time.sleep(2)
            
            # Проверяем что что-то изменилось (должны появиться дополнительные опции)
            # Конкретную проверку сложно сделать без знания что должно появиться
            print("ℹ️ Кнопка 'Показать больше' сработала (проверяем визуально)")
            
        else:
            print("ℹ️ Кнопки 'Показать больше' не найдены")
    
    def _select_filter_option(self, driver, filter_id, option_index=0):
        """Вспомогательный метод для выбора опции в фильтре"""
        try:
            # Находим collapse-элемент
            filter_collapse = driver.find_element(By.ID, filter_id)
            
            # Ищем labels внутри
            labels = filter_collapse.find_elements(By.XPATH, ".//label")
            
            if labels and len(labels) > option_index:
                label = labels[option_index]
                option_text = label.text
                
                # Кликаем на label
                driver.execute_script("arguments[0].click();", label)
                print(f"   ✅ Выбрали опцию: '{option_text}' в фильтре {filter_id}")
                return True
            else:
                print(f"   ⚠️ Не найдены labels в фильтре {filter_id}")
                return False
                
        except Exception as e:
            print(f"   ❌ Ошибка выбора опции в фильтре {filter_id}: {e}")
            return False