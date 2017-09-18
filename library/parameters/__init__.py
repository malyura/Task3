# -*- coding: utf-8 -*-

"""Методы инициализации параметров."""

from parameters.Common import builtin_lib
from parameters.data import Data
from parameters.settings import Settings


class Parameters(
    Data,
    Settings
):
    """Модуль инициализации параметров."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """Инициализация экземпляра библиотеки поиска значений параметров."""
        super(Parameters, self).__init__()

        self.smoke_test_module = None

    @property
    def variables_module(self):
        """Производится загрузка variables модуля.

        Алгоритм:
          1. Попытка загрузить variables модуль с именем из параметра ${VARIABLE_MODULE}
          2. Попытка загрузить variables модуль с именем 'Staging'
          3. Если не удались оба варианта, то variables модуль = None

        Returns:
            object: Объект с переменными из variables модуля.
        """
        variables_module = None
        try:
            variables_module_name = builtin_lib().get_variable_value(name='${VARIABLE_MODULE}')
            variables_module = __import__(name=variables_module_name)
        except (ImportError, TypeError):
            try:
                variables_module = __import__('Staging')
            except ImportError:
                builtin_lib().log(message=u'Variables module was not found in PYTHONPATH')
        return variables_module

    def get_fixed_parameter(self, name):
        """Метод получения параметра.

        Значение параметра ищется по следующему алгоритму:
          1. Попытка получить значение переменной из текущего контекста
          2. Переменная из текущего variables модуля (см. property variables_module)
          3. Если оба варианта закончились неудачно, то значение запрашиваемой переменной = None

        Args:
            name (str): наименование параметра.

        Returns:
            object: значение параметра.
            None: в случае, если параметр так и не был найден.
        """
        try:
            # Загрузка значения переменной из общего контекста
            value = builtin_lib().get_variable_value('${' + name + '}', default=None)

            # Если в общем контексте данной переменной нет, пытаемся загрузить из текущего variables модуля
            if value is None:
                builtin_lib().log(u"Variable {} doesn't resolved in the execution context. "
                                  u"Trying to look into the variables module.".format(name), level='DEBUG')
                value = object.__getattribute__(self.variables_module, name)
            builtin_lib().log(u'Parameter {} was found in variables module {}. '
                              u'Value: {}'.format(name, self.variables_module.__name__, value), level='DEBUG')
            return value
        except AttributeError:
            if self.variables_module:
                builtin_lib().log(u'{} not found in {}'.format(name, self.variables_module.__name__), level='DEBUG')
            else:
                builtin_lib().log(u'{} no loaded: Systest parameters not loaded.'.format(name), level='DEBUG')

        return None
