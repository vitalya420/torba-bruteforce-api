from typing import Optional

from aiosqlite import Cursor

from app.database.abc import Executor
from app.database.decorators import query
from app.schemas.qr_codes import UserQrCodeCount
from app.schemas.user import UserSchema
from app.utils.miscs import get_utc_now


async def int_from_count(cursor: Cursor) -> int:
    result = await cursor.fetchone()
    return result[0]


class UsersExecutor(Executor):
    """Executor for user-related database operations."""

    @query("INSERT INTO users(telegram_id, display_name, created_at) "
           "VALUES (:telegram_id, :display_name, :created_at)")
    async def _create_user(self, telegram_id: int, display_name: str, created_at: int):
        """
        Create user
        :param telegram_id: Telegram id of the user
        :param display_name: Display name
        :param created_at: UTC time in seconds
        :return: None
        """

    async def create_user(self, telegram_id: int, display_name: str):
        """
        Proxy to _create_user but created_at sets automatically
        :param telegram_id: Telegram id of the user
        :param display_name: Display name
        :return: None
        """
        await self._create_user(telegram_id, display_name, get_utc_now())

    @query("SELECT * FROM users WHERE telegram_id = :telegram_id")
    async def select_user(self, telegram_id: int) -> Optional[UserSchema]:
        """
        Select user
        :param telegram_id: Telegram id of the user
        :return: UserSchema if user exists else None
        """

    @query.file('queries/count_users_qr_codes.sql')
    async def count_qr_codes(self) -> list[UserQrCodeCount]:
        """
        Count user's unused QR codes for user's active invite code
        :return: Int value
        """

    @query.file('queries/count_user_qr_codes_for_code.sql', cursor_callback=int_from_count)
    async def count_user_qr_codes_for_code(self, telegram_id: int, code: str) -> int:
        ...

    @query.file('queries/select_users.sql')
    async def _select_users(self, limit: int = 10, offset: int = 0) -> list[UserSchema]:
        ...

    async def select_users(self, limit: int = 10, offset: int = 0):
        return await self._select_users(min(10, limit), offset)

    @query.file('queries/update_users_invite_code.sql')
    async def set_invite_code(self, telegram_id: int, code: str):
        """
        Updates user and sets value of user.active_invite_code
        :param telegram_id: Telegram id
        :param code: Invite code string
        :return: None
        """
