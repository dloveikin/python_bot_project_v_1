from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from bot_config import dp, bot
from bot_keyboard.client_keyboards import kb_cl
# вказуємо що хендлер буде використовувати у FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def command_start(message: types.Message):
    sending_message = f'''
    Привіт <b>{message.from_user.first_name} {message.from_user.last_name}!</b>\n
Давай зробимо візитку.'''
    # reply_markup=kb_cl - send to user the same keyboard
    await bot.send_message(message.chat.id, sending_message, parse_mode="html", reply_markup=kb_cl)

async def command_back(message: types.Message):
    # reply_markup=ReplyKeyboardRemove() - deleted keyboard after click
    await bot.send_message(message.chat.id, "Exit", parse_mode="html", reply_markup=ReplyKeyboardRemove())
# reply_markup=ReplyKeyboardRemove()

# створення моделі станів машини
class FSMData(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    photo_id = State()



async def command_download(message : types.Message):
    # ініціалізуємо перший стан
    await FSMData.first_name.set()
    await message.reply("Як до тебе можна звертатися?")
    # await bot.send_message(message.chat.id, "Введи своє ім'я")


async def usr_first_name(message :types.Message, state=FSMContext):
    # параметр з анотацією
    async with state.proxy() as data:
        # збереження результату у словник стану машини
        data['first_name']=message.text
    await FSMData.next()
    # перехід у наступний стан
    await message.reply("Тепер введи фамілію")


async def usr_last_name(message :types.Message, state=FSMContext):
    # параметр з анотацією
    async with state.proxy() as data:
        # збереження результату у словник стану машини
        data['last_name']=message.text
    await FSMData.next()
    # перехід у наступний стан
    await message.reply("Тепер введи свій номер телефону")


async def usr_phone_number(message :types.Message, state=FSMContext):
    # параметр з анотацією
    async with state.proxy() as data:
        # збереження результату у словник стану машини
        data['phone_number']=message.text
    await FSMData.next()
    # перехід у наступний стан
    await message.reply("Бажаєш завантажити фото?")


async def usr_photo_id(message :types.Message, state=FSMContext):
    # параметр з анотацією
    async with state.proxy() as data:
        # збереження результату у словник стану машини
        data['photo_id']=message.photo[0].file_id

    async with state.proxy() as data:
        await message.reply(str(data))

    await state.finish()


# Виклик функцій кліенту handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(command_back, commands=["back"])
    dp.register_message_handler(command_download, commands=["download"], state=None)
    dp.register_message_handler(usr_first_name, state=FSMData.first_name)
    dp.register_message_handler(usr_last_name, state=FSMData.last_name)
    dp.register_message_handler(usr_phone_number, state=FSMData.phone_number)
    dp.register_message_handler(usr_photo_id, content_types=["photo"], state=FSMData.photo_id)





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