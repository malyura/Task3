# -*- coding: utf-8 -*-

import base64
from robot.libraries.BuiltIn import BuiltIn


class Common(object):

    builtin = BuiltIn()

    BASE_URI = '/rest/api/latest'

    def http_lib(self):
        """Получение экземпляра библиотеки HttpLib.

        Returns:
            core.HttpLib.HttpLib: Экземпляр библиотеки HttpLib.
        """
        return self.builtin.get_library_instance('HttpLib')

    def get_default_headers(self):
        """Получение заголовков по умолчанию для запросов в API.

        Returns:
            dict: Заголовки по умолчанию.
        """
        default_headers = {
            'Content-Type': 'application/json'
        }
        return default_headers

    def modify_default_headers(self, *headers):
        """Получении модифицированных http-заголовков по-умолчанию.

        Args:
            headers (dict): дополнительные заголовки.

        Returns:
            dict: Заголовки по умолчанию + дополнительные заголовки.
        """
        final_headers = self.get_default_headers()
        for header in headers:
            if header is not None:
                final_headers.update(header)
        return final_headers

    def get_authorization(self, login, password):
        """Получение значения авторизационного заголовка.

        Args:
            login: логин пользователя.
            password: пароль пользователя.

        Returns:
            Значение авторизационного заголовка.
        """
        string_to_encode = '{}:{}'.format(login, password)
        return 'Basic ' + base64.b64encode(string_to_encode)

    @staticmethod
    def get_auth_header(authorization):
        """Получение авторизационного заголовка.

        Args:
            authorization: значение авторизационного заголовка.

        Returns:
            dict: Авторизационный заголовок.
        """
        return {'Authorization': authorization}
