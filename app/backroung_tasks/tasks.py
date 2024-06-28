import json

from app.backroung_tasks.torba_bruteforce import (create_account,
                                                  random_vodafone_number,
                                                  format_number, )
from app.database import db
from app.schemas.qr_codes import UserQrCodeCount
from app.utils.miscs import random_first_name, random_last_name, get_utc_now, with_callback
from app.webhooks.bot import send_qr_generated_log


async def do_bruteforce(telegram_id: int, code: str):
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
    return qr_code


async def after_user_active_invite_code_changed(user):
    print('Users invite code changed', user)


async def after_server_started(counts: list[UserQrCodeCount]):
    return
    for count in counts:
        telegram_id, code, amount = count
        await with_callback(
            do_bruteforce(telegram_id, code),
            send_qr_generated_log
        )
