from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_kb = InlineKeyboardMarkup()
registrate_button = InlineKeyboardButton(text='START SESSION', callback_data='start_session')
info_button = InlineKeyboardButton(text='INFO', callback_data='info')
start_kb.add(registrate_button, info_button)

back_kb = InlineKeyboardMarkup()
back_button = InlineKeyboardButton(text='BACK', callback_data='back')
back_kb.add(back_button)

yes_no_kb = InlineKeyboardMarkup()
yes_button = InlineKeyboardButton(text='YES', callback_data='yes')
no_button = InlineKeyboardButton(text='NO', callback_data='no')
yes_no_kb.add(yes_button, no_button)

quit_kb = InlineKeyboardMarkup()
quit_button = InlineKeyboardButton(text='QUIT', callback_data='quit')
quit_kb.add(back_button).add(quit_button)

confirm_kb = InlineKeyboardMarkup()
confirm_button = InlineKeyboardButton(text='CORRECT', callback_data='confirm')
not_confirm_button = InlineKeyboardButton(text='NOT CORRECT', callback_data='not_confirm')
confirm_kb.add(confirm_button, not_confirm_button).add(quit_button)

main_kb = InlineKeyboardMarkup()
get_info = InlineKeyboardButton(text='INSTRUCTIONS', callback_data='get_info')
main_kb.add(get_info).add(quit_button)