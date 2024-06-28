from contextlib import asynccontextmanager
from typing import Iterable, Optional

from aiosqlite import Connection, Cursor

from app.database.exceptions import Rollback


class Session:
    def __init__(self, connection: Connection, db_manager):
        self.connection = connection
        self.db_manager = db_manager

    async def execute(self, query, params: Optional[Iterable] = None) -> Cursor:
        print('executing', query, params)
        return await self.connection.execute(query, params)

    @asynccontextmanager
    async def transaction(self, commit: bool = False):
        await self.begin()
        try:
            yield self
            if commit:
                await self.commit()
        except Rollback:
            await self.rollback()
        finally:
            await self.close()

    async def close(self):
        if self.connection.is_alive():
            await self.connection.close()

    async def commit(self):
        await self.execute('COMMIT')

    async def begin(self):
        await self.execute('BEGIN')

    async def rollback(self):
        await self.execute('ROLLBACK')
