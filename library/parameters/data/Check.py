# -*- coding: utf-8 -*-

from parameters.Common import http_lib
from Data_Helper import ApiVar


class Check(object):
    def check_balance(self, balance_before, ammount, sub_id):
        """Проверка корректности баланса после его пополнения.

        Args:
            balance_before: Значение баланса до пополнения.
            ammount: Стоимость звонка.
            sub_id: Id абонента.
        """
        balance_after = http_lib().get_request("api", ApiVar.GET_SUBSCRIBERS.format(sub_id=sub_id)).json()["balance"]
        if int(balance_after) - int(ammount) == int(balance_before):
            pass
        else:
            raise Exception("balance is incorrect")
