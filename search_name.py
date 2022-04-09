import random
from threading import Thread
from datetime import datetime
import asyncio

"""Вводим нужно имя и создаем переменные для файлов"""
search_name = input('введите имя: ').capitalize()
files = ['female_names_rus.txt', 'male_names_rus.txt']
file_surnames = 'male_surnames_rus.txt'

"""Фиксирует начало выполнения работы"""
start_time = datetime.now()


async def random_fullname():
    """Поиск рандомной фамилии"""
    with open(file_surnames, 'r') as f:
        surname = random.choice(f.readlines())
        print('Подбираем  рандомную фамилию....')
        await asyncio.sleep(2)
        print(search_name, surname)


async def search_name_in_file(name):
    """проверка на наличие имени в файлах"""
    await asyncio.sleep(1)
    for file in files:
        with open(file, 'r') as f:
            if name in f.read():
                print(f'Имя {name} найдено в списке {file}')
            else:
                print(f'Имя {name} в списке {file} не найдено')

        """Создаем два потока для поиска в файлах"""
        thread1 = Thread(target=search_name_in_file, args=(name, ))
        thread2 = Thread(target=search_name_in_file, args=(name, ))

        """Запускаем потоки"""
        thread1.start()
        thread2.start()

        """Останавливаем потоки после выполнения их работы"""
        thread1.join()
        thread2.join()


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(random_fullname()), ioloop.create_task(search_name_in_file(search_name))]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
"""- Объявляем пару корутин, которые притворяются неблокирующими, используя sleep из asyncio
   - Корутины могут быть запущены только из другой корутины, или обёрнуты в задачу с помощью create_task
   - После того, как у нас оказались 2 задачи, объединим их, используя wait
   - Отправим на выполнение в цикл событий через run_until_complete
"""

"""Фиксирует конец выполнения работы"""
end_time = datetime.now()

print(f'[INFO] Время выполнения задачи: {end_time - start_time}')




