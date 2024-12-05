import uuid

class Task:
    """
    Класс для представления задачи. Каждый объект задачи имеет уникальный идентификатор и данные,
    такие как название, описание, категория, срок выполнения, приоритет и статус.

    Атрибуты:
        id (str): Уникальный идентификатор задачи (UUID).
        title (str): Название задачи.
        description (str): Описание задачи.
        category (str): Категория задачи.
        due_date (str): Срок выполнения задачи в формате "YYYY-MM-DD".
        priority (str): Приоритет задачи ("низкий", "средний", "высокий").
        status (str): Статус задачи ("не выполнена" или "выполнена").

    Методы:
        __init__(self, title: str, description: str, category: str, 
                 due_date: str, priority: str, status: str = "не выполнена"): 
            Конструктор для создания новой задачи с уникальным идентификатором.
        
        to_dict(self) -> dict:
            Преобразует объект задачи в словарь для сериализации.

        from_dict(data: dict) -> "Task":
            Статический метод для создания объекта задачи из словаря.
    """
    
    def __init__(self, title: str, description: str, category: str, 
                 due_date: str, priority: str, status: str = "не выполнена"):
        """
        Конструктор для создания новой задачи с уникальным идентификатором.

        Аргументы:
            title (str): Название задачи.
            description (str): Описание задачи.
            category (str): Категория задачи.
            due_date (str): Срок выполнения задачи в формате "YYYY-MM-DD".
            priority (str): Приоритет задачи ("низкий", "средний", "высокий").
            status (str, опционально): Статус задачи. По умолчанию "не выполнена".
        """
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self) -> dict:
        """
        Преобразует объект задачи в словарь для сериализации.

        Возвращает:
            dict: Словарь, представляющий объект задачи.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """
        Статический метод для создания объекта задачи из словаря.

        Аргументы:
            data (dict): Словарь, содержащий данные задачи.

        Возвращает:
            Task: Новый объект задачи, созданный из словаря.
        """
        return Task(
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"]
        )
