from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
Bot.set_current(bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
Dispatcher.set_current(dp)

CHANNEL_ID = os.getenv('CHANNEL_ID')


