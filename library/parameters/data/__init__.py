# -*- coding: utf-8 -*-

from Check import Check
from Request import Request


class Data(
    Check,
    Request
):
    """Пакет для получения функциональных параметров."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """Конструктор класса для получения функциональных параметров."""
        super(Data, self).__init__()
