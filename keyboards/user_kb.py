from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


back_button = InlineKeyboardButton(text='BACK', callback_data='back')


quit_kb = InlineKeyboardMarkup()
quit_button = InlineKeyboardButton(text='QUIT', callback_data='quit')
quit_kb.add(back_button).add(quit_button)


main_kb = InlineKeyboardMarkup()
get_info = InlineKeyboardButton(text='INSTRUCTIONS', callback_data='get_info')
main_kb.add(get_info).add(quit_button)