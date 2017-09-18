# -*- coding: utf-8 -*-

from parameters.Common import oracle_db_lib, http_lib, get_default_headers
from core.HttpLib import requests_lib
import json
from Data_Helper import DbVar, ApiVar


class Request(object):
    def get_positive_balance_subscribers(self):
        """Получение данных об абонентах с положительным балансом.

        Returns:
            Данные об абонентах с положительным балансом.
        """
        return oracle_db_lib().execute_sql(DbVar.SELECT_POSITIVE_BAL_SUBS)

    def get_subs_for_conn_to_plan(self, subs):
        """Получение списка доступных для подключения тарифных планов.

        Если список пустой, то выполняется переход к следующему абоненту.
        Если в списке присутствует хотя бы один элемент, то выполняется проверка возможности перехода на данный ТП.
        Если список conflicts в полученном ответе пустой, то возвращеются данные о абоненте и ТП. Иначе,
        выбирается другой ТП. Если нет подходящего ТП, то выбирается другой абонент.

        Args:
            subs: Данные об абонентах.

        Returns:
            Значение Id абонента.
            Значение Id тарифного плана.
            Значение стоимости перехода на тарифный план.
        """
        for sub in subs:
            resp_plan = http_lib().get_request("api", ApiVar.GET_AVAILABLE_PLAN.format(sub_id=sub['SUBS_ID'])).json()
            if len(resp_plan) > 0:
                for item in resp_plan:
                    data = json.dumps({'ratePlanId': item['ratePlanId']})
                    headers = get_default_headers()
                    resp_plan_change = http_lib().post_request("api", ApiVar.GET_RP_CHANGE_CONFLICTS.format(
                        sub_id=sub['SUBS_ID']), headers=headers, data=data).json()

                    if not resp_plan_change["conflicts"]:
                        return sub['SUBS_ID'], item['ratePlanId'], (
                            int(resp_plan_change['activation_cost']) + int(resp_plan_change['recurring_cost']))

    def add_balance(self, sub_id, ammount):
        """Пополнение баланса.

        Args:
            sub_id: Значение id абонента.
            ammount: Сумма пополнения
        """
        if ammount > 0:
            headers = get_default_headers()
            data = json.dumps({"subscriberId": sub_id, "amount": ammount})
            requests_lib().put_request("api", "payments/add", data=data, headers=headers)

    def get_sub_out(self, call_tariff, duration):
        """Получение данных об абоненте, совершающем звонок.

        Баланс абонента должен быть больше стоимости звонка.

        Args:
            call_tariff: Стоимость 1 мин вызова.
            duration: Продолжительность вызова в мин.

        Returns:
            Данные об абоненте, совершающем исходящий звонок.
        """
        resp = oracle_db_lib().execute_sql(DbVar.SELECT_DATA_FOR_SUB_OUT.format(tariff=call_tariff, duration=duration))
        for item in resp:
            return item

    def get_sub_in(self, sub_out):
        """Получение данных об абоненте, принимающем звонок.

        Из списка для выбора принимающего абонента исключаем абонента совершающего звонок.

        Args:
            sub_out: Данные об абоненте, совершающем звонок.

        Returns:
            Данные об абоненте, принимающем входящий звонок.
        """
        resp = oracle_db_lib().execute_sql(DbVar.SELECT_DATA_FOR_SUB_IN.format(sub_out_msi=sub_out['MSISDN']))
        for item in resp:
            return item

    def get_content(self, sub_out, sub_in, call_tariff, duration):
        """Получение контента файла.

        Args:
            sub_out: Данные об абоненте, совершающем звонок.
            sub_in: Данные об абоненте, принимающем звонок.
            call_tariff: Стоимость 1 мин вызова.
            duration: Продолжительность вызова в мин.

        Returns:
            Строка с контентом.
        """
        return ';'.join([str(sub_out['MSISDN']), str(sub_in['MSISDN']), call_tariff, duration])
