from aiogram import Bot
from aiogram.types import Message
from core.keyboards.reply import start_keyboard
from core.settings import settings
from core.utils.commands import set_commands

# (формат -> https://schedule.kpi.ua/)
async def get_start(message: Message, bot: Bot):   
    await message.answer('Шановне панство, вітаю! Я бот щоденник який буде вам нагадувати про ваші пари, щоб ви жодної не пропустили. Для того щоб отримувати сповіщення, будь ласка, вкажіть групу', reply_markup=start_keyboard)

async def startup(bot: Bot) -> None:
    await set_commands(bot)
    #await bot.send_message(settings.bots.admin_id, text="Бота запущено!")
    print('Бота запущено')

async def shutdown(bot: Bot) -> None:
    #await bot.send_message(settings.bots.admin_id, text="Бота вимкнено!")
    print('Бота вимкнено')

async def info(message: Message) -> None:
    text = [
        "<u><b>Додаткова інформація щодо команд:</b></u>\n",
        "👉<b>set_group</b> - закріплює код групи за чатом, щоб бот знав розклад якої групи відправляти в цей чат.\n",
        "👉<b>set_link</b> - закріплює посилання за викладачем.\n",
        "👉<b>remove_link</b> - видаляє закріплене за викладачем посилання.\n",
        "👉<b>remove_group</b> - відкріплює код групи від чату, після цього бот не зможе надсилати сповіщення в чат.\n\n",
        "Інформацію про розклад бот безе з сайту scheduler.kpi.ua",
        "Посилання на пари треба вказувати самостійно.\n",
        "Якщо виникли якісь питання чи пропозиції звертайтесь до @sanyamaha\n",
        "P.S. Бот може не працювати з 19:00 до 8:00"
    ]
    await message.answer(text='\n'.join(text), parse_mode='HTML')
