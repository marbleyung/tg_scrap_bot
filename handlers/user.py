from dataclasses import dataclass
from aiogram.dispatcher.filters.state import StatesGroup, State

from lexicon.lexicon import *
from keyboards.user_kb import *
from services.create_file import create_file
from services.database import *
from services.scrap_channel import *


@dataclass
class User(StatesGroup):
    userdata = State()
    userdata_confirm = State()
    get_code = State()


class Parse(StatesGroup):
    keyword = State()
    group_id = State()
    my_groups = State()
    large_parse = State()


async def process_start(message, state):
    await message.answer(text=f'{LEXICON_EN["start"]}',
                         reply_markup=start_kb)
    await state.finish()


async def process_get_info(callback, state):
    await callback.message.edit_text(text=f'{LEXICON_EN["info"]}',
                                     reply_markup=back_kb)
    await state.finish()


async def process_help(message, state):
    await message.answer(text=f'{LEXICON_EN["help"]}',
                         reply_markup=start_kb)
    await state.finish()


async def process_start_session(callback, state):
    await callback.message.edit_text(text=f'{LEXICON_EN["instructions"]}',
                                     reply_markup=quit_kb)
    await User.userdata.set()


async def process_phone_number(message, state):
    data = message.text.split()
    await state.update_data(phone=data[-1], api_hash=data[1], api_id=data[0])
    await message.answer(text=f"❗️Is your data correct?\n"
                              f"Api_id: {data[0]}\n"
                              f"Api_hash: {data[1]}\n"
                              f"Phone number: {data[2]}\n",
                         reply_markup=yes_no_kb)
    await User.next()


async def process_yes(callback, state):
    await callback.message.edit_text(text=f"❗️Now Telegram will sent you code for login\n"
                                          f"Please, send it in next format:\n"
                                          f"code_*****",
                                     reply_markup=quit_kb)
    data = await state.get_data()
    phone = data['phone']
    api_id = data['api_id']
    api_hash = data['api_hash']
    client = TelegramClient(str(callback.from_user.id), api_id=api_id, api_hash=api_hash)
    await client.connect()
    phone_code = await client.send_code_request(phone)
    phone_code_hash = phone_code.phone_code_hash
    await state.update_data(phone_code_hash=phone_code_hash)
    await client.disconnect()
    await User.next()


async def get_code(message, state):
    await state.update_data(code=message.text.strip().split('_')[-1])
    data = await state.get_data()
    client = TelegramClient(str(message.from_user.id),
                            api_id=data['api_id'],
                            api_hash=data['api_hash'])
    await client.connect()
    try:
        await client.sign_in(phone=data['phone'],
                             code=data['code'],
                             phone_code_hash=data['phone_code_hash'])
        await message.answer(text='perfect!')
        create_user(id=message.from_user.id,
                    api_id=data['api_id'],
                    api_hash=data['api_hash'],
                    phone=data['phone'],
                    phone_hash=data['phone_code_hash'])

        await message.answer(text='registered',
                             reply_markup=parse_kb)
    except Exception as e:
        await message.answer(text=f"Error: {e}. Check /help")
    finally:
        await client.disconnect()
    await state.finish()


async def process_parse_command(message):
    try:
        is_user_registered = str(select_user(message.from_user.id)[0][0])
        await message.answer(text=f'{LEXICON_EN["parsing_options"]}\n'
                                  f'🔎Select parsing option',
                             reply_markup=parse_kb)
    except:
        await message.answer(text='❗️You are not registered, start session first\n'
                                  'Registered and still getting this problem? Check /help',
                             reply_markup=reg_kb)


async def process_parse(callback):
    try:
        is_user_registered = str(select_user(callback.from_user.id)[0][0])
        await callback.message.edit_text(text=f'{LEXICON_EN["parsing_options"]}\n'
                                              f'f🔎Select parsing option',
                             reply_markup=parse_kb)
    except:
        await callback.message.edit_text(text='❗️You are not registered, start session first\n'
                                              'Registered and still getting this problem? Check /help',
                                         reply_markup=reg_kb)
    await callback.answer()


async def get_group_keyword(callback):
    await callback.message.edit_text(text='Enter keyword to find groups\n'
                                          'example: python',
                                     reply_markup=quit_kb)
    await Parse.keyword.set()


async def process_keyword(message, state):
    result = select_user(message.from_user.id)
    api_id, api_hash = result[0][2], result[0][1]
    keyword = message.text.strip()
    try:
        await find_channel(keyword=keyword, api_hash=api_hash,
                                    api_id=api_id, username=str(message.from_user.id))
        create_file(file_path=f'{message.from_user.id}.html',
                    message=message.from_user.id)
        await message.answer(text='👏🏻Successfully parsed👏🏻',
                             reply_markup=parse_kb)
    except Exception as e:
        await message.answer(text=f'Error: {e}. Check /help',
                             reply_markup=parse_kb)
    await state.finish()


async def get_group_id(callback):
    await callback.message.edit_text(text='Enter group username or link to group AND limit value (1-10)\n'
                                          'example: https://t.me/ivanoise 5\n'
                                          'example: ivanoise 2\n'
                                          '🔝as more limit value is, then more users you will get. Read /info🔝\n',
                                          # '🤑Buy premium version to increase limit🤑',
                                     reply_markup=quit_kb)
    await Parse.group_id.set()


