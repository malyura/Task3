*** Settings ***
Resource         ..${/}..${/}resource${/}common.robot

*** Keywords ***
Suite Setup
    [Documentation]    Suite_setup
    [Timeout]          1 minute

    Comment    Получение параметров окружения
    ${API_URL}=                 Parameters.Get Api Url
    ${DB_CONNECTION_STRING}=    Parameters.Get Db Connection String
    ${SSH_HOST}=                Parameters.Get Ssh Host
    ${SSH_USERNAME}=            Parameters.Get Ssh Username
    ${SSH_PASSWORD}=            Parameters.Get Ssh Password


    Comment    Установка соединений
    RequestsLibrary.Create Session    alias=api    url=${API_URL}

    OracleDb.Connect    connection_string=${DB_CONNECTION_STRING}

    SshLib.Connect    host=${SSH_HOST}
    SshLib.Login    username=${SSH_USERNAME}    password=${SSH_PASSWORD}



Suite Teardown
    Comment    Закрываем соединение с БД
    OracleDb.Disconnect

    Comment    Закрываем все http-соединения
    RequestsLibrary.Delete All Sessions

    Comment    Закрываем все shh-соединения
    SshLib.Close connect
