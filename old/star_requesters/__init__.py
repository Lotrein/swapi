"""
Пакет star_requesters.
Назначение: хранение модулей для проекта SWAPI.

Перечень модулей:
1. exceptions: содержит пользовательские исключения.
2. requesters: описывает логику взаимодействия со "swapi.dev"

Автор кода:
Грехов Максим

Контактные данные:
email: lotrein46@yamagl.ru
"""

from .requesters import APIRequester, SQRequrester  # noqa: F401
