from pathlib import Path

import pytest

import app


def _run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *argv: str,
) -> None:
    # La app usa "tasks.json" en el directorio actual: lo aislamos en tmp_path.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["app.py", *argv])
    app.main()


def test_no_args_prints_usage(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path)
    assert "Usage" in capsys.readouterr().out


def test_add_command_creates_task(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "add", "Estudiar", "Git")
    assert "Tarea #1 agregada" in capsys.readouterr().out
    assert (tmp_path / "tasks.json").exists()


def test_list_command_when_empty(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "list")
    assert "No hay tareas disponibles." in capsys.readouterr().out


def test_list_command_shows_tasks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "add", "Tarea uno")
    capsys.readouterr()
    _run(monkeypatch, tmp_path, "list")
    out = capsys.readouterr().out
    assert "#1" in out
    assert "Tarea uno" in out


def test_done_command_completes_task(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "add", "Tarea")
    capsys.readouterr()
    _run(monkeypatch, tmp_path, "done", "1")
    assert "completada" in capsys.readouterr().out


def test_delete_command_removes_task(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "add", "Tarea")
    capsys.readouterr()
    _run(monkeypatch, tmp_path, "delete", "1")
    assert "borrada" in capsys.readouterr().out


def test_reindex_command(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "reindex")
    assert "renumeradas" in capsys.readouterr().out


def test_unknown_command(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "frobnicate")
    assert "Unknown command." in capsys.readouterr().out


def test_done_with_unknown_id_prints_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "done", "99")
    assert "Error:" in capsys.readouterr().out


def test_done_without_id_prints_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _run(monkeypatch, tmp_path, "done")
    assert "Error:" in capsys.readouterr().out
