# generate_reports.py
import subprocess
import os
import time
import webbrowser

def run_tests_with_report(marker, report_name, description):
    """Запускает тесты с определенной меткой и генерирует HTML отчет"""
    print(f"🚀 Запускаем {description}...")
    
    command = [
        "pytest", 
        "tests/", 
        "-m", marker,
        "-v",
        "--html", f"reports/{report_name}",
        "--self-contained-html"
    ]
    
    start_time = time.time()
    result = subprocess.run(command, capture_output=True, text=True)
    elapsed_time = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ {description} завершены успешно")
    else:
        print(f"⚠️  {description} завершены с предупреждениями")
    
    print(f"📊 Отчет сохранен: reports/{report_name}")
    print(f"⏱️  Время выполнения: {elapsed_time:.2f} секунд")
    print("-" * 60)
    
    return result.returncode, elapsed_time

def main():
    """Генерирует все отчеты"""
    print("📈 ГЕНЕРАЦИЯ HTML ОТЧЕТОВ ДЛЯ EXCURSIUM")
    print("=" * 60)
    
    # Создаем папку для отчетов если ее нет
    os.makedirs("reports", exist_ok=True)
    
    # Запускаем тесты по категориям
    test_categories = [
        ("smoke", "smoke_test_report.html", "Smoke-тесты (базовая проверка)"),
        ("calculator", "calculator_test_report.html", "Тесты калькулятора стоимости"),
        ("filter", "filter_test_report.html", "Тесты фильтров экскурсий"),
        ("price", "price_test_report.html", "Тесты отображения цен"),
        ("validation", "validation_test_report.html", "Тесты валидации полей"),
        ("regression", "regression_test_report.html", "Регрессионные тесты"),
    ]
    
    results = []
    
    for marker, report_name, description in test_categories:
        returncode, elapsed_time = run_tests_with_report(marker, report_name, description)
        results.append((description, returncode, elapsed_time))
    
    # Генерируем сводный отчет
    print("\n📋 СВОДНЫЙ ОТЧЕТ:")
    print("=" * 60)
    print(f"{'ТИП ТЕСТОВ':<35} {'СТАТУС':<20} {'ВРЕМЯ':>10}")
    print("-" * 60)
    
    all_passed = True
    for description, returncode, elapsed_time in results:
        status = "✅ УСПЕХ" if returncode == 0 else "⚠️  ЕСТЬ ОШИБКИ"
        if returncode != 0:
            all_passed = False
        print(f"{description:<35} {status:<20} {elapsed_time:>6.2f} сек")
    
    # Финальный полный отчет
    print("\n🎯 Генерируем полный отчет всех тестов...")
    full_start = time.time()
    subprocess.run([
        "pytest", "tests/", "-v", 
        "--html", "reports/full_test_report.html",
        "--self-contained-html"
    ])
    full_time = time.time() - full_start
    
    print(f"📊 Полный отчет сохранен: reports/full_test_report.html")
    print(f"⏱️  Общее время выполнения: {full_time:.2f} секунд")
    
    # Итоговый статус
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ВСЕ ОСНОВНЫЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("⚠️  НЕКОТОРЫЕ ТЕСТЫ ИМЕЮТ ОШИБКИ")
    
    print("\n📁 ПАПКА С ОТЧЕТАМИ: reports/")
    print("📄 ОСНОВНЫЕ ОТЧЕТЫ:")
    print("   - smoke_test_report.html (быстрая проверка)")
    print("   - calculator_test_report.html (тесты калькулятора)")
    print("   - filter_test_report.html (тесты фильтров)")
    print("   - full_test_report.html (все тесты)")
    
    # Предлагаем открыть отчеты
    print("\n🔗 Открыть отчеты в браузере? (y/n)")
    choice = input().strip().lower()
    if choice in ['y', 'yes', 'д', 'да']:
        webbrowser.open('reports/smoke_test_report.html')
        webbrowser.open('reports/full_test_report.html')
        print("✅ Отчеты открыты в браузере!")

if __name__ == "__main__":
    main()