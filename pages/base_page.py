from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage:  # ← ДОЛЖНО БЫТЬ BasePage
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
    
    def open_url(self, url, timeout=30):
        """Открывает URL с обработкой проверки безопасности"""
        print(f"🌐 Открываем: {url}")
        self.driver.get(url)
        
        # Ждём прохождения проверки безопасности
        start_time = time.time()
        while time.time() - start_time < timeout:
            if "Verify" not in self.driver.current_url and "Проверка безопасности" not in self.driver.title:
                print("✅ Проверка безопасности пройдена")
                time.sleep(3)
                return True
            print("⏳ Ожидаем проверку безопасности...")
            time.sleep(5)
        
        print("⚠️  Возможно, требуется ручное прохождение проверки")
        return False
    
    def find_element(self, by, value, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def find_clickable(self, by, value, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    
    def is_element_present(self, by, value):
        try:
            self.find_element(by, value, timeout=5)
            return True
        except:
            return False