from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton("/help")
b2 = KeyboardButton("/download")
b3 = KeyboardButton("/delete")
b4 = KeyboardButton("/create")
b5 = KeyboardButton("/cansel")

# update keyboard after click - one_time_keyboard=True
kb_cl = ReplyKeyboardMarkup(resize_keyboard=True)

# .add - add new line with buttin
# .row(b1, ... ,b_n) - add line
# .insert(b1) - add new button in line
kb_cl.add(b1).row(b2, b3).add(b4).insert(b5)

kb_cl_data = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b6 = KeyboardButton("Так")
b7 = KeyboardButton("Ні")