import pytest
import allure
from selenium.webdriver.common.by import By

@allure.epic("Навигация")
@allure.feature("Меню и ссылки")
class TestNavigation:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
    
    @allure.story("Главное меню")
    def test_main_menu_links(self):
        """Тест ссылок главного меню"""
        self.driver.get(self.base_url)
        
        # Ищем меню
        menu_selectors = [
            "nav",
            ".navbar",
            ".menu", 
            ".header",
            "[role='navigation']"
        ]
        
        menu_links = []
        for selector in menu_selectors:
            try:
                menu = self.driver.find_element(By.CSS_SELECTOR, selector)
                links = menu.find_elements(By.TAG_NAME, "a")
                menu_links.extend(links)
            except:
                continue
        
        # Убираем дубликаты по href
        unique_links = []
        seen_hrefs = set()
        for link in menu_links:
            href = link.get_attribute('href')
            if href and href not in seen_hrefs:
                unique_links.append(link)
                seen_hrefs.add(href)
        
        print(f"Уникальных ссылок в меню: {len(unique_links)}")
        
        for i, link in enumerate(unique_links[:10]):  # Первые 10 ссылок
            text = link.text.strip()
            href = link.get_attribute('href')
            if text:
                print(f"  {i+1}. {text} -> {href}")
    
    @allure.story("Хлебные крошки")
    def test_breadcrumbs(self):
        """Тест хлебных крошек (если есть)"""
        self.driver.get(self.base_url)
        
        breadcrumb_selectors = [
            ".breadcrumb",
            ".breadcrumbs",
            "[aria-label='breadcrumb']"
        ]
        
        for selector in breadcrumb_selectors:
            try:
                breadcrumbs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if breadcrumbs:
                    print(f"Найдены хлебные крошки: {len(breadcrumbs)}")
                    return
            except:
                continue
        
        print("⚠️ Хлебные крошки не найдены")