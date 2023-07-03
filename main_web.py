from aiogram import types
import handlers
from aiohttp import web
from create_bot import dp, bot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
DOMAIN = os.getenv('DOMAIN')

app = web.Application()

webhook_path = f'/{TOKEN}'

async def set_webhook():
    webhook_uri = DOMAIN + webhook_path
    await bot.set_webhook(webhook_uri)
async def on_startup(_):
    await set_webhook()
    print("Бот вышел в онлайн")

handlers.register_handlers_other(dp)

async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]

    if token == TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)

        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)

app.router.add_post(f'/{TOKEN}', handle_webhook)

if __name__ == "__main__":
    app.on_startup.append(on_startup)

    web.run_app(
        app,
        host='0.0.0.0',
        port=80,
    )
