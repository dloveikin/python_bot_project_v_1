from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
import data_base.bot_db
from bot_config import bot, dp
from bot_keyboard.client_keyboards import kb_cl
from data_base.bot_db import sql_add_data, sql_read, sql_delete, sql_get_photo_id
# вказуємо що хендлер буде використовувати у FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def command_start(message: types.Message):
    sending_message = f'''
    Привіт <b>{message.from_user.first_name} {message.from_user.last_name}!</b>\n
Давай зробимо візитку.'''
    # reply_markup=kb_cl - send to user the same keyboard
    await bot.send_message(message.chat.id, sending_message, parse_mode="html", reply_markup=kb_cl)

    # @dp.message_handler(lambda message: "*" in message.text)
    @dp.message_handler()
    async def empty_message(message: types.Message):
        await message.answer("Для роботи з ботом необхідно скористатися меню")
        await message.delete()


async def command_back(message: types.Message):
    # reply_markup=ReplyKeyboardRemove() - deleted keyboard after click
    await bot.send_message(message.chat.id, "Exit", parse_mode="html", reply_markup=ReplyKeyboardRemove())
# reply_markup=ReplyKeyboardRemove()


# created model for machine
class FSMData(StatesGroup):
    login = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    photo_id = State()


# state="*" - будь-яких 4-ч станів
# @dp.message_handler(state="*", commands="cansel")
async def cansel_data(message: types.Message, state = FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return await message.reply("Данні вводу відсутні")
    else:
        await state.finish()
        await message.reply("Всі введені дані були успішно очищені")


async def command_create(message: types.Message, state=FSMContext):
    # initialized first state
    await FSMData.login.set()
    user_login = f"@{message.from_user.username}"
    async with state.proxy() as data:
        # save machine state to dictionary
        data['login'] = user_login
    await FSMData.next()
    await message.reply("Як до тебе можна звертатися?")


async def usr_first_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['first_name'] = message.text
    await FSMData.next()
    # next state
    await message.reply("Тепер введи фамілію")


async def usr_last_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['last_name'] = message.text
    await FSMData.next()
    # next state
    await message.reply("Тепер введи свій номер телефону")


async def usr_phone_number(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['phone_number'] = message.text
    await FSMData.next()
    # next state
    await message.reply("Чи бажаєш завантажити фото?")


async def usr_photo_id(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['photo_id'] = message.photo[0].file_id
    async with state.proxy() as data:
        await message.reply("Чудово, всі данні були успішно записані")
        # вивід повного складу словника
        await bot.send_message(message.from_user.id, tuple(data.values()))
        await bot.send_message(message.from_user.id, f"""
        Давай перевіримо твої данні:\n
    Твій юзернейм: {data["login"]}\n
    Твоє ім'я та фамілія: {data["first_name"]} {data["last_name"]}\n""")
    # writing to database part

    await sql_add_data(state)
    await state.finish()


async def command_download(message: types.Message):
    await sql_read(message)


async def command_delete(message: types.Message):
    login = "@" + message.from_user.username
    await sql_delete(login)
    await message.reply("Ваші дані були успішно видалені з сереверу ")


async def command_download_photo(message: types.Message):
    login = "@" + message.from_user.username
    file_id = await sql_get_photo_id(login)
    await bot.send_message(message.from_user.id, file_id)
    file = await bot.get_file(file_id)
    file_path = file.file_path
    print(file_path)
    await bot.download_file(file_path, "resume_doc\\"+message.from_user.username+".jpg")


# Виклик функцій кліенту handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(command_download, commands=["download"])
    dp.register_message_handler(cansel_data, commands=["cansel"], state="*")
    dp.register_message_handler(command_create, commands=["create"], state=None)
    dp.register_message_handler(usr_first_name, state=FSMData.first_name)
    dp.register_message_handler(usr_last_name, state=FSMData.last_name)
    dp.register_message_handler(usr_phone_number, state=FSMData.phone_number)
    dp.register_message_handler(usr_photo_id, content_types=["photo"], state=FSMData.photo_id)
    dp.register_message_handler(command_delete, commands=["delete"])
    dp.register_message_handler(command_download_photo, commands=["get"])


# @dp.message_handler()
# async def command_info(message):
#     sticker_id = message.sticker.file_id
#     await bot.send_message(message.chat.id, sticker_id)

# @dp.message_handler()
# async def echo_test(message: types.Message):
#     await message.answer(message.text)
#     await message.reply(message.text)
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
