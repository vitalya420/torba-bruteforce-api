from app.database.abc import Executor
from app.database.decorators import query


class QRCodesExecutor(Executor):
    @query.file('queries/create_qr_code.sql')
    async def create_qr_code(self, text, code, telegram_id, created_at, extra_json):
        pass