async def process_group_id(message, state):
    await message.answer(text='Parsing...This might take some time')
    result = select_user(message.from_user.id)
    api_id, api_hash = result[0][2], result[0][1]
    link_and_limit = message.text.strip().split()
    link, limit = link_and_limit[0], link_and_limit[1]
    limit = int(limit)
    print(link, limit)
    if limit > 10 or limit < 1:
        await message.answer(text='Limit should be in range 1...10')
    else:
        try:
            status = await parse_group_by_id(limit=limit, api_hash=api_hash,
                                             api_id=api_id,
                                             username=str(message.from_user.id),
                                             chat=link)
            create_file(file_path=f'{message.from_user.id}.html',
                        message=message.from_user.id)
            await message.answer(text=f"👏🏻Successfully parsed", reply_markup=parse_kb)
        except Exception as e:
            await message.answer(text=f'Error: {e}. Check /help',
                                 reply_markup=parse_kb)
    await state.finish()


async def get_my_groups(callback):
    result = select_user(callback.from_user.id)
    api_id, api_hash = result[0][2], result[0][1]
    await callback.message.answer(text='Creating list of your groups...\n')
    try:
        user_groups = await create_groups_list(username=callback.from_user.id,
                                               api_id=api_id, api_hash=api_hash)
        await callback.message.edit_text(text=f'{user_groups[0]}\n',
                                         reply_markup=quit_kb)
        await Parse.my_groups.set()
        await callback.message.answer(text=
                                           f'If you want to parse a CHAT: send just its number\n'
                                           f'For example, if you got "ChatName" in number 5, just send 5\n'
                                           f'If you want to parse a CHANNEL: send its number and limit (1-10) like this:\n'
                                           f'3 9\n'
                                           f"❗️Don't know what is limit, what is chat and what is channel? Check /info first")
    except Exception as e:
        await callback.message.edit_text(text=f'Error: {e}. Please, check /help',
                                         reply_markup=parse_kb)


async def process_my_groups(message, state):
    await message.answer(text='Parsing...This might take some time')
    result = select_user(message.from_user.id)
    api_id, api_hash = result[0][2], result[0][1]
    data = message.text.strip().split()
    if len(data) == 1:
        chat_type = 1
        limit = 1
    elif len(data) == 2:
        chat_type = 0
        limit = data[1]
    if int(limit) > 10 or int(limit) < 1:
        await message.answer(text='Limit should be in range 1...10')
    else:
        try:
            status = await parse_my_groups(chat_type=chat_type, api_hash=api_hash,
                                           api_id=api_id, username=str(message.from_user.id),
                                           limit=int(limit), chat_number=int(data[0]))
            create_file(file_path=f'{message.from_user.id}.html',
                        message=message.from_user.id)
            await message.answer(text='👏🏻Successfully parsed👏🏻',
                                 reply_markup=parse_kb)
        except Exception as e:
            await message.answer(text=f'Error: {e}. Check /help',
                                 reply_markup=parse_kb)
    await state.finish()


async def get_large_parse_data(callback):
    await callback.message.edit_text(text='Enter keyword and limit (1-5)\n ❗️USE COMMA AS A SEPARATOR❗️\n'
                                          'example: python, 2\n'
                                          'example: python chat, 5',
                                     reply_markup=quit_kb)
    await Parse.large_parse.set()


async def process_large_parse_data(message, state):
    await message.answer(text=f"Parsing... It may take few minutes")
    result = select_user(message.from_user.id)
    api_id, api_hash = result[0][2], result[0][1]
    keyword, limit = message.text.strip().split(',')
    limit = int(limit)
    if limit < 1 or limit > 5:
        await message.answer(text="For this option limit should be in range 1...5")
    else:
        try:
            await large_parse(username=str(message.from_user.id),
                              limit=limit, api_hash=api_hash,
                              api_id=api_id, keyword=keyword)
            create_file(file_path=f'{message.from_user.id}.html',
                        message=message.from_user.id)
            await message.answer(text='👏🏻Successfully parsed👏🏻',
                                 reply_markup=parse_kb)
        except Exception as e:
            await message.answer(text=f'Error: {e}. Check /help',
                                 reply_markup=parse_kb)
    await state.finish()


async def process_back(callback):
    await callback.message.edit_text(text=LEXICON_EN['start'],
                                     reply_markup=start_kb)


async def process_quit(callback, state):
    await state.finish()
    await callback.message.edit_text('🤚🏻Bye')


async def process_delete(message, state):
    await state.finish()
    text = delete_user(message.from_user.id)
    await message.answer(text=f"Status: {text}")


def register_user_handlers(dp):
    dp.register_message_handler(process_start, commands=['start'], state='*')
    dp.register_message_handler(process_help, commands=['help'], state='*')
    dp.register_message_handler(process_delete, commands=['del', 'delete'], state='*')
    dp.register_callback_query_handler(process_get_info, text=['info'], state='*')
    dp.register_callback_query_handler(process_quit, text=['quit'], state='*')
    dp.register_callback_query_handler(process_start_session, text=['start_session', 'no'], state='*')
    dp.register_callback_query_handler(process_back, text=['back'])
    dp.register_message_handler(process_phone_number, state=User.userdata)
    dp.register_callback_query_handler(process_yes, text=['yes', 'not_confirm'], state=[User.userdata_confirm,
                                                                                        ])
    dp.register_message_handler(get_code, state=User.get_code)
    dp.register_callback_query_handler(process_parse, text=['parse'])
    dp.register_message_handler(process_parse_command, commands=['parse'])
    dp.register_callback_query_handler(get_my_groups, text='parse_1')
    dp.register_message_handler(process_my_groups, state=Parse.my_groups)
    dp.register_callback_query_handler(get_group_id, text='parse_2')
    dp.register_message_handler(process_group_id, state=Parse.group_id)
    dp.register_callback_query_handler(get_group_keyword, text='parse_3')
    dp.register_message_handler(process_keyword, state=Parse.keyword)
    dp.register_callback_query_handler(get_large_parse_data, text='parse_4')
    dp.register_message_handler(process_large_parse_data, state=Parse.large_parse)