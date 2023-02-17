import random
import requests
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert, select, update
from bot.keyboards.inline import inline_kb1
from bot.database.main import async_session, Users, Urls, Scores
from bot.states.main import StateBot


async def get_qr(msg: Message, state: StateBot.processing_qr):
    if msg.photo:
        await msg.answer('Обработка началась')
        await msg.answer(f'Твой код {random.choice(["вредоносный", "безопасный"])}')
    elif msg.text:
        try:
            requests.get(url=msg.text, timeout=3)
            async with async_session() as session:
                a = select(Urls).where(Urls.url == msg.text)
                b = await session.execute(a)
                if b.scalars().all() == []:
                    await session.execute(insert(Urls).values(url=msg.text))
                    await session.commit()
                else:
                    d = await session.execute(select(Urls.pk).where(Urls.url == msg.text))
                    d = int(d.scalars().all()[0])
                    pk = await session.execute(select(Scores.pk).where(Scores.url == d))
                    pk = pk.scalars().all()
                    if pk == []:
                        await msg.answer(f'ваша ссылка {random.choice(["вредоносная", "безопасная"])}')
                    else:
                        positive = await session.execute(
                            select(Scores.positive).where(Scores.pk == int(pk[0])))
                        negative = await session.execute(
                            select(Scores.negative).where(Scores.url == int(pk[0])))
                        await msg.answer(f'ваша ссылка {random.choice(["вредоносная", "безопасная"])}\n'
                                         f'Оценки:\n'
                                         f'Положительных:{positive.scalars().all()[0]}\n'
                                         f'Отрицательных:{negative.scalars().all()[0]}', reply_markup=inline_kb1)
                        await state.update_data(pk=pk)
        except requests.exceptions.MissingSchema:
            await msg.answer('это не ссылка')
        except requests.exceptions.InvalidURL:
            await msg.answer('Неверная ссылка')
        except requests.exceptions.InvalidSchema:
            await msg.answer('Неверная ссылка')
        except requests.ConnectionError:
            await msg.answer('Неверная ссылка')
        except requests.exceptions.ReadTimeout:
            await msg.answer('Неверная ссылка')
        except requests.exceptions:
            await msg.answer('Неверная ссылка')
    else:
        await msg.answer('ты какую-то хуйню прислал')


async def report(callback_query: CallbackQuery, state: StateBot.processing_qr):
    user_data = await state.get_data()
    pk = int(user_data['pk'][0])
    async with async_session() as session:
        if callback_query.data == '1':
            positive = await session.execute(
                select(Scores.positive).where(Scores.url == pk))
            positive = int(positive.scalars().all()[0])
            a = update(Scores).where(Scores.url == pk).values(positive=positive+1)
            await session.execute(a)
            await session.commit()
            await callback_query.message.edit_reply_markup()
        else:
            negative = await session.execute(
                select(Scores.negative).where(Scores.url == pk))
            negative = int(negative.scalars().all()[0])
            a = update(Scores).where(Scores.url == pk).values(negative=negative + 1)
            await session.execute(a)
            await session.commit()
            await callback_query.message.edit_reply_markup()

def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(get_qr, content_types=['any'], state=StateBot.processing_qr)
    dp.register_callback_query_handler(report, lambda a: a.data, state=StateBot.processing_qr)
