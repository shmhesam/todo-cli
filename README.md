# todo-cli

A tiny command-line to-do manager written in Python. No dependencies, tasks are stored in a simple JSON file.

## Install

```bash
git clone https://github.com/shmhesam/todo-cli.git
cd todo-cli
pip install -e .
```

Requires Python 3.10+. You can also run it without installing: `python -m todo <command>`.

## Usage

```bash
todo add Buy milk          # add a task
todo list                  # list all tasks
todo list --pending        # only pending tasks
todo list --done           # only completed tasks
todo done 1                # mark task #1 as done
todo undo 1                # mark task #1 as not done
todo edit 1 New title      # change the title of task #1
todo remove 1              # delete task #1
todo clear                 # delete all completed tasks
```

Example:

```
$ todo add Write README
Added #1: Write README
$ todo done 1
Updated #1: [x]   1  Write README
```

## Where are tasks stored?

In `~/.todo-cli/tasks.json`. Set the `TODO_FILE` environment variable to use another file.

## Development

```bash
pip install pytest
pytest
```

## Project structure

```
todo/
  cli.py       # argument parsing and output
  core.py      # task logic (pure functions)
  storage.py   # JSON file read/write
tests/
  test_todo.py
```

## License

MIT
