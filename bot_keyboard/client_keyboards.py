from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("/help")
b2 = KeyboardButton("/back")
b3 = KeyboardButton("/next")
b4 = KeyboardButton("/download")

# update keyboard after click - one_time_keyboard=True
kb_cl = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# .add - add new line with buttin
# .row(b1, ... ,b_n) - add line
# .insert(b1) - add new button in line
kb_cl.add(b1).row(b2, b3).add(b4)
