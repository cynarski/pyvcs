import pytest

from pyvcs.cli import main
from pyvcs.repository import Repository

pytestmark = pytest.mark.unit  # potem można zrobić pytest -m unit


def test_with_standard_command(capsys):
    exit_code = main(["init"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Initialized empty PyVCS repository in" in captured.out


def test_without_command_displays_help(capsys):
    exit_code = main([])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "usage:" in captured.out
    assert "init" in captured.out


def test_help_exits_successfully(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    assert exc_info.value.code == 0

    captured = capsys.readouterr()

    assert "Python project version control system" in captured.out
    assert "init" in captured.out


def test_unknown_command_fails(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["unknown"])

    assert exc_info.value.code == 2

    captured = capsys.readouterr()

    assert "usage:" in captured.err

def test_status_outside_repository_returns_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = main(["status"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "fatal: not a PyVCS repository\n"

def test_status_inside_repository_returns_success(tmp_path, monkeypatch, capsys):
    Repository.init(str(tmp_path))
    monkeypatch.chdir(tmp_path)

    exit_code = main(["status"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Nothing to commit, working tree clean" in captured.out


def test_status_with_changes_still_returns_success(tmp_path, monkeypatch, capsys):
    Repository.init(str(tmp_path))
    (tmp_path / "new.txt").write_text("hello", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["status"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "new.txt" in captured.out