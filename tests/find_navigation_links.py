from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def find_navigation_links():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        print("🔍 Тщательно ищем навигационные ссылки...")
        driver.get("https://excursium.com")
        time.sleep(10)
        
        # Сохраняем HTML для анализа
        with open("main_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 HTML главной страницы сохранён")
        
        # 1. Ищем ВСЕ ссылки на странице
        print("\n🔗 ВСЕ ссылки на главной странице:")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Всего ссылок: {len(all_links)}")
        
        # Показываем первые 30 ссылок с текстом
        links_with_text = []
        for i, link in enumerate(all_links):
            try:
                text = link.text.strip()
                href = link.get_attribute('href')
                if text and 'ekskursii' in href:
                    links_with_text.append((text, href))
                    if len(links_with_text) <= 30:  # Показываем первые 30
                        displayed = "✅" if link.is_displayed() else "❌"
                        print(f"   {displayed} {i}: '{text}' -> {href}")
            except:
                continue
        
        print(f"\n📊 Ссылок с текстом и 'ekskursii': {len(links_with_text)}")
        
        # 2. Ищем конкретно по тексту
        print("\n🎯 Поиск по конкретным текстам:")
        target_texts = [
            "Все экскурсии",
            "Все экскурсии для школьников", 
            "Экскурсии",
            "Экскурсии для школьников",
            "Посмотреть все экскурсии",
            "Выбрать экскурсию",
            "Каталог экскурсий",
            "Экскурсии для школьников"
        ]
        
        for text in target_texts:
            try:
                elements = driver.find_elements(By.XPATH, f"//a[contains(text(), '{text}')]")
                print(f"\n🔍 '{text}': найдено {len(elements)}")
                for i, elem in enumerate(elements):
                    if elem.is_displayed():
                        href = elem.get_attribute('href')
                        print(f"   ✅ {i}: displayed, href: {href}")
                    else:
                        print(f"   ❌ {i}: hidden")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        # 3. Ищем по классам и атрибутам
        print("\n🎨 Поиск по классам и атрибутам:")
        css_selectors = [
            "a.btn",
            "a.button",
            "a[class*='excurs']",
            "a[class*='tour']", 
            "a[class*='catalog']",
            "a[class*='all']",
            "a.btn-primary",
            "a.btn-success"
        ]
        
        for selector in css_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"\n🎨 {selector}: {len(elements)} элементов")
                    for i, elem in enumerate(elements[:3]):  # первые 3
                        text = elem.text.strip()
                        href = elem.get_attribute('href')
                        if text:
                            displayed = "✅" if elem.is_displayed() else "❌"
                            print(f"   {displayed} {i}: '{text}' -> {href}")
            except Exception as e:
                print(f"   ❌ {selector}: {e}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    find_navigation_links()