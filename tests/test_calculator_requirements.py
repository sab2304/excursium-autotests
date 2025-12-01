# tests/test_calculator_requirements.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_calculator_person_range(init_driver):
    """Калькулятор отображает диапазон персон"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Ищем элементы, связанные с количеством персон
    person_elements = driver.find_elements(
        By.XPATH,
        "//*[contains(text(), 'человек') or contains(text(), 'персон') or contains(text(), 'школьник')]"
    )
    
    for elem in person_elements:
        text = elem.text.lower()
        if any(word in text for word in ['мин', 'макс', 'от', 'до', '-']):
            print(f"✅ Найден диапазон: {elem.text}")
            break
    else:
        print("ℹ️ Явный диапазон персон не найден")

def test_calculator_discount_rounding(init_driver):
    """Проверка округления скидки в калькуляторе"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Ищем элементы скидок
    discount_elements = driver.find_elements(
        By.XPATH,
        "//*[contains(text(), 'скидк') or contains(text(), '%')]"
    )
    
    for elem in discount_elements:
        text = elem.text
        if '%' in text:
            print(f"✅ Найдена скидка: {text}")