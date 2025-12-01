# tests/debug_filters_detailed.py
import pytest
from selenium.webdriver.common.by import By
import time

def test_debug_filters_detailed(init_driver):
    """Детальная диагностика структуры фильтров"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    time.sleep(3)
    
    print("🔍 ДЕТАЛЬНАЯ ДИАГНОСТИКА ФИЛЬТРОВ:")
    
    # 1. Анализ aside контейнера
    print("\n📦 АНАЛИЗ ASIDE КОНТЕЙНЕРА:")
    aside = driver.find_element(By.XPATH, "//aside[contains(@class, 'col-xl-3')]")
    print(f"✅ Aside найден: class='{aside.get_attribute('class')}'")
    
    # Получаем ВЕСЬ HTML aside для анализа
    aside_html = aside.get_attribute('innerHTML')
    print(f"📝 Длина HTML aside: {len(aside_html)} символов")
    
    # Ищем ВСЕ элементы внутри aside
    all_elements = aside.find_elements(By.XPATH, ".//*")
    print(f"📊 Всего элементов в aside: {len(all_elements)}")
    
    # Группируем элементы по тегам
    tag_counts = {}
    for elem in all_elements:
        tag = elem.tag_name
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    print("🏷️ Распределение по тегам:")
    for tag, count in sorted(tag_counts.items()):
        print(f"   - {tag}: {count}")
    
    # 2. Детальный анализ чекбоксов
    print("\n✅ ДЕТАЛЬНЫЙ АНАЛИЗ ЧЕКБОКСОВ:")
    checkboxes = aside.find_elements(By.XPATH, ".//input[@type='checkbox']")
    print(f"Найдено чекбоксов: {len(checkboxes)}")
    
    for i, cb in enumerate(checkboxes[:10]):  # Первые 10
        try:
            cb_id = cb.get_attribute('id') or f"без_id_{i}"
            cb_name = cb.get_attribute('name') or "без имени"
            cb_class = cb.get_attribute('class') or "без класса"
            enabled = cb.is_enabled()
            displayed = cb.is_displayed()
            selected = cb.is_selected()
            
            print(f"   {i+1}. id: '{cb_id}'")
            print(f"      name: '{cb_name}', class: '{cb_class}'")
            print(f"      enabled: {enabled}, displayed: {displayed}, selected: {selected}")
            
            # Ищем связанный label
            try:
                if cb_id and cb_id != f"без_id_{i}":
                    label = aside.find_element(By.XPATH, f".//label[@for='{cb_id}']")
                    print(f"      label: '{label.text}'")
            except:
                print(f"      label: не найден")
                
        except Exception as e:
            print(f"   {i+1}. Ошибка анализа: {e}")
    
    # 3. Поиск группирующих элементов
    print("\n📁 ПОИСК ГРУППИРУЮЩИХ ЭЛЕМЕНТОВ:")
    
    # Ищем возможные контейнеры групп
    group_selectors = [
        ".//div[contains(@class, 'card')]",
        ".//div[contains(@class, 'collapse')]",
        ".//div[contains(@class, 'accordion')]",
        ".//div[contains(@class, 'filter')]",
        ".//div[@data-toggle]",
        ".//div[contains(@class, 'mb-')]",
        ".//div[contains(@class, 'mt-')]",
        ".//div[contains(@class, 'pt-')]",
        ".//div[contains(@class, 'pb-')]",
        ".//fieldset",
        ".//div[h5 or h6 or strong]"
    ]
    
    for selector in group_selectors:
        groups = aside.find_elements(By.XPATH, selector)
        if groups:
            print(f"✅ Найдено по '{selector}': {len(groups)}")
            for group in groups[:2]:
                try:
                    # Ищем заголовок
                    title_elem = group.find_element(By.XPATH, ".//h5 | .//h6 | .//strong | .//span[contains(@class, 'title')]")
                    title = title_elem.text if title_elem else "без заголовка"
                    print(f"   - Группа: '{title}'")
                    
                    # Считаем чекбоксы в группе
                    group_checkboxes = group.find_elements(By.XPATH, ".//input[@type='checkbox']")
                    print(f"     Чекбоксов в группе: {len(group_checkboxes)}")
                    
                except:
                    print(f"   - Группа без заголовка")
    
    # 4. Поиск текстовых меток рядом с чекбоксами
    print("\n🏷️ ПОИСК ТЕКСТОВЫХ МЕТОК:")
    
    # Ищем все текстовые элементы в aside
    text_elements = aside.find_elements(By.XPATH, ".//*[text()]")
    meaningful_texts = []
    
    for elem in text_elements:
        text = elem.text.strip()
        if text and len(text) > 2 and len(text) < 100:
            meaningful_texts.append(text)
    
    print(f"📝 Уникальных текстовых элементов: {len(set(meaningful_texts))}")
    print("📋 Примеры текстов:")
    for text in list(set(meaningful_texts))[:20]:
        print(f"   - '{text}'")
    
    # 5. Проверка видимости и доступности
    print("\n👀 ПРОВЕРКА ВИДИМОСТИ:")
    
    visible_checkboxes = [cb for cb in checkboxes if cb.is_displayed()]
    enabled_checkboxes = [cb for cb in checkboxes if cb.is_enabled()]
    
    print(f"👁️  Видимых чекбоксов: {len(visible_checkboxes)}")
    print(f"🎯 Доступных чекбоксов: {len(enabled_checkboxes)}")
    
    # 6. Сохраняем структуру для ручного анализа
    with open("filters_detailed_structure.txt", "w", encoding="utf-8") as f:
        f.write("ДЕТАЛЬНАЯ СТРУКТУРА ФИЛЬТРОВ:\n")
        f.write("="*50 + "\n")
        
        for i, cb in enumerate(checkboxes):
            try:
                cb_id = cb.get_attribute('id') or f"без_id_{i}"
                cb_name = cb.get_attribute('name') or "без имени"
                enabled = cb.is_enabled()
                displayed = cb.is_displayed()
                
                f.write(f"{i+1}. id: {cb_id}, name: {cb_name}, enabled: {enabled}, displayed: {displayed}\n")
            except:
                f.write(f"{i+1}. Ошибка анализа\n")
    
    print("💾 Детальная структура сохранена: filters_detailed_structure.txt")
    print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])