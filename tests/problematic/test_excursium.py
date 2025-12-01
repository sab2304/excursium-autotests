import pytest 
from selenium.webdriver.common.by import By 
import time 
 
def test_excursium_homepage(driver): 
    driver.get("https://excursium.com/") 
    time.sleep(10) 
 
    print(f"Page title: {driver.title}") 
    print(f"Current URL: {driver.current_url}") 
 
    assert "экскурсии" in driver.title.lower() 
 
    buttons = driver.find_elements(By.TAG_NAME, "button") 
    print(f"Found {len(buttons)} buttons on page") 
 
    driver.save_screenshot("reports/excursium_homepage.png") 
    print("Screenshot saved") 
