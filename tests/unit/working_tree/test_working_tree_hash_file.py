import pytest

from pyvcs.repository import Repository
from pyvcs.working_tree import hash_file, snapshot_worktree

pytestmark = pytest.mark.unit


def test_empty_working_tree(tmp_path):
    repo = Repository.init(str(tmp_path))

    assert snapshot_worktree(repo) == {}


def test_working_tree_with_one_file(tmp_path):
    repo = Repository.init(str(tmp_path))

    file_path = tmp_path / "a.txt"
    file_path.write_text("hello", encoding="utf-8")

    assert snapshot_worktree(repo) == {
        "a.txt": hash_file(file_path),
    }


def test_working_tree_with_nested_file(tmp_path):
    repo = Repository.init(str(tmp_path))

    directory = tmp_path / "src"
    directory.mkdir()

    file_path = directory / "main.py"
    file_path.write_text("print('hello')", encoding="utf-8")

    assert snapshot_worktree(repo) == {
        "src/main.py": hash_file(file_path),
    }


def test_working_tree_with_multiple_files(tmp_path):
    repo = Repository.init(str(tmp_path))

    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"

    a.write_text("AAA", encoding="utf-8")
    b.write_text("BBB", encoding="utf-8")

    assert snapshot_worktree(repo) == {
        "a.txt": hash_file(a),
        "b.txt": hash_file(b),
    }


def test_repository_directory_is_ignored(tmp_path):
    repo = Repository.init(str(tmp_path))

    normal_file = tmp_path / "a.txt"
    normal_file.write_text("AAA", encoding="utf-8")

    internal_file = repo.repo_path / "internal"
    internal_file.write_text("should be ignored", encoding="utf-8")

    snapshot = snapshot_worktree(repo)

    assert "a.txt" in snapshot
    assert ".pyvcs/internal" not in snapshot


def test_binary_file(tmp_path):
    repo = Repository.init(str(tmp_path))

    file_path = tmp_path / "binary.bin"
    file_path.write_bytes(b"\x00\x01\x02\xff")

    assert snapshot_worktree(repo) == {
        "binary.bin": hash_file(file_path),
    }


def test_content_change_changes_hash(tmp_path):
    repo = Repository.init(str(tmp_path))

    file_path = tmp_path / "a.txt"
    file_path.write_text("before", encoding="utf-8")

    before = snapshot_worktree(repo)["a.txt"]

    file_path.write_text("after", encoding="utf-8")

    after = snapshot_worktree(repo)["a.txt"]

    assert before != after