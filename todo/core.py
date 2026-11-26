"""Pure task logic (no printing, no file access)."""

from datetime import datetime


def add_task(tasks: list[dict], title: str) -> dict:
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {
        "id": next_id,
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    return task


def find_task(tasks: list[dict], task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise KeyError(f"No task with id {task_id}.")


def set_done(tasks: list[dict], task_id: int, done: bool = True) -> dict:
    task = find_task(tasks, task_id)
    task["done"] = done
    return task


def remove_task(tasks: list[dict], task_id: int) -> dict:
    task = find_task(tasks, task_id)
    tasks.remove(task)
    return task


def clear_done(tasks: list[dict]) -> int:
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    return before - len(tasks)


def filter_tasks(tasks: list[dict], show: str = "all") -> list[dict]:
    if show == "done":
        return [t for t in tasks if t["done"]]
    if show == "pending":
        return [t for t in tasks if not t["done"]]
    return list(tasks)
