import asyncio


async def after_user_active_invite_code_changed(user):
    print('Users invite code changed', user)