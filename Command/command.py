from abc import ABC, abstractmethod
from TaskManager.taskManager import *
from Validation.validation import *

class Command(ABC):
    """Абстрактный класс для команд. Все команды должны реализовывать метод execute()."""
    @abstractmethod
    def execute(self):
        pass

class ViewTasksCommand(Command):
    """Команда для просмотра всех задач."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.
        
        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Выполняет просмотр всех задач.

        Получает все задачи из менеджера задач и выводит их. Если задач нет, выводится сообщение о пустом списке.
        """
        tasks = self.manager.view_tasks()
        if not tasks:
            print("Список задач пуст")
        for task in tasks:
            print(task.to_dict())
            
class ViewTasksByCategoryCommand(Command):
    """Команда для просмотра задач по категории."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.
        
        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Выполняет просмотр задач по указанной категории.

        Запрашивает у пользователя категорию и получает все задачи из менеджера задач для указанной категории.
        Если задач в категории нет, выводится соответствующее сообщение.
        """
        category = input("Введите категорию: ").strip()
        tasks = self.manager.view_tasks(category=category)
        if not tasks:
            print(f"Задачи в категории '{category}' не найдены")
        for task in tasks:
            print(task.to_dict())

class AddTaskCommand(Command):
    """Команда для добавления новой задачи."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.

        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Добавляет новую задачу.

        Запрашивает у пользователя данные для новой задачи (название, описание, категорию, срок выполнения, приоритет).
        Создает задачу и добавляет её в список задач в менеджере.
        Если введены некорректные данные, выводится сообщение об ошибке.
        """
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
    """Команда для пометки задачи как выполненной."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.

        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Помечает задачу как выполненную.

        Запрашивает у пользователя ID задачи и помечает задачу с этим ID как выполненную.
        Если задача с данным ID не найдена, выводится сообщение об ошибке.
        """
        task_id = input("Введите ID задачи: ").strip()
        if self.manager.mark_completed(task_id):
            print("Задача выполнена")
        else:
            print("Задача не найдена")

class DeleteTaskCommand(Command):
    """Команда для удаления задачи."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.

        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Удаляет задачу по ID или по категории.

        Запрашивает ID задачи или категорию для удаления. Если указан ID, удаляется задача с данным ID,
        если категории — удаляются все задачи из указанной категории.
        """
        task_id = input("Введите ID задачи (или оставьте пустым для удаления по категории): ").strip()
        category = None
        if not task_id:
            category = input("Введите категорию для удаления: ").strip()
        self.manager.delete_task(task_id=task_id, category=category)
        print("Удаление завершено")

class SearchTasksCommand(Command):
    """Команда для поиска задач по ключевому слову."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.

        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Ищет задачи по ключевому слову.

        Запрашивает у пользователя ключевое слово и ищет задачи, в которых это слово встречается
        в названии, описании или категории. Если такие задачи не найдены, выводится сообщение.
        """
        keyword = input("Введите ключевое слово для поиска: ").strip()
        tasks = self.manager.search_tasks(keyword)
        if not tasks:
            print(f"Задачи с ключевым словом '{keyword}' не найдены")
        for task in tasks:
            print(task.to_dict())

class EditTaskCommand(Command):
    """Команда для редактирования задачи."""
    def __init__(self, manager: TaskManager):
        """Инициализация команды с менеджером задач.

        :param manager: Менеджер задач, который управляет задачами.
        """
        self.manager = manager

    def execute(self):
        """Редактирует существующую задачу.

        Запрашивает у пользователя ID задачи и позволяет редактировать название, описание, категорию, срок выполнения
        и приоритет задачи. После редактирования сохраняет изменения в менеджере задач.
        Если задача с данным ID не найдена, выводится сообщение об ошибке.
        """
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
            self.manager.save_tasks()

            print("Задача успешно отредактирована.")

        except Exception as e:
            print(f"Ошибка: ID не существует")

class ExitCommand(Command):
    """Команда для выхода из программы."""
    def execute(self):
        exit()
