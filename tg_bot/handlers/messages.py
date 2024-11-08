from aiogram import types
from aiogram import Router

async def echo_message(message: types.Message):
    await message.answer("Для начала работы бота /start")

def register_message_handlers(router: Router):
    router.message.register(echo_message)
