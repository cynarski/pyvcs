from dataclasses import dataclass
from pathlib import Path


# Generates __init__ and other common methods automatically. 
# # frozen=True makes the object immutable after creation. 
# # slots=True prevents adding arbitrary new attributes.

@dataclass(frozen=True, slots=True)
class Repository:
    worktree: Path

    # Runs automatically after the generated __init__. 
    # Converts the given path to an absolute resolved path.
    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "worktree",
            Path(self.worktree).resolve()
        )

    @property
    def vcs_dir(self) -> Path:
        return self.worktree / ".pyvcs"

    @property
    def objects_dir(self) -> Path:
        return self.vcs_dir / "objects"

    @property
    def refs_dir(self) -> Path:
        return self.vcs_dir / "refs"

    @property
    def heads_dir(self) -> Path:
        return self.refs_dir / "heads"

    @property
    def head_file(self) -> Path:
        return self.vcs_dir / "HEAD"