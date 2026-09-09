from pathlib import Path

class Repository:
    def __init__(self, path: str = ".") -> None:
        self.path = Path(path or ".").resolve()

        self.repo_path = self.path / ".vcs"
        self.index_file = self.repo_path / "index"
        self.objects_path = self.repo_path / "objects"
        self.branches_path = self.repo_path / "branches"
        self.head_file = self.repo_path / "HEAD"