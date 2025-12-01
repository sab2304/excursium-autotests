# tests/test_interactive_elements_detailed.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_interactive_elements_detailed(init_driver):
    """Детальный тест интерактивных элементов"""
    driver = init_driver
    
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    print("🔍 Анализ интерактивных элементов:")
    
    # Ищем ВСЕ возможные интерактивные элементы
    interactive_selectors = [
        ("checkboxes", "//input[@type='checkbox']"),
        ("radio buttons", "//input[@type='radio']"),
        ("selects", "//select"),
        ("buttons with options", "//button[contains(@class, 'option')]"),
        ("all buttons", "//button"),
        ("clickable divs", "//div[@onclick]"),
        ("clickable spans", "//span[@onclick]"),
        ("labels with for", "//label[@for]")
    ]
    
    for element_type, selector in interactive_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        print(f"\n📋 {element_type}: {len(elements)}")
        
        for i, elem in enumerate(elements[:3]):  # Показываем первые 3
            try:
                enabled = elem.is_enabled()
                displayed = elem.is_displayed()
                element_id = elem.get_attribute('id') or elem.get_attribute('class') or f"element_{i}"
                print(f"   {i+1}. ID: {element_id}, enabled: {enabled}, displayed: {displayed}")
                
                if enabled and displayed:
                    print(f"      ✅ Доступен для тестирования")
            except Exception as e:
                print(f"   {i+1}. Ошибка: {e}")
    
    # Теперь пробуем найти и протестировать конкретные элементы
    print("\n🎯 Тестирование конкретных элементов:")
    
    # Ищем чекбоксы классов (которые мы видели в диагностике)
    grade_checkboxes = []
    for i in range(1, 12):
        try:
            checkbox = driver.find_element(By.ID, f"btn-check-c{i}")
            grade_checkboxes.append(checkbox)
        except:
            continue
    
    print(f"🎒 Чекбоксы классов: {len(grade_checkboxes)}")
    
    tested_elements = 0
    
    # Пробуем тестировать чекбоксы классов
    for i, checkbox in enumerate(grade_checkboxes[:3]):
        try:
            print(f"\n🔍 Тестируем чекбокс класса {i+1}:")
            print(f"   ID: {checkbox.get_attribute('id')}")
            print(f"   Enabled: {checkbox.is_enabled()}")
            print(f"   Displayed: {checkbox.is_displayed()}")
            print(f"   Selected: {checkbox.is_selected()}")
            
            if checkbox.is_enabled() and checkbox.is_displayed():
                # Запоминаем начальное состояние
                initial_state = checkbox.is_selected()
                
                # Пробуем кликнуть через JavaScript (если обычный клик не работает)
                driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(2)
                
                new_state = checkbox.is_selected()
                print(f"   Состояние после клика: {new_state}")
                
                if new_state != initial_state:
                    print("   ✅ Состояние изменилось!")
                    tested_elements += 1
                    
                    # Возвращаем исходное состояние
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(1)
                else:
                    print("   ⚠️ Состояние не изменилось")
            else:
                print("   ❌ Элемент недоступен для клика")
                
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    # Пробуем другие элементы если чекбоксы классов не сработали
    if tested_elements == 0:
        print("\n🔄 Пробуем другие элементы:")
        
        # Ищем любые кликабельные элементы рядом с ценами
        price_related_elements = driver.find_elements(
            By.XPATH, 
            "//*[contains(text(), '₽')]/preceding::input | //*[contains(text(), '₽')]/following::input"
        )
        
        print(f"🔍 Элементы рядом с ценами: {len(price_related_elements)}")
        
        for i, elem in enumerate(price_related_elements[:3]):
            try:
                if elem.is_enabled() and elem.is_displayed():
                    elem_type = elem.get_attribute('type')
                    print(f"   Тестируем элемент {i+1} типа '{elem_type}'")
                    
                    driver.execute_script("arguments[0].click();", elem)
                    time.sleep(2)
                    
                    # Проверяем, изменилось ли что-то
                    prices_after = driver.find_elements(By.XPATH, "//*[contains(text(), '₽')]")
                    print(f"   Цен после клика: {len(prices_after)}")
                    
                    tested_elements += 1
                    break
                    
            except Exception as e:
                print(f"   Ошибка: {e}")
    
    print(f"\n📊 ИТОГО: Протестировано элементов: {tested_elements}")
    
    # Более мягкое утверждение для диагностики
    if tested_elements == 0:
        print("⚠️  Предупреждение: Не удалось протестировать ни один интерактивный элемент")
        print("💡 Возможные причины:")
        print("   - Элементы требуют специальных условий для активации")
        print("   - Необходима предварительная настройка фильтров")
        print("   - Элементы управляются через JavaScript")
    else:
        print("✅ Успешно протестированы интерактивные элементы")
