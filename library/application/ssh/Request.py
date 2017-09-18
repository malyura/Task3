# -*- coding: utf-8 -*-

from Common import Common
from datetime import datetime
from random import choice
from string import digits
from Data_Helper import SshVar


class Request(Common):
    def load_file_to_ssh(self, content):
        """Загрузка файла с контентом в BRT.

        Args:
            content: Контент для файла.

        Returns:
            Строка с путем к файлу.
            Текущее время (время загрузки файла)
        """
        file_path = SshVar.FILE_PATH_FOR_UPLOAD + ''.join(choice(digits) for i in range(6)) + ".txt"
        self.ssh_lib().execute_command(SshVar.UPLOAD_FILE.format(content=content, filepath=file_path))
        return file_path, datetime.utcnow()
