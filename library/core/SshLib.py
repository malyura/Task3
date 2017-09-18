# -*- coding: utf-8 -*-

from SSHLibrary import SSHLibrary


class SshLib(object):
    """Библиотека для работы с SSH."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._connection = SSHLibrary()

    def connect(self, host):
        """Подключение к SSH хосту

        Args:
            host: Имя хоста
        """
        self._connection.open_connection(host=host)

    def login(self, username, password):
        """Авторизация для входа на SSH

        Args:
            username: Имя
            password: Пароль
        """
        self._connection.login(username=username, password=password)

    def execute_command(self, command):
        """Выполнение команды на SSH

        Args:
            command: Строка с командой

        Returns:
            Строка с результатом выполнения команды
        """
        return self._connection.execute_command(command=command)

    def close_connect(self):
        """Закрытие соединения с SSH"""
        self._connection.close_all_connections()

    def file_should_not_exist(self, file_path):
        """Проверка отстутсвия файла"""
        self._connection.file_should_not_exist(file_path)
