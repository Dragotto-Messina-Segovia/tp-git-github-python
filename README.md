# TP Git + Github en Python

Proyecto para practicar un flujo colaborativo completo en Git y GitHub, y configurar un CI básico para feedback temprano.

# Task Manager

Aplicación mínima en Python para gestionar tareas desde línea de comandos.
Permite agregar, listar, completar, borrar y renumerar tareas guardadas en un archivo JSON local.

## Requisitos

- Python 3.11+

## Setup (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```bash
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Setup (Linux / macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Ejecutar la app

```bash
# muestra ayuda de comandos
python app.py

# agregar tarea
python app.py add "Estudiar Git y GitHub"

# listar tareas
python app.py list

# marcar tarea como completada
python app.py done 1

# borrar tarea
python app.py delete 1

# renumerar IDs de tareas
python app.py reindex
```

Las tareas se persisten en `tasks.json` en el directorio del proyecto.

## Formato, lint y tipos

```bash
# formatea el código
python -m ruff format .

# verifica formato sin modificar (como en CI)
python -m ruff format --check .

# linter rápido (pyflakes, pycodestyle, isort, etc.)
python -m ruff check .

# chequeo de tipos (modo strict)
python -m mypy app.py task_manager.py

# linter más exhaustivo
python -m pylint app.py task_manager.py tests/
```

## Tests

Los tests están en `tests/` y se ejecutan con `pytest`. La cobertura se mide
sobre `task_manager.py` y `app.py`, con un umbral mínimo del 80% (configurado en
`pyproject.toml`).

```bash
# corre todos los tests con reporte de cobertura
python -m pytest

# falla cuando la cobertura es < 80%
python -m pytest --cov-fail-under=80
```


## CI (GitHub Actions)

El workflow de CI está en `.github/workflows/ci_quality_gate.yml` y valida los Pull Requests a `dev` y `main`, además de los pushes a `main`.

## Flujo de trabajo con Git

- Base de trabajo en `dev`.
- Cada cambio se realiza en una rama corta a partir de `dev`, con prefijos como `feat/...` o `fix/...`.
- Toda integración de features/fixes se hace mediante Pull Request hacia `dev`.
- Cada PR debe ser revisado y aprobado por otro integrante antes del merge.
- Para liberar versión, se mergea `dev` hacia `main`.
- Formato de commits usado por el equipo: `<tipo>[<contexto>] : <descripción>`.

## Integrantes

- Dragotto Santiago
- Messina Nicolás
- Segovia Máximo