# Robot API Patterns

## RequestsLibrary basics
- Create one session per suite with `Create Session` and reuse the alias.
- Prefer `json=${payload}` for JSON requests.
- Assert status codes with `Should Be Equal As Integers`.

## Session keyword pattern
```
Open API Session
    [Arguments]    ${alias}=api
    Create Session    ${alias}    ${BASE_URL}    headers=${DEFAULT_HEADERS}    timeout=${TIMEOUT}
```

## Response assertion pattern
```
${response}=    Get Request    api    /health
Should Be Equal As Integers    ${response.status_code}    200
```

## FakerLibrary payload pattern
```
${name}=    Name
${email}=    Email
&{payload}=    Create Dictionary    name=${name}    email=${email}
```

## OpenAPI spec mapping
- Accept one of these spec inputs:
- `openapi-specs/openapi.json`
- `openapi-specs/path--<path>-<method>.json`
- `openapi-specs/tag-<tag>.json`
- Types 2 and 3 require `openapi-specs/index.json` to map to spec files.
- Path/method index uses `file`, `path`, `method` (lowercase).
- Tag index uses `file`, `tag`.
- Resolve index `file` values as `openapi-specs/<file>` unless a full path is provided.
- When a suite uses a specific spec, reference it in `Documentation`.

### Path/method index format
```
{
  "items": [
    {
      "file": "path--metrics-get.json",
      "path": "/metrics",
      "method": "get"
    }
  ]
}
```

### Tag index format
```
{
  "items": [
    {
      "file": "tag-ai-token-management.json",
      "tag": "AI Token Management"
    }
  ]
}
```
