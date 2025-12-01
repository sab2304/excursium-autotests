try:
    from pages.main_page import MainPage
    from pages.excursions_page import ExcursionsPage
    print("✅ Импорт MainPage и ExcursionsPage работает!")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")

# Проверим содержимое файлов
print("\n🔍 Проверяем файлы...")
try:
    with open("pages/main_page.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "class MainPage" in content:
            print("✅ pages/main_page.py содержит класс MainPage")
        else:
            print("❌ pages/main_page.py НЕ содержит класс MainPage")
except Exception as e:
    print(f"❌ Не могу прочитать main_page.py: {e}")

try:
    with open("pages/excursions_page.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "class ExcursionsPage" in content:
            print("✅ pages/excursions_page.py содержит класс ExcursionsPage")
        else:
            print("❌ pages/excursions_page.py НЕ содержит класс ExcursionsPage")
except Exception as e:
    print(f"❌ Не могу прочитать excursions_page.py: {e}")