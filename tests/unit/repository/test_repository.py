from pathlib import Path

import pytest

from pyvcs.repository import Repository
from pyvcs.exceptions import RepositoryNotFoundError

pytestmark = pytest.mark.unit  # potem można zrobić pytest -m unit


def test_repository_resolves_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.path == tmp_path.resolve()


def test_repository_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.repo_path == tmp_path / ".pyvcs"


def test_objects_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.objects_path == tmp_path / ".pyvcs" / "objects"


def test_branches_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.branches_path == tmp_path / ".pyvcs" / "branches"


def test_index_file(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.index_file == tmp_path / ".pyvcs" / "index"


def test_head_file(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.head_file == tmp_path / ".pyvcs" / "HEAD"


def test_init_creates_suitable_dirs_and_files(tmp_path):
    repo = Repository.init(str(tmp_path))

    assert repo.repo_path.is_dir()
    assert repo.objects_path.is_dir()
    assert repo.branches_path.is_dir()
    assert repo.head_file.is_file()
    assert repo.head_file.read_text(encoding="utf-8") == "master\n"
    assert not repo.index_file.exists()


def test_reinit_does_not_overwrite_head(tmp_path):
    repo = Repository.init(str(tmp_path))

    repo.head_file.write_text(
        "feature-login\n",
        encoding="utf-8",
    )

    Repository.init(str(tmp_path))

    assert repo.head_file.read_text(encoding="utf-8") == "feature-login\n"


def test_init_does_not_modify_existing_files(tmp_path):
    file = tmp_path / "example.txt"
    file.write_text("hello", encoding="utf-8")

    Repository.init(str(tmp_path))

    assert file.read_text(encoding="utf-8") == "hello"