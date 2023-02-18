from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from bot.states.main import StateBot
from bot.database.main import engine, Users, async_session
from sqlalchemy import insert, select, update


async def start(msg: Message):
    async with async_session() as session:
        a = select(Users).where(Users.tg_id == msg.from_user.id)
        b = await session.execute(a)
        if b.scalars().all() == []:
            await session.execute(insert(Users).values(tg_id=msg.from_user.id))
            await session.commit()
    await msg.answer(f'Здравствуйте, {msg.from_user.username}👋🏻\n'
                     f'Отправьте мне QR-код или ссылку, а я отправлю вам всю информацию о них')
    await StateBot.processing_qr.set()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state=[StateBot.get_qr, None])
