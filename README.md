# robotframework-writing-skills
Reusable skill set for building and running Robot Framework API tests.

## Overview
- This repository contains skill packages that are meant to be copied into another AI project's config skills folder.
- The workflow is based on `uv` and Robot Framework.

## How to use in another AI project

This repo is a source of skill content. Do not point your AI directly at this repo root and expect automatic loading.

1. Open your target AI project config folder.
2. Locate (or create) its `skills/` directory.
3. Copy each skill folder from this repo `skills/` into that target `skills/` directory.
4. Keep each folder name unchanged so skill metadata and references continue to work.

Example copy structure:

```text
<target-ai-project-config>/skills/
  openapi-splitter/
  robot-env-bootstrap/
  robot-api-test-suite/
  robot-test-runner/
  robot-beginner-test-guide/
```

## Skills

Use the instructions in each copied `SKILL.md` file to drive the workflow.

- `skills/openapi-splitter/`
  - Docs: `skills/openapi-splitter/SKILL.md`
  - Purpose: Split a large OpenAPI JSON into per-tag or per-route specs.
  - Quick use: `python scripts/split_openapi.py --mode tags` or `python scripts/split_openapi.py --mode routes`

- `skills/robot-env-bootstrap/`
  - Docs: `skills/robot-env-bootstrap/SKILL.md`
  - Purpose: Bootstrap a Robot Framework API test workspace with `uv`, `.venv`, and a project-root `.env`.
  - Quick use: `python scripts/bootstrap_env.py`

- `skills/robot-api-test-suite/`
  - Docs: `skills/robot-api-test-suite/SKILL.md`
  - Purpose: Generate or update Robot Framework API suites and keywords from OpenAPI routes.
  - Inputs: `openapi-specs/` outputs (from `openapi-splitter`) plus target routes/tags.

- `skills/robot-test-runner/`
  - Docs: `skills/robot-test-runner/SKILL.md`
  - Purpose: Run Robot tests with `.venv`, generate output artifacts, and log the exact command.
  - Example target: `tests/<domain>/<action>.robot`

- `skills/robot-beginner-test-guide/`
  - Docs: `skills/robot-beginner-test-guide/SKILL.md`
  - Purpose: End-to-end guided flow from bootstrap to splitting OpenAPI, generating suites, and running tests.

### Typical sequence

1. `robot-env-bootstrap` (if the environment is not set up)
2. `openapi-splitter` (split or refresh OpenAPI specs)
3. `robot-api-test-suite` (generate/update tests)
4. `robot-test-runner` (execute the suite)

## Root Env Contract

- Runtime configuration is read only from the project-root `.env`.
- Required keys are `BASE_URL`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD`.
- If the root `.env` file is missing, or any required value is empty, downstream workflows stop and tell the user to fix `.env` before retrying.

## Security notes

- Treat `.env`, test logs, and run artifacts as sensitive.
- Do not commit secrets or credential snapshots to source control.
- Review generated logs before sharing, especially when responses may contain tokens or user data.
