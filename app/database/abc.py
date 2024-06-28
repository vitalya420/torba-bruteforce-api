from abc import ABC

from app.database.session import Session


class Executor(ABC):
    """
    Abstract base class representing an executor that manages a session
    for executing transactions.

    Attributes:
        _session: The session instance used for executing transactions.
    """

    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self) -> Session:
        return self._session
