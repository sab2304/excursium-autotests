import pytest 
from selenium.webdriver.common.by import By 
import time 
 
def test_real_homepage(driver): 
    driver.get("https://excursium.com/") 
    time.sleep(5) 
 
    # Если мы на странице проверки безопасности, нажимаем "Подтвердить" 
    if "Verify/Entry" in driver.current_url: 
        print("На странице проверки безопасности, нажимаем 'Подтвердить'") 
        confirm_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Подтвердить')]") 
        confirm_btn.click() 
        time.sleep(8) 
 
    print(f"Текущий заголовок: {driver.title}") 
    print(f"Текущий URL: {driver.current_url}") 
 
    # Исследуем что на странице после проверки 
    buttons = driver.find_elements(By.TAG_NAME, "button") 
    print(f"Найдено кнопок: {len(buttons)}") 
    for i, btn in enumerate(buttons): 
        if btn.text: 
            print(f"  {i+1}. '{btn.text}'") 
 
    # Сохраняем скриншот реальной главной страницы 
    driver.save_screenshot("reports/real_homepage.png") 
    print("Скриншот сохранен: reports/real_homepage.png") 
