from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config import TOKEN
bot = Bot(token=TOKEN)
Bot.set_current(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
Dispatcher.set_current(dp)


