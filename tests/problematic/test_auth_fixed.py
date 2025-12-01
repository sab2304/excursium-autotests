# tests/test_auth_fixed.py
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_fixed_login(init_driver):
    """Исправленный тест входа с правильной формой"""
    driver = init_driver
    
    # Прямой переход на страницу входа
    driver.get("https://excursium.com/Client/Login")
    print("📄 Перешли на страницу входа")
    time.sleep(3)
    
    try:
        # 1. Находим ПРАВИЛЬНУЮ форму входа (первую форму с кнопкой login-btn)
        login_form = driver.find_element(By.CSS_SELECTOR, "form.mt-5.mb-3")
        print("✅ Найдена форма входа")
        
        # 2. Находим элементы в этой форме
        email_field = login_form.find_element(By.CSS_SELECTOR, "input[type='email']")
        password_field = login_form.find_element(By.CSS_SELECTOR, "input[name='password']")
        login_button = login_form.find_element(By.ID, "login-btn")  # Используем ID кнопки!
        
        print("✅ Найдены все элементы формы")
        
        # 3. Заполняем форму
        email_field.clear()
        email_field.send_keys("aleskobelev@tut.by")
        time.sleep(1)
        
        password_field.clear() 
        password_field.send_keys("34670Esk")
        time.sleep(1)
        
        print("✅ Данные заполнены")
        
        # 4. Нажимаем кнопку Войти
        login_button.click()
        print("✅ Кнопка нажата")
        
        # 5. Ждем результат
        time.sleep(5)
        
        # 6. Проверяем результат
        current_url = driver.current_url
        print(f"📎 Текущий URL: {current_url}")
        
        if "/Client/Login" not in current_url:
            print("🎉 УСПЕХ! Вошли в систему!")
            assert True
        else:
            # Проверяем сообщение об ошибке
            try:
                error_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'Ошибка авторизации')]")
                print(f"❌ Ошибка: {error_msg.text}")
            except:
                print("⚠️  Остались на странице входа без явной ошибки")
            
            # Сохраняем скриншот для анализа
            driver.save_screenshot("login_fixed_issue.png")
            print("📸 Скриншот сохранен: login_fixed_issue.png")
            pytest.fail("Не удалось войти в систему")
            
    except Exception as e:
        print(f"💥 Ошибка: {e}")
        driver.save_screenshot("login_exception.png")
        pytest.fail(f"Тест упал с ошибкой: {e}")