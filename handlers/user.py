from dataclasses import dataclass
from telethon import TelegramClient
from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from lexicon.lexicon import *
from keyboards.user_kb import *


@dataclass
class User(StatesGroup):
    phone = State()
    phone_confirm = State()
    api_id = State()
    api_hash = State()
    confirm_data = State()
    session = State()


async def process_start(message):
    await message.answer(text=f'{LEXICON_EN["start"]}',
                         reply_markup=main_kb)


async def process_get_info(callback):
    await callback.message.edit_text(text=f'{LEXICON_EN["info"]}',
                                     reply_markup=quit_kb)



async def process_start_session(callback, state):
    await callback.message.edit_text(text='Please, share your phone number',
                                     reply_markup=quit_kb)
    await User.phone.set()


async def process_phone_number(message, state):
    await state.update_data(phone=message.text)
    await message.answer(text=f"Is {message.text} your correct number?\n"
                              f"If not, there will be an error",
                         reply_markup=yes_no_kb)
    await User.next()


async def process_yes(callback, state):
    phone = await state.get_data()
    phone = phone['phone']
    await callback.message.edit_text(text=f"Phone number: {phone}\n"
                                          f"Now please go to https://my.telegram.org, login and press 'API development tools'\n"
                                          f"And in this message sent your App api_id (just copy, paste and send)",
                                     reply_markup=quit_kb)
    await User.api_id.set()


async def get_api_id(message, state):
    await state.update_data(api_id=message.text.strip())
    await message.answer(text=f"In this message sent your App api_hash (it is on the same page that was App api_id)")
    await User.next()


async def get_api_hash(message, state):
    await state.update_data(api_hash=message.text.strip())
    data = await state.get_data()
    await message.answer(text=f"Make sure that your API_ID and API_HASH are correct otherwise it will be error\n"
                                 f"api_id = {data['api_id']}\n"
                                 f"api_hash = {data['api_hash']}\n"
                                 f"Is the data correct?",
                            reply_markup=confirm_kb)
    await User.next()


async def confirm_data(callback, state):
    data = await state.get_data()
    await callback.message.edit_text(text=f"api_id = {data['api_id']}\n"
                                          f"api_hash = {data['api_hash']}\n"
                                          f"You will get a code from telegram soon\n"
                                          f"Please enter it here",
                                     reply_markup=quit_kb)
    phone = data['phone']
    api_id = data['api_id']
    api_hash = data['api_hash']
    client = TelegramClient(str(callback.from_user.id), api_id, api_hash)
    await client.connect()

    phone_code = await client.send_code_request(phone)
    phone_code_hash = phone_code.phone_code_hash
    await state.update_data(phone_code_hash=phone_code_hash)
    await User.next()


async def get_code(message, state):
    await state.update_data(code=message.text.strip())
    data = await state.get_data()
    client = TelegramClient(str(message.from_user.id), data['api_id'], data['api_hash'])
    await client.connect()
    try:
        await client.sign_in(phone=data['phone'],
                             code=data['code'],
                             phone_code_hash=data['phone_code_hash'])
        await message.answer(text='perfect!')
    except Exception as e:
        await message.answer(text=e)
    await state.finish()#


async def process_back(callback):
    await callback.message.edit_text(text=LEXICON_EN['start'],
                                     reply_markup=main_kb)


async def process_quit(callback, state):
    await state.finish()
    await callback.message.edit_text('Bye')


def register_user_handlers(dp):
    dp.register_message_handler(process_start, commands=['start'])
    dp.register_callback_query_handler(process_get_info, text=['get_info'])
    dp.register_callback_query_handler(process_quit, text=['quit'], state='*')
    dp.register_callback_query_handler(process_start_session, text=['start_session', 'no'], state='*')
    dp.register_callback_query_handler(process_back, text=['back'])
    dp.register_message_handler(process_phone_number, state=User.phone)
    dp.register_callback_query_handler(process_yes, text=['yes', 'not_confirm'], state=[User.phone_confirm,
                                                                                        User.confirm_data])
    dp.register_message_handler(get_api_id, state=User.api_id)
    dp.register_message_handler(get_api_hash, state=User.api_hash)
    dp.register_callback_query_handler(confirm_data, state=User.confirm_data, text='confirm')
    dp.register_message_handler(get_code, state=User.session)
