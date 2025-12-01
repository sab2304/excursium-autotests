from .base_page import BasePage
from selenium.webdriver.common.by import By
import time

class MainPage(BasePage):  # ← ДОЛЖНО БЫТЬ MainPage
    # Локаторы
    EXCURSIONS_LINKS = [
        (By.XPATH, "//a[contains(text(), 'Все экскурсии')]"),
        (By.XPATH, "//a[contains(text(), 'Посмотреть все экскурсии')]"),
        (By.XPATH, "//a[contains(text(), 'Экскурсии для школьников')]"),
        (By.XPATH, "//a[contains(@href, 'ekskursii') and string-length(text()) > 0]"),
    ]
    
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")
    
    def open(self):
        return self.open_url("https://excursium.com")
    
    def search_excursions(self, query=""):
        try:
            search_input = self.find_element(*self.SEARCH_INPUT)
            search_input.clear()
            
            if query:
                search_input.send_keys(query)
                print(f"🔍 Ищем: {query}")
            
            search_input.send_keys("\n")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")
            return False
    
    def go_to_excursions(self):
        """Улучшенный переход на экскурсии с прокруткой"""
        print("🔗 Пытаемся найти ссылку на экскурсии...")
        
        for i, (by, value) in enumerate(self.EXCURSIONS_LINKS):
            try:
                print(f"  Попытка {i+1}: {value}")
                elements = self.driver.find_elements(by, value)
                
                if not elements:
                    print(f"    ❌ Элементы не найдены")
                    continue
                
                print(f"    Найдено элементов: {len(elements)}")
                
                for j, element in enumerate(elements):
                    try:
                        text = element.text.strip()
                        href = element.get_attribute('href')
                        displayed = element.is_displayed()
                        
                        print(f"      Элемент {j}: '{text}' -> {href} (visible: {displayed})")
                        
                        if displayed and text and 'ekskursii' in href:
                            print(f"    ✅ Найдена подходящая ссылка: '{text}'")
                            
                            # Прокрутим к элементу перед кликом
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            time.sleep(1)
                            
                            # Используем JavaScript для клика
                            self.driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            
                            # Проверяем что перешли на нужную страницу
                            if "ekskursii" in self.driver.current_url:
                                print(f"✅ Успешно перешли по ссылке: {text}")
                                return True
                            else:
                                print(f"❌ Не удалось перейти по ссылке: {text}")
                                
                    except Exception as e:
                        print(f"      Ошибка при клике: {e}")
                        continue
                        
            except Exception as e:
                print(f"    ❌ Ошибка поиска: {e}")
                continue
        
        print("❌ Ни одна ссылка на экскурсии не сработала")
        return False
    
    def go_to_excursions_direct(self):
        """Прямой переход на страницу экскурсий"""
        return self.open_url("https://excursium.com/ekskursii-dlya-shkolnikov/list")