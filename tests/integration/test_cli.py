"""Exercise the installed CLI from a directory outside the project."""

import subprocess

import pytest

pytestmark = pytest.mark.integration


def invoke(tmp_path, *arguments):
    return subprocess.run(
        ["pyvcs", *arguments],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )


def test_help(tmp_path):
    result = invoke(tmp_path, "--help")
    assert result.returncode == 0
    assert result.stdout.count("usage:") == 1
    assert "init" in result.stdout
    assert result.stderr == ""


def test_no_arguments(tmp_path):
    result = invoke(tmp_path)
    assert result.returncode == 0
    assert result.stdout.count("usage:") == 1
    assert result.stderr == ""


def test_unknown_command(tmp_path):
    result = invoke(tmp_path, "unknown")
    assert result.returncode == 2
    assert "invalid choice" in result.stderr
