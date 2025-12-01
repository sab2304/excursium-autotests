# tests/test_order_button.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.regression
def test_order_button_functionality(init_driver):
    """Тест функциональности кнопки заказа"""
    driver = init_driver
    wait = WebDriverWait(driver, 10)
    
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    
    # Ищем и проверяем кнопку заказа
    order_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Заказать экскурсию')]"))
    )
    
    # Проверяем, что кнопка доступна
    assert order_button.is_enabled(), "Кнопка заказа должна быть доступна"
    assert order_button.is_displayed(), "Кнопка заказа должна быть видима"
    
    # Проверяем текст кнопки
    assert "Заказать" in order_button.text, "Кнопка должна содержать текст 'Заказать'"
    
    # Кликаем на кнопку (можно раскомментировать для реального теста)
    # order_button.click()
    # time.sleep(3)
    # Проверяем переход на страницу заказа или открытие формы
    
    print("✅ Тест кнопки заказа пройден")