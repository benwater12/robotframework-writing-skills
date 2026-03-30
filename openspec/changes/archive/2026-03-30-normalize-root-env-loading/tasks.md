## 1. Inventory And Shared Env Rules

- [x] 1.1 Identify every script, skill, or helper in the Robot API workflow that reads, validates, or documents runtime env variables.
- [x] 1.2 Define the canonical root `.env` resolution rule and the shared required-variable list (`BASE_URL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`) in the implementation surface that will own env loading.
- [x] 1.3 Define one stop-message format for missing root `.env` files and one stop-message format for missing or empty required variables.

## 2. Implementation Updates

- [x] 2.1 Update the bootstrap implementation to resolve `<project-root>/.env` consistently and stop with the shared fix-first message when configuration is incomplete.
- [x] 2.2 Update test execution or related helper flows to read from the same root `.env` path, validate the same required variables, and stop before continuing when validation fails.
- [x] 2.3 Remove or replace any flow-specific env-loading logic that conflicts with the shared root `.env` contract.

## 3. Documentation And Verification

- [x] 3.1 Update affected skill documentation so the described env behavior matches the implemented root `.env` contract and stop-on-missing-config behavior.
- [x] 3.2 Verify a configured project still works when `<project-root>/.env` contains all required values.
- [x] 3.3 Verify the missing-file path stops with a fix-first message when `<project-root>/.env` is absent and the missing-variable path stops when required variables are unset or empty.
