"""
Модуль star_requesters.requesters.

Назначение:
Выполнение запросов к API swapi.dev, получение данных о категориях
и их содержимого.

Перечень классов (с иерархией):
1. APIRequester
    1.1. SWRequester

Методы:
1. APIRequester.get()
2. SWRequester.get_sw_categories()
3. SWRequester.get_sw_info()
"""

import requests  # type: ignore[import]
from datetime import datetime
from star_requesters.exceptions import (CategoryIsNotJsonError,
                                        WrongUrlDataType,
                                        HttpError,
                                        ConnectionError,
                                        IncorrectUrlFormat,
                                        UnknownError,
                                        MismathJSONFormat)


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


class SWRequester(APIRequester):
    """Класс SWRequester является дочерним по отношению к APIRequester
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
