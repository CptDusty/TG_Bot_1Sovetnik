import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import main, user_data, thanks
from aiogram import types
from config import bot
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота

# Диспетчер
dp = Dispatcher()
dp.include_routers(main.router, user_data.router, thanks.router)
# Хэндлер на команду /start
#@dp.message(Command("start"))
#async def cmd_start(message: types.Message):
   # await message.answer(f'{message.from_user.id}')
# Запуск процесса поллинга новых апдейтов
async def start():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(start())
