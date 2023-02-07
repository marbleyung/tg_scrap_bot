from aiogram import Dispatcher, types


async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/info', description='Information'),
        types.BotCommand(command='/parse', description='To parse menu'),
        types.BotCommand(command='/start', description='To start menu'),
    ]
    await dp.bot.set_my_commands(main_menu_commands)
