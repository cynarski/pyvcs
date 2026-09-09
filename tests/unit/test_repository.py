from pathlib import Path

import pytest

from pyvcs.repository import Repository

pytestmark = pytest.mark.unit  # potem można zrobić pytest -m unit


def test_repository_resolves_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.path == tmp_path.resolve()


def test_repository_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.repo_path == tmp_path / ".vcs"


def test_objects_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.objects_path == tmp_path / ".vcs" / "objects"


def test_branches_path(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.branches_path == tmp_path / ".vcs" / "branches"


def test_index_file(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.index_file == tmp_path / ".vcs" / "index"


def test_head_file(tmp_path):
    repo = Repository(str(tmp_path))

    assert repo.head_file == tmp_path / ".vcs" / "HEAD"
