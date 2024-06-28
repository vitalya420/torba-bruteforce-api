
async def send_to_user(telegram_id: int, text: str):
    print(f"send to {telegram_id} content {text}")


async def send_qr_generated_log(result):
    telegram_id, qr = result
    await send_to_user(telegram_id, f"New qr generated {qr}")
