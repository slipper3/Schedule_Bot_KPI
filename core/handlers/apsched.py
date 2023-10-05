from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
import core.database.dataManip as dm
import core.handlers.pingin as ping
import asyncio

weekday = {
    1: 'Пн',
    2: 'Вв',
    3: 'Ср',
    4: 'Чт',
    5: 'Пт',
    6: 'Сб',
}

async def send_link(time, bot: Bot):
    Chat_Group = await dm.get_chat_group()
    Current_WD = await ping.Current()
    if Current_WD['data']['currentWeek'] == 1:
        Current_Week = 'scheduleFirstWeek'
    else:
        Current_Week = 'scheduleSecondWeek'
    Current_Day = weekday[Current_WD['data']['currentDay']]
    for item in Chat_Group:
        print(item[0])
        teacher, lesson, les_type = await ping.Lesson(item[1], Current_Week, Current_Day, time)
        if len(teacher) == 1:
            link = await dm.get_link(item[1], teacher[0])
            if link != None:
                text = [
                    f"💃 <b>О {time} вас чекає пара</b> 🕺\n",
                    f"🔸{lesson[0]} ({les_type[0]})",
                    f"🔸Разом з {teacher[0]}\n",
                    f"<a href='{link}'>Посилання на пару</a>\n"
                ]
                try:
                    await bot.send_message(item[0], '\n'.join(text), parse_mode='HTML')
                    print('sended')
                except TelegramForbiddenError:
                    try:
                        await dm.remove_group_byId(item[0])
                    except Exception as err:
                        print(err)
                    else:
                        print('Користувач заблокував бота, айді користувача було видалено з бази')
                except Exception as err:
                    print(err)
            else: 
                text = [
                    f"💃 <b>О {time} вас чекає пара</b> 🕺\n",
                    f"🔸{lesson[0]} ({les_type[0]})",
                    f"🔸Разом з {teacher[0]}\n",
                    "<i>Посилання на пару не закріплено</i>"
                ]
                try:
                    await bot.send_message(item[0], '\n'.join(text), parse_mode='HTML')
                    print('sended')
                except TelegramForbiddenError:
                    try:
                        await dm.remove_group_byId(item[0])
                    except Exception as err:
                        print(err)
                    else:
                        print('Користувач заблокував бота, айді користувача було видалено з бази')
                except Exception as err:
                    print(err)
        elif len(teacher) >= 2: 
            text = [
                f"💃 <b>О {time} вас чекють пари</b> 🕺\n",    
            ]
            counter = 0
            for tch in teacher:
                link = await dm.get_link(item[1], tch)
                if link != None:
                    text.append(f"🔸{lesson[counter]} ({les_type[counter]})")
                    text.append(f"🔸Разом з {tch}\n")
                    text.append(f"<a href='{link}'>Посилання на пару</a>\n")
                else: 
                    text.append(f"🔸{lesson[counter]} ({les_type[counter]})")
                    text.append(f"🔸Разом з {tch}\n")
                    text.append("<i>Посилання на пару не закріплено</i>\n")
                counter += 1
            try:
                await bot.send_message(item[0], '\n'.join(text), parse_mode='HTML')
                print('sended')
            except TelegramForbiddenError:
                try:
                    await dm.remove_group_byId(item[0])
                except Exception as err:
                    print(err)
                else:
                    print('Користувач заблокував бота, айді користувача було видалено з бази')
            except Exception as err:
                print(err)


"""ШО ми робимо?
Робимо запит в базу (чат-група) -> створюємо список
Пінгуємо current отримуємо неділю та день
По списку для кожної групи  
    Пінгуємо lesson->певний тиждень->певний день->певний час
    Якщо отримали якийсь результат -> витягуємо вчителя, предмет та час
    Далі робимо запит в базу (вчитель-лінк)
    Надсилаємо повідомлення
"""

if __name__ == '__main__':
    asyncio.run(send_link('8.30'))