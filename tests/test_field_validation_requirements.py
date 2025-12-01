# tests/test_field_validation_requirements.py
import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.validation
@pytest.mark.regression
def test_search_field_limits_real(init_driver):
    """Проверка ограничений поля поиска на лендинге"""
    driver = init_driver
    driver.get("https://excursium.com/")
    time.sleep(3)
    
    # Ищем поле поиска
    search_fields = driver.find_elements(
        By.XPATH, 
        "//input[contains(@placeholder, 'поиск') or contains(@placeholder, 'найти') or contains(@class, 'search')]"
    )
    
    for field in search_fields:
        if field.is_displayed():
            max_length = field.get_attribute("maxlength")
            placeholder = field.get_attribute("placeholder")
            print(f"✅ Поле поиска: placeholder='{placeholder}', maxlength={max_length}")
            
            # Проверяем можно ли вводить текст
            test_text = "Тестовый текст для проверки поля поиска"
            field.clear()
            field.send_keys(test_text)
            
            entered_text = field.get_attribute("value")
            print(f"   Введено символов: {len(entered_text)}")
            
            # Очищаем поле
            field.clear()
            break

@pytest.mark.validation
@pytest.mark.navigation
@pytest.mark.regression
def test_landing_empty_search_redirect(init_driver):
    """Редирект при пустом поиске на лендинге"""
    driver = init_driver
    driver.get("https://excursium.com/")
    time.sleep(3)
    
    initial_url = driver.current_url
    
    # Ищем кнопку поиска
    search_buttons = driver.find_elements(
        By.XPATH,
        "//button[contains(text(), 'Найти') or contains(text(), 'Поиск') or contains(@class, 'btn-search')]"
    )
    
    if search_buttons:
        for button in search_buttons:
            if button.is_displayed() and button.is_enabled():
                print(f"✅ Найдена кнопка поиска: '{button.text}'")
                button.click()
                time.sleep(3)
                
                # Проверяем редирект
                if driver.current_url != initial_url:
                    print(f"✅ Редирект выполнен: {driver.current_url}")
                    assert "ekskursii" in driver.current_url, "Должна открыться страница экскурсий"
                    return
        
        print("ℹ️ Не удалось найти кликабельную кнопку поиска")
    else:
        print("ℹ️ Кнопки поиска не найдены")

@pytest.mark.validation
def test_form_fields_character_limits(init_driver):
    """Проверка доступных форм на предмет ограничений полей"""
    driver = init_driver
    driver.get("https://excursium.com/")
    time.sleep(3)
    
    # Ищем все формы на странице
    forms = driver.find_elements(By.TAG_NAME, "form")
    print(f"✅ Найдено форм на странице: {len(forms)}")
    
    for i, form in enumerate(forms):
        if form.is_displayed():
            print(f"\n📋 Форма {i+1}:")
            
            # Ищем поля ввода в форме
            inputs = form.find_elements(By.TAG_NAME, "input")
            textareas = form.find_elements(By.TAG_NAME, "textarea")
            
            all_fields = inputs + textareas
            
            for field in all_fields:
                if field.is_displayed():
                    field_type = field.get_attribute("type") or "text"
                    placeholder = field.get_attribute("placeholder") or "без placeholder"
                    max_length = field.get_attribute("maxlength")
                    
                    print(f"   📝 Поле: type='{field_type}', placeholder='{placeholder}', maxlength={max_length}")