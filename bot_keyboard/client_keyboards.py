from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = KeyboardButton("/help")
b2 = KeyboardButton("/download")
b3 = KeyboardButton("/delete")
b4 = KeyboardButton("/create")
b5 = KeyboardButton("/cancel")
b6 = KeyboardButton("/back")
b7 = KeyboardButton("/get")
b8 = KeyboardButton("/menu")
b9 = KeyboardButton("/next")
b10 = KeyboardButton("/job")
b11 = KeyboardButton("/education")

# update keyboard after click - one_time_keyboard=True
kb_cl = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_cl_1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_cl_0 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_cl_3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_cl_4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_cl_5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

kb_cl.row(b1, b4, b8)
kb_cl_0.add(b5)
kb_cl_1.row(b6, b5)
kb_cl_3.row(b7, b3, b4, b2)
kb_cl_4.row(b10, b9)
kb_cl_5.row(b11, b8)
# .add - add new line with buttin
# .row(b1, ... ,b_n) - add line
# .insert(b1) - add new button in line
# kb_cl.add(b1).row(b2, b3).add(b4).insert(b5)


kb_cl_data = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b6 = KeyboardButton("Так")
b7 = KeyboardButton("Ні")

