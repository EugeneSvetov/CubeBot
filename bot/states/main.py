from aiogram.dispatcher.filters.state import StatesGroup, State


class StateBot(StatesGroup):
    processing_qr = State()
    get_qr = State()
