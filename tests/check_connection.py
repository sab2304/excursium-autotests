import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def check_connection():
    print("🔍 Проверяем доступность сайта...")
    
    # 1. Проверяем через requests
    try:
        response = requests.get("https://excursium.com", timeout=10)
        print(f"✅ Сайт доступен через requests: статус {response.status_code}")
    except Exception as e:
        print(f"❌ Сайт недоступен через requests: {e}")
    
    # 2. Проверяем через Selenium
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        print("🌐 Пробуем открыть через Selenium...")
        driver.get("https://excursium.com")
        time.sleep(10)
        
        print(f"✅ Сайт открыт: {driver.title}")
        driver.quit()
    except Exception as e:
        print(f"❌ Ошибка Selenium: {e}")

if __name__ == "__main__":
    check_connection()