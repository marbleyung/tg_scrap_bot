from aiogram import Dispatcher, types


async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/get_info', description='Info'),
    ]
    await dp.bot.set_my_commands(main_menu_commands)
