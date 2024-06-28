from sanic import Request, BadRequest
from sanic_ext import serializer

from app.serializers.named_tuple_serializer import (named_tuple_serializer,
                                                    many_named_tuple_serializer)
from app.utils.decorators import telegram_user_required
from . import users
from app.database import db
from app.backroung_tasks.tasks import after_user_active_invite_code_changed


@users.get('/')
@serializer(many_named_tuple_serializer)
async def get_users(request: Request):
    return await db.select_users_joined_codes()


@users.get('/self')
@telegram_user_required
@serializer(named_tuple_serializer)
async def get_user(request: Request):
    return request.ctx.user


@users.get('/qr_code', name='get qr code')
@telegram_user_required
@serializer(named_tuple_serializer)
async def get_next_qr_code(request: Request):
    qr = await db.select_first_qr_code(request.ctx.user.telegram_id)
    return qr


@users.patch('/qr_code', name='set qr code used')
@telegram_user_required
@serializer(named_tuple_serializer)
async def set_qr_code_used(request: Request):
    text = request.json.get('text', None)
    if text is None:
        raise BadRequest("Retard alert")
    await db.set_qr_code_used(text)
    request.app.ctx.task_manager.create(after_user_active_invite_code_changed(
        await db.select_user(request.ctx.user.telegram_id)
    ))
    qr = await db.select_first_qr_code(request.ctx.user.telegram_id)
    return qr


@users.get('/qr_codes', name='list qr codes')
@telegram_user_required
@serializer(many_named_tuple_serializer)
async def list_qr_codes(request: Request):
    qr_codes = await db.select_qr_codes(request.ctx.user.telegram_id)
    return qr_codes
