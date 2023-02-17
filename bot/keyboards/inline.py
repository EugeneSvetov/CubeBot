from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_1 = InlineKeyboardButton('Класс', callback_data='1')
inline_btn_2 = InlineKeyboardButton('Некласс', callback_data='0')

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
