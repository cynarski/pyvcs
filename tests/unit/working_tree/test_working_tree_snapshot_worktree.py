from pyvcs.repository import Repository
from pyvcs.working_tree import hash_file, snapshot_worktree


def test_snapshot_contains_file(tmp_path):
    repo = Repository.init(str(tmp_path))

    file_path = tmp_path / "hello.txt"
    file_path.write_text("hello", encoding="utf-8")

    snapshot = snapshot_worktree(repo)

    assert snapshot == {
        "hello.txt": hash_file(file_path),
    }


def test_snapshot_contains_nested_file(tmp_path):
    repo = Repository.init(str(tmp_path))

    source_dir = tmp_path / "src"
    source_dir.mkdir()

    file_path = source_dir / "app.py"
    file_path.write_text("print('hello')", encoding="utf-8")

    snapshot = snapshot_worktree(repo)

    assert snapshot == {
        "src/app.py": hash_file(file_path),
    }


def test_snapshot_ignores_repository_metadata(tmp_path):
    repo = Repository.init(str(tmp_path))

    file_path = tmp_path / "hello.txt"
    file_path.write_text("hello", encoding="utf-8")

    snapshot = snapshot_worktree(repo)

    assert "hello.txt" in snapshot
    assert ".pyvcs/HEAD" not in snapshot

    assert all(
        not path.startswith(".pyvcs/")
        for path in snapshot
    )

def test_empty_worktree_returns_empty_snapshot(tmp_path):
    repo = Repository.init(str(tmp_path))

    snapshot = snapshot_worktree(repo)

    assert snapshot == {}