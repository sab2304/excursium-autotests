# tests/debug_filters.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_debug_filters_structure(init_driver):
    """Диагностика реальной структуры и поведения фильтров"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    
    print("=== ДИАГНОСТИКА ФИЛЬТРОВ ===")
    time.sleep(3)
    
    # 1. Ищем все кнопки фильтров и их структуру
    print("🔍 СТРУКТУРА КНОПОК ФИЛЬТРОВ:")
    filter_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'accordion-button')]")
    print(f"Найдено accordion-кнопок: {len(filter_buttons)}")
    
    for i, btn in enumerate(filter_buttons):
        print(f"\n🎯 Кнопка {i+1}:")
        print(f"   Текст: '{btn.text}'")
        print(f"   Классы: '{btn.get_attribute('class')}'")
        print(f"   data-bs-target: '{btn.get_attribute('data-bs-target')}'")
        print(f"   aria-expanded: '{btn.get_attribute('aria-expanded')}'")
        print(f"   aria-controls: '{btn.get_attribute('aria-controls')}'")
    
    # 2. Ищем collapse-элементы (контент фильтров)
    print("\n📂 СТРУКТУРА КОНТЕНТА ФИЛЬТРОВ:")
    collapse_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'collapse')]")
    print(f"Найдено collapse-элементов: {len(collapse_elements)}")
    
    for i, collapse in enumerate(collapse_elements):
        print(f"\n📦 Collapse {i+1}:")
        print(f"   ID: '{collapse.get_attribute('id')}'")
        print(f"   Классы: '{collapse.get_attribute('class')}'")
        print(f"   Отображается: {collapse.is_displayed()}")
        
        # Смотрим что внутри collapse
        inner_elements = collapse.find_elements(By.XPATH, ".//*")
        print(f"   Элементов внутри: {len(inner_elements)}")
        
        # Показываем типы элементов внутри
        element_types = {}
        for elem in inner_elements[:10]:  # первые 10
            tag = elem.tag_name
            element_types[tag] = element_types.get(tag, 0) + 1
        
        print(f"   Типы элементов: {element_types}")
    
    # 3. Проверяем состояние фильтров по умолчанию
    print("\n🎚️ СОСТОЯНИЕ ФИЛЬТРОВ ПО УМОЛЧАНИЮ:")
    for i, btn in enumerate(filter_buttons[:3]):  # первые 3
        aria_expanded = btn.get_attribute('aria-expanded')
        print(f"   Фильтр '{btn.text}': aria-expanded='{aria_expanded}'")
        
        # Находим соответствующий collapse
        target_id = btn.get_attribute('data-bs-target')
        if target_id and target_id.startswith('#'):
            target_id = target_id[1:]  # убираем #
            try:
                target_element = driver.find_element(By.ID, target_id)
                print(f"     Collapse отображается: {target_element.is_displayed()}")
                print(f"     Collapse классы: '{target_element.get_attribute('class')}'")
            except:
                print(f"     Collapse не найден: {target_id}")
    
    # 4. Тестируем клик на одну кнопку и смотрим изменения
    print("\n🧪 ТЕСТИРУЕМ КЛИК НА ФИЛЬТР:")
    if filter_buttons:
        first_btn = filter_buttons[0]
        print(f"Кликаем на: '{first_btn.text}'")
        
        # Состояние до клика
        before_expanded = first_btn.get_attribute('aria-expanded')
        target_id = first_btn.get_attribute('data-bs-target')
        
        print(f"До клика: aria-expanded='{before_expanded}'")
        if target_id:
            target_id = target_id[1:]
            target_before = driver.find_element(By.ID, target_id)
            print(f"До клика: collapse отображается={target_before.is_displayed()}")
        
        # Кликаем
        driver.execute_script("arguments[0].click();", first_btn)
        time.sleep(2)
        
        # Состояние после клика
        after_expanded = first_btn.get_attribute('aria-expanded')
        print(f"После клика: aria-expanded='{after_expanded}'")
        
        if target_id:
            target_after = driver.find_element(By.ID, target_id)
            print(f"После клика: collapse отображается={target_after.is_displayed()}")
            
            # Смотрим что внутри после открытия
            if target_after.is_displayed():
                options = target_after.find_elements(By.XPATH, ".//input[@type='checkbox'] | .//label | .//a")
                print(f"Опций найдено: {len(options)}")
                for opt in options[:3]:  # первые 3 опции
                    print(f"   - {opt.tag_name}: text='{opt.text}'")
    
    # 5. Скриншот
    driver.save_screenshot("filters_debug.png")
    print("📸 Скриншот сохранен: filters_debug.png")
    
    print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")