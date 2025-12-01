# tests/debug_login_page.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_debug_login_page(init_driver):
    """Диагностика страницы входа"""
    driver = init_driver
    
    # Переходим прямо на страницу входа
    driver.get("https://excursium.com/Client/Login")
    
    print("=== ДИАГНОСТИКА СТРАНИЦЫ ВХОДА ===")
    time.sleep(3)
    
    # 1. Ищем все поля ввода
    print("🔍 Все поля ввода на странице:")
    all_inputs = driver.find_elements(By.TAG_NAME, "input")
    for i, inp in enumerate(all_inputs):
        input_type = inp.get_attribute('type')
        input_name = inp.get_attribute('name')
        input_id = inp.get_attribute('id')
        input_placeholder = inp.get_attribute('placeholder')
        
        print(f"  {i+1}. type: '{input_type}', name: '{input_name}', id: '{input_id}', placeholder: '{input_placeholder}'")
    
    # 2. Ищем все кнопки
    print("\n🎯 Все кнопки на странице:")
    all_buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, btn in enumerate(all_buttons):
        print(f"  {i+1}. text: '{btn.text}', type: '{btn.get_attribute('type')}'")
    
    # 3. Ищем все формы
    print("\n📋 Все формы на странице:")
    all_forms = driver.find_elements(By.TAG_NAME, "form")
    for i, form in enumerate(all_forms):
        print(f"  Форма {i+1}:")
        print(f"    id: '{form.get_attribute('id')}'")
        print(f"    class: '{form.get_attribute('class')}'")
        print(f"    action: '{form.get_attribute('action')}'")
    
    # 4. Скриншот
    driver.save_screenshot("login_page_debug.png")
    print("📸 Скриншот сохранен: login_page_debug.png")
    
    print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")