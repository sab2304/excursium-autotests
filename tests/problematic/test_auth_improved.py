# tests/test_auth_improved.py
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
            # Ждем полной загрузки главной страницы
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)  # Дополнительная пауза
            
            # 1. Находим и кликаем на кнопку-человечка
            user_icon = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/header/nav/div/ul/li[4]/a"))
            )
            print("✅ Найдена кнопка-человечек")
            user_icon.click()
            time.sleep(2)
            
            # 2. Ждем загрузки страницы входа
            print("⏳ Ждем загрузки страницы входа...")
            WebDriverWait(driver, 15).until(
                EC.url_contains("/Client/Login")
            )
            print("✅ Страница входа загружена")
            time.sleep(2)
            
            # 3. Находим форму входа
            login_form = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "form.mt-5.mb-3"))
            )
            print("✅ Найдена форма входа")
            
            # 4. Находим поля ВНУТРИ формы
            email_field = login_form.find_element(By.CSS_SELECTOR, "input[type='email']")
            password_field = login_form.find_element(By.CSS_SELECTOR, "input[name='password']")
            login_button = login_form.find_element(By.XPATH, ".//button[contains(text(), 'Войти')]")
            
            print("✅ Найдены все элементы формы")
            
            # 5. Очищаем поля и заполняем ОЧЕНЬ МЕДЛЕННО (как человек)
            email_field.clear()
            time.sleep(0.5)
            for char in "aleskobelev@tut.by":
                email_field.send_keys(char)
                time.sleep(0.1)  # Имитируем ввод человека
            
            password_field.clear()
            time.sleep(0.5)
            for char in "34670Esk":
                password_field.send_keys(char)
                time.sleep(0.1)  # Имитируем ввод человека
            
            print("✅ Данные для входа заполнены (медленно)")
            
            # 6. Ждем и нажимаем кнопку
            time.sleep(1)
            login_button.click()
            print("✅ Нажата кнопка входа")
            
            # 7. Ждем результат входа (дольше)
            print("⏳ Ждем обработки входа...")
            time.sleep(5)
            
            # 8. Проверяем успешность входа разными способами
            current_url = driver.current_url
            print(f"📎 Текущий URL: {current_url}")
            
            # Если остались на странице входа, проверяем ошибку
            if "/Client/Login" in current_url:
                try:
                    error_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'Ошибка авторизации')]")
                    print(f"❌ Ошибка авторизации: '{error_msg.text}'")
                    pytest.fail("Ошибка авторизации")
                except:
                    print("⚠️  Остались на странице входа, но ошибки не найдено")
                    # Возможно нужна дополнительная проверка (капча и т.д.)
                    pytest.fail("Не удалось войти - остались на странице входа")
            else:
                print("✅ УСПЕХ! Ушли со страницы входа!")
                
                # Проверяем что мы на главной или в ЛК
                if "excursium.com" in current_url and "Login" not in current_url:
                    print("✅ Авторизация прошла успешно!")
                else:
                    print(f"✅ Перешли на: {current_url}")
                    
        except Exception as e:
            print(f"❌ Ошибка в тесте авторизации: {e}")
            driver.save_screenshot("login_error_improved.png")
            print("📸 Скриншот ошибки сохранен: login_error_improved.png")
            pytest.fail(f"Тест авторизации не пройден: {e}")