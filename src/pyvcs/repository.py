from pathlib import Path
from typing import Self

from pyvcs.exceptions import RepositoryNotFoundError

DEFAULT_BRANCH = "master"
REPO_DIR_NAME = ".pyvcs"

# hooks – folder zawierający skrypty, uruchamiane automatycznie po wykonaniu określonych akcji,
# info – folder zawierający plik exclude z listą ignorowanych plików,
# logs – folder zawierający historię operacji na gałęziach,
# objects – folder zawierający pliki tree i blob,
# refs – folder zawierający pliki gałęzi i tagów,
# config – plik z lokalną konfiguracją repozytorium,
# HEAD – plik z nazwą bieżącej gałęzi,
# index – plik binarny zawierający listę plików w przechowalni.

class Repository:
    def __init__(self, path: str = ".") -> None:
        self.path = Path(path or ".").resolve()

        self.repo_path = self.path / REPO_DIR_NAME
        self.index_file = self.repo_path / "index"
        self.objects_path = self.repo_path / "objects"
        self.branches_path = self.repo_path / "branches"
        self.head_file = self.repo_path / "HEAD"


    @classmethod
    def init(cls, path: str = ".") -> Self:

        repo = cls(path)

        repo.path.mkdir(parents=True, exist_ok=True)
        repo.repo_path.mkdir(parents=True, exist_ok=True)
        repo.objects_path.mkdir(parents=True, exist_ok=True)
        repo.branches_path.mkdir(parents=True, exist_ok=True)
        # repo.index_file.touch(exist_ok=True)

        if not repo.head_file.exists():
            repo.head_file.write_text(
                f"{DEFAULT_BRANCH}\n",
                encoding="utf-8",
            )

        return repo


    @classmethod
    def find(cls, start: str = ".") -> Self:
        current = Path(start).resolve()

        if current.is_file():
            current = current.parent

        while True:
            repo_dir = current / REPO_DIR_NAME

            if repo_dir.is_dir():
                return cls(str(current))

            if current.parent == current:
                raise RepositoryNotFoundError(
                    f"Not a PyVCS repository: {start}"
                )

            current = current.parent
