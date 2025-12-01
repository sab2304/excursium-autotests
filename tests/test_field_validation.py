# tests/test_field_validation.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

class TestFieldValidation:
    def test_find_registration_form(self, init_driver):
        """Поиск формы регистрации на странице"""
        self.driver = init_driver
        self.driver.get("https://excursium.com")
        print("🔍 Ищем форму регистрации...")
        
        try:
            # Ждем загрузки страницы
            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            # Ищем все формы
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            print(f"📋 Найдено форм на странице: {len(forms)}")
            
            # Ищем индикаторы формы регистрации
            reg_indicators = [
                "//form[contains(@action, 'register')]",
                "//form[contains(@class, 'register')]",
                "//form[.//input[contains(@name, 'email')]]",
                "//*[contains(text(), 'Регистрация')]/ancestor-or-self::form",
                "//*[contains(text(), 'Зарегистрироваться')]/ancestor-or-self::form"
            ]
            
            found_forms = []
            for indicator in reg_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    if elements:
                        found_forms.extend(elements)
                        print(f"✅ Найдена форма по селектору: {indicator}")
                except Exception as e:
                    print(f"⚠️ Ошибка с селектором {indicator}: {e}")
                    continue
            
            # Выводим информацию о найденных формах
            if forms or found_forms:
                all_forms = list(set(forms + found_forms))  # Убираем дубликаты
                print(f"📄 Всего уникальных форм: {len(all_forms)}")
                
                for i, form in enumerate(all_forms):
                    print(f"\n📄 Форма {i+1}:")
                    print(f"   ID: {form.get_attribute('id') or 'нет'}")
                    print(f"   Class: {form.get_attribute('class') or 'нет'}")
                    print(f"   Action: {form.get_attribute('action') or 'нет'}")
                    print(f"   Method: {form.get_attribute('method') or 'нет'}")
                    
                    # Ищем поля внутри формы
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    print(f"   Поля ввода: {len(inputs)}")
                    for inp in inputs:
                        input_type = inp.get_attribute("type")
                        input_name = inp.get_attribute("name")
                        print(f"     - type: {input_type}, name: {input_name}")
            else:
                print("❌ Формы не найдены на странице")
                
            # Дополнительно ищем кнопки регистрации
            reg_buttons = [
                "//button[contains(text(), 'Регистрация')]",
                "//a[contains(text(), 'Регистрация')]",
                "//*[contains(@class, 'register')]"
            ]
            
            for button_selector in reg_buttons:
                try:
                    buttons = self.driver.find_elements(By.XPATH, button_selector)
                    if buttons:
                        print(f"🎯 Найдена кнопка регистрации: {button_selector}")
                except:
                    continue
                
        except Exception as e:
            print(f"❌ Ошибка при поиске форм: {e}")
            pytest.fail(f"Ошибка при поиске форм: {e}")
    
    def test_search_field_limits(self, init_driver):
        """Тестирование ограничений поля поиска"""
        self.driver = init_driver
        self.driver.get("https://excursium.com")
        print("🔍 Тест поля поиска:")
        
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Разные селекторы для поля поиска
            search_selectors = [
                "//input[@type='search']",
                "//input[contains(@class, 'search')]",
                "//input[contains(@placeholder, 'поиск')]",
                "//input[contains(@placeholder, 'search')]",
                "//input[@name='search']",
                "//input[@id='search']"
            ]
            
            search_field = None
            for selector in search_selectors:
                try:
                    search_field = self.driver.find_element(By.XPATH, selector)
                    if search_field and search_field.is_displayed():
                        print(f"✅ Найдено поле поиска: {selector}")
                        break
                except:
                    continue
            
            if not search_field:
                print("⏭️ Поле поиска не найдено")
                pytest.skip("Поле поиска не найдено")
            
            # Тестируем ввод длинного текста
            long_text = "A" * 1000
            search_field.clear()
            search_field.send_keys(long_text)
            
            # Получаем фактическое значение
            actual_value = search_field.get_attribute("value")
            print(f"   Попытка ввести: {len(long_text)} символов")
            print(f"   Фактически введено: {len(actual_value)} символов")
            
            # Проверяем, что поле приняло ввод
            assert len(actual_value) > 0, "Поле поиска не приняло ввод"
            print("✅ Поле поиска обработало длинный запрос")
            
        except Exception as e:
            print(f"❌ Ошибка теста поля поиска: {e}")
            pytest.fail(f"Тест поля поиска не удался: {e}")