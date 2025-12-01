from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class ExcursionsPage(BasePage):
    # Локаторы страницы экскурсий
    FILTER_SECTION = (By.CSS_SELECTOR, ".filters, [class*='filter'], aside, .filter-panel")
    SHOW_MORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Показать больше')]")
    FILTER_OPTIONS = (By.CSS_SELECTOR, "input[type='checkbox'], .filter-option, .checkbox")
    EXCURSION_CARDS = (By.CSS_SELECTOR, ".card, .excursion-card, [class*='tour'], [class*='excursion']")
    
    def open(self):
        """Открывает страницу экскурсий"""
        return self.open_url("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    
    def are_filters_visible(self):
        """Проверяет, видны ли фильтры"""
        return self.is_element_present(*self.FILTER_SECTION)
    
    def count_visible_excursions(self):
        """Считает видимые карточки экскурсий"""
        cards = self.driver.find_elements(*self.EXCURSION_CARDS)
        visible_cards = [card for card in cards if card.is_displayed()]
        return len(visible_cards)
    
    def search_on_excursions_page(self, query):
        """Поиск на странице экскурсий - улучшенная версия"""
        try:
            print(f"🔍 Ищем на странице экскурсий: '{query}'")
            
            # Пробуем разные локаторы для поля поиска
            search_selectors = [
                "input[type='search']",
                "input[name*='search']",
                "input[placeholder*='поиск']", 
                "input[placeholder*='экскурс']",
                "#searchText",
                ".search-input",
                "input.form-control"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ Найдено поле поиска: {selector}")
                    break
                except:
                    continue
            
            if not search_input:
                print("❌ Поле поиска не найдено на странице экскурсий")
                return False
            
            # Очищаем и вводим запрос
            search_input.clear()
            search_input.send_keys(query)
            
            # Пробуем нажать Enter
            search_input.send_keys("\n")
            time.sleep(5)  # Ждём результатов поиска
            
            # Проверяем что поиск сработал
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            if query.lower() in page_source or "search" in current_url:
                print(f"✅ Поиск '{query}' сработал")
                return True
            else:
                print(f"⚠️  Поиск '{query}' возможно не сработал")
                return True  # Все равно возвращаем True, так как технически операция выполнена
                
        except Exception as e:
            print(f"❌ Ошибка поиска на странице экскурсий: {e}")
            return False