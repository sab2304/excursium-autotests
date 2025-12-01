# tests/find_login.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_find_login_elements(init_driver):
    """Найдем ВСЕ возможные элементы для входа"""
    driver = init_driver
    driver.get("https://excursium.com")
    
    print("=== ПОИСК ВСЕХ ЭЛЕМЕНТОВ ДЛЯ ВХОДА ===")
    time.sleep(3)
    
    # 1. Все кликабельные элементы
    print("🎯 ВСЕ КЛИКАБЕЛЬНЫЕ ЭЛЕМЕНТЫ:")
    
    # Кнопки
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"Кнопки ({len(buttons)}):")
    for i, btn in enumerate(buttons):
        if btn.is_displayed():
            print(f"  🟢 {i+1}. '{btn.text}' | class: {btn.get_attribute('class')}")
        else:
            print(f"  🔴 {i+1}. '{btn.text}' | class: {btn.get_attribute('class')}")
    
    # Ссылки
    links = driver.find_elements(By.TAG_NAME, "a") 
    print(f"\nСсылки (первые 30 из {len(links)}):")
    for i, link in enumerate(links[:30]):
        text = link.text.strip()
        if text and len(text) < 100:
            href = link.get_attribute('href')
            print(f"  🔗 {i+1}. '{text}' -> {href}")
    
    # 2. Элементы с определенными классами
    auth_classes = ['login', 'auth', 'signin', 'user', 'account', 'enter', 'войти', 'вход']
    print(f"\n🔐 ЭЛЕМЕНТЫ С КЛАССАМИ АВТОРИЗАЦИИ:")
    for class_name in auth_classes:
        elements = driver.find_elements(By.XPATH, f"//*[contains(@class, '{class_name}')]")
        if elements:
            print(f"  Класс '{class_name}': {len(elements)} элементов")
            for el in elements[:5]:  # первые 5
                print(f"    - {el.tag_name}: '{el.text}'")
    
    # 3. Все инпуты (поля ввода)
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"\n📝 ПОЛЯ ВВОДА ({len(inputs)}):")
    for inp in inputs:
        input_type = inp.get_attribute('type')
        input_name = inp.get_attribute('name')
        input_placeholder = inp.get_attribute('placeholder')
        if input_name or input_placeholder:
            print(f"  📦 type: {input_type}, name: {input_name}, placeholder: {input_placeholder}")
    
    # 4. Скриншот
    driver.save_screenshot("login_elements.png")
    print("📸 Скриншот сохранен: login_elements.png")
    
    print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")