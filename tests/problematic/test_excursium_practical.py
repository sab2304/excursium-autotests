import pytest
from selenium.webdriver.common.by import By
import time

def test_page_availability(driver):
    """Тестируем доступность основных страниц Excursium"""
    pages = [
        ("Главная", "https://excursium.com/"),
        ("Экскурсии", "https://excursium.com/ekskursii-dlya-shkolnikov/list"),
        ("О нас", "https://excursium.com/about"),
        ("Контакты", "https://excursium.com/contacts")
    ]
    
    for page_name, page_url in pages:
        print(f"\n=== Проверяем: {page_name} ===")
        driver.get(page_url)
        time.sleep(5)
        
        print(f"URL: {driver.current_url}")
        print(f"Заголовок: {driver.title}")
        
        if "Verify/Entry" in driver.current_url:
            print("🔒 Страница защищена проверкой безопасности")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if btn.text:
                    print(f"  Кнопка: '{btn.text}'")
        else:
            print("✅ Страница доступна напрямую")
            headings = driver.find_elements(By.TAG_NAME, "h1")
            for h in headings:
                if h.text:
                    print(f"  Заголовок H1: '{h.text}'")

def test_excursions_page_structure(driver):
    """Детальный анализ страницы экскурсий"""
    driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    time.sleep(5)
    
    print(f"\n=== СТРУКТУРА СТРАНИЦЫ ЭКСКУРСИЙ ===")
    print(f"Заголовок: {driver.title}")
    print(f"URL: {driver.current_url}")
    
    if "Verify/Entry" not in driver.current_url:
        print("✅ Страница экскурсий доступна!")
        
        filters = driver.find_elements(By.CSS_SELECTOR, "[class*='filter'], [class*='Filter']")
        print(f"Найдено элементов фильтрации: {len(filters)}")
        
        cards = driver.find_elements(By.CSS_SELECTOR, "[class*='card'], [class*='item'], [class*='product']")
        print(f"Найдено карточек экскурсий: {len(cards)}")
        
        driver.save_screenshot("reports/excursions_page.png")
        print("📸 Скриншот сохранен: reports/excursions_page.png")
        
    else:
        print("🔒 Страница требует проверки безопасности")