import requests as rq
import json

import asyncio

#Силка на api груп
link_group = 'https://schedule.kpi.ua/api/schedule/groups'
link_les = "https://schedule.kpi.ua/api/schedule/lessons?groupId=" 
current = "https://schedule.kpi.ua/api/time/current"
teacher_name = "https://schedule.kpi.ua/api/schedule/lecturer/list"


#Функція для отримання данних про групи
async def req_group(Code):
    try:
        #Отримаємо відповідь від сайту
        response = rq.get(link_group).text
        #Конвертуємо в словник
        group_dict = json.loads(response)

        for item in group_dict['data']:
            if item['name'] == Code['group'].upper() and item['faculty'] == Code['faculty'].upper():
                group_id = item['id']
                return group_id
    except Exception as err:
        print(err)

#Функція для отримання данних про факультети
async def req_lesson(group_id):
    try:
        link_les = link_les + group_id
        #Отримаємо відповідь від сайту
        response = rq.get(link_les).text
        #Конвертуємо в словник
        lesson_dict = json.loads(response)

        return lesson_dict
    except Exception as err:
        print(err)

async def Current():
    try:
        response = rq.get(current).text
        curr = json.loads(response)
        return curr
    except Exception as err:
        print(err)

async def Lesson(group_id: str, cur_week, cur_day, time):
    teacher = []
    lesson = []
    les_type = []
    try:
        link_less = link_les + group_id
        response = rq.get(link_less).text
        lesson_dict = json.loads(response)
        for item in lesson_dict['data'][cur_week]:
            if item['day'] == cur_day:
                for pair in item['pairs']:
                    if pair['time'] == time:
                        teacher.append(pair['teacherName'])
                        lesson.append(pair['name'])
                        les_type.append(pair['type'])
        return teacher, lesson, les_type
    except Exception as err:
        print(err)
    

async def Teacher(teacher):
    try:
        response = rq.get(teacher_name).text
        name_dict = json.loads(response)
        for item in name_dict['data']:
            if item['name'] == teacher:
                return True
        return False
    except Exception as err:
        print(err)


async def main():
    result = await Current()
    print(result)    

if __name__ == '__main__':
    asyncio.run(main())