# -*- coding: utf-8 -*-

from Common import Common
from datetime import datetime, timedelta
from Data_Helper import DbVar


class Check(Common):
    def is_check_balance_sub_out(self, sub_out, balance_before, tariff, duration):
        """Проверка списания средств за исходящий звонок.

        Args:
            sub_out: Данные абонента, совершающего звонок.
            balance_before: Баланс абонента до совершения звонка.
            tariff: Стоимость минуты вызова.
            duration: Длительность вызова в минутах.

        Returns:
            True/False при верном/не верном списании.
        """
        balance_after = self.oracle_db_lib().execute_sql(DbVar.SELECT_BALANCE.format(msisdn=sub_out['MSISDN']))[0][
            'BALANCE']
        if balance_before - (int(tariff) * int(duration)) == balance_after:
            return True
        else:
            return False

    def is_check_call_history(self, sub_out, sub_in, call_history, date_load, tariff, duration):
        """Проверка корректности значений из таблицы БД CALL_HISTORY.

        Args:
            sub_out: Данные абонента, совершающего звонок.
            sub_in: Данные абонента, принимающего звонок.
            call_history: Данные по совершенному звонку из таблицы БД.
            date_load: Дата загрузки файла с информацией о звонке.
            tariff: Стоимость минуты вызова.
            duration: Длительность вызова в минутах.

        Returns:
            Результат (True/False) проверки поля OUT_MSISDN (исходящий абонент).
            Результат (True/False) проверки поля IN_MSISDN (принимающий абонента).
            Результат (True/False) проверки поля START_DATE (дата начала звонка).
            Результат (True/False) проверки поля END_DATE (дата завершения звонка).
            Результат (True/False) проверки поля PRICE (стоимость звонка).
        """
        start_date = datetime.strptime(call_history['START_DATE'], "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(call_history['END_DATE'], "%Y-%m-%dT%H:%M:%S")
        if str(sub_out['MSISDN']) == str(call_history['OUT_MSISDN']):
            check_msisdn_out = True
        else:
            check_msisdn_out = False

        if str(sub_in['MSISDN']) == call_history['IN_MSISDN']:
            check_msisdn_in = True
        else:
            check_msisdn_in = False

        if start_date - date_load <= timedelta(minutes=2):
            check_start_date = True
        else:
            check_start_date = False

        if end_date == start_date + timedelta(minutes=int(duration)):
            check_end_date = True
        else:
            check_end_date = False

        if call_history['PRICE'] == int(tariff) * int(duration):
            check_price = True
        else:
            check_price = False
        return check_msisdn_out, check_msisdn_in, check_start_date, check_end_date, check_price
