# pages/auth_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class AuthPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open_login_form(self):
        """Открытие формы входа с улучшенной обработкой ошибок"""
        try:
            # Ждем полной загрузки страницы
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            # Пробуем разные селекторы для кнопки входа
            login_selectors = [
                "//button[contains(text(), 'Вход')]",
                "//a[contains(text(), 'Вход')]",
                "//*[contains(@class, 'login')]",
                "//*[contains(text(), 'Вход')]"
            ]
            
            login_btn = None
            for selector in login_selectors:
                try:
                    login_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if login_btn:
                        break
                except TimeoutException:
                    continue
            
            if not login_btn:
                print("❌ Кнопка входа не найдена")
                return False
            
            # Скроллим к элементу и кликаем через JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
            self.driver.execute_script("arguments[0].click();", login_btn)
            
            # Ждем появления формы входа
            self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            
            print("✅ Форма входа открыта")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при открытии формы входа: {e}")
            return False
    
    def login(self, email, password):
        """Выполнение входа с улучшенной обработкой ошибок"""
        try:
            # Ждем появления полей формы
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Очищаем и заполняем поля
            email_field.clear()
            email_field.send_keys(email)
            password_field.clear()
            password_field.send_keys(password)
            
            # Ищем кнопку отправки
            submit_selectors = [
                "//button[@type='submit']",
                "//input[@type='submit']",
                "//button[contains(text(), 'Войти')]",
                "//input[contains(@value, 'Войти')]"
            ]
            
            submit_btn = None
            for selector in submit_selectors:
                try:
                    submit_btn = self.driver.find_element(By.XPATH, selector)
                    if submit_btn:
                        break
                except:
                    continue
            
            if submit_btn:
                self.driver.execute_script("arguments[0].click();", submit_btn)
                print("✅ Данные для входа отправлены")
                return True
            else:
                print("❌ Кнопка отправки не найдена")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при входе: {e}")
            return False
    
    def is_login_successful(self):
        """Проверка успешного входа"""
        try:
            # Ищем элементы, указывающие на успешный вход
            success_indicators = [
                "//*[contains(text(), 'Выйти')]",
                "//*[contains(text(), 'Выход')]",
                "//*[contains(@class, 'logout')]",
                "//*[contains(text(), 'aleskobelev')]"
            ]
            
            for indicator in success_indicators:
                try:
                    if self.driver.find_elements(By.XPATH, indicator):
                        print("✅ Вход выполнен успешно")
                        return True
                except:
                    continue
            
            print("❌ Признаки успешного входа не найдены")
            return False
            
        except Exception as e:
            print(f"❌ Ошибка при проверке входа: {e}")
            return False