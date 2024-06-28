from sanic import Request
from sanic_ext import serializer

from app.serializers.named_tuple_serializer import (named_tuple_serializer,
                                                    many_named_tuple_serializer)
from app.utils.decorators import telegram_user_required
from . import users
from app.database import db


@users.get('/')
@serializer(many_named_tuple_serializer)
async def get_users(request: Request):
    return await db.select_users_joined_codes()


@users.get('/self')
@telegram_user_required
@serializer(named_tuple_serializer)
async def get_user(request: Request):
    return request.ctx.user
