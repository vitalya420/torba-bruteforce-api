import os.path
import sqlite3
from typing import Optional, Union

import aiosqlite
from aiosqlite import Connection, Cursor

from app.database.decorators import query_file
from app.database.exceptions import QueryNotFound, InviteCodeExists
from app.schemas.qr_codes import UserQrCodeCount
from app.schemas.user import UserSchema, UserJoinedInviteCode
from app.utils.miscs import get_utc_now


def load_queries_from_folder(folder: str) -> dict:
    abs_path = os.path.join(os.getcwd(), folder)
    _mapping = {}
    for file in os.listdir(abs_path):
        file_abs_path = os.path.join(abs_path, file)
        if os.path.isfile(file_abs_path) and file_abs_path.endswith('.sql'):
            name = os.path.splitext(file)[0]
            with open(file_abs_path, 'r') as query_file_:
                _mapping[name] = query_file_.read()
    return _mapping


class Database:
    def __init__(self, db_path: str, queries_folder: str):
        self.db_path = db_path
        self.queries_mapping = load_queries_from_folder(queries_folder)
        self.connection: Union[Connection, None] = None

    async def connect(self):
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_path)

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def execute(self, query_name: str, params: Optional[dict] = None, *, commit: bool = False) -> Cursor:
        query = self.queries_mapping.get(query_name, None)
        if query is None:
            raise QueryNotFound(f"Query {query} not found")
        cursor = await self.connection.execute(query, params or ())
        if commit:
            await self.commit()
        return cursor

    async def commit(self):
        await self.connection.commit()

    @query_file("create_user", commit_after=True)
    async def create_user(self, telegram_id: int, created_at: int, *, display_name: Optional[str] = None):
        ...

    @query_file("update_user")
    async def update_user(self, telegram_id: int, *, display_name: Optional[str] = None):
        ...

    @query_file("select_user")
    async def select_user(self, telegram_id: int) -> Union[UserSchema, None]:
        ...

    @query_file("select_users")
    async def select_users(self, limit: int = 10, offset: int = 0) -> tuple[UserSchema]:
        ...

    @query_file("insert_invite_code", commit_after=True)
    async def insert_invite_code_(self, code: str, created_by: int, created_at: int):
        ...

    @query_file("update_users_invite_code", commit_after=True)
    async def update_users_invite_code(self, code: str, telegram_id: int):
        ...

    @query_file("insert_history_line", commit_after=True)
    async def insert_history_line(self, user: int, code: str, created_at: int):
        ...

    @query_file("select_users_joined_codes", cursor_callback=UserJoinedInviteCode.from_cursor)
    async def select_users_joined_codes(self):
        ...

    @query_file("count_users_qr_codes")
    async def count_users_qr_codes(self) -> list[UserQrCodeCount]:
        ...

    @query_file("create_qr_code", commit_after=True)
    async def create_qr_code(self, text: str, code: str, telegram_id: int, created_at: int, extra_json: str):
        ...

    async def insert_invite_code(self, code: str, telegram_id: int, created_at: int):
        # TODO: Transaction
        try:
            await self.insert_invite_code_(code, telegram_id, created_at)
        except sqlite3.IntegrityError:
            raise InviteCodeExists(f"Invite code {code} exists")
        finally:
            await self.update_users_invite_code(code, telegram_id)
            await self.insert_history_line(telegram_id, code, get_utc_now())


db = Database('database.db', 'queries')
