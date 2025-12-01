# tests/debug_after_login.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_debug_after_login(init_driver):
    """Диагностика что происходит после попытки входа"""
    driver = init_driver
    
    # Переходим прямо на страницу входа
    driver.get("https://excursium.com/Client/Login")
    
    print("=== ДИАГНОСТИКА ПОСЛЕ ВХОДА ===")
    time.sleep(2)
    
    # Заполняем форму
    login_form = driver.find_element(By.CSS_SELECTOR, "form.mt-5.mb-3")
    email_field = login_form.find_element(By.CSS_SELECTOR, "input[type='email']")
    password_field = login_form.find_element(By.CSS_SELECTOR, "input[name='password']")
    login_button = login_form.find_element(By.XPATH, ".//button[contains(text(), 'Войти')]")
    
    email_field.send_keys("aleskobelev@tut.by")
    password_field.send_keys("34670Esk")
    print("✅ Данные заполнены")
    
    # Нажимаем кнопку
    login_button.click()
    print("✅ Кнопка нажата")
    
    # Ждем и смотрим что произошло
    time.sleep(3)
    
    print(f"📎 URL после входа: {driver.current_url}")
    
    # Ищем сообщения об ошибках
    print("🔍 Ищем сообщения об ошибках:")
    error_messages = driver.find_elements(By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'alert') or contains(text(), 'неверн') or contains(text(), 'error')]")
    for msg in error_messages:
        if msg.is_displayed():
            print(f"  🚨 Сообщение об ошибке: '{msg.text}'")
    
    # Ищем любые сообщения на странице
    print("🔍 Ищем любые сообщения:")
    all_messages = driver.find_elements(By.XPATH, "//*[contains(@class, 'message') or contains(@class, 'alert') or contains(@class, 'info')]")
    for msg in all_messages:
        if msg.is_displayed() and msg.text.strip():
            print(f"  💬 Сообщение: '{msg.text}'")
    
    # Скриншот
    driver.save_screenshot("after_login_debug.png")
    print("📸 Скриншот сохранен: after_login_debug.png")
    
    print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")