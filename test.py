import asyncio

from app.database.executors import UsersExecutor, InviteCodesExecutor
from app.database import db


async def main():

    async with db.transaction([UsersExecutor, InviteCodesExecutor], commit=True) as executors:
        user_executor: UsersExecutor = executors[0]
        invite_code_executor: InviteCodesExecutor = executors[1]
        await invite_code_executor.insert_invite_code('GAYSAX1337', 1, 6969)


asyncio.run(main())
