import json
from typing import List, Optional
from Task.task import *

class TaskManager:
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.storage_file, "r") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        except FileNotFoundError:
            return []

    def save_tasks(self):
        with open(self.storage_file, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def view_tasks(self, category: Optional[str] = None) -> List[Task]:
        if category:
            return [task for task in self.tasks if task.category == category]
        return self.tasks

    def search_tasks(self, keyword: str) -> List[Task]:
        return [
            task for task in self.tasks
            if (
                keyword.lower() in task.title.lower() or
                keyword.lower() in task.description.lower() or
                keyword.lower() in task.category.lower()
            )
        ]
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Поиск задачи по ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_completed(self, task_id: str):
        for task in self.tasks:
            if task.id == task_id:
                task.status = "выполнена"
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: Optional[str] = None, category: Optional[str] = None):
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        self.save_tasks()
