*** Settings ***
Library    Collections
Library    RequestsLibrary
Library    core.OracleDb.OracleDb       WITH NAME    OracleDb
Library    core.HttpLib.HttpLib         WITH NAME    HttpLib
Library    core.SshLib.SshLib           WITH NAME    SshLib
Library    application.api.Api          WITH NAME    API
Library    application.db.Db            WITH NAME    DB
Library    application.ssh.Ssh          WITH NAME    SSH
Library    parameters.Parameters        WITH NAME    Parameters