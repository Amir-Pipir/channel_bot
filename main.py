import handlers
from create_bot import dp
from aiogram import executor


async def on_startup(_):
    print("Бот вышел в онлайн")


handlers.register_handlers_other(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
