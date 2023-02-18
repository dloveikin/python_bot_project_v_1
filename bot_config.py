''' Створення екземплярів боту і диспечера для подальших імпортів'''
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from token_key import api_token
# import storage class with for saveing data in RAM (STARE MACHINE)
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# create
fsm_memory = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=api_token)
dp = Dispatcher(bot, storage=fsm_memory)