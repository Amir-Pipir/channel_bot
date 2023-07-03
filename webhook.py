from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
import os
import handlers
from create_bot import bot, dp


load_dotenv()

token = os.getenv('TOKEN')
WEBHOOK_DOMAIN = os.getenv('DOMAIN')
WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = '8443'


handlers.register_handlers_other(dp)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_DOMAIN, drop_pending_updates=True)


async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path='', on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)