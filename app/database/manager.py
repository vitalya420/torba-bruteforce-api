from contextlib import asynccontextmanager
from typing import Sequence, Type

import aiosqlite

from .abc import Executor
from .session import Session


class SQLiteDatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @asynccontextmanager
    async def transaction(self,
                          executors=Sequence[Type[Executor]],
                          commit: bool = False):
        """
        Creates new session and starts transaction inside of it
        :yields: instances of executors with session
        """
        conn = await aiosqlite.connect(self.db_path)
        session = Session(conn, self)
        async with session.transaction(commit):  # It's close the connection
            yield [executor(session) for executor in executors]

    @asynccontextmanager
    async def session(self,
                      executors=Sequence[Type[Executor]]):
        """
        Creates new session. Doesn't start transaction
        :param executors: sequence of executors classes
        :return:
        """
        conn = await aiosqlite.connect(self.db_path)
        session = Session(conn, self)
        yield [executor(session) for executor in executors]
        await session.close()
