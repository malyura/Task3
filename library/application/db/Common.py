# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn


class Common(object):

    builtin = BuiltIn()

    ISSUE_STATUS_TODO = 10000  # ID статуса задачи: 'To Do'
    ISSUE_TYPE_TASK = 10002  # ID типа Issue: 'Task'

    def oracle_db_lib(self):
        """Получение экземпляра библиотеки OracleDb.

        Returns:
            core.OracleDb.OracleDb: Instance of OracleDb library.
        """
        return self.builtin.get_library_instance('OracleDb')
