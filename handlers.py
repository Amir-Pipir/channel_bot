from aiogram import types
from create_bot import bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import CHANNEL_ID
from bitrix_API import insert_lead

kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Проживание в Кингдом",
                                                                            "ТрансформациЯ в Мы").row("Консалтинг")


class Approve(StatesGroup):
    phone = State()
    que1 = State()
    que2 = State()
    que3 = State()


async def start(update: types.ChatJoinRequest):
    await bot.send_message(chat_id=update.from_user.id,text= "Чтобы пройти в телеграм канал, пожалуйста отправьте свой контакт и ответьте на 3 вопросов",
                           reply_markup=kb)


async def start_que(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.contact.phone_number
    await message.answer("Откуда вы про нас узнали?")
    await Approve.que1.set()


async def answer1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['que1'] = message.text
    await message.answer("Ваш email?")
    await Approve.next()


async def answer2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['que2'] = message.text
    await message.answer("Какая программа вас интересует?", reply_markup=kb2)
    await Approve.next()


async def answer3(message: types.Message, state: FSMContext):
    answ3 = message.text
    async with state.proxy() as data:
        number = data['phone']
        answ1 = data['que1']
        answ2 = data['que2']
    await message.answer(f"Ваши ответы:\n\n1. {answ1}\n2. {answ2}\n3. {answ3}\n")
    x = await insert_lead(number, answ1, answ2, answ3, message.from_user.username, message.from_user.first_name)
    if x is True:
        await state.finish()
        try:
            await bot.approve_chat_join_request(CHANNEL_ID, message.from_user.id)
            await message.answer("Вы добавлены в канал!")
        except:
            await message.answer("Вы уже есть в канале!")
    else:
        await state.finish()
        await message.answer("Ошибка!Email неправильно введен!\nПопробуйте снова", reply_markup=kb)


def register_handlers_other(dp: Dispatcher):
    dp.register_chat_join_request_handler(start)
    dp.register_message_handler(start_que, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(answer1, state=Approve.que1)
    dp.register_message_handler(answer2, state=Approve.que2)
    dp.register_message_handler(answer3, state=Approve.que3)
