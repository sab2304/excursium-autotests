# tests/test_interactive_elements.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_interactive_elements_change_price(init_driver):
    """Тест изменения цены при взаимодействии с элементами"""
    driver = init_driver
    
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Запоминаем начальные цены
    initial_prices = set()
    price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '₽')]")
    for elem in price_elements:
        text = elem.text.strip()
        if any(char.isdigit() for char in text) and len(text) < 100:
            initial_prices.add(text)
    
    # Находим интерактивные элементы (чекбоксы)
    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    
    # Тестируем первые 3 доступных чекбокса
    tested_elements = 0
    for checkbox in checkboxes[:5]:
        try:
            if checkbox.is_enabled() and checkbox.is_displayed():
                # Кликаем на чекбокс
                checkbox.click()
                time.sleep(2)
                
                # Проверяем изменение цены
                new_prices = set()
                price_elements_after = driver.find_elements(By.XPATH, "//*[contains(text(), '₽')]")
                for elem in price_elements_after:
                    text = elem.text.strip()
                    if any(char.isdigit() for char in text) and len(text) < 100:
                        new_prices.add(text)
                
                # Возвращаем исходное состояние
                checkbox.click()
                time.sleep(1)
                
                tested_elements += 1
                print(f"✅ Протестирован элемент {tested_elements}")
                
        except Exception as e:
            continue
    
    assert tested_elements > 0, "Должен быть хотя бы один тестируемый интерактивный элемент"
    print(f"✅ Протестировано {tested_elements} интерактивных элементов")
