from hashlib import sha256
from pathlib import Path

from pyvcs.objects import Blob
from pyvcs.repository import Repository

CHUNK_SIZE = 64 * 1024


def hash_file(file_path: Path) -> str:
    data = file_path.read_bytes()
    blob = Blob(data)

    return sha256(blob.serialize()).hexdigest()


def snapshot_worktree(repo: Repository) -> dict[str, str]:
    snapshot: dict[str, str] = {}

    paths = sorted(
        repo.path.rglob("*"),  # find everythin in repo path
        key=lambda path: path.relative_to(repo.path).as_posix(),
    )

    for path in paths:
        if not path.is_file():
            continue

        if repo.repo_path in path.parents:
            continue

        relative_path = path.relative_to(repo.path).as_posix()

        snapshot[relative_path] = hash_file(path)

    return snapshot
