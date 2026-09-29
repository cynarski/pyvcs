from hashlib import sha256
from pathlib import Path

from pyvcs.repository import Repository
from pyvcs.exceptions import RepositoryNotFoundError

CHUNK_SIZE = 64 * 1024

def hash_file(file_path: Path)-> str:
    digest = sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            digest.update(chunk)

    return digest.hexdigest()

def snapshot_worktree(repo: Repository) -> dict[str, str]:
    snapshot: dict[str, str] = {}

    paths = sorted(
        repo.path.rglob("*"),
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
