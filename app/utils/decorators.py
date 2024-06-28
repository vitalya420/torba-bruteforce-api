from sanic import Request, BadRequest

from app.database import db
from app.utils.miscs import get_utc_now


def telegram_user_required(func):
    async def decorator(request: Request, *args, **kwargs):
        if request.ctx.telegram_user is None:
            raise BadRequest
        db_user = await db.select_user(request.ctx.telegram_user.telegram_id)
        if db_user is None:
            await db.create_user(telegram_id=request.ctx.telegram_user.telegram_id,
                                 display_name=request.ctx.telegram_user.first_name,
                                 created_at=get_utc_now())
            db_user = await db.select_user(request.ctx.telegram_user.telegram_id)
        request.ctx.user = db_user
        res = await func(request, *args, **kwargs)
        return res

    return decorator
