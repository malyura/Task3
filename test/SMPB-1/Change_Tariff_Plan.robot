*** Settings ***
Documentation     Проверка функциональности смены ТП
Resource          .${/}resource.robot
Suite Setup       Suite Setup
Suite Teardown    Suite Teardown


*** Variables ***


*** Test Cases ***
Change tariff plan
    [Documentation]    Проверка функциональности смены ТП
    ${sub_id}    ${rate_plan_id}    ${balance}=    Precondition

    Change Rate Plan    ${sub_id}    ${rate_plan_id}

    Check Rate Plan By Api    ${sub_id}    ${rate_plan_id}

    Check Rate Plan By Db    ${sub_id}    ${rate_plan_id}

    Check Balance After Change Plan    ${sub_id}    ${balance}


*** Keywords ***
Precondition
    [Documentation]    Получение тестовых данных для проверки смены ТП
    ${subs_positive_balance} =    PARAMETERS.Get Positive Balance Subscribers

    ${sub_id}    ${rate_plan_id}    ${ammount}=    PARAMETERS.Get Subs For Conn To Plan    subs=${subs_positive_balance}

    ${balance}=    API.Get Balance    sub_id=${sub_id}

    PARAMETERS.Add Balance    sub_id=${sub_id}    ammount=${ammount}

    Wait Until Keyword Succeeds   2 min    5 seconds    PARAMETERS.Check Balance    balance_before=${balance}
    ...                                                                             ammount=${ammount}
    ...                                                                             sub_id=${sub_id}

    [Return]    ${sub_id}    ${rate_plan_id}    ${balance}


Change Rate Plan
    [Documentation]    Выполнение запроса на смену ТП
    [Arguments]    ${sub_id}    ${rate_plan_id}

    API.Request Change Plan    sub_id=${sub_id}    rate_plan_id=${rate_plan_id}


Check Rate Plan By Api
    [Documentation]    Проверка данных по ТП в API
    [Arguments]    ${sub_id}    ${rate_plan_id}

    ${rate_plan_id_by_api}    API.Get Rate Plan By Api    sub_id=${sub_id}

    Should Be Equal    ${rate_plan_id}    ${rate_plan_id_by_api}    msg=API: Rate plan incorrect


Check Rate Plan By Db
    [Documentation]    Проверка данных по ТП в БД
    [Arguments]    ${sub_id}    ${rate_plan_id}

    ${rate_plan_id_by_db}    DB.Get Rate Plan By Db    sub_id=${sub_id}
    Should Be Equal    ${rate_plan_id}    ${rate_plan_id_by_db}    msg=DB: Rate plan incorrect


Check Balance After Change Plan
    [Documentation]    Проверка правильности списания средств после смены ТП
    [Arguments]    ${sub_id}    ${balance}

    ${balance_after_change}=    API.Get Balance    sub_id=${sub_id}
    Should Be Equal    ${balance}    ${balance_after_change}    msg=API: Balance after change TP incorrect




