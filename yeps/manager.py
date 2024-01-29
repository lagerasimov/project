from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import json

class TaskStatus(Enum):
    Новая = "Новая"
    Выполняется = "Выполняется"
    Ревью = "Ревью"
    Выполнено = "Выполнено"
    Отменено = "Отменено"

@dataclass
class Task:
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    status_changed_at: datetime

    def to_dict(self):
        return asdict(self)

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def change_task_status(self, task_title, new_status):
        for task in self.tasks:
            if task.title == task_title:
                old_status = task.status
                task.status = new_status
                task.status_changed_at = datetime.now()
                return True
        return False

    def cancel_task(self, task_title):
        return self.change_task_status(task_title, TaskStatus.Отменено)

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump(tasks_data, file, default=str)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            tasks_data = json.load(file)
            self.tasks = [Task(**task_data) for task_data in tasks_data]
