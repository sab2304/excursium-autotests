# tests/debug_filters_structure.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_debug_filters_structure(init_driver):
    """Диагностика реальной структуры фильтров на странице"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    time.sleep(3)
    
    print("🔍 ДИАГНОСТИКА СТРУКТУРЫ ФИЛЬТРОВ:")
    
    # 1. Ищем ВСЕ возможные элементы фильтров
    print("\n📋 Поиск всех элементов фильтров:")
    
    filter_selectors = [
        ("div с классом filter", "//div[contains(@class, 'filter')]"),
        ("section с классом filter", "//section[contains(@class, 'filter')]"),
        ("div с классом facet", "//div[contains(@class, 'facet')]"),
        ("div с классом category", "//div[contains(@class, 'category')]"),
        ("div с классом option", "//div[contains(@class, 'option')]"),
        ("fieldset", "//fieldset"),
        ("form с классом filter", "//form[contains(@class, 'filter')]"),
        ("элементы с data-атрибутами фильтров", "//*[@data-filter or @data-facet]"),
        ("чекбоксы", "//input[@type='checkbox']"),
        ("радиокнопки", "//input[@type='radio']"),
        ("select элементы", "//select"),
        ("кнопки фильтров", "//button[contains(@class, 'filter')]"),
        ("labels фильтров", "//label[contains(@for, 'filter')]"),
    ]
    
    for element_type, selector in filter_selectors:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ {element_type}: {len(elements)} элементов")
            for i, elem in enumerate(elements[:2]):  # Показываем первые 2
                try:
                    text = elem.text[:100] if elem.text else "нет текста"
                    classes = elem.get_attribute('class') or "нет класса"
                    print(f"   {i+1}. class: '{classes}', text: '{text}'")
                except:
                    print(f"   {i+1}. невозможно прочитать")
        else:
            print(f"❌ {element_type}: не найдено")
    
    # 2. Ищем текст связанный с фильтрацией
    print("\n🔤 Текст связанный с фильтрацией:")
    filter_texts = [
        "фильтр", "filter", "сортировка", "sort", "категория", "category",
        "цена", "price", "время", "time", "дата", "date", "место", "location"
    ]
    
    for text in filter_texts:
        elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
        if elements:
            print(f"✅ '{text}': {len(elements)} элементов")
            for elem in elements[:2]:
                print(f"   - {elem.text[:100]}...")
    
    # 3. Ищем кнопки управления фильтрами
    print("\n🔄 Кнопки управления фильтрами:")
    button_texts = [
        "Показать больше", "Еще", "More", "Все", "All",
        "Применить", "Apply", "Сбросить", "Reset", "Поиск", "Search"
    ]
    
    for text in button_texts:
        elements = driver.find_elements(By.XPATH, f"//button[contains(text(), '{text}')]")
        if elements:
            print(f"✅ Кнопка '{text}': {len(elements)} элементов")
    
    # 4. Анализ структуры страницы
    print("\n🏗️ Общая структура страницы:")
    
    # Основные контейнеры
    containers = [
        ("header", "//header"),
        ("main", "//main"),
        ("section", "//section"),
        ("aside", "//aside"),
        ("nav", "//nav"),
        ("div с id", "//div[@id]")
    ]
    
    for container_type, selector in containers:
        elements = driver.find_elements(By.XPATH, selector)
        if elements:
            print(f"✅ {container_type}: {len(elements)} элементов")
            for elem in elements[:1]:
                elem_id = elem.get_attribute('id') or "без id"
                classes = elem.get_attribute('class') or "без класса"
                print(f"   - id: '{elem_id}', class: '{classes}'")
    
    # 5. Сохраняем скриншот и исходный код для анализа
    driver.save_screenshot("filters_debug.png")
    print("📸 Скриншот сохранен: filters_debug.png")
    
    with open("filters_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("💾 Исходный код сохранен: filters_page_source.html")
    
    print("\n✅ ДИАГНОСТИКА ЗАВЕРШЕНА")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])