# tests/test_excursion_page_comprehensive.py
import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.regression
@pytest.mark.slow
def test_excursion_page_comprehensive(init_driver):
    """Комплексный тест страницы экскурсии"""
    driver = init_driver
    
    # 1. Переход на страницу
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    time.sleep(3)
    
    # 2. Проверка основных элементов
    assert "Третьяковской" in driver.title or "Третьяковск" in driver.title, "Заголовок должен содержать название экскурсии"
    
    # 3. Проверка наличия цен
    price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '₽')]")
    assert len(price_elements) > 0, "Должны отображаться цены"
    
    # 4. Проверка кнопки заказа
    order_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Заказать')]")
    assert len(order_buttons) > 0, "Должна быть кнопка заказа"
    assert order_buttons[0].is_enabled(), "Кнопка заказа должна быть доступна"
    
    # 5. Проверка информации о скидках
    discount_info = driver.find_elements(By.XPATH, "//*[contains(text(), 'скидк')]")
    assert len(discount_info) > 0, "Должна быть информация о скидках"
    
    # 6. Проверка интерактивных элементов
    interactive_elements = driver.find_elements(
        By.XPATH, 
        "//input[@type='checkbox'] | //input[@type='radio'] | //select"
    )
    assert len(interactive_elements) > 0, "Должны быть интерактивные элементы"
    
    print("✅ Комплексный тест страницы экскурсии пройден")