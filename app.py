import sys

from task_manager import TaskManager


def main() -> None:
    manager = TaskManager()

    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "python app.py add 'task'\n"
            "python app.py list\n"
            "python app.py done <id>\n"
            "python app.py delete <id>\n"
            "python app.py reindex"
        )
        return

    command = sys.argv[1]

    try:
        if command == "add":
            description = " ".join(sys.argv[2:])
            task = manager.add_task(description)
            print(f"Tarea #{task['id']} agregada")

        elif command == "list":
            tasks = manager.list_tasks()

            if not tasks:
                print("No hay tareas disponibles.")
                return

            for task in tasks:
                status = "✓" if task["done"] else "X"
                print(f"#{task['id']} - [{status}] {task['description']}")

        elif command == "done":
            task_id = int(sys.argv[2])
            manager.complete_task(task_id)
            print(f"Tarea #{task_id} completada.")

        elif command == "delete":
            task_id = int(sys.argv[2])
            manager.delete_task(task_id)
            print(f"Tarea #{task_id} borrada.")

        elif command == "reindex":
            manager.reindex_tasks()
            print("Tareas renumeradas.")
        else:
            print("Unknown command.")

    except (ValueError, IndexError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
