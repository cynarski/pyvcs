import json

from pyvcs.repository import Repository


def read_index(repo: Repository) -> dict[str, str]:
    if not repo.index_file.exists():
        return {}

    content = repo.index_file.read_text(encoding='utf-8')

    if not content.strip():
        return {}

    return json.loads(content)


def write_index(repo: Repository, snapshot: dict[str, str]) -> None:
    repo.index_file.write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )