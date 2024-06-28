from typing import NamedTuple


class UserQrCodeCount(NamedTuple):
    telegram_id: int
    active_invite_code: str
    count: int
