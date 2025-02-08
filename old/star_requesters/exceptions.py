"""
Модуль star_requesters.exceptions.

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

import requests  # type: ignore[import]


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
