# tests/test_excursion_calculator_v2.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_excursion_calculator_v2(init_driver):
    """Тестирование калькулятора стоимости экскурсии через фильтры"""
    driver = init_driver
    wait = WebDriverWait(driver, 10)
    
    # Переходим на конкретную страницу экскурсии
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    print("📄 Перешли на страницу экскурсии")
    
    # Ждем загрузки страницы
    time.sleep(3)
    
    # 1. Ищем основной калькулятор/форму
    print("\n🔍 Поиск калькулятора:")
    
    # Ищем контейнеры с ценами и калькулятором
    calculator_selectors = [
        "//div[contains(@class, 'calculator')]",
        "//div[contains(@class, 'price')]",
        "//div[contains(@class, 'cost')]",
        "//form[contains(@class, 'calculator')]",
        "//section[contains(@class, 'price')]"
    ]
    
    for selector in calculator_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ Найден элемент калькулятора: {selector}")
            for elem in elements:
                print(f"   - {elem.get_attribute('class')}: {elem.text[:200]}...")
    
    # 2. Работаем с фильтрами классов (grade)
    print("\n🎒 Работа с фильтрами классов:")
    
    # Ищем чекбоксы классов (1-11 класс)
    grade_checkboxes = []
    for i in range(1, 12):
        try:
            checkbox = driver.find_element(By.ID, f"btn-check-c{i}")
            grade_checkboxes.append(checkbox)
            print(f"✅ Найден чекбокс класса {i}")
        except:
            continue
    
    # Выбираем конкретный класс (например, 5 класс)
    if grade_checkboxes:
        try:
            grade_5 = driver.find_element(By.ID, "btn-check-c5")
            if not grade_5.is_selected():
                grade_5.click()
                print("✅ Выбрали 5 класс")
                time.sleep(1)
        except Exception as e:
            print(f"❌ Не удалось выбрать класс: {e}")
    
    # 3. Ищем элементы для количества человек
    print("\n👥 Поиск элементов количества:")
    
    # Ищем кнопки/селекторы для количества
    quantity_selectors = [
        "//button[contains(@class, 'counter')]",
        "//div[contains(@class, 'quantity')]",
        "//input[contains(@class, 'counter')]",
        "//*[contains(@class, 'person')]",
        "//*[contains(text(), 'человек')]/following::input",
        "//*[contains(text(), 'персон')]/following::input"
    ]
    
    for selector in quantity_selectors:
        try:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                print(f"✅ Найдены элементы количества: {selector} - {len(elements)} шт.")
                for elem in elements[:2]:
                    print(f"   - {elem.tag_name}: {elem.get_attribute('class')}")
        except:
            pass
    
    # 4. Ищем и взаимодействуем с элементами увеличения/уменьшения количества
    print("\n🔢 Взаимодействие с счетчиками:")
    
    # Ищем кнопки +/-
    plus_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '+')]")
    minus_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '-')]")
    
    print(f"✅ Найдено кнопок '+': {len(plus_buttons)}")
    print(f"✅ Найдено кнопок '-': {len(minus_buttons)}")
    
    # Пробуем нажать на кнопки увеличения
    for i, button in enumerate(plus_buttons[:3]):
        try:
            button.click()
            print(f"✅ Нажали кнопку '+' #{i+1}")
            time.sleep(0.5)
        except:
            print(f"❌ Не удалось нажать кнопку '+' #{i+1}")
    
    # 5. Проверяем обновление цены
    print("\n💰 Проверка обновления цены:")
    
    # Ждем возможного обновления цены
    time.sleep(2)
    
    # Ищем обновленные цены
    price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'руб') or contains(text(), '₽')]")
    print(f"✅ Найдено элементов с ценами: {len(price_elements)}")
    
    # Выводим уникальные цены
    unique_prices = set()
    for elem in price_elements:
        text = elem.text.strip()
        if text and any(char.isdigit() for char in text):
            unique_prices.add(text)
    
    print("📊 Уникальные цены на странице:")
    for price in list(unique_prices)[:10]:  # Показываем первые 10
        print(f"   - {price}")
    
    # 6. Ищем итоговую стоимость
    print("\n💎 Поиск итоговой стоимости:")
    
    total_selectors = [
        "//*[contains(text(), 'Итог')]",
        "//*[contains(text(), 'Всего')]",
        "//*[contains(text(), 'Общая')]",
        "//*[contains(@class, 'total')]",
        "//*[contains(@class, 'final')]"
    ]
    
    for selector in total_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ Найдены элементы итога ({selector}):")
            for elem in elements[:2]:
                print(f"   - {elem.text}")
    
    # 7. Ищем кнопку бронирования/заказа
    print("\n📦 Поиск кнопки бронирования:")
    
    booking_buttons = driver.find_elements(By.XPATH, 
        "//button[contains(text(), 'Забронировать') or contains(text(), 'Заказать') or contains(text(), 'Оформить')]")
    
    print(f"✅ Найдено кнопок бронирования: {len(booking_buttons)}")
    for button in booking_buttons[:2]:
        print(f"   - {button.text}")
    
    # 8. Делаем детальный скриншот
    driver.save_screenshot("calculator_detailed_result.png")
    print("📸 Детальный скриншот сохранен: calculator_detailed_result.png")
    
    # 9. Сохраняем HTML страницы для анализа
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("💾 Исходный код страницы сохранен: page_source.html")
    
    print("\n✅ ТЕСТ ЗАВЕРШЕН")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])