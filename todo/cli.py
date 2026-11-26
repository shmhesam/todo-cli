"""Command-line interface."""

import argparse
import sys

from . import __version__, core, storage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo", description="A tiny command-line to-do manager."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a new task")
    p_add.add_argument("title", nargs="+", help="task title")

    p_list = sub.add_parser("list", help="list tasks")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--done", action="store_true", help="only completed tasks")
    group.add_argument("--pending", action="store_true", help="only pending tasks")

    for name, text in (
        ("done", "mark a task as done"),
        ("undo", "mark a task as not done"),
        ("remove", "delete a task"),
    ):
        p = sub.add_parser(name, help=text)
        p.add_argument("id", type=int, help="task id")

    p_edit = sub.add_parser("edit", help="change a task's title")
    p_edit.add_argument("id", type=int, help="task id")
    p_edit.add_argument("title", nargs="+", help="new title")

    sub.add_parser("clear", help="delete all completed tasks")
    return parser


def format_task(task: dict) -> str:
    mark = "x" if task["done"] else " "
    return f"[{mark}] {task['id']:>3}  {task['title']}"


def run(args: argparse.Namespace) -> int:
    tasks = storage.load()

    if args.command == "add":
        task = core.add_task(tasks, " ".join(args.title))
        storage.save(tasks)
        print(f"Added #{task['id']}: {task['title']}")

    elif args.command == "list":
        show = "done" if args.done else "pending" if args.pending else "all"
        shown = core.filter_tasks(tasks, show)
        if not shown:
            print("No tasks.")
        for task in shown:
            print(format_task(task))

    elif args.command in ("done", "undo"):
        task = core.set_done(tasks, args.id, done=args.command == "done")
        storage.save(tasks)
        print(f"Updated #{task['id']}: {format_task(task)}")

    elif args.command == "edit":
        task = core.edit_task(tasks, args.id, " ".join(args.title))
        storage.save(tasks)
        print(f"Updated #{task['id']}: {format_task(task)}")

    elif args.command == "remove":
        task = core.remove_task(tasks, args.id)
        storage.save(tasks)
        print(f"Removed #{task['id']}: {task['title']}")

    elif args.command == "clear":
        count = core.clear_done(tasks)
        storage.save(tasks)
        print(f"Removed {count} completed task(s).")

    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except (ValueError, KeyError) as exc:
        message = exc.args[0] if exc.args else str(exc)
        print(f"Error: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
