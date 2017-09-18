# -*- coding: utf-8 -*-

import json
import re
from xml.dom import minidom
from robot.api import logger
from robot.utils import is_unicode as _is_unicode
from robot.libraries.BuiltIn import BuiltIn


def requests_lib():
    """Получение экземпляра библиотеки RequestsLibrary.

    Returns:
        RequestsLibrary.RequestsLibrary: Instance of RequestsLibrary library.
    """
    return BuiltIn().get_library_instance('RequestsLibrary')


class HttpLib(object):

    builtin = BuiltIn()

    def get_request(self, alias, uri, headers=None, params=None, code=200):
        """Выполнение GET-запроса.

        Args:
            alias: alias HTTP-соединения.
            uri: URL path.
            headers (dict): заголовки HTTP-запроса.
            params (dict): URL параметры.
            code: ожидаемый HTTP-код ответа.

        Returns:
            requests.Response: HTTP-ответ сервера.
        """
        response = requests_lib().get_request(
            alias=alias,
            uri=uri,
            headers=headers,
            params=params
        )
        self.write_log(response)
        self.check_response_code(response, code)
        return response

    def post_request(self, alias, uri, headers=None, params=None, data=None, code=200):
        """Выполнение POST-запроса.

        Args:
            alias: alias HTTP-соединения.
            uri: URL path.
            headers (dict): заголовки HTTP-запроса.
            params (dict): URL параметры.
            data: тело HTTP-запроса.
            code: ожидаемый HTTP-код ответа.

        Returns:
            requests.Response: HTTP-ответ сервера.
        """
        response = requests_lib().post_request(
            alias=alias,
            uri=uri,
            headers=headers,
            params=params,
            data=data
        )
        self.write_log(response)
        self.check_response_code(response, code)
        return response

    def check_response_code(self, response, expected_code):
        """

        Args:
            response (requests.Response): объект ответа библиотеки requests.
            expected_code: ожидаемый код ответа.
        """
        if response.status_code != int(expected_code):
            self.builtin.fail(msg='Response code is invalid. '
                                  'Expected: {}, Actual: {}'.format(expected_code, response.status_code))

    def write_log(self, response):
        """
        Logging of http-request and response

        *Args:*\n
        _response_ - object [ http://docs.python-requests.org/en/latest/api/#requests.Response | "Response" ]

        *Response:*\n
        Formatted output of request and response in test log

        Example:
        | *Test cases* | *Action*                          | *Argument*            | *Argument*                | *Argument*  |
        | Simple Test  | RequestsLibrary.Create session    | Alias                 | http://www.example.com    |             |
        |              | ${response}=                      | RequestsLibrary.Get request       | Alias         | /           |
        |              | RequestsLogger.Write log          | ${response}           |                           |             |
        """
        msg, converted_string = self.get_formatted_response(response)

        # вывод сообщения в лог
        logger.info('\n'.join(msg))
        if converted_string:
            logger.info(converted_string)

    def get_formatted_response(self, response):
        """Format response for http-request.

        Args:\n
            response: response for http-request.\n

        Returns:\n
            Formatted response for http-request.
        """
        msg = []
        # информация о запросе
        msg.append(
            '> {0} {1}'.format(response.request.method, response.request.url))
        for req_key, req_value in response.request.headers.items():
            msg.append('> {header_name}: {header_value}'.format(header_name=req_key,
                                                                header_value=req_value))
        msg.append('>')
        if response.request.body:
            msg.append(response.request.body)
        msg.append('* Elapsed time: {0}'.format(response.elapsed))
        msg.append('>')
        # информация о ответе
        msg.append('< {0} {1}'.format(response.status_code, response.reason))
        for res_key, res_value in response.headers.items():
            msg.append('< {header_name}: {header_value}'.format(header_name=res_key,
                                                                header_value=res_value))
        msg.append('<')
        # тело ответа
        converted_string = ''
        if response.content:
            # получение кодировки входящего сообщения
            response_content_type = response.headers.get('content-type')
            if 'application/json' in response_content_type:
                response_content = self.get_decoded_response_body(response.content, response_content_type)
                converted_string = json.loads(response_content)
                converted_string = json.dumps(converted_string, sort_keys=True,
                                              ensure_ascii=False, indent=4,
                                              separators=(',', ': '))
            elif 'application/xml' in response_content_type:
                xml = minidom.parseString(response.content)
                converted_string = xml.toprettyxml()
            else:
                response_content = self.get_decoded_response_body(response.content, response_content_type)
                msg.append(response_content)

        return msg, converted_string

    def get_decoded_response_body(self, response_content, response_content_type):
        """ Decode body response.

        Args:\n
            response_content: response.\n
            response_content_type: response type.\n

        Returns:\n
            Decoded response.
        """
        match = re.findall(re.compile('charset=(.*)'),
                           response_content_type)
        # перекодирование тела ответа в соответствие с кодировкой, если она присутствует в ответе
        if len(match) == 0 or _is_unicode(response_content):
            return response_content
        else:
            response_charset = match[0]
            return response_content.decode(response_charset)
