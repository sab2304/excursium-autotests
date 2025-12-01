# tests/debug_excursion_page.py
import pytest
from selenium.webdriver.common.by import By
import time

@pytest.mark.debug
@pytest.mark.slow
def test_debug_excursion_page(init_driver):
    """Диагностика страницы конкретной экскурсии"""
    driver = init_driver
    
    # Переходим на страницу экскурсий и кликаем на первую
    driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    print("🏞️ Перешли на страницу экскурсий")
    time.sleep(3)
    
    # Находим и кликаем на первую карточку экскурсии
    try:
        first_card = driver.find_element(By.CLASS_NAME, "card")
        card_link = first_card.find_element(By.TAG_NAME, "a")
        card_url = card_link.get_attribute("href")
        print(f"🔗 URL первой экскурсии: {card_url}")
        
        # Переходим на страницу экскурсии
        driver.get(card_url)
        print("📄 Перешли на страницу экскурсии")
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Не удалось перейти на страницу экскурсии: {e}")
        # Если не получилось, используем дефолтный URL для тестирования
        driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/poznavatelnyy-kvest-po-muzeyu-kosmonavtiki")
        print("📄 Используем тестовую страницу экскурсии")
        time.sleep(3)
    
    # Анализ страницы
    print("\n🔍 АНАЛИЗ СТРАНИЦЫ ЭКСКУРСИИ:")
    
    # 1. Заголовок и URL
    print(f"📄 Заголовок: {driver.title}")
    print(f"🌐 URL: {driver.current_url}")
    
    # 2. Ищем калькулятор
    print("\n🧮 ПОИСК КАЛЬКУЛЯТОРА:")
    calculator_selectors = [
        "//*[contains(@class, 'calculator')]",
        "//*[contains(@class, 'price')]",
        "//*[contains(text(), 'Цена')]",
        "//*[contains(text(), 'Стоимость')]",
        "//*[contains(text(), 'Рассчитать')]"
    ]
    
    for selector in calculator_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ '{selector}': {len(elements)} элементов")
            for elem in elements[:2]:
                print(f"   - {elem.tag_name}: '{elem.text[:100]}...'")
    
    # 3. Ищем поля ввода для количества персон
    print("\n👥 ПОИСК ПОЛЕЙ ДЛЯ ПЕРСОН:")
    person_selectors = [
        "//input[@type='number']",
        "//input[contains(@placeholder, 'человек')]",
        "//input[contains(@placeholder, 'персон')]",
        "//*[contains(text(), 'человек')]",
        "//*[contains(text(), 'персон')]"
    ]
    
    for selector in person_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ '{selector}': {len(elements)} элементов")
            for elem in elements:
                print(f"   - {elem.tag_name}: placeholder='{elem.get_attribute('placeholder')}', value='{elem.get_attribute('value')}'")
    
    # 4. Ищем элементы скидок
    print("\n💰 ПОИСК СКИДОК:")
    discount_selectors = [
        "//*[contains(text(), 'скидк')]",
        "//*[contains(text(), 'discount')]",
        "//*[contains(@class, 'discount')]"
    ]
    
    for selector in discount_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ '{selector}': {len(elements)} элементов")
            for elem in elements[:2]:
                print(f"   - {elem.tag_name}: '{elem.text}'")
    
    # 5. Скриншот
    driver.save_screenshot("excursion_debug.png")
    print("📸 Скриншот сохранен: excursion_debug.png")
    
    print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")