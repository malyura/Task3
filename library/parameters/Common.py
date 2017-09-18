# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn

builtin = BuiltIn()


def builtin_lib():
    """Получение экземпляра библиотеки BuiltIn.

    Returns:
        BuiltIn: экземпляр библиотеки BuiltIn.
    """
    return builtin


def oracle_db_lib():
    """
    Получение активного экземпляра библиотеки OracleDB.

    Returns:
        OracleDB.OracleDB: экземпляр библиотеки OracleDB.
    """
    return builtin_lib().get_library_instance(name="OracleDB")


def parameters_lib():
    """Функция получения экземпляра библиотеки работы с параметрами (библиотека parameters).

    Returns:
        parameters.Parameters: экземпляр библиотеки Parameters.
    """
    return builtin_lib().get_library_instance(name='Parameters')


def api_lib():
    """Функция получения экземпляра библиотеки с методами для работы с OpenAPI.

    Returns:
        oapi.Oapi: экземпляр библиотеки Oapi.
    """
    return builtin_lib().get_library_instance(name='OAPI')


def db_lib():
    """Функция получения экземпляра библиотеки параметров.

    Returns:
        bis.Bis: экземпляр библиотеки BIS.
    """
    return builtin_lib().get_library_instance(name='BIS')


def http_lib():
    """Получение экземпляра библиотеки HttpLib.

    Returns:
        core.HttpLib.HttpLib: Экземпляр библиотеки HttpLib.
    """
    return builtin.get_library_instance('HttpLib')


def get_default_headers():
    """Получение заголовков по умолчанию для запросов в API.

    Returns:
        dict: Заголовки по умолчанию.
    """
    default_headers = {
        'Content-Type': 'application/json'
    }
    return default_headers


def ssh_lib():
    """Получение экземпляра библиотеки ShhLib.

    Returns:
        core.ShhLib.ShhLib: Экземпляр библиотеки ShhLib.
    """
    return builtin.get_library_instance('SshLib')
