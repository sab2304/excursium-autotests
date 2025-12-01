import pytest
from selenium.webdriver.common.by import By
import time

TEST_ENVIRONMENTS = [
    "https://stage.excursium.com/",
    "https://test.excursium.com/",
    "https://dev.excursium.com/",
    "https://staging.excursium.com/",
    "https://qa.excursium.com/"
]

def test_check_environments(driver):
    for env_url in TEST_ENVIRONMENTS:
        print(f"Проверяем: {env_url}")
        try:
            driver.get(env_url)
            time.sleep(3)
            if "Verify/Entry" not in driver.current_url:
                print(f"  ДОСТУПНО! Заголовок: {driver.title}")
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if btn.text and "найти" in btn.text.lower():
                        print(f"     Найдена кнопка: '{btn.text}'")
            else:
                print(f"  Требуется проверка безопасности")
        except Exception as e:
            print(f"  Ошибка: {e}")