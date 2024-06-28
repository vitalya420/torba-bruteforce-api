from sanic import Request, json, BadRequest

from app.database import db
from app.database.exceptions import InviteCodeExists
from app.utils.decorators import telegram_user_required
from app.utils.miscs import get_utc_now
from . import invite_codes
from app.backroung_tasks.tasks import after_user_active_invite_code_changed


# @invite_codes.get('/')
# async def get_invite_codes(request: Request):
#     pass


@invite_codes.post('/')
@telegram_user_required
async def set_invite_code(request: Request):
    code = request.json.get('code', None)
    if code is None:
        raise BadRequest('Which one?')

    try:
        await db.insert_invite_code(code, request.ctx.user.telegram_id, get_utc_now())
        retval = json({'ok': True, 'already_exists': False})
    except InviteCodeExists:
        retval = json({'ok': True, 'already_exists': True})

    request.app.ctx.task_manager.create(after_user_active_invite_code_changed(
        await db.select_user(request.ctx.user.telegram_id)
    ))
    return retval
