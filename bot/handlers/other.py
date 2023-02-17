import random

from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from bot.states.main import StateBot


async def get_qr(msg: Message):
    await msg.photo[-1].download(f'bot/media/img/qr_code_{msg.from_user.username}.jpg')
    await msg.answer('Обработка началась')
    await msg.answer(f'Твой код {random.choice(["вредоносный","безопасный"])}')


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(get_qr, content_types=ContentType.PHOTO, state=StateBot.processing_qr)
