from aiogram.utils import executor
import logging
from bot_config import dp
from bot_handlers import client_handler




# Configure logging
logging.basicConfig(level=logging.INFO)

# future connection to database

async def on_starup(_):
    # \033[1;32m - ANCI green color code
    print("\033[1;32m === BOT ONLINE SUCCESSFULLY ===")

client_handler.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_starup)



