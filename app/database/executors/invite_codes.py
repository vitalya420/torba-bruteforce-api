from app.database.abc import Executor
from app.database.decorators import query


class InviteCodesExecutor(Executor):
    @query.file('queries/insert_invite_code.sql')
    async def insert_invite_code(self, code: str, created_by: int, created_at: int):
        ...


