import pytest

from pyvcs.object_store import ObjectStore
from pyvcs.repository import Repository

pytestmark = pytest.mark.unit

def test_exists_returns_true_for_existing_object(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    object_id = store.write(b"hello")

    assert store.exists(object_id) is True


def test_exists_returns_false_for_missing_object(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    assert store.exists("a" * 64) is False