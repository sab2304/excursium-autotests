# tests/test_auth.py
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestAuthentication:
    def test_successful_login(self, init_driver):
        """Тест успешного входа в систему"""
        driver = init_driver
        driver.get("https://excursium.com")
        
        print("🔐 Тестируем авторизацию: aleskobelev@tut.by")
        
        try:
            # Ждем загрузки главной страницы
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 1. Находим и кликаем на кнопку-человечка
            user_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/header/nav/div/ul/li[4]/a"))
            )
            print("✅ Найдена кнопка-человечек")
            user_icon.click()
            
            # 2. Ждем загрузки новой страницы входа
            print("⏳ Ждем загрузки страницы входа...")
            WebDriverWait(driver, 10).until(
                EC.url_contains("/Client/Login")
            )
            print("✅ Страница входа загружена")
            
            # 3. Находим форму входа - берем ПЕРВУЮ форму с классом 'mt-5 mb-3'
            login_form = driver.find_element(By.CSS_SELECTOR, "form.mt-5.mb-3")
            print("✅ Найдена форма входа")
            
            # 4. Находим поля ВНУТРИ этой формы (используем более гибкие селекторы)
            email_field = login_form.find_element(By.CSS_SELECTOR, "input[type='email']")
            password_field = login_form.find_element(By.CSS_SELECTOR, "input[name='password']")
            
            # Ищем кнопку по содержимому текста (contains text)
            login_button = login_form.find_element(By.XPATH, ".//button[contains(text(), 'Войти')]")
            
            print("✅ Найдены все элементы формы")
            
            # 5. Заполняем поля
            email_field.clear()
            email_field.send_keys("aleskobelev@tut.by")
            
            password_field.clear()
            password_field.send_keys("34670Esk")
            print("✅ Данные для входа заполнены")
            
            # 6. Нажимаем кнопку "Войти"
            login_button.click()
            print("✅ Нажата кнопка входа")
            
            # 7. Ждем результат входа
            time.sleep(3)
            
            # 8. Проверяем успешность входа
            current_url = driver.current_url
            print(f"📎 URL после входа: {current_url}")
            
            # Если вернулись на главную - вход успешен
            if current_url == "https://excursium.com/" or "Login" not in current_url:
                print("✅ Авторизация прошла успешно - вернулись на главную страницу")
            else:
                # Ищем сообщение об успехе на странице
                try:
                    success_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Войти как') or contains(text(), 'skobelev')]")
                    if success_message.is_displayed():
                        print("✅ Найдено сообщение об успешном входе")
                    else:
                        pytest.fail("Не удалось подтвердить успешную авторизацию")
                except:
                    pytest.fail("Не удалось подтвердить успешную авторизацию")
                
        except Exception as e:
            print(f"❌ Ошибка в тесте авторизации: {e}")
            driver.save_screenshot("login_error.png")
            print("📸 Скриншот ошибки сохранен: login_error.png")
            pytest.fail(f"Тест авторизации не пройден: {e}")
    
    def test_login_form_elements(self, init_driver):
        """Тест элементов формы входа"""
        driver = init_driver
        
        # Переходим прямо на страницу входа для теста
        driver.get("https://excursium.com/Client/Login")
        
        try:
            # Ждем загрузки страницы входа
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 1. Находим форму входа
            login_form = driver.find_element(By.CSS_SELECTOR, "form.mt-5.mb-3")
            print("✅ Найдена форма входа")
            
            # 2. Находим элементы ВНУТРИ формы
            email_field = login_form.find_element(By.CSS_SELECTOR, "input[type='email']")
            password_field = login_form.find_element(By.CSS_SELECTOR, "input[name='password']")
            login_button = login_form.find_element(By.XPATH, ".//button[contains(text(), 'Войти')]")
            
            # 3. Проверяем что элементы отображаются
            assert email_field.is_displayed(), "Поле email не отображается"
            assert password_field.is_displayed(), "Поле password не отображается"
            assert login_button.is_displayed(), "Кнопка 'Войти' не отображается"
            
            print("✅ Все обязательные элементы формы входа найдены и отображаются")
            
        except Exception as e:
            print(f"❌ Ошибка в тесте элементов формы: {e}")
            driver.save_screenshot("form_elements_error.png")
            print("📸 Скриншот ошибки сохранен: form_elements_error.png")
            pytest.fail(f"Тест элементов формы не пройден: {e}")