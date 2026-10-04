import pytest

from pyvcs.status import Status, compare_snapshots

pytestmark = pytest.mark.unit


def test_empty_index_and_empty_worktree_is_clean():
    result = compare_snapshots({}, {})

    assert result == Status(
        modified=[],
        deleted=[],
        untracked=[],
    )


def test_file_only_in_worktree_is_untracked():
    result = compare_snapshots(
        {},
        {"a.txt": "AAA"},
    )

    assert result == Status(
        modified=[],
        deleted=[],
        untracked=["a.txt"],
    )


def test_same_file_in_index_and_worktree_is_clean():
    result = compare_snapshots(
        {"a.txt": "AAA"},
        {"a.txt": "AAA"},
    )

    assert result == Status(
        modified=[],
        deleted=[],
        untracked=[],
    )


def test_changed_file_is_modified():
    result = compare_snapshots(
        {"a.txt": "AAA"},
        {"a.txt": "BBB"},
    )

    assert result == Status(
        modified=["a.txt"],
        deleted=[],
        untracked=[],
    )


def test_missing_worktree_file_is_deleted():
    result = compare_snapshots(
        {"a.txt": "AAA"},
        {},
    )

    assert result == Status(
        modified=[],
        deleted=["a.txt"],
        untracked=[],
    )


def test_mixed_changes():
    result = compare_snapshots(
        {
            "tracked.txt": "AAA",
            "deleted.txt": "BBB",
        },
        {
            "tracked.txt": "CCC",
            "new.txt": "DDD",
        },
    )

    assert result == Status(
        modified=["tracked.txt"],
        deleted=["deleted.txt"],
        untracked=["new.txt"],
    )