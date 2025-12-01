import pytest 
from selenium.webdriver.common.by import By 
import time 
 
def test_explore_excursium(driver): 
    driver.get("https://excursium.com/") 
    time.sleep(8) 
 
    print("=== ИНФОРМАЦИЯ О СТРАНИЦЕ ===") 
    print(f"Заголовок: {driver.title}") 
    print(f"URL: {driver.current_url}") 
 
    print("КНОПКИ:") 
    buttons = driver.find_elements(By.TAG_NAME, "button") 
    for i, btn in enumerate(buttons): 
        if btn.text: 
            print(f"{i+1}. '{btn.text}'") 
 
    print("ПОЛЯ ВВОДА:") 
    inputs = driver.find_elements(By.TAG_NAME, "input") 
    for i, inp in enumerate(inputs[:10]): 
        placeholder = inp.get_attribute('placeholder') 
        print(f"{i+1}. type: {inp.get_attribute('type')}, placeholder: {placeholder}") 
 
    driver.save_screenshot("reports/explore_page.png") 
    print("Скриншот сохранен: reports/explore_page.png") 
