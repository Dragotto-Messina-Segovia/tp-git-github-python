import json
from pathlib import Path

import pytest

from task_manager import TaskManager


def _manager(tmp_path: Path) -> TaskManager:
    return TaskManager(file_path=tmp_path / "tasks.json")


# --- carga / persistencia ---


def test_new_manager_starts_empty(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    assert manager.list_tasks() == []


def test_add_task_persists_to_disk(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    manager = TaskManager(file_path=path)
    manager.add_task("Estudiar Git")

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data == [{"id": 1, "description": "Estudiar Git", "done": False}]


def test_tasks_are_reloaded_from_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    TaskManager(file_path=path).add_task("Tarea previa")

    reloaded = TaskManager(file_path=path)
    assert [task["description"] for task in reloaded.list_tasks()] == ["Tarea previa"]


# --- add_task ---


def test_add_task_returns_created_task(tmp_path: Path) -> None:
    task = _manager(tmp_path).add_task("Comprar pan")
    assert task == {"id": 1, "description": "Comprar pan", "done": False}


def test_add_task_assigns_incremental_ids(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    first = manager.add_task("A")
    second = manager.add_task("B")
    assert (first["id"], second["id"]) == (1, 2)


def test_add_task_id_is_max_plus_one_after_delete(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    manager.add_task("A")  # id 1
    manager.add_task("B")  # id 2
    manager.delete_task(1)
    third = manager.add_task("C")
    assert third["id"] == 3


@pytest.mark.parametrize("description", ["", "   ", "\n\t"])
def test_add_task_rejects_blank_description(tmp_path: Path, description: str) -> None:
    manager = _manager(tmp_path)
    with pytest.raises(ValueError, match="no puede estar vacía"):
        manager.add_task(description)


# --- complete_task ---


def test_complete_task_marks_done(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    manager.add_task("Tarea")
    completed = manager.complete_task(1)
    assert completed["done"] is True


def test_complete_task_unknown_id_raises(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    with pytest.raises(ValueError, match="no encontrada"):
        manager.complete_task(99)


# --- delete_task ---


def test_delete_task_removes_it(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    manager.add_task("Tarea")
    manager.delete_task(1)
    assert manager.list_tasks() == []


def test_delete_task_unknown_id_raises(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    with pytest.raises(ValueError, match="no encontrada"):
        manager.delete_task(1)


# --- reindex_tasks ---


def test_reindex_tasks_renumbers_sequentially(tmp_path: Path) -> None:
    manager = _manager(tmp_path)
    manager.add_task("A")  # id 1
    manager.add_task("B")  # id 2
    manager.add_task("C")  # id 3
    manager.delete_task(2)
    manager.reindex_tasks()
    assert [task["id"] for task in manager.list_tasks()] == [1, 2]


def test_reindex_tasks_persists_changes(tmp_path: Path) -> None:
    path = tmp_path / "tasks.json"
    manager = TaskManager(file_path=path)
    manager.add_task("A")
    manager.add_task("B")
    manager.delete_task(1)
    manager.reindex_tasks()

    data = json.loads(path.read_text(encoding="utf-8"))
    assert [task["id"] for task in data] == [1]
