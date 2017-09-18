# -*coding: utf-8 -*-

from parameters.Common import parameters_lib


class DbParameters(object):
    """Класс для получения параметров подключения к БД."""

    def __init__(self):
        """Конструктор класса для получения параметров подключения к БД."""
        super(DbParameters, self).__init__()

    def get_db_connection_string(self):
        """Получение connection string для БД JIRA."""
        db_username = parameters_lib().get_fixed_parameter('DB_USER_NAME')
        db_password = parameters_lib().get_fixed_parameter('DB_USER_PASSWORD')
        db_host = parameters_lib().get_fixed_parameter('DB_HOST')
        db_port = parameters_lib().get_fixed_parameter('DB_PORT')
        db_sid = parameters_lib().get_fixed_parameter('DB_SID')
        return '{}/{}@{}:{}/{}'.format(db_username, db_password, db_host, db_port, db_sid)
