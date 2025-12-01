# tests/debug_form_structure.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_debug_form_structure(init_driver):
    """Анализ полной структуры формы входа"""
    driver = init_driver
    driver.get("https://excursium.com/Client/Login")
    
    print("=== ПОЛНЫЙ АНАЛИЗ ФОРМЫ ===")
    time.sleep(3)
    
    # Находим ВСЕ формы
    forms = driver.find_elements(By.TAG_NAME, "form")
    print(f"📋 Найдено форм: {len(forms)}")
    
    for i, form in enumerate(forms):
        print(f"\n🎯 Форма {i+1}:")
        print(f"   Классы: {form.get_attribute('class')}")
        print(f"   ID: {form.get_attribute('id')}")
        print(f"   Action: {form.get_attribute('action')}")
        
        # Все элементы внутри формы
        all_elements = form.find_elements(By.XPATH, ".//*")
        print(f"   Всего элементов в форме: {len(all_elements)}")
        
        for element in all_elements:
            tag = element.tag_name
            element_type = element.get_attribute('type')
            element_name = element.get_attribute('name')
            element_id = element.get_attribute('id')
            element_class = element.get_attribute('class')
            
            if tag in ['input', 'button', 'select', 'textarea']:
                print(f"     📦 {tag} | type: {element_type} | name: {element_name} | id: {element_id} | class: {element_class}")
    
    # Ищем скрытые поля
    print("\n🔍 Скрытые поля (type='hidden'):")
    hidden_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='hidden']")
    for field in hidden_fields:
        print(f"   🕵️ {field.get_attribute('name')} = {field.get_attribute('value')}")
    
    # Скриншот
    driver.save_screenshot("form_structure.png")
    print("📸 Скриншот сохранен: form_structure.png")