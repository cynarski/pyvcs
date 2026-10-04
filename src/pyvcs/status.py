from dataclasses import dataclass

from pyvcs.index import read_index
from pyvcs.repository import Repository
from pyvcs.working_tree import snapshot_worktree


@dataclass(frozen=True)
class Status:
    modified: list[str]
    deleted: list[str]
    untracked: list[str]


def compare_snapshots(index: dict[str, str], worktree: dict[str, str]) -> Status:
    modified, deleted, untracked = [], [], []

    for path, worktree_hash in worktree.items():
        if path not in index:
            untracked.append(path)
        elif index[path] != worktree_hash:
            modified.append(path)

    for path in index:
        if path not in worktree:
            deleted.append(path)

    return Status(
        modified=sorted(modified),
        deleted=sorted(deleted),
        untracked=sorted(untracked),
    )


def get_status(repo: Repository) -> Status:
    index = read_index(repo)
    worktree = snapshot_worktree(repo)

    return compare_snapshots(index, worktree)
