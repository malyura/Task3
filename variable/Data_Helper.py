# -*- coding: utf-8 -*-

class ApiVar(object):
    CHANGE_RATE_PLAN = "/subscribers/{sub_id}/changeRatePlan"
    GET_SUBSCRIBERS = "/subscribers/{sub_id}"
    GET_AVAILABLE_PLAN = "subscribers/{sub_id}/getAvailableRatePlans"
    GET_RP_CHANGE_CONFLICTS = "subscribers/{sub_id}/getRatePlanChangeConflicts"


class DbVar(object):
    SELECT_BALANCE = "SELECT BALANCE FROM SUBSCRIBERS WHERE MSISDN = {msisdn}"
    SELECT_CALL_HISTORY = """\
            SELECT call_id,
            session_id,
            out_msisdn,
            in_msisdn,
            Cast(start_date AS TIMESTAMP) AS start_date,
            Cast(end_date AS TIMESTAMP) AS end_date,
            price
        FROM call_history
        WHERE session_id = '{session_id}'
        """
    SELECT_RATE_PLAN = "SELECT RTPL_RTPL_ID FROM SUBSCRIBERS WHERE SUBS_ID={sub_id}"
    SELECT_POSITIVE_BAL_SUBS = "SELECT * FROM SUBSCRIBERS WHERE BALANCE > 0"
    SELECT_DATA_FOR_SUB_OUT = "SELECT * FROM SUBSCRIBERS WHERE BALANCE > {tariff} * {duration}"
    SELECT_DATA_FOR_SUB_IN = "SELECT * FROM SUBSCRIBERS WHERE MSISDN <> {sub_out_msi}"


class SshVar(object):
    GET_INFO_FROM_LOG = "cat /home/a1qa/temp/logs/log-{date}.log | grep -P 'Received file .*{filepath}.* session_id:'"
    PATTERN_FOR_SEARCH_IN_LOG = "{filepath}.+session_id: (\d+)"
    UPLOAD_FILE = """echo "{content}" > {filepath}"""
    FILE_PATH_FOR_UPLOAD = "/home/a1qa/temp/input/file-"
