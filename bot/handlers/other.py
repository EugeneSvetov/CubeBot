import random
import requests
from aiogram import Dispatcher
from aiogram.types import Message
from bot.states.main import StateBot


async def get_qr(msg: Message):
    if msg.photo:
        await msg.answer('Обработка началась')
        await msg.answer(f'Твой код {random.choice(["вредоносный", "безопасный"])}')
    elif msg.text:
        try:
            requests.get(msg.text)
            await msg.answer(f'ваша ссылка {random.choice(["вредоносная", "безопасная"])}')
        except requests.exceptions.MissingSchema:
            await msg.answer('это не ссылка')
        except requests.exceptions.InvalidURL:
            await msg.answer('Неверная ссылка')
    else:
        await msg.answer('ты какую-то хуйню прислал')


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(get_qr, content_types=['any'], state=StateBot.processing_qr)
