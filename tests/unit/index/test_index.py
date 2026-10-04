import pytest

from pyvcs.index import read_index, write_index
from pyvcs.repository import Repository

pytestmark = pytest.mark.unit


def test_missing_index_returns_empty_dict(tmp_path):
    repo = Repository(str(tmp_path))

    assert read_index(repo) == {}


def test_empty_index_returns_empty_dict(tmp_path):
    repo = Repository.init(str(tmp_path))
    repo.index_file.write_text("", encoding="utf-8")

    assert read_index(repo) == {}


def test_write_and_read_index(tmp_path):
    repo = Repository.init(str(tmp_path))

    snapshot = {
        "a.txt": "AAA",
        "b.txt": "BBB",
    }

    write_index(repo, snapshot)

    assert read_index(repo) == snapshot


def test_index_json_is_sorted(tmp_path):
    repo = Repository.init(str(tmp_path))

    write_index(
        repo,
        {
            "z.txt": "ZZZ",
            "a.txt": "AAA",
            "m.txt": "MMM",
        },
    )

    content = repo.index_file.read_text(encoding="utf-8")

    assert content.index('"a.txt"') < content.index('"m.txt"')
    assert content.index('"m.txt"') < content.index('"z.txt"')