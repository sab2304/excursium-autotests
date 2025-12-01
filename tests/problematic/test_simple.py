import pytest 
 
def test_simple(): 
    print("Simple test works!") 
    assert 1 == 1 
 
def test_with_selenium(driver): 
    driver.get("https://google.com") 
    print(f"Page title: {driver.title}") 
    assert "Google" in driver.title 
