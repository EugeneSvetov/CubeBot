import random
import base64
import re

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiohttp import ClientConnectorError, ContentTypeError
from sqlalchemy import insert, select, update
import aiohttp
from bot.database.main import async_session, Urls, Scores, Comments
from bot.keyboards.inline import inline_kb1, inline_kb2
from bot.states.main import StateBot


async def get_qr(msg: Message, state: StateBot.processing_qr):
    if msg.photo:
        await msg.photo[-1].download(f'bot/media/{msg.photo[0]["file_unique_id"]}.jpg')
        with open(f'bot/media/{msg.photo[0]["file_unique_id"]}.jpg', "rb") as f:
            bytes_ = bytes(f.read())
        encoded = base64.b64encode(bytes_)
        data = encoded.decode('ascii')
        async with aiohttp.ClientSession() as session:
            a = await session.post('http://127.0.0.1:8000/check_qr', json={'file': data})
            result = await a.json()
        if result['data'] == 'Не найдены qr коды на фото!':
            await msg.answer(result['data'])
        else:
            result = re.search(r'https?://[\w\-.]+/?', result['data']).group(0)
    elif msg.text:
        try:
            async with aiohttp.ClientSession() as session:
                await session.get(msg.text, timeout=2)
        except aiohttp.InvalidURL:
            await msg.answer('Неверная ссылка')
        except TimeoutError:
            await msg.answer('Не удалось осуществить запрос')
        except AssertionError:
            await msg.answer('Пожалуйста, отправьте кореектную ссылку')
        except ClientConnectorError:
            await msg.answer('Пожалуйста, отправьте кореектную ссылку')
        except AttributeError:
            await msg.answer('Пожалуйста, отправьте кореектную ссылку')
        except ContentTypeError:
            await msg.answer('Пожалуйста, отправьте кореектную ссылку')

        result = re.search(r'https?://[\w\-.]+/?', msg.text).group(0)
    else:
        await msg.answer('Пожалуйста, отправьте ссылку или QR-код')

    async with async_session() as session:
        a = select(Urls.pk).where(Urls.url == result)
        b = await session.execute(a)
        b = b.scalars().all()
        if b == []:
            await session.execute(insert(Urls).values(url=result))
            await session.commit()
            a = select(Urls.pk).where(Urls.url == result)
            b = await session.execute(a)
            b = b.scalars().all()
            await session.execute(insert(Scores).values(url=b[0], positive=0, negative=0))
            await session.commit()
        c = select(Comments.text).where(Comments.url == b[0])
        e = await session.execute(c)
        e = e.scalars().all()
        d = await session.execute(select(Urls.pk).where(Urls.url == result))
        pk = int(d.scalars().all()[0])
        positive = await session.execute(
            select(Scores.positive).where(Scores.url == pk))
        negative = await session.execute(
            select(Scores.negative).where(Scores.url == pk))
        positive = positive.scalars().all()
        negative = negative.scalars().all()
        async with aiohttp.ClientSession() as session:
            a = await session.post('http://127.0.0.1:8000/phishing', json={'url':result})
            result1 = await a.json()
        choice = f'📊 Данные о {result}:\n\n'\
        f'🤖 Предсказание нашей модели машинного обучения (с точностью 97%): {result1["predict"]}\n'\
        f'📃 SSL Сертификат: {["✅ Доступен" if result1["ssl"]["availability"] == True else "❌ Не доступен"][0]} и {["валидный" if result1["ssl"]["invalid_ssl"] == False else "❌ невалидный"][0]}\n'\
        f'🔄 Перенаправления: {["✅ Остсутвуют" if result1["redirect"] == False else len(result1["redirect"])][0]}\n'\
        f'🛡 Защищнное соединение: {"✅ Доступно" if result1["is_https"] == True else "❌ Недоступно"}'
        a = ['✍️ '+ i for i in e]
        n = "\n\n".join(a)
        if e == []:
            await msg.answer(f'{choice}\n\n'
                         f'Оценки:\n\n'
                         f'😁 Положительных: {positive[0]}\n'
                         f'😡 Отрицательных: {negative[0]}\n\n', reply_markup=inline_kb1)
        else:
            await msg.answer(f'{choice}\n\n'
                             f'Оценки:\n\n'
                             f'😁 Положительных: {positive[0]}\n'
                             f'😡 Отрицательных: {negative[0]}\n\n'
                             f'Отзывы:\n\n{n}', reply_markup=inline_kb1)
        await state.update_data(positive=positive[0], pk=pk, negative=negative[0], choice=choice, url = result, n=n)
        await session.close()


async def score(callback_query: CallbackQuery, state: StateBot.processing_qr):
    user_data = await state.get_data()
    pk = user_data['pk']
    choice = user_data['choice']
    positive = user_data['positive']
    negative = user_data['negative']
    n = user_data['n']
    if callback_query.data == '1':
        async with async_session() as session:
            a = update(Scores).where(Scores.url == pk).values(positive=positive + 1, negative=negative)
            await session.execute(a)
            await session.commit()
        await callback_query.message.edit_text(f'{choice}\n\n'
                                               f'Оценки:\n\n'
                                               f'😁 Положительных: {positive + 1}\n'
                                               f'😡 Отрицательных: {negative}\n\n'
                                               f'Отзывы:\n\n{n}')
        await callback_query.message.edit_reply_markup(inline_kb2)
    elif callback_query.data == '0':
        async with async_session() as session:
            a = update(Scores).where(Scores.url == pk).values(negative=negative + 1, positive=positive)
            await session.execute(a)
            await session.commit()
        await callback_query.message.edit_text(f'{choice}\n\n'
                                               f'Оценки:\n\n'
                                               f'😁 Положительных: {positive}\n'
                                               f'😡 Отрицательных: {negative + 1}\n\n'
                                               f'Отзывы:\n\n{n}')
        await callback_query.message.edit_reply_markup(inline_kb2)
    if callback_query.data == 'report':
        await callback_query.message.answer('Поделитесь своим мнение о сайте')
        await StateBot.reporting.set()


async def report(msg: Message, state: StateBot.reporting):
    data = await state.get_data()
    async with async_session() as session:
        a = select(Urls.pk).where(Urls.url == data['url'])
        b = await session.execute(a)
        b = b.scalars().all()
        await session.execute(insert(Comments).values(author=msg.from_user.id, url=b[0], text=msg.text))
        await session.commit()
    await msg.answer('Ваш отзыв учтён')
    await StateBot.processing_qr.set()


def register_other_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(get_qr, content_types=['any'], state=StateBot.processing_qr)
    dp.register_callback_query_handler(score, lambda a: a.data, state=StateBot.processing_qr)
    dp.register_message_handler(report, content_types=['text'], state=StateBot.reporting)
