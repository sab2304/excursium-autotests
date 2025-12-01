import sys 
import os 
# Добавляем src в PYTHONPATH 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src')) 
 
try: 
    from pages.main_page import MainPage 
    from utils.config import TestConfig 
    print("SUCCESS: All imports work!") 
    print("MainPage:", MainPage) 
    print("TestConfig:", TestConfig) 
except ImportError as e: 
    print("ERROR:", e) 
    print("Current sys.path:", sys.path) 
