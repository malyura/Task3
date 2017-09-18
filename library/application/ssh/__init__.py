# -*- coding: utf-8 -*-

from Request import Request
from Check import Check


class Ssh(
    Request,
    Check
):
    """Общий контейнер для всех keywords для работы с БД."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
