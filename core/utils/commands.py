from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='/start',
            description='Старт'
        ),
        BotCommand(
            command='/set_group',
            description='Встановити групу розклад якої ви хочете отримувати'
        ),
        BotCommand(
            command='/set_link',
            description='Лінк на пару прикріплюється до викладача'
        ),
        BotCommand(
            command='/remove_link',
            description='Видалити прикріплене посилання'
        ),
        BotCommand(
            command='/remove_group',
            description='Видалити прикріплену до чату групу'
        ),
        BotCommand(
            command='/info',
            description='Додаткова інформація'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())