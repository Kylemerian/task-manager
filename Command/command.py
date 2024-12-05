from abc import ABC, abstractmethod
from TaskManager.taskManager import *

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


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class ViewTasksCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        tasks = self.manager.view_tasks()
        if not tasks:
            print("Список задач пуст")
        for task in tasks:
            print(task.to_dict())
            
            
class ViewTasksByCategoryCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        category = input("Введите категорию: ").strip()
        tasks = self.manager.view_tasks(category=category)
        if not tasks:
            print(f"Задачи в категории '{category}' не найдены")
        for task in tasks:
            print(task.to_dict())


class AddTaskCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        try:
            title = get_input("Название: ", "Ошибка: Название не может быть пустым")
            description = get_input("Описание: ", "Ошибка: Описание не может быть пустым")
            category = get_input("Категория: ", "Ошибка: Категория не может быть пустой")
            due_date = get_valid_date("Срок выполнения (YYYY-MM-DD): ")
            priority = get_valid_priority("Приоритет (низкий/средний/высокий): ")

            task = Task(title, description, category, due_date, priority)
            self.manager.add_task(task)
            print("Задача успешно добавлена")
        except ValueError as e:
            print(f"Ошибка: {e}")


class CompleteTaskCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        task_id = input("Введите ID задачи: ").strip()
        if self.manager.mark_completed(task_id):
            print("Задача выполнена")
        else:
            print("Задача не найдена")

class DeleteTaskCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        task_id = input("Введите ID задачи (или оставьте пустым для удаления по категории): ").strip()
        category = None
        if not task_id:
            category = input("Введите категорию для удаления: ").strip()
        self.manager.delete_task(task_id=task_id, category=category)
        print("Удаление завершено")

class SearchTasksCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        keyword = input("Введите ключевое слово для поиска: ").strip()
        tasks = self.manager.search_tasks(keyword)
        if not tasks:
            print(f"Задачи с ключевым словом '{keyword}' не найдены")
        for task in tasks:
            print(task.to_dict())

class EditTaskCommand(Command):
    def __init__(self, manager: TaskManager):
        self.manager = manager

    def execute(self):
        try:
            task_id = input("Введите ID задачи для редактирования: ").strip()

            task = self.manager.get_task_by_id(task_id)

            print(f"Редактирование задачи: {task.title} (ID: {task.id})")

            title = input(f"Новое название (текущее: {task.title}): ").strip() or task.title
            description = input(f"Новое описание (текущее: {task.description}): ").strip() or task.description
            category = input(f"Новая категория (текущая: {task.category}): ").strip() or task.category

            due_date = get_valid_date(f"Новый срок выполнения (текущий: {task.due_date}, формат: YYYY-MM-DD): ")
            priority = get_valid_priority(f"Новый приоритет (текущий: {task.priority}, варианты: низкий/средний/высокий): ")

            task.title = title
            task.description = description
            task.category = category
            task.due_date = due_date or task.due_date
            task.priority = priority or task.priority

            print("Задача успешно отредактирована.")

        except Exception as e:
            print(f"Ошибка: ID не существует")

class ExitCommand(Command):
    def execute(self):
        exit()
