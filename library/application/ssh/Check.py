# -*- coding: utf-8 -*-

from Common import Common
from datetime import datetime
import re
from Data_Helper import SshVar


class Check(Common):
    def check_success(self, filepath):
        """Проверка успешности обработки файла через лог SSH.

        Args:
            filepath: Путь к файлу.

        Returns:
            Значение id сессии звонка (session_id).
        """
        date = datetime.now().strftime("%Y-%m-%d")
        command = SshVar.GET_INFO_FROM_LOG.format(date=date, filepath=filepath)
        resp = self.ssh_lib().execute_command(command)
        filepath = filepath.replace("/", "\/")
        pattern = SshVar.PATTERN_FOR_SEARCH_IN_LOG.format(filepath=filepath)
        session_id = re.findall(pattern, resp)[0]
        if len(session_id) == 0:
            raise Exception("session_id is incorrect")
        else:
            return session_id
