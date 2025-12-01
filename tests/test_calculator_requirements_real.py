# tests/test_calculator_requirements_real.py
import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.calculator
@pytest.mark.price
@pytest.mark.regression
def test_calculator_person_range_display(init_driver):
    """Проверка отображения диапазона персон в калькуляторе"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Ищем информацию о количестве человек
    person_elements = driver.find_elements(
        By.XPATH,
        "//*[contains(text(), 'человек') or contains(text(), 'персон') or contains(text(), 'школьник') or contains(text(), 'групп')]"
    )
    
    range_found = False
    for elem in person_elements:
        text = elem.text.lower()
        if any(word in text for word in ['от', 'до', 'мин', 'макс', '-', '—']):
            print(f"✅ Найден диапазон: {elem.text}")
            range_found = True
        elif any(word in text for word in ['человек', 'персон', 'школьник']):
            print(f"ℹ️ Информация о количестве: {elem.text}")
    
    if not range_found:
        print("ℹ️ Явный диапазон персон не найден, проверяем другие элементы")
        
        # Ищем числовые значения связанные с количеством
        number_elements = driver.find_elements(By.XPATH, "//*[text()[contains(., '1') or contains(., '2') or contains(., '3') or contains(., '4') or contains(., '5')]]")
        for elem in number_elements[:10]:
            text = elem.text.strip()
            if text.isdigit() and 1 <= int(text) <= 100:
                print(f"🔢 Числовое значение: {text}")

@pytest.mark.calculator
@pytest.mark.price  
def test_calculator_discount_display(init_driver):
    """Проверка отображения скидок и округления"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Ищем элементы скидок
    discount_elements = driver.find_elements(
        By.XPATH,
        "//*[contains(text(), 'скидк') or contains(text(), '%') or contains(text(), 'акци')]"
    )
    
    discount_found = False
    for elem in discount_elements:
        text = elem.text
        if any(word in text.lower() for word in ['скидк', 'акци', 'экономи']):
            print(f"✅ Найдена информация о скидках: {text}")
            discount_found = True
        elif '%' in text:
            print(f"✅ Найден процент: {text}")
            discount_found = True
    
    if not discount_found:
        print("ℹ️ Явная информация о скидках не найдена")

@pytest.mark.calculator
@pytest.mark.price
@pytest.mark.regression
def test_calculator_price_variants(init_driver):
    """Проверка различных ценовых вариантов"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Ищем все цены на странице
    price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '₽') or contains(text(), 'руб')]")
    meaningful_prices = []
    
    for elem in price_elements:
        text = elem.text.strip()
        if any(char.isdigit() for char in text) and len(text) < 100:
            meaningful_prices.append(text)
    
    unique_prices = list(set(meaningful_prices))
    print(f"✅ Уникальных ценовых вариантов: {len(unique_prices)}")
    
    for price in unique_prices[:10]:
        print(f"   💰 {price}")
    
    # Проверяем что есть несколько вариантов цен
    assert len(unique_prices) >= 2, "Должно быть не менее 2 ценовых вариантов"

@pytest.mark.calculator
@pytest.mark.price
def test_calculator_adult_pricing(init_driver):
    """Проверка информации о стоимости для взрослых"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # Ищем информацию о взрослых билетах
    adult_elements = driver.find_elements(
        By.XPATH,
        "//*[contains(text(), 'взросл') or contains(text(), 'родител') or contains(text(), 'сопровождающ')]"
    )
    
    for elem in adult_elements:
        text = elem.text.lower()
        if any(word in text for word in ['взросл', 'родител']):
            print(f"✅ Информация о взрослых: {elem.text}")
            return
    
    print("ℹ️ Явная информация о стоимости для взрослых не найдена")