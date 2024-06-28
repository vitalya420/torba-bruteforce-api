import urllib.parse
from typing import Optional

import aiohttp


class Client:

    def __init__(self, telegram_id: int, first_name: str, last_name: Optional[str] = None):
        self.headers = {
            'x-telegram-user-id': telegram_id,
            'x-telegram-first-name': first_name,
            'x-telegram-last-name': last_name,
            'x-webhook-url': None
        }
        self.host = 'http://127.0.0.1:8080'

    async def get(self, endpoint):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(urllib.parse.urljoin(self.host, endpoint)) as resp:
                return await resp.json()

    async def self(self):
        endpoint = '/api/v1/users/self'
        return await self.get(endpoint)

    async def set_invite_code(self, code: str):
        endpoint = '/api/v1/invite_codes'

    async def get_qr_code(self):
        endpoint = '/api/v1/users/qr_code'
        return await self.get(endpoint)

    async def set_qr_code_used(self):
        endpoint = '/api/v1/users/qr_code'

    async def list_qr_codes(self):
        endpoint = 'api/v1/users/qr_code'
        return await self.get(endpoint)

    async def setup_webhook(self, webhook: str):
        self.headers['x-webhook-url'] = webhook

    @classmethod
    def from_attributes(cls, object_):
        return cls(
            getattr(object_.from_user, 'id', None),
            getattr(object_.from_user, 'first_name', None),
            getattr(object_.from_user, 'last_name', None),
        )
