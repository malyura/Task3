# -*coding: utf-8 -*-

from parameters.Common import parameters_lib


class ApiParameters(object):
    """Класс для получения параметров API."""

    def __init__(self):
        """Конструктор класса для получения параметров API."""
        super(ApiParameters, self).__init__()

    def get_api_url(self):
        """Получение hostname JIRA API."""
        api_schema = parameters_lib().get_fixed_parameter('API_SCHEMA')
        api_host = parameters_lib().get_fixed_parameter('API_HOST')
        api_port = parameters_lib().get_fixed_parameter('API_PORT')
        return '{}://{}:{}'.format(api_schema, api_host, api_port)
