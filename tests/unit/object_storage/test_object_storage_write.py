import pytest

from pyvcs.exceptions import ObjectNotFoundError
from pyvcs.object_store import ObjectStore
from pyvcs.repository import Repository

pytestmark = pytest.mark.unit  # potem można zrobić pytest -m unit

def test_write_returns_object_id(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    object_id = store.write(b"hello")

    assert isinstance(object_id, str)
    assert len(object_id) == 64


def test_write_creates_object_file(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    data = b"hello"
    object_id = store.write(data)

    object_path = (
        repo.objects_path
        / object_id[:2]
        / object_id[2:]
    )

    assert object_path.is_file()
    assert object_path.read_bytes() == data


def test_round_trip(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    data = b"hello"

    object_id = store.write(data)

    assert store.read(object_id) == data


def test_same_content_returns_same_object_id(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    first = store.write(b"hello")
    second = store.write(b"hello")

    assert first == second


def test_different_content_returns_different_object_ids(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    first = store.write(b"hello")
    second = store.write(b"world")

    assert first != second


def test_write_same_content_twice_does_not_fail(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    store.write(b"hello")
    store.write(b"hello")


def test_read_missing_object_raises_object_not_found_error(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    missing_object_id = "a" * 64

    with pytest.raises(ObjectNotFoundError):
        store.read(missing_object_id)


def test_binary_data_round_trip(tmp_path):
    repo = Repository.init(str(tmp_path))
    store = ObjectStore(repo)

    data = b"\x00\x01\xff\xab"

    object_id = store.write(data)

    assert store.read(object_id) == data