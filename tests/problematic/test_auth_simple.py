# tests/test_auth_simple.py
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_simple_login(init_driver):
    """Простой тест входа"""
    driver = init_driver
    
    # Прямой переход на страницу входа (минуя главную)
    driver.get("https://excursium.com/Client/Login")
    print("📄 Перешли прямо на страницу входа")
    time.sleep(3)
    
    # Заполняем форму
    email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
    
    # Быстро заполняем (как человек)
    email_field.send_keys("aleskobelev@tut.by")
    time.sleep(1)
    password_field.send_keys("34670Esk")
    time.sleep(1)
    
    print("✅ Данные заполнены")
    
    # Кликаем
    login_button.click()
    print("✅ Кнопка нажата")
    
    # Ждем
    time.sleep(5)
    
    # Проверяем результат
    current_url = driver.current_url
    print(f"📎 Текущий URL: {current_url}")
    
    if "/Client/Login" not in current_url:
        print("🎉 УСПЕХ! Вошли в систему!")
        assert True
    else:
        print("❌ Остались на странице входа")
        
        # Проверяем есть ли капча
        captcha_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'капч') or contains(text(), 'captcha') or contains(@class, 'captcha')]")
        if captcha_elements:
            print("🔍 Обнаружена капча! Нужно ручное вмешательство.")
        
        # Сохраняем скриншот для анализа
        driver.save_screenshot("login_issue.png")
        print("📸 Скриншот сохранен: login_issue.png")
        pytest.fail("Не удалось войти в систему")