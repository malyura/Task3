# -*- coding: utf-8 -*-

import cx_Oracle
import textwrap
from robot.api import logger
from datetime import datetime


class OracleDb(object):
    """Библиотека для работы с базой данных Oracle."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._connection = None

    def connect(self, connection_string):
        """Подключение к БД Oracle.

        Args:
            connection_string: строка с данными для подключения.
        """
        try:
            logger.debug('Connecting using connection string: {}'.format(connection_string))
            self._connection = cx_Oracle.connect(connection_string)
        except cx_Oracle.DatabaseError as info:
            raise Exception("Logon to oracle  Error:", str(info))

    def disconnect(self):
        """Закрытие соединения с Oracle."""
        self._connection.close()

    def execute_sql(self, sql_statement):
        """Выполнение SQL запроса к БД.

        Args:
            sql_statement: SQL запрос.

        Returns:
            list[dict]: Список словарей, соответствующих результатам SQL-запроса.
        """
        cursor = None
        try:
            cursor = self._connection.cursor()
            logger.info("Executing :\n\n{sql_text}\n".format(
                sql_text=textwrap.dedent(sql_statement))
            )
            cursor.execute(sql_statement)
            col_name = tuple(i[0] for i in cursor.description)
            return [dict(zip(col_name, row)) for row in cursor]
        finally:
            if cursor:
                self._connection.rollback()

    def format_sql_dict(self, sql_out_dict, encoding='utf-8'):
        """Форматирование значений списка словарей с сохранением структуры.

        Пример:
         sql_out=[{'ID': 1, 'NAME': 'Иванов'},{'ID': 2, 'NAME': 'Петров'}] будет преобразован в
         [{'ID': 1, 'NAME': 'Иванов'}, {'ID': 2, 'NAME': 'Петров'}].

        Args:
            sql_out_dict: вывод sql-выражения в виде списка словарей.
            encoding: кодировка, в которой будут возвращены результаты запроса.

        Returns:
            Форматированный вывод sql-выражения в виде списка словарей.
        """
        for dictionary in sql_out_dict:
            for key in dictionary.keys():
                dictionary[key] = self.get_formatted_value(dictionary[key], encoding)
        return sql_out_dict

    def get_formatted_value(self, value, encoding='utf-8'):
        """Форматирование значения.

        - datetime приводится к isoformat.
        - string декодируется в encoding.
        - float округляется до двух знаков после запятой.

        Args:
            value: значение для форматирования.
            encoding: кодировка для string.

        Returns:
            Отформатированное значение.
        """
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            value = value.decode(encoding)
        elif isinstance(value, float):
            value = round(value, 2)
        elif isinstance(value, cx_Oracle.LOB):
            value = value.read()
            value = value.decode(encoding)
        return value
