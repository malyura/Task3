*** Settings ***
Documentation     Проверка списания средств со счета абонента за совершение звонка
Resource          .${/}resource.robot
Suite Setup       Suite Setup
Suite Teardown    Suite Teardown



*** Variables ***
${CALL_TARIFF}=    5
${DURATION}=    10

*** Test Cases ***
Debiting Funds From Subs Acc
    [Documentation]    Проверка списания средств со счета абонента за совершение звонка
    ${sub_out}    ${sub_in}    ${content_file}    ${balance_sub_out}    ${balance_sub_in}=    Precondition

    ${file_path}    ${date_load}=    Upload Content File    ${content_file}

    ${session_id}=    Check Success Of Processing File    ${file_path}

    Check Balances Of Subs    ${sub_out}           ${sub_in}         ${balance_sub_out}
    ...                       ${balance_sub_in}    ${CALL_TARIFF}    ${DURATION}

    Check Call Record    ${sub_out}        ${sub_in}      ${date_load}
    ...                  ${CALL_TARIFF}    ${DURATION}    ${session_id}


*** Keywords ***
Precondition
    [Documentation]    Получение тестовых данных для проверки списания средств за звонок
    ${sub_out}=    PARAMETERS.Get Sub Out    call_tariff=${CALL_TARIFF}    duration=${DURATION}

    ${sub_in}=    PARAMETERS.Get Sub In    sub_out=${sub_out}

    ${content_file}=    PARAMETERS.Get Content    sub_out=${sub_out}            sub_in=${sub_in}
    ...                                           call_tariff=${CALL_TARIFF}    duration=${DURATION}

    ${balance_sub_out}=    DB.Get Balance By Db    sub=${sub_out}

    ${balance_sub_in}=    DB.Get Balance By Db    sub=${sub_in}

    [Return]    ${sub_out}    ${sub_in}    ${content_file}    ${balance_sub_out}    ${balance_sub_in}


Upload Content File
    [Documentation]    Загрузка файла с контентом из предусловия
    [Arguments]    ${content_file}

    ${file_path}    ${date_load}=     SSH.Load File To Ssh     content=${content_file}

    Wait Until Keyword Succeeds    2 min    5 seconds    File Should Not Exist    file_path=${file_path}

    [Return]    ${file_path}    ${date_load}


Check Success Of Processing File
    [Documentation]    Проверка успешности обработки файла в логе
    [Arguments]    ${file_path}

    ${session_id}=    Wait Until Keyword Succeeds    2 min    5 seconds    SSH.Check Success    filepath=${file_path}

    [Return]    ${session_id}


Check Balances Of Subs
    [Documentation]    Проверка правильности списания средств за совершение звонка
    [Arguments]    ${sub_out}    ${sub_in}    ${balance_sub_out}    ${balance_sub_in}    ${call_tariff}     ${duration}

    ${balance_sub_in_after}=    DB.Get Balance By Db    sub=${sub_in}

    Should Be Equal    ${balance_sub_in}    ${balance_sub_in_after}    msg=DB: Balance subs_in after call incorrect

    ${bool_res}=   DB.Is Check Balance Sub Out    sub_out=${sub_out}        balance_before=${balance_sub_out}
    ...                                           tariff=${CALL_TARIFF}     duration=${DURATION}

    Should Be True    ${bool_res}    msg=DB: Balance subs_out after call incorrect


Check Call Record
    [Documentation]    Проверка появления записи о звонке таблице call_history.
    [Arguments]    ${sub_out}    ${sub_in}    ${date_load}    ${CALL_TARIFF}    ${DURATION}    ${session_id}

    ${db_call_history_list}=    Wait Until Keyword Succeeds    2 min    5 seconds
    ...                                                   DB.Get Call History By Session Id    session_id=${session_id}

    ${db_call_history}=    Set Variable    ${db_call_history_list[0]}

    ${check_msisdn_out}    ${check_msisdn_in}    ${check_start_date}
    ...    ${check_end_date}    ${check_price}=     DB.Is Check Call History    sub_out=${sub_out}
    ...                                                                         sub_in=${sub_in}
    ...                                                                         call_history=${db_call_history}
    ...                                                                         date_load=${date_load}
    ...                                                                         tariff=${call_tariff}
    ...                                                                         duration=${duration}

    Should Be True    ${check_msisdn_out}    msg=DB: Msisdn out is incorrect
    Should Be True    ${check_msisdn_in}     msg=DB: Msisdn in is incorrect
    Should Be True    ${check_start_date}    msg=DB: Start date is incorrect (time delta > 2 min)
    Should Be True    ${check_end_date}      msg=DB: End date is incorrect
    Should Be True    ${check_price}         msg=DB: Price is incorrect

