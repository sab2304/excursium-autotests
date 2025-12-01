from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class RegistrationPage(BasePage):
    # Локаторы для полей формы
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
    NAME_FIELD = (By.CSS_SELECTOR, "input[name='name'], input[name='first_name'], #name")
    LAST_NAME_FIELD = (By.CSS_SELECTOR, "input[name='last_name'], input[name='surname']")
    PATRONYMIC_FIELD = (By.CSS_SELECTOR, "input[name='patronymic'], input[name='middle_name']")
    COMMENT_FIELD = (By.CSS_SELECTOR, "textarea[name='comment'], textarea[name='message']")
    PHONE_FIELD = (By.CSS_SELECTOR, "input[type='tel'], input[name='phone']")
    SEARCH_FIELD = (By.CSS_SELECTOR, "input[type='search']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .invalid-feedback, [class*='error']")
    
    def test_field_length_limits(self, field_locator, max_length, test_value):
        """Тестирует ограничение длины поля"""
        try:
            field = self.find_element(*field_locator)
            
            # Очищаем поле
            field.clear()
            
            # Пытаемся ввести значение длиннее максимального
            long_value = test_value * (max_length + 2)
            field.send_keys(long_value)
            
            # Получаем фактическое значение
            actual_value = field.get_attribute('value')
            actual_length = len(actual_value)
            
            print(f"📏 Поле: {field_locator[1]}")
            print(f"   Максимальная длина: {max_length}")
            print(f"   Введено символов: {len(long_value)}")
            print(f"   Фактически сохранено: {actual_length}")
            
            # Проверяем что длина не превышает максимальную
            if actual_length <= max_length:
                print(f"   ✅ Ограничение {max_length} символов работает")
                return True
            else:
                print(f"   ❌ Ограничение не работает: {actual_length} > {max_length}")
                return False
                
        except Exception as e:
            print(f"   ❌ Ошибка тестирования поля: {e}")
            return False
    
    def test_required_field(self, field_locator, field_name):
        """Тестирует обязательное поле"""
        try:
            field = self.find_element(*field_locator)
            
            # Проверяем атрибут required
            is_required = field.get_attribute('required')
            has_asterisk = self.driver.find_elements(By.XPATH, f"//label[contains(text(), '{field_name}')]//span[contains(text(), '*')]")
            
            print(f"🔴 Обязательное поле: {field_name}")
            print(f"   Атрибут required: {is_required}")
            print(f"   Знак * в label: {'есть' if has_asterisk else 'нет'}")
            
            return is_required is not None or len(has_asterisk) > 0
            
        except Exception as e:
            print(f"   ❌ Ошибка проверки обязательного поля: {e}")
            return False