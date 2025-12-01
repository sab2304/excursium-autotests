[pytest]
# Автоматические опции для всех запусков
addopts = -p no:selenium -p no:base-url -p no:sensitiveurl -v --tb=short

# Где искать тесты
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Настройки отчетов
console_output_style = classic

# Переменные окружения (опционально)
env =
    PYTHONPATH=.