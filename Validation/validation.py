from datetime import datetime

def get_input(prompt: str, error_message: str) -> str:
    """Получает ввод от пользователя и проверяет, чтобы он не был пустым"""
    while True:
        value = input(prompt).strip()
        if not value:
            print(error_message)
        else:
            return value

def get_valid_date(prompt: str) -> str:
    """Проверяет корректность формата даты YYYY-MM-DD"""
    while True:
        date_str = get_input(prompt, "Ошибка: Срок выполнения не может быть пустым")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Ошибка: Неверный формат даты. Укажите дату в формате YYYY-MM-DD")

def get_valid_priority(prompt: str) -> str:
    """Проверяет, что приоритет указан корректно"""
    valid_priorities = {"низкий", "средний", "высокий"}
    while True:
        priority = get_input(prompt, "Ошибка: Приоритет не может быть пустым")
        if priority.lower() in valid_priorities:
            return priority.lower()
        else:
            print("Ошибка: Приоритет должен быть 'низкий', 'средний' или 'высокий'")