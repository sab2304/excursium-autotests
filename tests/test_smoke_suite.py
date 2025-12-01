# tests/test_smoke_suite.py
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.smoke
def test_smoke_landing_page(init_driver):
    """Smoke-тест главной страницы"""
    driver = init_driver
    driver.get("https://excursium.com/")
    assert "ЭкскурсиУм" in driver.title
    print("✅ Smoke: Лендинг загружается")

@pytest.mark.smoke  
def test_smoke_excursions_page(init_driver):
    """Smoke-тест страницы экскурсий"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursii-dlya-shkolnikov/list")
    assert "экскурси" in driver.title.lower()
    print("✅ Smoke: Страница экскурсий загружается")

@pytest.mark.smoke
def test_smoke_excursion_detail(init_driver):
    """Smoke-тест детальной страницы экскурсии"""
    driver = init_driver
    driver.get("https://excursium.com/ekskursiya-dlya-shkolnikov/shedevry-tretyakovskoy-galerei")
    assert "третьяковск" in driver.title.lower()
    print("✅ Smoke: Детальная страница экскурсии загружается")