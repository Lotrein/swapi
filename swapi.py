from pathlib import Path
from datetime import datetime
import requests  # type: ignore[import]

"""
Модуль requesters.

Назначение:
Выполнение запросов к API swapi.dev, получение данных о категориях
и их содержимого.

Перечень классов (с иерархией):
1. APIRequester
    1.1. SQRequrester

Методы:
1. APIRequester.get()
2. SQRequrester.get_sw_categories()
3. SQRequrester.get_sw_info()
"""


class APIRequester:
    """Класс APIRequester включает в себя:
       - Инициализацию атрибута объекта base_url
       - Проверку на корректность введённого URL
       - Возвращения объекта класса Response для дочернего класса"""

    def __init__(self, base_url):

        # Проверяем тип данных переданного значения
        # Избавляемся от пробелов и "/" в конце и начале строки
        if isinstance(base_url, str):
            self.base_url = str.strip(base_url, '/ ')
            print(f'{datetime.now()}: Инициализирован объект {self}\n')
        else:
            raise WrongUrlDataType(base_url)

    def get(self):
        """Метод get() получает ответ от указанного URL
           и перехватывает ошибки"""

        # Выполняем запрос к указанному URL, сохраняем в переменную response
        # Выполняем проверки на успешность запроса
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
        except requests.HTTPError:
            raise HttpError(self.base_url, response.status_code)
        except requests.ConnectionError:
            raise ConnectionError(self.base_url)
        except requests.exceptions.MissingSchema:
            raise IncorrectUrlFormat(self.base_url)
        except requests.RequestException:
            raise UnknownError(self.base_url)

        # На всякий случай переводим ответ в utf-8
        response.encoding = 'utf-8'
        print(f'{datetime.now()}: Запрос к {self.base_url} выполнен.\n')

        return response

    def __str__(self):
        return f'APIRequester: {self.base_url}'


class SQRequrester(APIRequester):
    """Класс SQRequester является дочерним по отношению к APIRequester
       и включает в себя:
       - Получение списка доступных категорий из swapi.dev/api
       - Получение содержимого конкретной категории"""

    def __init__(self, base_url):
        super().__init__(base_url)

    def get_sw_categories(self):
        """Метод get_sw_categories возвращает перечень доступных категорий,
        отсортированный в алфавитном порядке.
        Также, перехватываются ошибки, связанные с преобразованием
        из JSON-формата в словарь Python"""

        # Сохраняем response от указанного URL в categories
        self.categories = self.get()

        # Выполняем проверки на возможность перевода JSON-объекта в словарь
        # Если невозможно, то программа прекращает выполнение
        if 'application/json' in self.categories.headers.get('Content-Type',
                                                             ''):
            try:
                self.categories = self.categories.json()
            except requests.exceptions.JSONDecodeError:
                raise MismathJSONFormat(self.categories)
        else:
            raise CategoryIsNotJsonError(self.base_url)

        # Получаем список категорий из словаря и сортируем в алфавитном порядке
        self.categories_keys = list(dict.keys(self.categories))
        list.sort(self.categories_keys)

        print(
            f'{datetime.now()}: Сформирован перечень категорий:'
            f'\n{self.categories_keys}\n')

        return self.categories_keys

    def get_sw_info(self, sw_type):
        """Метод get_sw_info возвращает данные с первой страницы
           в выбранной категории (в строковом типе)."""

        # Составляем URL к первой странице текущей категории
        category_url = self.base_url + '/' + sw_type + '/1/'

        # Запрос к адресу элемента категории
        category_response = requests.get(category_url)
        print(f'{datetime.now()}: Получено содержимое категории {sw_type}')

        return category_response.text

    def __str__(self):
        return f'SQRequester: {self.base_url}'


"""
Модуль exceptions.

Назначение:
Пользовательские детализизированные исключения.

Перечень классов (исключений):
1. CategoryIsNotJsonError
2. WrondUrlDataType
3. HttpError
4. ConnectionError
5. IncorrectUrlFormat
6. UnknownError
7. MismathJSONFormat
"""


class CategoryIsNotJsonError(ValueError):
    """Content-Type указанного URL не соответствует application/json"""

    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def __str__(self):
        return (f'Ошибка: Недопустимое содержимое ответа.\n'
                f'Ответ из {self.base_url} не является JSON-объектом, '
                f'поэтому не может быть преобразован в словарь\n')


class WrongUrlDataType(Exception):
    """В параметр для URL передано значение нестрокового типа"""

    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def __str__(self):
        return (f'Инициализация объекта {self.base_url} невозможна.\n'
                f'Объект передан в типе данных {type(self.base_url)}.\n'
                f'Необхомо ввести URL-адрес строкой вида "https://<адрес>".\n')


class HttpError(requests.HTTPError):
    """Сервер существует, но выдал ошибку"""

    def __init__(self, base_url, status_code):
        self.base_url = base_url
        self.status_code = status_code
        super().__init__()

    def __str__(self):
        return (f'Ошибка подключения к адресу: {self.base_url}\n'
                f'Код ошибки: {self.status_code}\n')


class ConnectionError(requests.ConnectionError):
    """Ошибка подключения к серверу"""

    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def __str__(self):
        return (f'Ошибка подключения к адресу: {self.base_url}\n'
                f'Возможно, введён некорректный адрес или есть проблемы '
                f'с сетью\n')


class IncorrectUrlFormat(requests.ConnectionError):
    """Параметр для URL передан в строковом типе,
       но не соответствуя формату https://"""

    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def __str__(self):
        return (f'Ошибка подключения к адресу: {self.base_url}\n'
                f'URL введён в некорректном формате.\n'
                f'Введите URL вида "https://<адрес>"\n')


class UnknownError(requests.ConnectionError):
    """Исключение на случай непредвиденных ошибок при запросе к адресу"""

    def __init__(self, base_url):
        self.base_url = base_url
        super().__init__()

    def __str__(self):
        return (f'Ошибка подключения к адресу: {self.base_url}\n'
                f'Неизвестная ошибка.\n')


class MismathJSONFormat(requests.ConnectionError):
    """Несоответствие JSON-формату при Content-Type = application/json"""

    def __init__(self, categories):
        self.categories = categories
        super().__init__()

    def __str__(self):
        return (f'Объект:\n{self.categories}:\n - не может быть '
                f'преобразован в словарь, '
                f'так как не соответствует формату.')


# Объявляем url с API сайта swapi.dev
url = 'https://swapi.dev/api'


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
save_sw_data(url)
