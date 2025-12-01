import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def debug_site():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        print("🔍 Открываем сайт...")
        driver.get("https://excursium.com")
        time.sleep(10)  # Увеличили время для прохождения проверки безопасности
        
        print(f"📄 Title: '{driver.title}'")
        print(f"🌐 URL: {driver.current_url}")
        print(f"📏 Page source length: {len(driver.page_source)}")
        
        # Если всё ещё на странице проверки
        if "Verify" in driver.current_url or "Проверка безопасности" in driver.title:
            print("🛡️  Сайт требует проверку безопасности...")
            print("⏳ Ждём 15 секунд для прохождения проверки...")
            time.sleep(15)
            
            # Обновляем страницу после проверки
            driver.refresh()
            time.sleep(5)
            
            print(f"📄 Новый Title: '{driver.title}'")
            print(f"🌐 Новый URL: {driver.current_url}")
        
        # Ищем поле поиска разными способами
        print("\n🔎 Ищем поле поиска...")
        selectors = [
            "input[type='search']",
            "#searchText", 
            "input.form-control",
            "input[placeholder*='Мосфильм']",
            "input[placeholder*='Кремль']",
            "input"  # Все поля ввода
        ]
        
        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✅ Найдено: {selector}")
                print(f"   Placeholder: {element.get_attribute('placeholder')}")
                print(f"   ID: {element.get_attribute('id')}")
                print(f"   Class: {element.get_attribute('class')}")
                print(f"   Type: {element.get_attribute('type')}")
            except:
                print(f"❌ Не найдено: {selector}")
        
        # Ищем ссылки на экскурсии (исправленный метод)
        print("\n🔗 Ищем ссылки на экскурсии...")
        excursion_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'ekskursii')]")
        print(f"Найдено ссылок: {len(excursion_links)}")
        for i, link in enumerate(excursion_links[:5]):  # первые 5
            print(f"   {i}: {link.text} -> {link.get_attribute('href')}")
        
        # Сохраняем скриншот для отладки
        driver.save_screenshot("debug_screenshot.png")
        print("📸 Скриншот сохранён: debug_screenshot.png")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_site()