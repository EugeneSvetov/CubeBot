from aiogram import Dispatcher
from aiogram.types import Message


async def echo(msg: Message):
    await msg.answer(msg.text)


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(echo, content_types=['text'])