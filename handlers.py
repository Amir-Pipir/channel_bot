from aiogram import types
from create_bot import bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from create_bot import CHANNEL_ID
from bitrix_API import insert_contact, insert_deal
import re

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("Проживание в Кингдом",
                                                                            "ТрансформациЯ в Мы").row("Консалтинг")


class Approve(StatesGroup):
    phone = State()
    que1 = State()
    que2 = State()
    que3 = State()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

async def start(update: types.ChatJoinRequest):
    await bot.send_message(chat_id=update.from_user.id, text="КингДОМ приветствует Вас! Для подключения к экосистеме КингДОМ отправьте свой контакт и ответьте пожалуйста на 3 вопроса",
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
    if not is_valid_email(message.text):
        await message.answer("Некорректный email, попробуйте еще раз")
        return
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
    await add_contatc_deal(number, answ1, answ2, answ3, message.from_user.first_name, message.from_user.last_name)
    await state.finish()
    try:
        await bot.approve_chat_join_request(CHANNEL_ID, message.from_user.id)
        await message.answer("Вы добавлены в канал!")
    except:
        await message.answer("Вы уже есть в канале!")

async def add_contatc_deal(number, ans1, email, ans3, user_fname, user_lname):
    contact_response = await insert_contact(number, ans1, email, ans3, user_fname, user_lname)
    if contact_response:
        contact_id = contact_response
        deal_response = await insert_deal(contact_id, user_fname, ans1, ans3)
        if deal_response:
            print('Новый контакт и сделка успешно добавлены в Битрикс24')
        else:
            print('Ошибка при создании сделки')
    else:
        print('Ошибка при создании контакта')



def register_handlers_other(dp: Dispatcher):
    dp.register_chat_join_request_handler(start)
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(start_que, content_types=types.ContentType.CONTACT)
    dp.register_message_handler(answer1, state=Approve.que1)
    dp.register_message_handler(answer2, state=Approve.que2)
    dp.register_message_handler(answer3, state=Approve.que3)
