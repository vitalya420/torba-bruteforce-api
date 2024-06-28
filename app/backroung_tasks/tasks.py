import asyncio
import json

from app.backroung_tasks.torba_bruteforce import (create_account,
                                                  random_vodafone_number,
                                                  format_number, )
from app.database import db
from app.schemas.qr_codes import UserQrCodeCount
from app.utils.miscs import random_first_name, random_last_name, get_utc_now


async def do_bruteforce(telegram_id: int, code: str):
    qr_codes = []
    count = await db.count_user_qr_codes_for_code(telegram_id, code)
    amount = max(0, 3 - count)
    for i in range(amount):
        phone = format_number(random_vodafone_number())
        first_name, last_name = random_first_name(), random_last_name()
        account = await create_account(phone, code, first_name, last_name)
        extra = {
            'phone': phone,
            'code': code,
            'first_name': first_name,
            'last_name': last_name
        }
        if account:
            registration_response, qr_code = account
            extra['registration_response'] = registration_response
            extra['qr_code'] = qr_code
        await db.create_qr_code(
            qr_code, code, telegram_id, get_utc_now(), json.dumps(extra)
        )
        count = await db.count_user_qr_codes_for_code(telegram_id, code)
        qr_codes.append(qr_code)
    return qr_codes


async def after_user_active_invite_code_changed(user):
    _ = asyncio.get_event_loop().create_task(do_bruteforce(user.telegram_id, user.active_invite_code))


async def after_server_started(counts: list[UserQrCodeCount]):
    for count in counts:
        _ = asyncio.get_event_loop().create_task(do_bruteforce(count.telegram_id, count.active_invite_code))
