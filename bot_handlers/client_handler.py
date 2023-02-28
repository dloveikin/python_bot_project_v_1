from aiogram import types, Dispatcher
from bot_config import bot, dp, photo_path
from bot_keyboard.client_keyboards import kb_cl, kb_cl_1, kb_cl_0, kb_cl_3, kb_cl_4 , kb_cl_5
from data_base.ORM.controller import orm_add_data, orm_delete_data, orm_get_data, orm_add_job, orm_add_education, select_all
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from resume_doc.generate_pdf import create_pdf


async def command_start(message: types.Message, state=FSMContext):
    sending_message = f'''
    Привіт <b>{message.from_user.first_name} {message.from_user.last_name}!</b>\n
Давай зробимо візитку.'''
    await bot.send_message(message.chat.id, sending_message, parse_mode="html", reply_markup=kb_cl)

    @dp.message_handler()
    async def empty_message(message: types.Message):
        await message.answer("Для роботи з ботом необхідно скористатися меню")
        await message.delete()


# created model for machine
class FSMData(StatesGroup):
    login = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    mail = State()
    vacantion = State()
    photo_id = State()


class FSMJob(StatesGroup):
    login = State()
    position = State()
    years = State()
    description = State()


class FSMEducation(StatesGroup):
    login = State()
    place = State()
    name = State()
    grade = State()


# state="*" - будь-яких 4-ч станів
# @dp.message_handler(state="*", commands="cansel")


