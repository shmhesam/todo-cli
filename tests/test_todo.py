import pytest

from todo import cli, core, storage


@pytest.fixture(autouse=True)
def temp_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setenv("TODO_FILE", str(path))
    return path


def test_add_assigns_incrementing_ids():
    tasks = []
    a = core.add_task(tasks, "first")
    b = core.add_task(tasks, "second")
    assert (a["id"], b["id"]) == (1, 2)


def test_add_rejects_empty_title():
    with pytest.raises(ValueError):
        core.add_task([], "   ")


def test_ids_stay_unique_after_removal():
    tasks = []
    core.add_task(tasks, "a")
    core.add_task(tasks, "b")
    core.remove_task(tasks, 1)
    core.add_task(tasks, "c")
    assert len({t["id"] for t in tasks}) == len(tasks)


def test_done_and_undo():
    tasks = []
    core.add_task(tasks, "a")
    assert core.set_done(tasks, 1)["done"] is True
    assert core.set_done(tasks, 1, done=False)["done"] is False


def test_missing_id_raises():
    with pytest.raises(KeyError):
        core.set_done([], 99)


def test_clear_done_and_filter():
    tasks = []
    core.add_task(tasks, "a")
    core.add_task(tasks, "b")
    core.set_done(tasks, 1)
    assert len(core.filter_tasks(tasks, "done")) == 1
    assert len(core.filter_tasks(tasks, "pending")) == 1
    assert core.clear_done(tasks) == 1
    assert len(tasks) == 1


def test_storage_roundtrip_unicode(temp_file):
    tasks = []
    core.add_task(tasks, "خرید نان")
    storage.save(tasks)
    assert storage.load()[0]["title"] == "خرید نان"


def test_corrupted_file_raises(temp_file):
    temp_file.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError):
        storage.load()


def test_cli_end_to_end(capsys):
    assert cli.main(["add", "write", "tests"]) == 0
    assert cli.main(["done", "1"]) == 0
    assert cli.main(["list", "--done"]) == 0
    out = capsys.readouterr().out
    assert "write tests" in out and "[x]" in out


def test_cli_error_exit_code(capsys):
    assert cli.main(["done", "42"]) == 1
    assert "Error" in capsys.readouterr().err
