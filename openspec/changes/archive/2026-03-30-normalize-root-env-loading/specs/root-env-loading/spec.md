## ADDED Requirements

### Requirement: Read runtime configuration from the project-root .env
Robot API workflow tooling SHALL resolve runtime configuration from the `.env` file located at the project root. Tooling MUST use the same root `.env` path regardless of the current working directory of an individual script or command invocation.

#### Scenario: Tool runs from the project root
- **WHEN** a bootstrap or execution flow reads runtime configuration while invoked from the project root
- **THEN** it loads values from `<project-root>/.env`

#### Scenario: Tool runs from a nested path or helper context
- **WHEN** a bootstrap or execution flow reads runtime configuration while invoked through a nested script, helper, or alternate working directory
- **THEN** it still resolves and reads `<project-root>/.env`

### Requirement: Stop when the project-root .env file is missing
Robot API workflow tooling SHALL stop the procedure when the expected project-root `.env` file does not exist. The failure message MUST identify the expected `.env` path and instruct the user to fix `.env` before retrying.

#### Scenario: Missing root .env
- **WHEN** a workflow attempts to read runtime configuration and `<project-root>/.env` is absent
- **THEN** it stops before continuing the workflow
- **THEN** it reports that the root `.env` file is missing and includes the expected file path
- **THEN** it instructs the user to fix `.env` before retrying

### Requirement: Stop when required variables are unset or empty
Robot API workflow tooling SHALL validate the required runtime variables `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` after reading the project-root `.env`. If any required variable is missing or empty, the tooling MUST stop the procedure and report the missing variable names with instructions to fix `.env` before retrying.

#### Scenario: One required variable is missing
- **WHEN** `<project-root>/.env` exists but one of `BASE_URL`, `ADMIN_USERNAME`, or `ADMIN_PASSWORD` is not set
- **THEN** the workflow stops before continuing
- **THEN** it reports the missing variable by name
- **THEN** it instructs the user to fix `.env` before retrying

#### Scenario: Multiple required variables are empty
- **WHEN** `<project-root>/.env` exists but multiple required variables are empty values
- **THEN** the workflow stops before continuing
- **THEN** it reports each missing or empty variable
- **THEN** it instructs the user to fix `.env` before retrying

### Requirement: Keep failure behavior consistent across affected flows
All affected Robot API workflow entry points SHALL use the same `.env` resolution rule and the same required-variable validation rule so users receive consistent behavior between bootstrap, execution, and related helper flows.

#### Scenario: Bootstrap and execution flows enforce the same contract
- **WHEN** a user runs bootstrap and later runs a test execution flow against the same project
- **THEN** both flows resolve the same root `.env` path
- **THEN** both flows stop on the same missing required variables
