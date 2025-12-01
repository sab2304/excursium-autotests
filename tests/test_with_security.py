import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class TestWithSecurity:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(15)

    def teardown_method(self):
        self.driver.quit()

    def test_bypass_security(self):
        """Тест обхода проверки безопасности"""
        print("🔍 Тестируем обход защиты...")
        
        # Открываем сайт
        self.driver.get("https://excursium.com")
        
        # Ждём прохождения проверки безопасности
        security_passed = False
        for i in range(6):  # 30 секунд максимум
            time.sleep(5)
            current_url = self.driver.current_url
            current_title = self.driver.title
            
            print(f"⏳ Попытка {i+1}: {current_title} - {current_url}")
            
            if "Verify" not in current_url and "Проверка безопасности" not in current_title:
                security_passed = True
                break
        
        assert security_passed, "Не удалось пройти проверку безопасности"
        print("✅ Проверка безопасности пройдена!")
        
        # Проверяем что мы на главной странице
        assert "excursium.com" in self.driver.current_url
        assert self.driver.title
        print(f"📄 Заголовок: {self.driver.title}")
        
        # Сохраняем скриншот
        self.driver.save_screenshot("after_security.png")
        print("📸 Скриншот после проверки сохранён")

    def test_direct_excursions_page(self):
        """Прямой переход на страницу экскурсий (может не требовать проверки)"""
        print("🔗 Прямой переход на экскурсии...")
        
        self.driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
        time.sleep(10)  # Ждём проверку безопасности
        
        # Проверяем что загрузилась страница экскурсий
        current_url = self.driver.current_url
        print(f"🌐 Текущий URL: {current_url}")
        
        assert "ekskursii" in current_url, "Не на странице экскурсий"
        assert self.driver.title, "Заголовок пустой"
        print(f"📄 Заголовок экскурсий: {self.driver.title}")
        print("✅ Страница экскурсий загружена")