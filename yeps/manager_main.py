from manager import TaskManager, Task, TaskStatus
from datetime import datetime
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument("file_path", help="Path to the JSON file for tasks")
    args = parser.parse_args()

    task_manager = TaskManager()

    try:
        task_manager.load_from_file(args.file_path)
        print("Задачи успешно загружены из файла.")
    except FileNotFoundError:
        print("Файл с задачами не найден. Создан новый файл.")

    while True:
        print("\nВыберите действие:")
        print("1. Добавить задачу")
        print("2. Изменить статус задачи")
        print("3. Отменить задачу")
        print("4. Просмотр задач")
        print("5. Сохранить и выйти")

        choice = input("Ваш выбор: ")

        if choice == "1":
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            status = input("Введите статус задачи (Новая, Выполняется, Ревью, Выполнено, Отменено): ")
            if status not in TaskStatus.__members__:
                print("Неверный статус. Используйте один из следующих: Новая, Выполняется, Ревью, Выполнено, Отменено")
                continue
            task_manager.add_task(Task(title=title, description=description, status=TaskStatus[status],
                                       created_at=datetime.now(), status_changed_at=datetime.now()))
            print("Задача успешно добавлена.")
        elif choice == "2":
            task_title = input("Введите название задачи для изменения статуса: ")
            new_status = input("Введите новый статус задачи: ")
            if new_status not in TaskStatus.__members__:
                print("Неверный статус. Используйте один из следующих: Новая, Выполняется, Ревью, Выполнено, Отменено")
                continue
            if task_manager.change_task_status(task_title, TaskStatus[new_status]):
                print(f"Статус задачи '{task_title}' успешно изменен на '{new_status}'.")
            else:
                print(f"Задача с названием '{task_title}' не найдена.")
        elif choice == "3":
            task_title = input("Введите название задачи для отмены: ")
            if task_manager.cancel_task(task_title):
                print(f"Задача '{task_title}' успешно отменена.")
            else:
                print(f"Задача с названием '{task_title}' не найдена.")
        elif choice == "4":
            for task in task_manager.tasks:
                print(f"{task.title} ({task.status.value})")
                print(f"Описание: {task.description}")
                print(f"Дата создания: {task.created_at}")
                print(f"Дата изменения статуса: {task.status_changed_at}")
                print()
        elif choice == "5":
            task_manager.save_to_file(args.file_path)
            print("Задачи успешно сохранены в файл.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите существующее действие.")
