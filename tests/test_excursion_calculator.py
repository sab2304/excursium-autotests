# tests/test_excursion_calculator.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_excursion_calculator(init_driver):
    """Тестирование калькулятора стоимости экскурсии"""
    driver = init_driver
    wait = WebDriverWait(driver, 10)
    
    # Переходим на конкретную страницу экскурсии
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    print("📄 Перешли на страницу экскурсии")
    
    # Ждем загрузки страницы
    time.sleep(3)
    
    # 1. Ищем и кликаем на кнопку "Рассчитать"
    try:
        calculate_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Рассчитать')]"))
        )
        calculate_button.click()
        print("✅ Нажали кнопку 'Рассчитать'")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Не удалось найти кнопку 'Рассчитать': {e}")
        # Пробуем альтернативные селекторы
        try:
            calculate_button = driver.find_element(By.XPATH, "//button[contains(., 'Рассчитать')]")
            calculate_button.click()
            print("✅ Нажали кнопку 'Рассчитать' (альтернативный селектор)")
            time.sleep(2)
        except:
            print("❌ Кнопка 'Рассчитать' не найдена")
    
    # 2. Ищем поля для ввода данных
    print("\n🔍 Поиск полей ввода:")
    
    # Ищем все возможные поля ввода
    input_fields = driver.find_elements(By.TAG_NAME, "input")
    select_fields = driver.find_elements(By.TAG_NAME, "select")
    textareas = driver.find_elements(By.TAG_NAME, "textarea")
    
    print(f"📝 Найдено input полей: {len(input_fields)}")
    print(f"📝 Найдено select полей: {len(select_fields)}")
    print(f"📝 Найдено textarea: {len(textareas)}")
    
    # Анализируем input поля
    for i, field in enumerate(input_fields):
        field_type = field.get_attribute("type")
        placeholder = field.get_attribute("placeholder")
        name = field.get_attribute("name")
        id_attr = field.get_attribute("id")
        
        print(f"  Input {i+1}: type='{field_type}', placeholder='{placeholder}', name='{name}', id='{id_attr}'")
    
    # 3. Пробуем найти и заполнить поля
    print("\n🔄 Попытка заполнения полей:")
    
    # Пробуем найти поле для количества человек
    person_selectors = [
        "//input[contains(@placeholder, 'человек')]",
        "//input[contains(@placeholder, 'персон')]",
        "//input[contains(@name, 'person')]",
        "//input[contains(@name, 'count')]",
        "//input[@type='number']"
    ]
    
    for selector in person_selectors:
        try:
            person_field = driver.find_element(By.XPATH, selector)
            person_field.clear()
            person_field.send_keys("15")
            print(f"✅ Заполнили поле количества человек: {selector}")
            break
        except:
            continue
    
    # 4. Ищем поле для класса/возраста
    class_selectors = [
        "//input[contains(@placeholder, 'класс')]",
        "//input[contains(@placeholder, 'возраст')]",
        "//select[contains(@name, 'class')]",
        "//select[contains(@name, 'age')]"
    ]
    
    for selector in class_selectors:
        try:
            class_field = driver.find_element(By.XPATH, selector)
            if class_field.tag_name == "select":
                # Для select выбираем первый вариант
                from selenium.webdriver.support.ui import Select
                select = Select(class_field)
                if len(select.options) > 1:
                    select.select_by_index(1)
                    print(f"✅ Выбрали вариант в select: {selector}")
            else:
                class_field.send_keys("5")
                print(f"✅ Заполнили поле класса: {selector}")
            break
        except:
            continue
    
    # 5. Ищем поле для локации
    location_selectors = [
        "//input[contains(@placeholder, 'школ')]",
        "//input[contains(@placeholder, 'адрес')]",
        "//input[contains(@placeholder, 'location')]"
    ]
    
    for selector in location_selectors:
        try:
            location_field = driver.find_element(By.XPATH, selector)
            location_field.send_keys("Москва")
            print(f"✅ Заполнили поле локации: {selector}")
            break
        except:
            continue
    
    # 6. Проверяем результат расчета
    print("\n💰 Проверка результата:")
    
    # Ищем элементы с ценами
    price_selectors = [
        "//*[contains(text(), 'руб')]",
        "//*[contains(text(), '₽')]",
        "//*[contains(@class, 'price')]",
        "//*[contains(@class, 'cost')]"
    ]
    
    for selector in price_selectors:
        price_elements = driver.find_elements(By.XPATH, selector)
        if price_elements:
            print(f"✅ Найдены элементы с ценами ({selector}): {len(price_elements)}")
            for elem in price_elements[:3]:
                if elem.text.strip():
                    print(f"   - '{elem.text}'")
    
    # 7. Делаем скриншот
    driver.save_screenshot("calculator_test_result.png")
    print("📸 Скриншот сохранен: calculator_test_result.png")
    
    print("\n✅ ТЕСТ ЗАВЕРШЕН")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])