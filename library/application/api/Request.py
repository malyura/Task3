# -*- coding: utf-8 -*-

from Common import Common
import json
from Data_Helper import ApiVar


class Request(Common):
    def request_change_plan(self, sub_id, rate_plan_id):
        """Выполнение запроса на смену ТП.

        Args:
            sub_id: id абонента.
            rate_plan_id: id тарифного плана.
        """
        headers = self.get_default_headers()
        data = json.dumps({'ratePlanId': rate_plan_id})
        self.http_lib().post_request("api", ApiVar.CHANGE_RATE_PLAN.format(sub_id=sub_id),
                                     headers=headers, data=data, code=202)

    def get_rate_plan_by_api(self, sub_id):
        """Получение данных о тарифном плане абонента.

        Args:
            sub_id: id абонента.

        Returns:
            Значение id тарифного плана.
        """
        resp = self.http_lib().get_request("api", ApiVar.GET_SUBSCRIBERS.format(sub_id=sub_id)).json()
        return resp["ratePlan"]["ratePlanId"]

    def get_balance(self, sub_id):
        """Получение данных о балансе абонента.

        Args:
            sub_id: id абонента.

        Returns:
            Значение баланса.
        """
        resp = self.http_lib().get_request("api", ApiVar.GET_SUBSCRIBERS.format(sub_id=sub_id)).json()
        return resp["balance"]
