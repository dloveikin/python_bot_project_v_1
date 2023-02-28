from aiogram.utils import executor
import logging
from bot_config import dp
from bot_handlers import client_handler
from data_base import bot_db
from data_base.ORM import controller
# from resume_doc.file_generator import file_create

# Configure logging
logging.basicConfig(level=logging.INFO)

# future connection to database


async def on_starup(_):
    # \033[1;32m - ANCI green color code
    print("\033[1;32m === BOT ONLINE SUCCESSFULLY ===")
    bot_db.sql_start()
    await controller.base_start()


client_handler.register_handlers_client(dp)
# file_create()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_starup)