async def cansel_all_data(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Данні вводу відсутні")
    else:
        await state.finish()
        await message.reply("Всі введені дані були успішно очищені")
    await command_menu(message)


async def cansel_current_data(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    print(current_state, "стейт до очищення")
    await FSMData.previous()
    print(current_state, "стейт після очищення")
    if current_state == "FSMData:login" or current_state is None:
        await state.finish()
        await message.reply("Данні вводу відсутні")
        await command_create(message, state)

    else:
        await bot.send_message(message.from_user.id, "Поточна відповідь на питання була очищенна\n"
                                                     "Будь-ласка, дайте відповідь на минуле питання")


async def command_create(message: types.Message, state=FSMContext):
    # initialized first state
    await FSMData.login.set()
    user_login = f"@{message.from_user.username}"
    async with state.proxy() as data:
        # save machine state to dictionary
        data['login'] = user_login
    await bot.send_message(message.from_user.id, "Як до тебе можна звертатися?", reply_markup=kb_cl_0)
    await FSMData.next()


async def usr_first_name(message: types.Message, state=FSMContext):
    print("user")
    # await FSMData.next()
    # await bot.send_message(message.from_user.id, "Як до тебе можна звертатися?", reply_markup=kb_cl_0)
    async with state.proxy() as data:
        # save machine state to dictionary
        data['first_name'] = message.text
    await message.reply("Тепер введи фамілію", reply_markup=kb_cl_1)
    await FSMData.next()
    # next state


async def usr_last_name(message: types.Message, state=FSMContext):
    # await FSMData.next()
    # await message.reply("Тепер введи фамілію", reply_markup=kb_cl_1)
    async with state.proxy() as data:
        # save machine state to dictionary
        data['last_name'] = message.text
    await message.reply("Тепер введи свій номер телефону", reply_markup=kb_cl_1)
    await FSMData.next()

    # next state


async def usr_phone_number(message: types.Message, state=FSMContext):
    # await FSMData.next()
    # await message.reply("Тепер введи свій номер телефону", reply_markup=kb_cl_1)
    async with state.proxy() as data:
        # save machine state to dictionary
        data['phone_number'] = message.text
    await message.reply("Зараз необхідно додати електрону пошту", reply_markup=kb_cl_1)
    await FSMData.next()
    # next state


async def usr_mail(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['mail'] = message.text
    await message.reply("Зараз необхідно додати опис посади", reply_markup=kb_cl_1)
    await FSMData.next()


async def usr_vacantion(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['vacantion'] = message.text
    await message.reply("Будь-ласка завантажте своє фото у фрматі файлу без стиснення", reply_markup=kb_cl_1)
    await FSMData.next()


async def usr_photo_id(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        # data['photo_id'] = message.photo[0].file_id
        data['photo_id'] = message.document.file_id
    await message.reply("Чудово, всі данні були успішно записані", reply_markup=kb_cl_1)
    # writing to database part
    await orm_add_data(state)
    await state.finish()
    await menu_job(message)


async def command_menu(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Виберіть наступну дію:\n"
                           "Команда /get - Відобразить Ваш наявний запис у базі данних\n"
                           "Команда /delete - Видалить Ваш наявний запис з бази данних\n"
                           "Команда /create - Оновить наявний запис в базі даних, або створить новий запис\n"
                           "Команда /download - Згенерує і відправить Вам готовий файл з резюме\n"
                           , reply_markup=kb_cl_3)


async def command_get(message: types.Message):
    # await sql_read(message)
    login = "@" + message.from_user.username
    usr = await orm_get_data(login)
    if usr is None:
        await message.reply("База данних користувача порожня")
    else:
        await bot.send_photo(message.from_user.id, usr.photo_id, f"{usr.first_name} {usr.last_name}")


async def command_delete(message: types.Message):
    login = "@" + message.from_user.username
    # await sql_delete(login)
    mess = await orm_delete_data(login)
    if mess is None:
        await message.reply("База данних користувача порожня")
    else:
        await message.reply("Ваші дані були успішно видалені з сереверу")


async def command_download(message: types.Message):
    login = "@" + message.from_user.username
    usr = await orm_get_data(login)
    if usr is None:
        await message.reply("База данних користувача порожня")
    else:
        file_id = usr.photo_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "resume_doc\\photo\\"+message.from_user.username+".jpg")
        local_photo_path = photo_path + message.from_user.username+".jpg"
        final_file_path = "resume_doc\\user_doc\\"+message.from_user.username+".pdf"
        user, educations, jobs  = await select_all(login)
        jobs_dicts = [job.to_dict() for job in jobs]
        educations_dicts = [education.to_dict() for education in educations]
        create_pdf(user.first_name,
                   user.last_name,
                   user.phone_number,
                   mail=user.mail,
                   vacantion=user.vacantion,
                   last_jobs=jobs_dicts,
                   educations=educations_dicts,
                   photo_path=local_photo_path,
                   final_file_path=final_file_path)
        await message.reply_document(open(final_file_path, "rb"))





async def command_create_job(message: types.Message, state=FSMContext):
    # initialized first state
    await FSMJob.login.set()
    user_login = f"@{message.from_user.username}"
    async with state.proxy() as data:
        # save machine state to dictionary
        data['login'] = user_login
    await bot.send_message(message.from_user.id, "Ким ти працював?", reply_markup=kb_cl_0)
    await FSMJob.next()


async def command_next(message: types.Message):
    # initialized first state
    await bot.send_message(message.from_user.id,
        "Виберіть наступну дію:\n"
        "Команда /education - Додати освіту \n"
        "Команда /menu - Повернутись в меню\n"
        , reply_markup=kb_cl_5)


async def job_position(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['position'] = message.text
    await message.reply("Тепер введи роки роботи", reply_markup=kb_cl_1)
    await FSMJob.next()
    # next state


async def job_years(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['years'] = message.text
    await message.reply("Чим ти займався на цій посаді?", reply_markup=kb_cl_1)
    await FSMJob.next()
    # next state


async def job_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['description'] = message.text
    await message.reply("Чудово, всі данні були успішно записані", reply_markup=kb_cl_1)
    # вивід повного складу словника
    await bot.send_message(message.from_user.id, tuple(data.values()))
    await bot.send_message(message.from_user.id, f"""
    Давай перевіримо твої данні:\n
    Посада на якій ти працював: {data["position"]}\n
    Роки роботи: {data["years"]}\n 
    Опис роботи: {data["description"]}\n""")
    # writing to database part

    # await sql_add_data(state)
    # await orm_add_data(state)
    await orm_add_job(state)
    await state.finish()
    await menu_job(message)
    # next state


async def menu_job(message: types.Message):
    await bot.send_message(message.from_user.id,
        "Виберіть наступну дію:\n"
        "Команда /job - Додати місце роботи \n"
        "Команда /next - Перейти до наступного кроку\n"
        , reply_markup=kb_cl_4)


async def create_education(message: types.Message, state=FSMContext):
    # initialized first state
    await FSMJob.login.set()
    user_login = f"@{message.from_user.username}"
    async with state.proxy() as data:
        # save machine state to dictionary
        data['login'] = user_login
    await FSMEducation.next()
    await bot.send_message(message.from_user.id, "Де саме ти навчався?", reply_markup=kb_cl_0)
    await FSMEducation.next()


async def education_place(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['place'] = message.text
    await message.answer("Як називається твоя спеціальніть?", reply_markup=kb_cl_1)
    await FSMEducation.next()


async def education_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
         # save machine state to dictionary
        data['name'] = message.text
    await message.answer("Який у тебе ступінь?", reply_markup=kb_cl_1)
    await FSMEducation.next()


async def education_grade(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # save machine state to dictionary
        data['grade'] = message.text
    await message.reply("Чудово, всі данні були успішно записані", reply_markup=kb_cl_1)
    # вивід повного складу словника
    await bot.send_message(message.from_user.id, tuple(data.values()))
    await bot.send_message(message.from_user.id, f"""
            Давай перевіримо твої данні:\n
            Твоя спеціальність: {data["name"]}\n
            Твій ступінь: {data["grade"]}\n""")
    # writing to database part
    await orm_add_education(state)
    await state.finish()
    await menu_education(message)


async def menu_education(message: types.Message):
    # initialized first state
    await bot.send_message(message.from_user.id,
        "Виберіть наступну дію:\n"
        "Команда /education - Додати освіту \n"
        "Команда /menu - Повернутись в меню\n"
        , reply_markup=kb_cl_5)


# Виклик функцій кліенту handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(cansel_all_data, commands=["cancel"], state="*")
    dp.register_message_handler(cansel_current_data, commands=["back"], state="*")
    dp.register_message_handler(command_create, commands=["create"], state=None)
    dp.register_message_handler(usr_first_name, state=FSMData.first_name)
    dp.register_message_handler(usr_last_name, state=FSMData.last_name)
    dp.register_message_handler(usr_phone_number, state=FSMData.phone_number)
    dp.register_message_handler(usr_mail, state=FSMData.mail)
    dp.register_message_handler(usr_vacantion, state=FSMData.vacantion)
    dp.register_message_handler(usr_photo_id, content_types=["document"], state=FSMData.photo_id)
    dp.register_message_handler(command_delete, commands=["delete"])
    dp.register_message_handler(command_get, commands=["get"])
    dp.register_message_handler(command_download, commands=["download"])
    dp.register_message_handler(command_menu, commands=["menu"])
    dp.register_message_handler(job_position, state=FSMJob.position)
    dp.register_message_handler(job_years, state=FSMJob.years)
    dp.register_message_handler(job_description, state=FSMJob.description)
    dp.register_message_handler(command_next, commands=["next"])
    dp.register_message_handler(command_create_job, commands=["job"], state=None)
    dp.register_message_handler(create_education, commands=["education"], state=None)
    dp.register_message_handler(education_place, state=FSMEducation.place)
    dp.register_message_handler(education_name, state=FSMEducation.name)
    dp.register_message_handler(education_grade, state=FSMEducation.grade)

