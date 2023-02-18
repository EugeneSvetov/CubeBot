from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_1 = InlineKeyboardButton('👍', callback_data='1')
inline_btn_2 = InlineKeyboardButton('👎', callback_data='0')

inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)


inline_btn_3 = InlineKeyboardButton('Отзыв', callback_data='report')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_3)