*** Settings ***
Documentation    Route keywords for <resource_name>/<action>.

*** Keywords ***
Call <action> Route
    [Arguments]    ${payload}=${None}    ${expected_status}=200    ${alias}=api
    ${response}=    No Operation
    RETURN    ${response}
