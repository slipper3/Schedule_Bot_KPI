from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.basіc import *
from core.settings import settings
import core.handlers.pingin as ping
import core.database.dataManip as dm
from core.keyboards.reply import * 
from core.handlers.apsched import send_link


bot = Bot(token=settings.bots.bot_token)
dp = Dispatcher()

sched = AsyncIOScheduler()
sched.add_job(send_link, 'cron', hour=8, minute=25, args=['8.30', bot])
sched.add_job(send_link, 'cron', hour=10, minute=20, args=['10.25', bot])
sched.add_job(send_link, 'cron', hour=12, minute=15, args=['12.20', bot])
sched.add_job(send_link, 'cron', hour=14, minute=10, args=['14.15', bot])
sched.add_job(send_link, 'cron', hour=16, minute=5, args=['16.10', bot])
sched.add_job(send_link, 'cron', hour=18, minute=25, args=['18.30', bot])

@dp.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Дія скасована')
    await callback.answer()

@dp.callback_query(F.data == 'info')
async def call(callback: CallbackQuery):
    await info(callback.message)
    await callback.answer()
@dp.callback_query(F.data == 'link')
async def call(callback: CallbackQuery, state: FSMContext):
    await set_link(message=callback.message, state=state)
    await callback.answer()
@dp.callback_query(F.data == 'group')
async def call(callback: CallbackQuery, state: FSMContext):
    await set_group(message=callback.message, state=state)
    await callback.answer()
 
#-------------------------------------
# ДІАЛОГ ГРУПА
#-------------------------------------
class GroupSet(StatesGroup):
    group = State()
    faculty = State()

data_data = { 
    'group': str,
    'faculty': str,
}

async def set_group(message: Message, state: FSMContext) -> None:
    await state.set_state(GroupSet.group)
    await message.answer('Введіть код групи', reply_markup=cancel_keyboard)

@dp.message(GroupSet.group)
async def group(message: Message, state: FSMContext) -> None:
    data_data['group'] = message.text
    await state.set_state(GroupSet.faculty)
    await message.answer('Введіть факультет', reply_markup=cancel_keyboard)

@dp.message(GroupSet.faculty)
async def faculty(message: Message, state: FSMContext) -> None:
    data_data['faculty'] = message.text
    await state.clear()
    group_id = await ping.req_group(data_data)
    if group_id != None:    
        done = await dm.save_id(message.chat.id, group_id)
        if done:
            await message.answer('Група успішно збережена ✅\n\nТепер коли ви встановили групу, можете додити посилання')
            return
        else:
            await message.answer('Сталась невідома помилка 🤷')
    else:
        await message.answer('Такої групи або факультету не існує 😔')




#-------------------------------------
# ДІАЛОГ ЛІНК
#-------------------------------------
class LinkSet(StatesGroup):
    teacher = State()
    link = State()

data_link = { 
    'teacher': str,
    'link': str,
}

async def set_link(message: Message, state: FSMContext) -> None:
    await state.set_state(LinkSet.teacher)
    await message.answer('Введіть ПІБ викладача', reply_markup=cancel_keyboard)

@dp.message(LinkSet.teacher)
async def get_lesson_type(message: Message, state: FSMContext) -> None:
    if await ping.Teacher(message.text):
        data_link['teacher'] = message.text
        await state.set_state(LinkSet.link)
        await message.answer('Введіть посилання на пару', reply_markup=cancel_keyboard)
    else:
        await message.answer('Викладача не знайдено')

@dp.message(LinkSet.link)
async def get_link(message: Message, state: FSMContext) -> None:
    data_link['link'] = message.text
    await state.clear()
    group_id = await dm.select_group(message.chat.id)
    if group_id == None:
        await message.answer('Група у вашому чаті не вказана або вказана не вірно')
        return
    await dm.save_link(group_id, data_link['teacher'], data_link['link'])
    await message.answer('Посилання було успішно збережено ✅')


#--------------------------
#ДІАЛОГ ВИДАЛЕННЯ ЛІНКУ
#--------------------------
class remove_teacher(StatesGroup):
    teacher = State()

remove_data = {
    'teacher': str
}

async def remove_link(message: Message, state: FSMContext):
    await state.set_state(remove_teacher.teacher)
    await message.answer('Введіть ПІБ вчителя', reply_markup=cancel_keyboard)

@dp.message(remove_teacher.teacher)
async def get_teacher(message: Message, state: FSMContext):
    remove_data['teacher'] = message.text
    await state.clear()
    done = await dm.remove_link(remove_data['teacher'])
    if done:
        await message.answer('Посилання було успішно видалено ✅')
    else:
        await message.answer('Такого викладача нема в базі')




async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.message.register(get_start, CommandStart())
    dp.message.register(set_group, Command('set_group'))
    dp.message.register(set_link, Command('set_link'))
    dp.message.register(dm.remove_group, Command('remove_group'))
    dp.message.register(remove_link, Command('remove_link'))
    dp.message.register(info, Command('info'))

    sched.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__=='__main__':
    asyncio.run(main())