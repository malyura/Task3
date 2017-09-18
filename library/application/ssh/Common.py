# -*- coding: utf-8 -*-

from robot.libraries.BuiltIn import BuiltIn


class Common(object):
    builtin = BuiltIn()

    def ssh_lib(self):
        """Получение экземпляра библиотеки ShhLib.

        Returns:
            core.ShhLib.ShhLib: Экземпляр библиотеки ShhLib.
        """
        return self.builtin.get_library_instance('SshLib')
