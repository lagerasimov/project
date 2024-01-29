from dataclasses import dataclass
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


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.history = []

    def add_task(self, task):
        self.tasks.append(task)
        self.history.append(f"Добавлена задача '{task.title}' ({task.status.value}). Описание: {task.description}, "
                            f"Время создания: {task.created_at}, Время изменения статуса: {task.status_changed_at}")

    def change_task_status(self, task_title, new_status):
        for task in self.tasks:
            if task.title == task_title:
                old_status = task.status
                task.status = new_status
                task.status_changed_at = datetime.now()
                self.history.append(f"Статус задачи '{task.title}' изменен с '{old_status.value}' на '{new_status.value}'. "
                                    f"Описание: {task.description}, Время создания: {task.created_at}, "
                                    f"Время изменения статуса: {task.status_changed_at}")
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
