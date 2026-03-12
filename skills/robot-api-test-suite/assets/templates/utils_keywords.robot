*** Settings ***
Documentation    Shared utils keywords.

*** Keywords ***
Open API Session
    [Arguments]    ${alias}=api
    Create Session    ${alias}    ${BASE_URL}    headers=${DEFAULT_HEADERS}    timeout=${TIMEOUT}

Reset Scenario Data
    No Operation

Capture Failure Details
    Run Keyword If Test Failed    Log    Scenario failed. Review response logs.

Get Json
    [Arguments]    ${endpoint}    ${expected_status}=200    ${alias}=api
    ${response}=    GET On Session    ${alias}    ${endpoint}
    Should Be Equal As Integers    ${response.status_code}    ${expected_status}
    RETURN    ${response}

Post Json
    [Arguments]    ${endpoint}    ${payload}    ${expected_status}=201    ${alias}=api
    ${response}=    POST On Session    ${alias}    ${endpoint}    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    ${expected_status}
    RETURN    ${response}

Put Json
    [Arguments]    ${endpoint}    ${payload}    ${expected_status}=200    ${alias}=api
    ${response}=    Put Request    ${alias}    ${endpoint}    json=${payload}
    Should Be Equal As Integers    ${response.status_code}    ${expected_status}
    RETURN    ${response}

Delete Json
    [Arguments]    ${endpoint}    ${expected_status}=204    ${alias}=api
    ${response}=    DELETE On Session    ${alias}    ${endpoint}
    Should Be Equal As Integers    ${response.status_code}    ${expected_status}
    RETURN    ${response}

Build Example Payload
    ${name}=    Name
    ${email}=    Email
    &{payload}=    Create Dictionary    name=${name}    email=${email}
    RETURN    ${payload}
