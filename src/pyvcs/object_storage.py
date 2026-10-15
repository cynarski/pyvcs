import hashlib
from pathlib import Path

from pyvcs.exceptions import ObjectNotFoundError
from pyvcs.repository import Repository


class ObjectStorage:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo


    def calculate_object_id(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _object_path(self, object_id: str) -> Path:
        prefix = object_id[:2]
        suffix = object_id[2:]

        return self.repo.objects_path / prefix / suffix

    def write(self, data: bytes) -> str:
        object_id = self.calculate_object_id(data)
        object_path = self._object_path(object_id)

        if object_path.exists():
            return object_id

        object_path.parent.mkdir(parents=True, exist_ok=True)
        object_path.write_bytes(data)

        return object_id

    def read(self, object_id: str) -> bytes:
        object_path = self._object_path(object_id)

        if not object_path.exists():
            raise ObjectNotFoundError(f"Object not found: {object_id}")

        return object_path.read_bytes()

    def exists(self, object_id: str) -> bool:
        return self._object_path(object_id).is_file()