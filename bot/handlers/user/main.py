from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from bot.states.main import StateBot
from bot.database.main import session, engine, Users
from sqlalchemy import insert, select, update


async def start(msg: Message):
    data = insert(Users).values(tg_id=msg.from_user.id)
    with engine.connect() as conn:
        if session.query(Users).filter_by(tg_id=msg.from_user.id).first() is None:
            result = conn.execute(data)
            conn.commit()
    await msg.answer(f'Привет,{msg.from_user.username}👋🏻\n'
                     f'Присылай QR-код или ссылку и я отправлю всю информацию о нём')
    await StateBot.processing_qr.set()



def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state=[StateBot.get_qr, None])
