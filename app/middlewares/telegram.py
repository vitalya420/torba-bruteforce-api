from typing import NamedTuple, Optional

from sanic import Request

from app import app


class TelegramUser(NamedTuple):
    telegram_id: int
    first_name: str
    last_name: Optional[str]


@app.middleware('request')
async def telegram_middleware(request: Request):
    telegram_id = request.headers.get('x-telegram-user-id', None)
    first_name = request.headers.get('x-telegram-first-name', None)
    last_name = request.headers.get('x-telegram-last-name', None)
    telegram_user = None
    if all([telegram_id, first_name]):
        telegram_user = TelegramUser(telegram_id, first_name, last_name)
    request.ctx.telegram_user = telegram_user
