from typing import NamedTuple, Optional


class UserQrCodeCount(NamedTuple):
    telegram_id: int
    active_invite_code: str
    count: int


class QRCode(NamedTuple):
    id: int
    text: str
    invite_code: str
    user: int
    used: int
    created_at: int
    used_at: Optional[int]
    extra_json: dict
