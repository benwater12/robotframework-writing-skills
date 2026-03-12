*** Settings ***
Documentation    Scenario for <action> route. Spec: openapi-specs/path--<path>-<method>.json (from openapi-specs/index.json, method lowercase)
Resource    ../../resources/<resource_name>_resources.robot
Resource    ../../keywords/<resource_name>/<action>_keywords.robot
Resource    ../../keywords/utils_keywords.robot
Suite Setup    Open API Session
Suite Teardown    Close All Sessions
Test Setup    Reset Scenario Data
Test Teardown    Capture Failure Details
Force Tags    api

*** Test Cases ***
<action>_scenario
    [Documentation]    Replace <action>_scenario with the route action and update the spec reference.
    ${payload}=    Build Example Payload
    ${response}=    Post Json    /example    ${payload}    201
    Log    ${response.text}
