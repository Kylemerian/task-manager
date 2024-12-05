import uuid
from datetime import datetime
from typing import Optional

class Task:
    def __init__(self, title: str, description: str, category: str, 
                 due_date: str, priority: str, status: str = "не выполнена"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self) -> dict:
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
        return Task(
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"]
        )
