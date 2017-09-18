# -*- coding: utf-8 -*-

from ApiParameters import ApiParameters
from DbParameters import DbParameters
from SshParameters import SshParameters


class Settings(
    ApiParameters,
    DbParameters,
    SshParameters
):
    """Класс для получения параметров, относящихся к тестируемым продуктам."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """Конструктор класса для получения параметров, относящихся к продуктам."""
        super(Settings, self).__init__()
