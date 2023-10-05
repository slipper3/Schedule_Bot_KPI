import psycopg2
from aiogram.types import Message
from core.database.config import host, user, password, dbname, port
#from config import host, user, password, dbname, port
import asyncio

async def save_id(chatID, groupID) -> None:
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""INSERT INTO public."Chat_Data"("chatID","groupID") VALUES (%s, %s)
                           ON CONFLICT ("chatID") DO UPDATE SET "groupID" = (%s)""", (chatID, groupID, groupID))
        return True
    except Exception as err:
        print(err)
        return False
    finally:
        con.commit()
        con.close()


async def save_link(group_id, teacher, link) -> None:
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""SELECT "teacher" FROM public."Link_Data" WHERE "groupID" = (%s) AND "teacher" = (%s);""", [group_id, teacher])
            resoult = cursor.fetchone()
            if resoult == None:
                cursor.execute("""INSERT INTO public."Link_Data"("groupID","teacher","pair_link") VALUES (%s, %s, %s);""", (group_id, teacher, link))
            else:
                cursor.execute("""UPDATE public."Link_Data" SET "pair_link" = (%s) WHERE "teacher" = (%s) AND "groupID" = (%s);""", [link, teacher, group_id])
    except Exception as err:
        print(err)
    finally:
        con.commit()
        con.close()

async def select_group(chat_id):
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""SELECT "groupID" FROM public."Chat_Data" WhERE "chatID"=(%s);""", [chat_id])
            result = cursor.fetchone()
            #print(result)
            return result
    except Exception as err:
        print(err)
    finally:
        con.commit()
        con.close()


async def get_chat_group():
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""SELECT * FROM public."Chat_Data" """)
            result = cursor.fetchall()
            #print(result)
            return result
    except Exception as err:
        print(err)
    finally:
        con.commit()
        con.close()

async def get_link(group_id, teacher):
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""SELECT "pair_link" FROM public."Link_Data" 
                           WHERE "groupID"=(%s) AND "teacher"=(%s);""", [group_id, teacher])
            result = cursor.fetchone()
            #print(result)
            return result[0]
    except Exception as err:
        print(err)
    finally:
        con.commit()
        con.close()


async def remove_group(message: Message):
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        chat_id = message.chat.id
        with con.cursor() as cursor:
            cursor.execute("""DELETE FROM public."Chat_Data" WHERE "chatID" = (%s)""", [chat_id])
            await message.answer('Групу успішно відкріплено ✅')
            return True
    except Exception as err:
        print(err)
        return False
    finally:
        con.commit()
        con.close()

async def remove_group_byId(chat_id):
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""DELETE FROM public."Chat_Data" WHERE "chatID" = (%s)""", [chat_id])
            return True
    except Exception as err:
        print(err)
        return False
    finally:
        con.commit()
        con.close()

async def remove_link(teacher):
    try:
        con = psycopg2.connect(
            host=host, 
            dbname=dbname, 
            user=user, 
            password=password, 
            port=port
            )
        with con.cursor() as cursor:
            cursor.execute("""SELECT "teacher" FROM public."Link_Data" WHERE "teacher" = (%s);""", [teacher])
            result = cursor.fetchone()
            if result != None:
                cursor.execute("""DELETE FROM public."Link_Data" WHERE "teacher" = (%s)""", [teacher])
                return True
            else:
                return False
    except Exception as err:
        print(err)
        return False
    finally:
        con.commit()
        con.close()


async def main():
    result = await get_link('ee35f04e-6465-4822-b082-eadd1f46d202', 'Назаренко Наталія Миколаївна')
    print(result)

if __name__ == '__main__':
    asyncio.run(main())