class PyVCSError(Exception):
    """Base exception for PyVCS."""


class RepositoryNotFoundError(PyVCSError):
    """Raised when no PyVCS repository can be found."""