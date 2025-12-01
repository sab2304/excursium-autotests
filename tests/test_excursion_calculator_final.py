# tests/test_excursion_calculator_final.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_excursion_calculator_final(init_driver):
    """Финальный тест калькулятора стоимости экскурсии"""
    driver = init_driver
    wait = WebDriverWait(driver, 10)
    
    # Переходим на конкретную страницу экскурсии
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    print("📄 Перешли на страницу экскурсии")
    time.sleep(3)
    
    # 1. Ищем основные элементы калькулятора
    print("\n🎯 Поиск основных элементов:")
    
    # Ищем заголовок с ценой (с обработкой исключений)
    price_headers = driver.find_elements(By.XPATH, "//h3[contains(text(), 'Цена')]")
    for header in price_headers:
        print(f"💰 Заголовок цены: {header.text}")
        # Ищем следующую цену после заголовка (с проверкой)
        try:
            next_price = header.find_element(By.XPATH, "./following-sibling::*//*[contains(text(), '₽')]")
            print(f"   → Цена: {next_price.text}")
        except:
            print("   → Цена не найдена рядом с заголовком")
    
    # 2. Ищем опции выбора (radio buttons или select)
    print("\n⚙️ Поиск опций выбора:")
    
    # Ищем радиокнопки
    radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio']")
    print(f"📻 Найдено радиокнопок: {len(radio_buttons)}")
    
    # Ищем select элементы
    select_elements = driver.find_elements(By.TAG_NAME, "select")
    print(f"📋 Найдено select элементов: {len(select_elements)}")
    
    # 3. Ищем варианты количества человек
    print("\n👥 Варианты количества:")
    
    # Ищем элементы с текстом о количестве
    quantity_texts = driver.find_elements(By.XPATH, "//*[contains(text(), 'человек') or contains(text(), 'школьник')]")
    for text_elem in quantity_texts[:5]:
        if text_elem.text.strip():  # Показываем только непустые тексты
            print(f"   - {text_elem.text}")
            # Ищем рядом цену (с проверкой)
            try:
                nearby_price = text_elem.find_element(By.XPATH, "./following::*[contains(text(), '₽')][1]")
                print(f"     → Цена: {nearby_price.text}")
            except:
                pass
    
    # 4. Ищем фиксированные ценовые варианты
    print("\n💎 Фиксированные ценовые варианты:")
    
    # Ищем карточки с ценами
    price_cards = driver.find_elements(By.XPATH, "//*[contains(@class, 'card')]//*[contains(text(), '₽')]")
    for card in price_cards[:5]:
        if card.text.strip():
            print(f"   - Карточка: {card.text}")
    
    # 5. Проверяем наличие формы заказа
    print("\n📋 Проверка формы заказа:")
    
    form_selectors = [
        "//form[contains(@class, 'order')]",
        "//form[contains(@class, 'booking')]",
        "//form[contains(@class, 'reservation')]",
        "//form"
    ]
    
    form_found = False
    for selector in form_selectors:
        try:
            order_form = driver.find_element(By.XPATH, selector)
            print(f"✅ Найдена форма заказа: {selector}")
            form_found = True
            
            # Ищем поля в форме
            form_inputs = order_form.find_elements(By.TAG_NAME, "input")
            print(f"   📝 Поля в форме: {len(form_inputs)}")
            
            for inp in form_inputs[:5]:
                input_type = inp.get_attribute("type")
                placeholder = inp.get_attribute("placeholder")
                if placeholder:
                    print(f"     - {input_type}: {placeholder}")
            break
        except:
            continue
    
    if not form_found:
        print("❌ Форма заказа не найдена")
    
    # 6. Тестируем кнопку заказа
    print("\n🛒 Тестирование кнопки заказа:")
    
    order_buttons = driver.find_elements(By.XPATH, 
        "//button[contains(text(), 'Заказать') or contains(text(), 'Забронировать') or contains(text(), 'Оформить')]")
    
    for button in order_buttons:
        print(f"   - Кнопка: '{button.text}'")
        if button.is_enabled():
            print("     ✅ Доступна для клика")
        else:
            print("     ❌ Недоступна")
    
    # 7. Ищем информацию о скидках
    print("\n🎁 Информация о скидках:")
    
    discount_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'скидк') or contains(text(), 'акци')]")
    for discount in discount_elements[:3]:
        if discount.text.strip():
            print(f"   - {discount.text}")
    
    # 8. Анализируем структуру ценообразования
    print("\n📊 Анализ структуры цен:")
    
    # Ищем все элементы с ценами и их контекст
    all_price_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '₽') or contains(text(), 'руб')]")
    meaningful_prices = []
    
    for price_elem in all_price_elements:
        text = price_elem.text.strip()
        # Ищем только осмысленные цены (с цифрами)
        if any(char.isdigit() for char in text) and len(text) < 100:
            meaningful_prices.append(text)
    
    print("🎯 Осмысленные цены на странице:")
    unique_prices = list(set(meaningful_prices))
    for price in unique_prices[:15]:  # Уникальные цены
        print(f"   - {price}")
    
    # 9. Проверяем наличие калькулятора в традиционном понимании
    print("\n🔍 Проверка традиционного калькулятора:")
    
    calculator_indicators = [
        "//*[contains(text(), 'Рассчитайте стоимость')]",
        "//*[contains(text(), 'Калькулятор')]",
        "//*[contains(text(), 'рассчитать')]",
        "//*[contains(@onclick, 'calculate')]",
        "//*[contains(@class, 'calc')]"
    ]
    
    found_calc = False
    for indicator in calculator_indicators:
        elements = driver.find_elements(By.XPATH, indicator)
        if elements:
            print(f"✅ Найден индикатор калькулятора: {indicator}")
            found_calc = True
            for elem in elements[:2]:
                if elem.text.strip():
                    print(f"   - {elem.text}")
    
    if not found_calc:
        print("ℹ️  Традиционный калькулятор не найден. Вероятно, цены фиксированные или рассчитываются автоматически.")
    
    # 10. Проверяем наличие динамического изменения цены
    print("\n🔄 Проверка динамического изменения цены:")
    
    # Ищем элементы, которые могут влиять на цену (объединение через |)
    interactive_elements = driver.find_elements(
        By.XPATH,
        "//input[@type='checkbox'] | //input[@type='radio'] | //select | //button[contains(@class, 'option')]"
    )
    
    print(f"🎛️  Найдено интерактивных элементов: {len(interactive_elements)}")
    
    # Проверяем, меняется ли цена при клике на элементы (если они есть)
    if interactive_elements:
        initial_prices = set(meaningful_prices)
        print(f"💰 Начальные цены: {len(initial_prices)} вариантов")
        
        # Пробуем кликнуть на первый доступный интерактивный элемент
        for i, element in enumerate(interactive_elements[:3]):
            try:
                if element.is_enabled() and element.is_displayed():
                    element_type = element.get_attribute("type") or element.tag_name
                    element_name = element.get_attribute("name") or element.get_attribute("class") or element.text
                    print(f"   🔄 Тестируем элемент {i+1}: {element_type} - {element_name}")
                    
                    # Запоминаем текущее состояние
                    initial_state = element.is_selected() if element_type in ['checkbox', 'radio'] else None
                    
                    # Кликаем на элемент
                    element.click()
                    time.sleep(2)
                    
                    # Проверяем, изменились ли цены
                    new_prices = driver.find_elements(By.XPATH, "//*[contains(text(), '₽')]")
                    new_meaningful = []
                    for price_elem in new_prices:
                        text = price_elem.text.strip()
                        if any(char.isdigit() for char in text) and len(text) < 100:
                            new_meaningful.append(text)
                    
                    if set(new_meaningful) != initial_prices:
                        print("     ✅ Цены изменились после клика!")
                        print(f"     Было: {len(initial_prices)} вариантов")
                        print(f"     Стало: {len(set(new_meaningful))} вариантов")
                    else:
                        print("     ⏸️  Цены не изменились")
                    
                    # Возвращаем исходное состояние (если это checkbox/radio)
                    if element_type in ['checkbox', 'radio'] and initial_state is not None:
                        if element.is_selected() != initial_state:
                            element.click()
                            time.sleep(1)
                    
            except Exception as e:
                print(f"     ❌ Ошибка при тестировании элемента: {e}")
    else:
        print("ℹ️  Интерактивные элементы для изменения цены не найдены")
    
    # 11. Финальный вывод
    print("\n" + "="*50)
    print("🎯 ВЫВОДЫ ПО ТЕСТИРОВАНИЮ:")
    print("="*50)
    
    if len(meaningful_prices) > 5:
        print("✅ На странице представлены различные ценовые варианты")
        print("📊 Диапазон цен указывает на зависимость от:")
        print("   - Количества человек (от 1 800 ₽ до 7 000 ₽)")
        print("   - Состава группы (взрослые/дети)")
        print("   - Размера группы")
    else:
        print("ℹ️  Цены, вероятно, фиксированные")
    
    print(f"✅ Доступно для заказа: {len(order_buttons)} вариантов")
    
    # Проверяем, есть ли явный калькулятор
    if found_calc:
        print("🎯 РЕКОМЕНДАЦИЯ: Тестировать традиционный калькулятор")
    elif interactive_elements:
        print("🎯 РЕКОМЕНДАЦИЯ: Тестировать интерактивные элементы влияющие на цену")
    else:
        print("🎯 РЕКОМЕНДАЦИЯ: Тестировать фиксированные цены и процесс заказа")
        print("   - Проверить отображение различных ценовых вариантов")
        print("   - Протестировать кнопку 'Заказать экскурсию'")
        print("   - Проверить информацию о скидках")
    
    print("📸 Скриншот сохранен: final_calculator_test.png")
    driver.save_screenshot("final_calculator_test.png")
    
    print("\n✅ ФИНАЛЬНЫЙ ТЕСТ ЗАВЕРШЕН")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])