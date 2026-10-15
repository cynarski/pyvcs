class PyVCSError(Exception):
    """Base exception for PyVCS."""


class RepositoryNotFoundError(PyVCSError):
    """Raised when no PyVCS repository can be found."""



class ObjectNotFoundError(PyVCSError):
    """Raised when an object cannot be found in the object store."""