from pathlib import Path

import pytest

from pyvcs.repository import Repository
from pyvcs.exceptions import RepositoryNotFoundError

pytestmark = pytest.mark.unit  # potem można zrobić pytest -m unit

def test_init_creates_missing_worktree(tmp_path):
    project_path = tmp_path / "my-project"

    repo = Repository.init(str(project_path))

    assert repo.path.is_dir()


def test_find_repository_from_root(tmp_path):
    expected_repo = Repository.init(str(tmp_path))

    found_repo = Repository.find(str(tmp_path))

    assert found_repo.path == expected_repo.path


def test_find_repository_from_subdirectory(tmp_path):
    Repository.init(str(tmp_path))

    nested_directory = tmp_path / "src" / "pyvcs"
    nested_directory.mkdir(parents=True)

    repo = Repository.find(str(nested_directory))

    assert repo.path == tmp_path.resolve()


def test_find_raises_when_repository_does_not_exist(tmp_path):
    with pytest.raises(RepositoryNotFoundError):
        Repository.find(str(tmp_path))


def test_find_repository_from_file(tmp_path):
    Repository.init(str(tmp_path))

    source_file = tmp_path / "src" / "app.py"
    source_file.parent.mkdir()
    source_file.write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    repo = Repository.find(str(source_file))

    assert repo.path == tmp_path.resolve()


def test_find_returns_nearest_repository(tmp_path):
    Repository.init(str(tmp_path))

    inner = tmp_path / "projects" / "inner"
    Repository.init(str(inner))

    nested = inner / "src"
    nested.mkdir()

    repo = Repository.find(str(nested))

    assert repo.path == inner.resolve()