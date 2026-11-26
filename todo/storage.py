"""Reading and writing tasks to a JSON file."""

import json
import os
import tempfile
from pathlib import Path


def default_path() -> Path:
    """Return the tasks file path (override with the TODO_FILE env var)."""
    env = os.environ.get("TODO_FILE")
    if env:
        return Path(env)
    return Path.home() / ".todo-cli" / "tasks.json"


def load(path: Path | None = None) -> list[dict]:
    path = path or default_path()
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Tasks file is corrupted: {path}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Tasks file has an unexpected format: {path}")
    return data


def save(tasks: list[dict], path: Path | None = None) -> None:
    path = path or default_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write to a temp file first so a crash can't corrupt the real file.
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
