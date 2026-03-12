*** Settings ***
Documentation    Shared resources for <resource_name>.
Library    RequestsLibrary
Library    FakerLibrary

*** Variables ***
${BASE_URL}    https://api.example.com
${TIMEOUT}    10
&{DEFAULT_HEADERS}    Accept=application/json    Content-Type=application/json
