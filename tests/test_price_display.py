# tests/test_price_display.py
import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.price
@pytest.mark.regression
def test_price_display(init_driver):
    """Тест отображения различных ценовых вариантов"""
    driver = init_driver
    
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Проверяем, что отображаются различные ценовые варианты
    price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '₽')]")
    meaningful_prices = []
    
    for elem in price_elements:
        text = elem.text.strip()
        if any(char.isdigit() for char in text) and len(text) < 100:
            meaningful_prices.append(text)
    
    # Проверяем, что есть несколько ценовых вариантов
    assert len(set(meaningful_prices)) >= 3, "Должно отображаться не менее 3 ценовых вариантов"
    
    # Проверяем, что есть информация о взрослых билетах
    adult_price_info = driver.find_elements(By.XPATH, "//*[contains(text(), 'взрослый')]")
    assert len(adult_price_info) > 0, "Должна быть информация о стоимости для взрослых"
    
    print("✅ Тест отображения цен пройден")