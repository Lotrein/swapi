# Здесь не совсем понимаю, зачем нам импортировать APIRequester,
# если мы его не используем.
# Но pytest сругнулся на то, что я его не добавил, поэтому пришлось прописать
from star_requesters import APIRequester, SQRequrester  # noqa: F401
from pathlib import Path
from datetime import datetime

# Объявляем url с API сайта swapi.dev
# url = 'https://swapi.dev/api'


def save_sw_data(url):
    """Функция save_sw_data принимает на вход URL-адрес
       и с помощью пакета star_requests сохраняет информацию
       о категориях со swapi.dev в файлы"""

    # Создаём объект класса SWRequesters, передавая ему URL
    sqrequester_object = SQRequrester(url)

    # Получаем и сохраняем список категорий
    # с помощью метода get_sw_cetegories()
    categories_list = sqrequester_object.get_sw_categories()

    # Указываем имя папки в корне проекта, куда будут сохраняться файлы
    folder_for_file = 'data'

    # Создаём папку
    Path(folder_for_file).mkdir(exist_ok=True)

    # Объявляем счётчик для подсчёта сохранённых файлов
    i = 0

    # Открываем цикл и идём по каждой категории из списка
    for category in categories_list:
        i += 1

        # Формируем полный путь файла для его дальнейшего открытия
        full_file_path = f'{folder_for_file}/{category}.txt'

        # Открываем файл на запись и записываем в него данные,
        # полученные методом get_sw_info() по текущей категории
        with open(full_file_path, 'w') as f:
            f.write(sqrequester_object.get_sw_info(category))
            print(f'{datetime.now()}: Выполнена запись в {full_file_path}\n')

    print(f'{datetime.now()}: Файлы сохранены в '
          f'"{folder_for_file}/"\nКоличество файлов: {i}')


# Вызываем функцию для получения и сохранения информации
# о категориях из swapi.dev в файловую систему
save_sw_data('https://swapi.dev/api')
