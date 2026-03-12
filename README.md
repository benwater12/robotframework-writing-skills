# robotframework-writing-skills
Just a simple skill set often used to write robot tests

## Overview
- Written useing codex, as agent skill files. should be fine to use directly into other AI agents
- using uv and robotframework as main packages

## Flow

## Skills

Use the skill instructions in each folder to drive the workflow. Each skill is documented in its `SKILL.md` file.

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
