import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestManual:
    def setup_method(self):
        print("🚀 Setting up Chrome driver...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        print("✅ Chrome driver ready!")

    def teardown_method(self):
        print("🔚 Closing browser...")
        self.driver.quit()
        print("✅ Browser closed!")

    def test_google(self):
        print("🌐 Testing Google...")
        self.driver.get("https://www.google.com")
        print(f"📄 Page title: {self.driver.title}")
        assert "Google" in self.driver.title
        print("✅ Google test passed!")

    def test_example(self):
        print("🌐 Testing Example.com...")
        self.driver.get("https://example.com")
        print(f"📄 Page title: {self.driver.title}")
        assert "Example" in self.driver.title
        print("✅ Example test passed!")