import json
from pathlib import Path
from typing import TypedDict


class Task(TypedDict):
    id: int
    description: str
    done: bool


class TaskManager:
    def __init__(self, file_path: str | Path = "tasks.json") -> None:
        self.file_path = Path(file_path)
        self.tasks: list[Task] = self._load_tasks()

    def _load_tasks(self) -> list[Task]:
        if not self.file_path.exists():
            return []

        with open(self.file_path, encoding="utf-8") as file:
            tasks: list[Task] = json.load(file)
            return tasks

    def _save_tasks(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, description: str) -> Task:
        if not description.strip():
            raise ValueError("La descripción de una tarea no puede estar vacía")

        next_id = max(task["id"] for task in self.tasks) + 1 if self.tasks else 1

        task: Task = {
            "id": next_id,
            "description": description,
            "done": False,
        }

        self.tasks.append(task)
        self._save_tasks()

        return task

    def list_tasks(self) -> list[Task]:
        return self.tasks

    def complete_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task["id"] == task_id:
                task["done"] = True
                self._save_tasks()
                return task

        raise ValueError("Tarea no encontrada")

    def delete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self._save_tasks()
                return

        raise ValueError("Tarea no encontrada")

    def reindex_tasks(self) -> None:
        for index, task in enumerate(self.tasks, start=1):
            task["id"] = index

        self._save_tasks()
