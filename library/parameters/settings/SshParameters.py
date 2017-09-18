# -*coding: utf-8 -*-

from parameters.Common import parameters_lib


class SshParameters(object):
    """Класс для получения параметров SSH."""

    def __init__(self):
        """Конструктор класса для получения параметров SSH."""
        super(SshParameters, self).__init__()

    def get_ssh_host(self):
        """Получение hostname SSH."""
        return parameters_lib().get_fixed_parameter('SSH_HOST')

    def get_ssh_username(self):
        """Получение имени пользователя для доступа к SSH."""
        return parameters_lib().get_fixed_parameter('SSH_USER_NAME')

    def get_ssh_password(self):
        """Получение пароля пользователя для доступа к SSH."""
        return parameters_lib().get_fixed_parameter('SSH_USER_PASSWORD')
