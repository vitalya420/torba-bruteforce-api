import asyncio

from sanic import Sanic

from .backroung_tasks import BackgroundTasksManager
from .database import db

app = Sanic(__name__)
task_manager = BackgroundTasksManager()

from .blueprints import users, invite_codes
from .middlewares import telegram_middleware

app.blueprint([
    users,
    invite_codes
])


@app.before_server_start
async def connect_db(app_: Sanic):
    await db.connect()
    task_manager.loop = asyncio.get_event_loop()
    app_.ctx.task_manager = task_manager


@app.before_server_stop
async def close_db(*_):
    await db.close()
