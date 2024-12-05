import json
from typing import List, Optional
from Task.task import *

class TaskManager:
    """
    Класс для управления задачами, включая загрузку, сохранение, добавление, просмотр,
    поиск, редактирование и удаление задач.

    Атрибуты:
        storage_file (str): Имя файла для хранения задач в формате JSON.
        tasks (List[Task]): Список задач, загруженных из файла.

    Методы:
        load_tasks(): Загружает задачи из файла в список.
        save_tasks(): Сохраняет список задач в файл.
        add_task(task: Task): Добавляет новую задачу в список.
        view_tasks(category: Optional[str] = None): Просматривает все задачи или задачи по категории.
        search_tasks(keyword: str): Ищет задачи по ключевому слову (в названии, описании или категории).
        get_task_by_id(task_id: str) -> Optional[Task]: Возвращает задачу по уникальному ID.
        mark_completed(task_id: str): Помечает задачу как выполненную.
        delete_task(task_id: Optional[str] = None, category: Optional[str] = None): Удаляет задачу по ID или категории.
    """

    def __init__(self, storage_file: str = "tasks.json"):
        """
        Инициализирует менеджер задач с указанием файла для хранения данных.

        Аргументы:
            storage_file (str): Имя файла для хранения задач (по умолчанию "tasks.json").
        """
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        """
        Загружает задачи из JSON-файла.

        Возвращает:
            List[Task]: Список задач, загруженных из файла. Если файл не найден, возвращается пустой список.
        """
        try:
            with open(self.storage_file, "r") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        """
        Сохраняет текущий список задач в JSON-файл.

        Задачи сохраняются в файл в формате JSON.
        """
        with open(self.storage_file, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, task: Task):
        """
        Добавляет новую задачу в список и сохраняет изменения.

        Аргументы:
            task (Task): Задача, которую нужно добавить.
        """
        self.tasks.append(task)
        self.save_tasks()

    def view_tasks(self, category: Optional[str] = None) -> List[Task]:
        """
        Просматривает все задачи или задачи по заданной категории.

        Аргументы:
            category (Optional[str]): Категория, по которой нужно фильтровать задачи. По умолчанию все задачи.

        Возвращает:
            List[Task]: Список задач (или задачи по категории, если задан фильтр).
        """
        if category:
            return [task for task in self.tasks if task.category == category]
        return self.tasks

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Ищет задачи по ключевому слову в названии, описании или категории.

        Аргументы:
            keyword (str): Ключевое слово для поиска в задачах.

        Возвращает:
            List[Task]: Список задач, в которых встречается ключевое слово.
        """
        return [
            task for task in self.tasks
            if (
                keyword.lower() in task.title.lower() or
                keyword.lower() in task.description.lower() or
                keyword.lower() in task.category.lower()
            )
        ]
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Возвращает задачу по уникальному ID.

        Аргументы:
            task_id (str): Уникальный идентификатор задачи.

        Возвращает:
            Optional[Task]: Задача с данным ID или None, если задача не найдена.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_completed(self, task_id: str):
        """
        Помечает задачу как выполненную по ее уникальному ID.

        Аргументы:
            task_id (str): Уникальный идентификатор задачи для пометки как выполненной.

        Возвращает:
            bool: True, если задача была помечена как выполненная, иначе False.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.status = "выполнена"
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: Optional[str] = None, category: Optional[str] = None):
        """
        Удаляет задачу по ID или по категории.

        Аргументы:
            task_id (Optional[str]): Уникальный идентификатор задачи для удаления.
            category (Optional[str]): Категория, по которой нужно удалять задачи. Если указана категория, удаляются все задачи из этой категории.
        """
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        self.save_tasks()
