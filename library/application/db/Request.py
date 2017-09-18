# -*- coding: utf-8 -*-

from Common import Common
from Data_Helper import DbVar


class Request(Common):
    def get_call_history_by_session_id(self, session_id):
        """Получение данных о звонке из таблицы БД CALL_HISTORY.

        Args:
            session_id: Id сессии звонка.

        Returns:
            Данные о совершенном звонке.
        """
        sql_text = DbVar.SELECT_CALL_HISTORY.format(session_id=session_id)
        call_history = self.oracle_db_lib().format_sql_dict(self.oracle_db_lib().execute_sql(sql_text))
        if len(call_history) == 0:
            raise Exception
        else:
            return call_history

    def get_balance_by_db(self, sub):
        """Получение значения баланса абонента из БД.

        Args:
            sub: Данные об абоненте.

        Returns:
            Значение баланса абонента.
        """
        return self.oracle_db_lib().execute_sql(DbVar.SELECT_BALANCE.format(msisdn=sub['MSISDN']))[0]['BALANCE']

    def get_rate_plan_by_db(self, sub_id):
        """Получение значения ТП.

        Args:
            sub_id: Значение id абонента.

        Returns:
            Значение id тарифного плана.
        """
        return self.oracle_db_lib().execute_sql(DbVar.SELECT_RATE_PLAN.format(sub_id=sub_id))[0]['RTPL_RTPL_ID']
