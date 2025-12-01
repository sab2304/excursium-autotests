from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def simple_link_finder():
    print("🔍 Упрощённый поиск ссылок...")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        # Пробуем открыть с большим таймаутом
        print("🌐 Открываем сайт (может занять время)...")
        driver.set_page_load_timeout(60)
        driver.get("https://excursium.com")
        time.sleep(15)  # Даём больше времени на загрузку
        
        print(f"✅ Сайт открыт: {driver.title}")
        print(f"🌐 URL: {driver.current_url}")
        
        # Простой поиск ссылок на экскурсии
        print("\n🔗 Простой поиск ссылок:")
        
        # Ищем все ссылки с текстом
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Всего ссылок на странице: {len(all_links)}")
        
        # Показываем ссылки с текстом
        links_with_text = []
        for link in all_links:
            try:
                text = link.text.strip()
                if text and len(text) > 2:  # Исключаем пустые и очень короткие
                    href = link.get_attribute('href')
                    displayed = link.is_displayed()
                    links_with_text.append((text, href, displayed))
            except:
                pass
        
        print(f"\n📊 Ссылок с текстом: {len(links_with_text)}")
        
        # Показываем первые 20
        for i, (text, href, displayed) in enumerate(links_with_text[:20]):
            status = "✅" if displayed else "❌"
            print(f"{status} {i}: '{text}' -> {href}")
        
        # Ищем конкретно ссылки на экскурсии
        print("\n🎯 Ссылки содержащие 'ekskursii':")
        excursion_links = []
        for text, href, displayed in links_with_text:
            if href and 'ekskursii' in href:
                excursion_links.append((text, href, displayed))
        
        for i, (text, href, displayed) in enumerate(excursion_links):
            status = "✅" if displayed else "❌"
            print(f"{status} {i}: '{text}' -> {href}")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    simple_link_finder()