from lexicon.lexicon import *
from keyboards.user_kb import *


async def process_start(message):
    await message.answer(text=f'{LEXICON_EN["start"]}',
                         reply_markup=main_kb)


async def process_get_info(callback):
    await callback.message.edit_text(text=f'{LEXICON_EN["info"]}',
                                     reply_markup=quit_kb)


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
    dp.register_callback_query_handler(process_back, text=['back'])
