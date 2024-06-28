from typing import NamedTuple, Optional

from aiosqlite import Cursor

from app.schemas.invite_code import InviteCodeMin


class UserSchema(NamedTuple):
    telegram_id: int
    active_invite_code: Optional[str]
    display_name: Optional[str]
    created_at: int


class UserJoinedInviteCode(NamedTuple):
    telegram_id: int
    display_name: Optional[str]
    active_invite_code: Optional[InviteCodeMin]

    @classmethod
    async def from_cursor(cls, cursor: Cursor):
        results = await cursor.fetchall()
        retval = []
        for result in results:
            telegram_id, display_name, _, active_invite_code, *extra = result
            code = None
            if active_invite_code is not None:
                code = InviteCodeMin(active_invite_code, *extra)
            user = cls(telegram_id, display_name, code)
            retval.append(user)
        return retval