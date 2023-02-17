from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from bot.states.main import StateBot


async def start(msg: Message):
    await msg.answer(f'Привет,{msg.from_user.username}👋🏻\n'
                     f'Присылай QR-код или ссылку и я отправлю всю информацию о нём')
    await StateBot.processing_qr.set()




def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state=[StateBot.get_qr, None])
