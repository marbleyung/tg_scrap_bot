from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_kb = InlineKeyboardMarkup()
registrate_button = InlineKeyboardButton(text='START SESSION', callback_data='start_session')
info_button = InlineKeyboardButton(text='INFO', callback_data='info')
parse_button = InlineKeyboardButton(text='PARSE', callback_data='parse')
start_kb.add(registrate_button, info_button).add(parse_button)


reg_kb = InlineKeyboardMarkup().add(registrate_button, info_button)

back_kb = InlineKeyboardMarkup()
back_button = InlineKeyboardButton(text='BACK', callback_data='back')
back_kb.add(back_button)

yes_no_kb = InlineKeyboardMarkup()
yes_button = InlineKeyboardButton(text='YES', callback_data='yes')
no_button = InlineKeyboardButton(text='NO', callback_data='no')
yes_no_kb.add(yes_button, no_button)

quit_kb = InlineKeyboardMarkup()
quit_button = InlineKeyboardButton(text='QUIT', callback_data='quit')
quit_kb.add(quit_button)

confirm_kb = InlineKeyboardMarkup()
confirm_button = InlineKeyboardButton(text='CORRECT', callback_data='confirm')
not_confirm_button = InlineKeyboardButton(text='NOT CORRECT', callback_data='not_confirm')
confirm_kb.add(confirm_button, not_confirm_button).add(quit_button)

main_kb = InlineKeyboardMarkup()
get_info = InlineKeyboardButton(text='INSTRUCTIONS', callback_data='get_info')
main_kb.add(get_info).add(quit_button)

parse_kb = InlineKeyboardMarkup()
parse_1 = InlineKeyboardButton(text='PARSE MY GROUPS', callback_data='parse_1')
parse_2 = InlineKeyboardButton(text='PARSE GROUP BY LINK/USERNAME', callback_data='parse_2')
parse_3 = InlineKeyboardButton(text='FIND GROUPS', callback_data='parse_3')
parse_4 = InlineKeyboardButton(text='LARGE PARSING (SOON...)', callback_data='parse_4')
parse_kb.add(parse_1).add(parse_2).add(parse_3).add(parse_4).add(quit_button)
