import pytest

from pyvcs.cli import main

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
